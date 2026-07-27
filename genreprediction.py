import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import sys
import json
import torch
import torchaudio
from torch.utils.data import Dataset
import torch.nn.functional as F
import numpy as np
from keras.models import load_model

pred = load_model("genre_prediction.keras")

with open("config_model.json", "r") as f:
    config = json.load(f)

min = config["min"]
max = config["max"]
genre_mapping = config["genre_mapping"]

class GTZANDataset(Dataset):
  def __init__(self, file_paths, segment_len=66150):
    self.file_paths = file_paths
    self.segment_len = segment_len
    self.mel_spectrogram = torchaudio.transforms.MelSpectrogram(sample_rate=22050, n_fft=2048, hop_length=512, n_mels=128)
    self.amplitude_to_db = torchaudio.transforms.AmplitudeToDB()
    self.freq_masking = torchaudio.transforms.FrequencyMasking(freq_mask_param=15)
    self.time_masking = torchaudio.transforms.TimeMasking(time_mask_param=20)

  def __len__(self):
    return len(self.file_paths)

  def __getitem__(self, idx):
    images = []
    cuts = []
    waveform, sr = torchaudio.load(self.file_paths[idx])
    if waveform.shape[0] > 1:
      waveform = torch.mean(waveform, dim=0, keepdim=True)
    if sr != 22050:
      resampler = torchaudio.transforms.Resample(sr, 22050)
      waveform = resampler(waveform)
    if waveform.shape[1] > self.segment_len:
      n = waveform.shape[1] // self.segment_len
      for i in range(n):
        waveform_cut = waveform[:, i*self.segment_len:i*self.segment_len+self.segment_len]
        cuts.append(waveform_cut)
    elif waveform.shape[1] < self.segment_len:
      pad_amount = self.segment_len - waveform.shape[1]
      waveform_cut = F.pad(waveform, (0, pad_amount))
      cuts.append(waveform_cut)

    for i in cuts:
      mel_spec = self.mel_spectrogram(i)
      mel_spec = self.amplitude_to_db(mel_spec)
      mel_spec = mel_spec.squeeze(0).numpy()
      images.append(mel_spec)

    return images

def genre_prediction(sound):
  n=0
  sum=0
  maxv=0
  preds = []
  mean = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  data =[sound]
  images = GTZANDataset(data)
  images = np.array(images).astype('float32')
  images = (images - min) / (max - min + 1e-5)
  images = np.array(images).reshape(-1, 128, 130, 1)
  for i in pred.predict(images, verbose=0):
    for j in range(10):
      mean[j] = mean[j]+i[j]
      n=n+1
  sum = mean[0]+mean[1]+mean[2]+mean[3]+mean[4]+mean[5]+mean[6]+mean[7]+mean[8]+mean[9]
  for j in range(10):
    mean[j] = mean[j]/sum
  for k in range(10):
    if mean[k] > maxv:
      maxv = mean[k]
      kmax = k
  return list(genre_mapping.keys())[list(genre_mapping.values()).index(kmax)], maxv

sound = sys.argv[1]
genre, maxv = genre_prediction(sound)
print(genre, maxv)
