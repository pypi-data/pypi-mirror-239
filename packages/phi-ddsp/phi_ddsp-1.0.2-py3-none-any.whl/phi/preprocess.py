import yaml
import pathlib
import librosa as li
from phi.ddsp.core import extract_loudness, extract_pitch, extract_centroid
from effortless_config import Config
import numpy as np
from tqdm import tqdm
import numpy as np
from os import makedirs, path
import torch

class Dataset(torch.utils.data.Dataset):

    def __init__(self, out_dir):
        super().__init__()
        self.signals = np.load(path.join(out_dir, "signals.npy"))
        self.pitchs = np.load(path.join(out_dir, "pitchs.npy"))
        self.centroids = np.load(path.join(out_dir, "centroids.npy"))
        self.loudness = np.load(path.join(out_dir, "loudness.npy"))

    def __len__(self):
        return self.signals.shape[0]

    def __getitem__(self, idx):
        s = torch.from_numpy(self.signals[idx])
        p = torch.from_numpy(self.pitchs[idx])
        c = torch.from_numpy(self.centroids[idx])
        l = torch.from_numpy(self.loudness[idx])
        return s, p, c, l


def preprocess(f, sampling_rate, block_size, signal_length):
    x, _ = li.load(f)
    N = (signal_length - len(x) % signal_length) % signal_length
    x = np.pad(x, (0, N))

    pitch = extract_pitch(x, sampling_rate, block_size)
    centroid = extract_centroid(x, sampling_rate, block_size)
    loudness = extract_loudness(x, block_size)

    x = x.reshape(-1, signal_length)
    pitch = pitch.reshape(x.shape[0], -1)
    centroid = centroid.reshape(x.shape[0], -1)
    loudness = loudness.reshape(x.shape[0], -1)

    return x, pitch, centroid, loudness
