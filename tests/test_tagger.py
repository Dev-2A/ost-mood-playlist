from pathlib import Path
from app.services.audio_analyzer import extract_features
from app.services.tagger import auto_tag


def test_tagging():
    sample_dir = Path("data/samples")
    files = list(sample_dir.glob("*"))

    if not files:
        print("⚠️ data/samples/ 에 오디오 파일을 넣어주세요.")
        return

    for file in files:
        try:
            features = extract_features(file)
            tags = auto_tag(features)

            print(f"\n🎵 {file.name}")
            print(f"   BPM: {features.bpm:.1f}  ({tags.bpm_category})")
            print(f"   에너지: {features.energy:.3f}  ({tags.energy_level})")
            print(f"   밸런스: {features.valence:.3f}")
            print(f"   🏷️  무드: {', '.join(tags.mood)}")
            print(f"   🏷️  상황: {', '.join(tags.situation)}")
        except Exception as e:
            print(f"⚠️ 오류 ({file.name}): {e}")


if __name__ == "__main__":
    test_tagging()