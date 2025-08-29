# audio_recorder.py
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from typing import Optional, List, Callable

class AudioRecorder:
    """
    Класс для управления записью аудио.
    """
    def __init__(self, samplerate: int = 44100):
        self.samplerate = samplerate
        self.stream: Optional[sd.InputStream] = None
        self.frames: List[np.ndarray] = []
        self.is_recording = False
        self.is_paused = False
        self._callback: Optional[Callable[[str], None]] = None

    def set_status_callback(self, callback: Callable[[str], None]):
        """Установить callback для обновления статуса."""
        self._callback = callback

    def _update_status(self, message: str):
        """Внутренний метод для вызова callback'а статуса."""
        if self._callback:
            self._callback(message)

    def _audio_callback(self, indata, frames, time, status):
        """Callback для потока записи sounddevice."""
        if self.is_recording and not self.is_paused:
            self.frames.append(indata.copy())

    def start_recording(self):
        """Начать запись."""
        if not self.is_recording:
            try:
                self.frames = []
                self.is_recording = True
                self.is_paused = False

                self.stream = sd.InputStream(
                    samplerate=self.samplerate,
                    channels=1,
                    dtype='float32',
                    callback=self._audio_callback
                )
                self.stream.start()
                self._update_status("Запись...")
            except Exception as e:
                self.is_recording = False
                self._update_status(f"Ошибка записи: {e}")

    def pause_recording(self):
        """Поставить запись на паузу."""
        if self.is_recording and not self.is_paused:
            if self.stream:
                self.stream.stop()
            self.is_paused = True
            self._update_status("Пауза")

    def resume_recording(self):
        """Возобновить запись."""
        if self.is_recording and self.is_paused:
            # Пересоздаем поток после остановки
            if self.stream:
                self.stream.close()

            try:
                self.stream = sd.InputStream(
                    samplerate=self.samplerate,
                    channels=1,
                    dtype='float32',
                    callback=self._audio_callback
                )
                self.stream.start()
                self.is_paused = False
                self._update_status("Запись (возобновлена)...")
            except Exception as e:
                self.is_recording = False
                self._update_status(f"Ошибка возобновления: {e}")

    def stop_recording(self) -> str:
        """
        Остановить запись и сохранить файл.
        Возвращает сообщение о результате.
        """
        if self.is_recording:
            self.is_recording = False
            self.is_paused = False

            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            if self.frames:
                try:
                    # Проверка на пустой список фреймов
                    if self.frames:
                        audio_data = np.concatenate(self.frames, axis=0)
                        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                        sf.write(filename, audio_data, self.samplerate)
                        return filename
                    else:
                        return "Запись пустая"
                except Exception as e:
                    return f"Ошибка сохранения: {e}"
            else:
                return "Запись остановлена"
        return "Запись не велась"

    def toggle_pause(self):
        """Переключить состояние паузы."""
        if self.is_paused:
            self.resume_recording()
        else:
            self.pause_recording()
