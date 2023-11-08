import sys
import deepspeech
import collections
import numpy as np
import wave
import time

from datetime import datetime
from webrtcvad import Vad

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection
else:
    from multiprocessing.connection import Pipe as PipeConnection

from multiprocessing.sharedctypes import SynchronizedBase

from typing import Optional, List, Generator

from ..hal import Tactigon_Audio
from ..models import AudioSource, HotWord, TSpeech, TSpeechObject, TSpeechCommandEnum, VoiceConfig, Transcription

def millis():
    return datetime.now()

class Tactigon_Speech(Tactigon_Audio):

    config: VoiceConfig
    model: deepspeech.Model

    pipe: PipeConnection
    _command: SynchronizedBase

    tree_path: List[HotWord]
    current_branch: List[TSpeech]

    _transcription: str
    _time: int
    _is_timeout: bool

    def __init__(self, 
                pipe: PipeConnection,
                _command: SynchronizedBase,
                adpcm_pipe: Optional[PipeConnection], 
                audio_source: AudioSource,
                config: VoiceConfig,
                logger_level: int,
            ):

        self._command = _command
        self._transcription = ""
        self._is_timeout = False
        self.audio_source = audio_source
        
        self.config = config
        super().__init__(adpcm_pipe, self.audio_source, logger_level)
        self.vad = Vad(self.config.vad_aggressiveness)
        
        self.model = deepspeech.Model(self.config.model_full_path)

        if self.config.scorer_full_path:
            self.model.enableExternalScorer(self.config.scorer_full_path)
            self.model.setBeamWidth(self.config.beam_width)

        self.pipe = pipe
        self.run()
        self.destroy()
    
    def is_timeout(self, tick: datetime, timeout: int):
        return (millis() - tick).total_seconds() > timeout

    def vad_collector(self) -> Generator[bytes, bytes, None]:
        ticks = millis()
        num_padding_frames: int = int(self.frame_per_seconds * (self.config.vad_padding_ms / 1000))
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False

        self.logger.debug("[TSpeech] Clearing the queue...")
        self.clear()
        self.logger.debug("[TSpeech] Queue cleared")

        while True:
            with self._command.get_lock():
                if self._command.get_obj().value == TSpeechCommandEnum.STOP.value:
                    break

            frame = self.read()
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                if self.is_timeout(ticks, self.config.silence_timeout): 
                    self._is_timeout = True
                    break

                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced >= (self.config.vad_ratio * num_padding_frames):
                    triggered = True
                    ticks = millis()
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                if self.is_timeout(ticks, self.config.voice_timeout):
                    self._is_timeout = True
                    break

                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced >= (self.config.vad_ratio * num_padding_frames):
                    ring_buffer.clear()
                    break
        return None

    def run(self):
        with self._command.get_lock():
            self._command.get_obj().value = TSpeechCommandEnum.NONE.value
        
        while True:
            cmd: TSpeechCommandEnum
            with self._command.get_lock():
                cmd = TSpeechCommandEnum(self._command.get_obj().value)

            if cmd != TSpeechCommandEnum.NONE:
                if cmd == TSpeechCommandEnum.END:
                    break
                elif cmd == TSpeechCommandEnum.PLAY:
                    try:
                        audio_file: str
                        if self.pipe.poll(1):
                            audio_file = self.pipe.recv()
                        else:
                            audio_file = ""
                        self.play(audio_file)
                    except Exception as e:
                        print(e)
                        self.logger.warning("[TSpeech] Exception while playing a file. %s", e)

                elif cmd == TSpeechCommandEnum.LISTEN:
                    if self.pipe.poll(1):
                        try:
                            speech_tree: TSpeechObject = self.pipe.recv()
                            transcription = self.stt(speech_tree)
                            self.pipe.send(transcription)
                        except (Exception) as e:
                            self.stop_stream()
                            self.pipe.send(Transcription("", [], 0, False))
                            self.logger.info("[TSpeech] Exception while listening. %s", e)
                
                elif cmd == TSpeechCommandEnum.RECORD:
                    try:
                        audio_file: str
                        if self.pipe.poll(1):
                            audio_file = self.pipe.recv()
                        else:
                            audio_file = ""
                        self.record(audio_file)
                        self.pipe.send(audio_file)
                    except (Exception) as e:
                        self.stop_stream()
                        self.pipe.send(None)
                        self.logger.info("[TSpeech] Exception while recording. %s", e)

                else:
                    self.logger.error("[TSpeech] Received unknown command. %s", cmd)

                with self._command.get_lock():
                    self._command.get_obj().value = TSpeechCommandEnum.NONE.value

    def stt(self, speech_tree: TSpeechObject) -> Transcription:
        frames = self.vad_collector()

        text_so_far = ""
        self.tree_path: List[HotWord] = []
        self.current_branch: List[TSpeech] = speech_tree.t_speech
        self._is_timeout = False
        time_inference = 0

        self.model.clearHotWords()
        stt_stream = self.model.createStream()
        self.start_stream()

        self._transcription = ""
        
        for frame in frames:
            if frame is None:
                break

            delta = millis()
            data16 = np.frombuffer(frame, dtype='int16')
            self.model.clearHotWords()

            for hw_obj in self.current_branch:
                for hotword in hw_obj.hotwords:
                    self.model.addHotWord(hotword.word, hotword.boost)
            if self.config.stop_hotword:
                self.model.addHotWord(self.config.stop_hotword.word, self.config.stop_hotword.boost)

            stt_stream.feedAudioContent(data16)
            text = stt_stream.intermediateDecode()

            if text != text_so_far:
                self.logger.info("[TSpeech] Transcribed: %s", text)
                text_so_far = text

                self.check_branch(text)

                self._transcription = text_so_far

            delta = millis() - delta
            time_inference = time_inference + delta.total_seconds()

        text_so_far = stt_stream.finishStream()

        self.logger.debug("[TSpeech] Transcibed text: %s. Tree path: %s. Inference %f seconds", text_so_far, self.tree_path, time_inference)
        self.stop_stream()

        return Transcription(text_so_far, self.tree_path, time_inference, self._is_timeout)

    def record(self, filename: str):
        with wave.open(filename, mode='wb') as wave_file:
            wave_file.setsampwidth(2)
            wave_file.setnchannels(1)
            wave_file.setframerate(self.sample_rate)

            frames = self.vad_collector()

            self.start_stream()

            for frame in frames:
                if frame is None:
                    break

                wave_file.writeframes(frame)

            self.stop_stream()

    def play(self, audio_file):
        with wave.open(audio_file,"rb") as f:
            chunk = 1024

            if self.audio_source == AudioSource.MIC and self.stream.is_active():
                self.stream.stop_stream()

            audio_stream = self.pa.open(
                format=self.pa.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True
            )

            data = f.readframes(chunk)

            while data:
                with self._command.get_lock():
                    if self._command.get_obj().value == TSpeechCommandEnum.STOP.value:
                        break

                audio_stream.write(data)
                data = f.readframes(chunk)
                
            time.sleep(0.5)

            audio_stream.stop_stream()
            audio_stream.close()

    def check_branch(self, text: str):
        word_list = list(filter(lambda t: len(t) > 1 , text.split(" ")))
        if self.config.stop_hotword and self.config.stop_hotword.word in word_list[-2::]:
            self.tree_path.append(self.config.stop_hotword)
            return

        for tspeech in self.current_branch:
            for hotword in tspeech.hotwords:
                if hotword.word in word_list[-2::]:
                    self.tree_path.append(hotword)
                    self.current_branch = tspeech.children.t_speech if tspeech.children else []
                    return
        return
