import librosa
import numpy as np
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AudioFeatures:
    """오디오에서 추출한 특징값 모음"""
    file_path: str
    duration: float             # 재생 시간 (초)
    bpm: float                  # 템포
    energy: float               # 에너지 (0.0 ~ 1.0)
    valence: float              # 밝기/긍정성 추정 (0.0 ~ 1.0)
    spectral_centroid: float    # 음색 밝기
    zero_crossing_rate: float   # 음의 거칠기
    mfcc: list[float]           # 음색 특징 벡터 (20차원)


def extract_features(file_path: str | Path) -> AudioFeatures:
    """
    오디오 파일에서 특징을 추출합니다.
    지원 형식: mp3, wav, flac, ogg
    """
    file_path = str(file_path)
    
    # 오디오 로드 (모노, 22050Hz로 통일)
    y, sr = librosa.load(file_path, sr=22050, mono=True)
    
    # 재생 시간
    duration = librosa.get_duration(y=y, sr=sr)
    
    # BPM (템포)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo)
    
    # 에너지 (RMS 평균을 0~1로 정규화)
    rms = librosa.feature.rms(y=y)[0]
    energy = float(np.mean(rms))
    energy = min(energy * 10, 1.0)  # 정규화
    
    # 스펙트럴 센트로이드 (음색 밝기)
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_centroid = float(np.mean(spec_centroid))
    
    # 제로 크로싱 레이트 (음의 거칠기)
    zcr = librosa.feature.zero_crossing_rate(y=y)[0]
    zero_crossing_rate = float(np.mean(zcr))
    
    # MFCC (음색 특징 20차원)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc, axis=1).tolist()
    
    # Valence 추정: 밝은 음색 + 빠른 BPM = 긍정적
    # 단순 휴리스틱 (spectral_centroid 기반)
    valence = float(np.clip(spectral_centroid / 4000.0, 0.0, 1.0))
    
    return AudioFeatures(
        file_path=file_path,
        duration=duration,
        bpm=bpm,
        energy=energy,
        valence=valence,
        spectral_centroid=spectral_centroid,
        zero_crossing_rate=zero_crossing_rate,
        mfcc=mfcc_mean,
    )


def batch_extract(audio_dir: str | Path) -> list[AudioFeatures]:
    """
    디렉토리 내 모든 오디오 파일의 특징을 일괄 추출합니다.
    """
    audio_dir = Path(audio_dir)
    extensions = {".mp3", ".wav", ".flac", ".ogg"}
    results = []
    
    files = [f for f in audio_dir.rglob("*") if f.suffix.lower() in extensions]
    
    for i, file in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 분석 중: {file.name}")
        try:
            features = extract_features(file)
            results.append(features)
        except Exception as e:
            print(f"  ⚠️ 오류 발생 ({file.name}): {e}")
    
    return results