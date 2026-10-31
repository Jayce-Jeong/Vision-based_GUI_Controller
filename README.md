# Vision-based_GUI_Controller

화면(스크린샷)을 보고 GUI 를 제어하는 비전 기반 컨트롤러입니다.
**Google Colab** 에서 바로 실행할 수 있고, **Google Drive** 에 스크린샷·로그·체크포인트를 저장해
Colab 세션이 끝나도 결과가 유지됩니다. Colab 이 아닌 로컬 환경에서도 같은 코드가 동작합니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jayce-Jeong/Vision-based_GUI_Controller/blob/main/notebooks/colab_quickstart.ipynb)

## Colab 에서 사용하기

1. 위 배지를 눌러 `notebooks/colab_quickstart.ipynb` 를 엽니다.
2. 셀을 순서대로 실행합니다. (설치 → Drive 마운트 → 저장 확인)
3. Drive 권한 승인 창이 뜨면 허용합니다.

```python
from vgc import setup_environment

paths = setup_environment()          # Colab 이면 Drive 마운트 후 폴더 생성
img.save(paths.screenshots / "step_001.png")
```

> 공개 저장소이므로 설치에 토큰이 필요 없습니다. 재현성을 위해 `...git@<태그 또는 커밋>` 으로 버전을 고정할 수 있습니다.

## 저장 위치

| 환경 | 루트 폴더 |
|------|-----------|
| Colab (Drive 마운트) | `내 드라이브/Vision-based_GUI_Controller/` |
| 로컬 | `./.vgc_data/` |

루트 아래에 `screenshots/`, `logs/`, `checkpoints/`, `data/`, `outputs/` 가 자동 생성됩니다.

## 환경 변수

| 이름 | 기본값 | 설명 |
|------|--------|------|
| `VGC_DRIVE_MOUNT` | `/content/drive` | Drive 마운트 지점 |
| `VGC_PROJECT_DIR` | `Vision-based_GUI_Controller` | `MyDrive` 안의 프로젝트 폴더 |
| `VGC_LOCAL_ROOT` | `./.vgc_data` | 로컬 실행 시 저장 루트 |

## 디스플레이가 필요한 경우

Colab 에는 물리 디스플레이가 없습니다. GUI 앱을 띄워야 하면
`setup_environment(install_headless_display=True)` 로 Xvfb 가상 디스플레이를 시작하세요.

## 민감정보 취급

이 저장소는 공개이므로 비밀 값을 커밋하지 마세요.

- API 키·토큰은 코드/노트북에 직접 쓰지 말고 Colab 왼쪽 '보안 비밀'(🔑)에 저장한 뒤 `google.colab.userdata.get("NAME")` 으로 읽으세요.
- 노트북은 커밋 전에 셀 출력을 지우세요 (출력에 Drive 이메일·경로·키가 남을 수 있습니다).
- 스크린샷에 개인정보가 찍힐 수 있으니 Drive 의 `Vision-based_GUI_Controller/` 폴더를 공개 공유하지 마세요.
- `.env`, 키/인증서, 체크포인트 파일은 `.gitignore` 로 제외되어 있습니다.

## 로컬 개발

```bash
pip install -e ".[dev]"
```

```bash
python -m pytest -q
```

## 라이선스

Apache License 2.0 — [LICENSE](LICENSE) 참고.
