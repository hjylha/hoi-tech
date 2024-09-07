
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


@pytest.fixture
def aod_path():
    return rhf.get_aod_path()


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


def test_get_tech_path(aod_path):
    if aod_path.exists():
        assert rhf.get_tech_path().exists()


def test_get_scenario_paths(aod_path):
    if aod_path.exists():
        path_33, path_34 = rhf.get_scenario_paths()
        assert path_33.exists()
        assert path_34.exists()


def test_get_scenario_path_for_country(aod_path):
    if aod_path.exists():
        for code in ("AFG", "ENG", "FIN", "ITA", "SOV", "USA"):
            assert rhf.get_scenario_path_for_country(code).exists()


def test_get_misc_path(aod_path):
    if aod_path.exists():
        assert rhf.get_misc_path().exists()


def test_get_difficulty_path(aod_path):
    if aod_path.exists():
        assert rhf.get_difficulty_path().exists()


def test_get_minister_modifier_path(aod_path):
    if aod_path.exists():
        assert rhf.get_minister_modifier_path().exists()


def test_get_ideas_path(aod_path):
    if aod_path.exists():
        assert rhf.get_ideas_path().exists()


def test_get_ministers_path(aod_path):
    if aod_path.exists():
        for code in ("AFG", "ENG", "FIN", "ITA", "SOV", "USA"):
            assert rhf.get_ministers_path(code).exists()


def test_get_policies_path(aod_path):
    if aod_path.exists():
        assert rhf.get_policies_path().exists()


def test_get_tech_names_path(aod_path):
    if aod_path.exists():
        assert rhf.get_tech_names_path().exists()


def test_get_country_names_path(aod_path):
    if aod_path.exists():
        assert rhf.get_country_names_path().exists()


def test_get_save_game_path(aod_path):
    if aod_path.exists():
        assert rhf.get_save_game_path().exists()


@pytest.mark.parametrize(
        "text, result", [
            ("0", 0),
            ("314", 314),
            ("-5", -5),
            ("2.71", 2.71),
            ("0.500", 0.5),
            ("-3.140", -3.14),
            ("testing", "testing"),
            ('"quoted"', 'quoted'),
            ("  testing  ", "testing")
        ]
)
def test_change_type_if_necessary(text, result):
    assert rhf.change_type_if_necessary(text) == result