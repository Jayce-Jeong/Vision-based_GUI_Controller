"""Vision-based GUI Controller."""

from .env import (
    DEFAULT_DRIVE_MOUNT,
    DEFAULT_PROJECT_DIRNAME,
    ProjectPaths,
    get_project_paths,
    is_colab,
    mount_drive,
    setup_environment,
)

__all__ = [
    "DEFAULT_DRIVE_MOUNT",
    "DEFAULT_PROJECT_DIRNAME",
    "ProjectPaths",
    "get_project_paths",
    "is_colab",
    "mount_drive",
    "setup_environment",
]
__version__ = "0.1.0"
