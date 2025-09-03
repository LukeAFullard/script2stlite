import pytest
import os
from script2stlite.functions import (
    load_toml_from_file,
    file_exists,
    folder_exists,
    create_directory,
)


def test_load_toml_from_file(tmp_path):
    # Test loading a valid TOML file
    p = tmp_path / "test.toml"
    p.write_text('[tool.poetry]\nname = "my-project"\nversion = "0.1.0"')
    data = load_toml_from_file(p)
    assert data == {"tool": {"poetry": {"name": "my-project", "version": "0.1.0"}}}

    # Test with a non-existent file
    with pytest.raises(FileNotFoundError):
        load_toml_from_file("non_existent.toml")

    # Test with an invalid TOML file
    p = tmp_path / "invalid.toml"
    p.write_text("invalid toml content")
    with pytest.raises(RuntimeError):
        load_toml_from_file(p)


def test_file_folder_exists(tmp_path):
    # Test file_exists
    p = tmp_path / "test_file.txt"
    p.write_text("hello")
    assert file_exists(p) is True
    assert file_exists(tmp_path / "non_existent.txt") is False
    assert file_exists(tmp_path) is False  # It's a directory, not a file

    # Test folder_exists
    d = tmp_path / "test_dir"
    d.mkdir()
    assert folder_exists(d) is True
    assert folder_exists(tmp_path / "non_existent_dir") is False
    assert folder_exists(p) is False  # It's a file, not a directory


def test_create_directory(tmp_path):
    # Test creating a new directory
    new_dir = tmp_path / "new_dir"
    assert create_directory(new_dir) is True
    assert os.path.isdir(new_dir)

    # Test creating a directory that already exists
    assert create_directory(new_dir, exist_ok=True) is True
    assert os.path.isdir(new_dir)

    # Test creating nested directories
    nested_dir = tmp_path / "parent" / "child"
    assert create_directory(nested_dir) is True
    assert os.path.isdir(nested_dir)
