"""Google Colab / Google Drive 연동 유틸리티.

Colab 에서는 Google Drive 를 마운트해 결과물(스크린샷, 로그, 체크포인트, 데이터)을
영구 저장하고, 로컬(비-Colab) 환경에서는 같은 구조의 폴더를 로컬 디스크에 만든다.
따라서 호출하는 쪽 코드는 환경을 신경 쓸 필요 없이 ``ProjectPaths`` 만 사용하면 된다.

환경 변수
---------
VGC_DRIVE_MOUNT      Drive 마운트 지점 (기본: /content/drive)
VGC_PROJECT_DIR      Drive 안의 프로젝트 폴더 이름/경로 (기본: Vision-based_GUI_Controller)
VGC_LOCAL_ROOT       비-Colab 환경에서 사용할 루트 폴더 (기본: ./.vgc_data)
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DRIVE_MOUNT = "/content/drive"
DEFAULT_PROJECT_DIRNAME = "Vision-based_GUI_Controller"
# Drive 마운트 후 '내 드라이브' 루트 폴더 이름
_MY_DRIVE = "MyDrive"
_SUBDIRS = ("screenshots", "logs", "checkpoints", "data", "outputs")


def is_colab() -> bool:
    """현재 Google Colab 에서 실행 중이면 True."""
    return "google.colab" in sys.modules or bool(os.environ.get("COLAB_RELEASE_TAG"))


def mount_drive(mount_point: str | os.PathLike | None = None, force_remount: bool = False) -> Path:
    """Google Drive 를 마운트하고 마운트 지점을 반환한다.

    Colab 이 아니면 ``RuntimeError`` 를 발생시킨다. 이미 마운트되어 있으면
    다시 마운트하지 않는다.
    """
    mount = Path(mount_point or os.environ.get("VGC_DRIVE_MOUNT", DEFAULT_DRIVE_MOUNT))
    if not is_colab():
        raise RuntimeError("Google Drive 마운트는 Google Colab 에서만 가능합니다.")
    if (mount / _MY_DRIVE).is_dir() and not force_remount:
        return mount
    from google.colab import drive  # type: ignore[import-not-found]

    drive.mount(str(mount), force_remount=force_remount)
    return mount


@dataclass(frozen=True)
class ProjectPaths:
    """프로젝트 산출물이 저장되는 폴더 모음."""

    root: Path
    screenshots: Path
    logs: Path
    checkpoints: Path
    data: Path
    outputs: Path
    on_drive: bool

    def ensure(self) -> "ProjectPaths":
        for p in (self.root, self.screenshots, self.logs, self.checkpoints, self.data, self.outputs):
            p.mkdir(parents=True, exist_ok=True)
        return self


def get_project_paths(
    drive_mount: str | os.PathLike | None = None,
    project_dir: str | None = None,
    local_root: str | os.PathLike | None = None,
    use_drive: bool | None = None,
    create: bool = True,
) -> ProjectPaths:
    """저장 경로를 결정한다.

    * ``use_drive`` 가 None 이면 Colab 에서만 Drive 를 사용한다.
    * Drive 사용 시: ``<mount>/MyDrive/<project_dir>/``
    * 그렇지 않으면: ``<local_root>/`` (기본 ``./.vgc_data``)
    """
    if use_drive is None:
        use_drive = is_colab()

    if use_drive:
        mount = Path(drive_mount or os.environ.get("VGC_DRIVE_MOUNT", DEFAULT_DRIVE_MOUNT))
        name = project_dir or os.environ.get("VGC_PROJECT_DIR", DEFAULT_PROJECT_DIRNAME)
        root = mount / _MY_DRIVE / name
    else:
        root = Path(local_root or os.environ.get("VGC_LOCAL_ROOT", ".vgc_data")).expanduser().resolve()

    paths = ProjectPaths(
        root=root,
        **{name: root / name for name in _SUBDIRS},
        on_drive=bool(use_drive),
    )
    return paths.ensure() if create else paths


def setup_environment(
    mount: bool = True,
    project_dir: str | None = None,
    install_headless_display: bool = False,
) -> ProjectPaths:
    """Colab 노트북 첫 셀에서 호출하는 원스톱 초기화 함수.

    1. (Colab 이면) Drive 마운트
    2. 프로젝트 폴더 구조 생성
    3. (선택) 디스플레이가 없는 Colab 에서 GUI 를 띄우기 위한 가상 디스플레이 시작
    """
    use_drive = False
    if is_colab() and mount:
        mount_drive()
        use_drive = True

    paths = get_project_paths(project_dir=project_dir, use_drive=use_drive)

    if install_headless_display:
        _start_virtual_display()

    return paths


def _start_virtual_display(size: tuple[int, int] = (1280, 800)) -> None:
    """Xvfb 가상 디스플레이를 시작한다 (Colab 에는 물리 디스플레이가 없다)."""
    import subprocess

    if os.environ.get("DISPLAY"):
        return
    if not _which("Xvfb"):
        subprocess.run(["apt-get", "-qq", "install", "-y", "xvfb"], check=True)
    display = ":99"
    subprocess.Popen(
        ["Xvfb", display, "-screen", "0", f"{size[0]}x{size[1]}x24"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.environ["DISPLAY"] = display


def _which(cmd: str) -> str | None:
    from shutil import which

    return which(cmd)
