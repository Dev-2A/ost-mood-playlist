from pathlib import Path
from app.services.audio_analyzer import extract_features, batch_extract


def test_single_file():
    """단일 파일 특징 추출 테스트"""
    # data/samples/ 에 테스트용 오디오 파일을 하나 넣고 실행해줘
    sample_dir = Path("data/samples")
    files = list(sample_dir.glob("*"))

    if not files:
        print("⚠️ data/samples/ 에 오디오 파일을 넣어주세요.")
        return

    features = extract_features(files[0])
    print(f"\n📁 파일: {Path(features.file_path).name}")
    print(f"⏱️  재생시간: {features.duration:.1f}초")
    print(f"🥁 BPM: {features.bpm:.1f}")
    print(f"⚡ 에너지: {features.energy:.3f}")
    print(f"😊 밸런스: {features.valence:.3f}")
    print(f"🎼 스펙트럴 센트로이드: {features.spectral_centroid:.1f}")
    print(f"📊 MFCC (앞 5개): {[round(x, 2) for x in features.mfcc[:5]]}")


if __name__ == "__main__":
    test_single_file()