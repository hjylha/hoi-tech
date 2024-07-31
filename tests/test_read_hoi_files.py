
from pathlib import Path

import pytest

import fix_imports
import read_hoi_files as rhf


@pytest.fixture
def txt_file_content0():
    return {"key1": "normal value", "key2": 2, "key3": 3.14}

@pytest.fixture
def txt_file_content1():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    return content

@pytest.fixture
def txt_file_content2():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    layer1 = {
        "key1": [3, 5],
        "key2": ["a", "b", "c"]
    }
    content["layer0"]["layer1"] = layer1
    return content

@pytest.fixture
def txt_file_content3():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    layer2 = {"key1": [0, 1]}
    layer1 = {
        "key1": [3, 5],
        "key2": ["a", "b", "c"],
        "layer2": layer2
    }
    content["layer0"]["layer1"] = layer1

    return content


def test_read_txt_file0(txt_file_content0):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing0.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content0


def test_read_txt_file1(txt_file_content1):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing1.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content1

def test_read_txt_file2(txt_file_content2):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing2.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content2

def test_read_txt_file3(txt_file_content3):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing3.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content3