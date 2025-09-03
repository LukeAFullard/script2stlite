import pytest
from script2stlite.functions import load_toml_from_file

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
