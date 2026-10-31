from pathlib import Path

import pytest

from vgc import env


def test_local_paths(tmp_path, monkeypatch):
    monkeypatch.delenv("COLAB_RELEASE_TAG", raising=False)
    p = env.get_project_paths(local_root=tmp_path / "data", use_drive=False)
    assert not p.on_drive
    for d in (p.screenshots, p.logs, p.checkpoints, p.data, p.outputs):
        assert d.is_dir() and d.parent == p.root


def test_drive_paths_layout(tmp_path):
    p = env.get_project_paths(drive_mount=tmp_path, project_dir="proj", use_drive=True)
    assert p.on_drive
    assert p.root == tmp_path / "MyDrive" / "proj"
    assert p.screenshots.is_dir()


def test_drive_paths_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("VGC_DRIVE_MOUNT", str(tmp_path))
    monkeypatch.setenv("VGC_PROJECT_DIR", "custom")
    p = env.get_project_paths(use_drive=True)
    assert p.root == tmp_path / "MyDrive" / "custom"


def test_create_false_does_not_touch_disk(tmp_path):
    p = env.get_project_paths(drive_mount=tmp_path, use_drive=True, create=False)
    assert not p.root.exists()


def test_mount_outside_colab_raises(monkeypatch):
    monkeypatch.delenv("COLAB_RELEASE_TAG", raising=False)
    monkeypatch.setattr(env, "is_colab", lambda: False)
    with pytest.raises(RuntimeError):
        env.mount_drive()


def test_mount_skips_when_already_mounted(tmp_path, monkeypatch):
    (tmp_path / "MyDrive").mkdir()
    monkeypatch.setattr(env, "is_colab", lambda: True)
    assert env.mount_drive(tmp_path) == Path(tmp_path)


def test_setup_environment_local(tmp_path, monkeypatch):
    monkeypatch.setattr(env, "is_colab", lambda: False)
    monkeypatch.setenv("VGC_LOCAL_ROOT", str(tmp_path / "x"))
    p = env.setup_environment()
    assert not p.on_drive and p.root.is_dir()
