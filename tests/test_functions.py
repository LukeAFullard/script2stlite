import pytest
from script2stlite.functions import get_value_of_max_key, flatten_dict, load_text_from_file, load_yaml_from_file, load_yaml_from_url
import os
import requests

def test_get_value_of_max_key():
    # Test with a dictionary of version strings
    data = {'0.87.0': 'url1', '0.88.0': 'url2', '0.86.0': 'url3'}
    assert get_value_of_max_key(data) == 'url2'

    # Test with a dictionary of integers
    data = {1: 'a', 10: 'b', 5: 'c'}
    assert get_value_of_max_key(data) == 'b'

    # Test with an empty dictionary
    with pytest.raises(ValueError):
        get_value_of_max_key({})

    # Test with non-comparable keys
    with pytest.raises(TypeError):
        get_value_of_max_key({1: 'a', 'key': 'b'})

def test_flatten_dict():
    # Test with a simple nested dictionary
    d = {'a': 1, 'b': {'c': 2, 'd': 3}}
    expected = {'a': 1, 'b.c': 2, 'b.d': 3}
    assert flatten_dict(d) == expected

    # Test with multiple levels of nesting
    d = {'a': {'b': {'c': 1}}, 'd': 2}
    expected = {'a.b.c': 1, 'd': 2}
    assert flatten_dict(d) == expected

    # Test with a custom separator
    d = {'a': {'b': 1}, 'c': 2}
    expected = {'a_b': 1, 'c': 2}
    assert flatten_dict(d, sep='_') == expected

    # Test with an empty dictionary
    assert flatten_dict({}) == {}


def test_load_text_from_file(tmp_path):
    # Test loading a simple text file
    p = tmp_path / "test.txt"
    p.write_text("Hello, World!\n")
    content = load_text_from_file(p, escape_text=False)
    assert content == "Hello, World!\n"

    # Test the escaping logic
    p = tmp_path / "test_with_special_chars.txt"
    p.write_text("This is a `test` with backslashes \\ and dollar signs ${}.\n")
    content = load_text_from_file(p)
    expected = "This is a \\`test\\` with backslashes \\\\ and dollar signs \\${}.\n"
    assert content == expected

    # Test for FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_text_from_file("non_existent_file.txt")


def test_load_yaml_from_file(tmp_path):
    # Test loading a valid YAML file
    p = tmp_path / "test.yaml"
    p.write_text("key: value\nanother_key: 123")
    data = load_yaml_from_file(p)
    assert data == {"key": "value", "another_key": 123}

    # Test with a non-existent file
    with pytest.raises(FileNotFoundError):
        load_yaml_from_file("non_existent.yaml")

    # Test with an invalid YAML file
    p = tmp_path / "invalid.yaml"
    p.write_text("key: value: invalid")
    with pytest.raises(RuntimeError):
        load_yaml_from_file(p)

    # Test with a YAML file that is not a dictionary
    p = tmp_path / "not_a_dict.yaml"
    p.write_text("- item1\n- item2")
    with pytest.raises(ValueError):
        load_yaml_from_file(p)


def test_load_yaml_from_url(mocker):
    # Mock successful response
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock()
    mock_response.text = "key: value"
    mocker.patch('requests.get', return_value=mock_response)

    data = load_yaml_from_url("http://fakeurl.com/test.yaml")
    assert data == {"key": "value"}
    requests.get.assert_called_once_with("http://fakeurl.com/test.yaml", timeout=10)

    # Mock network error
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Network Error"))
    with pytest.raises(RuntimeError, match="Failed to fetch YAML file"):
        load_yaml_from_url("http://fakeurl.com/test.yaml")

    # Mock invalid YAML content
    mock_response.text = "key: value: invalid"
    mocker.patch('requests.get', return_value=mock_response)
    with pytest.raises(RuntimeError, match="Failed to parse YAML content"):
        load_yaml_from_url("http://fakeurl.com/test.yaml")

    # Mock non-dictionary YAML content
    mock_response.text = "- item1"
    mocker.patch('requests.get', return_value=mock_response)
    with pytest.raises(ValueError, match="YAML content is not a dictionary"):
        load_yaml_from_url("http://fakeurl.com/test.yaml")
