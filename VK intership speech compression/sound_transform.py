#!/usr/bin/env python
# coding: utf-8

# In[102]:

import numpy as np
from scipy import signal
import scipy.fft
import scipy.io.wavfile as wavfile

# In[62]:

def time_stretch(filename, new_filename, stretch_factor):
    # Чтение wav-файла
    sr, audio = wavfile.read(filename)
    
    # Параметры фазового вокодера
    frame_size = 2048 #* 2
    hop_length = frame_size // 4
    fft_size = frame_size

    # Анализ сигнала
    audio_frames = np.array([audio[i:i+frame_size] for i in range(0, len(audio)-frame_size, hop_length)])
    window = np.hanning(frame_size)
    audio_frames = window * audio_frames
    audio_spec = np.fft.rfft(audio_frames, fft_size, axis=1)
    audio_mag = np.abs(audio_spec)
    audio_phase = np.angle(audio_spec)

    # Изменение продолжительности
    new_size = int(round(len(audio_frames) * stretch_factor))
    new_frames = np.zeros((new_size, frame_size), dtype=np.float32)
    phase_advances = np.linspace(0, np.pi * hop_length, frame_size // 2 + 1)

    for i in range(new_size):
        t = float(i) / stretch_factor
        i0 = int(t)
        i1 = i0 + 1
        alpha = t - i0
        if i1 >= len(audio_frames):
            break
        mag = audio_mag[i0, :] * (1 - alpha) + audio_mag[i1, :] * alpha
        phase = audio_phase[i1, :] + alpha * (audio_phase[i0, :] - audio_phase[i1, :])
        phase_advance = phase_advances * stretch_factor
        phase = phase + phase_advance
        frame = mag * np.exp(1.0j * phase)
        frame_ifft = np.fft.irfft(frame, frame_size)
        new_frames[i, :] = frame_ifft * window

    # Синтез нового аудиофайла
    new_audio = np.zeros((new_size-1) * hop_length + frame_size, dtype=np.float32)
    for i in range(new_size):
        start = i * hop_length
        end = start + frame_size
        new_audio[start:end] += new_frames[i]
        
    
    # Проверяем содержание расширения .vaw
    if not new_filename.endswith(".wav"):
        new_filename += ".wav"
        
    # Cохраняем новый файл     
    return wavfile.write(new_filename, sr, new_audio.astype(np.int16))