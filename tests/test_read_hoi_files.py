
# from pathlib import Path

import pytest

import fix_imports
import file_paths as fp
import read_hoi_files as rhf


@pytest.fixture
def aod_path():
    return fp.get_aod_path()


def test_read_difficulty_file(aod_path):
    if aod_path.exists():
        difficulty_dict = rhf.read_difficulty_file()
        # hopefully nobody changes these
        difficulties = ["VERYEASY", "EASY", "NORMAL", "HARD", "VERYHARD"]
        for difficulty in difficulties:
            assert isinstance(difficulty_dict[difficulty], int)


def test_get_minister_and_policy_names(aod_path):
    if aod_path.exists():
        names = rhf.get_minister_and_policy_names()
        assert names["NPERSONALITY_GENERAL_STAFFER"] == "General Staffer"
        assert names["NAME_POLICY_CULTURE_ENTERPRISE"] == "Individualist Enterprise Culture"


def test_format_title():
    assert rhf.format_title("ARMAMENT_MINISTER") == "ArmamentMinister"


def test_get_government_titles(aod_path):
    if aod_path.exists():
        titles = rhf.get_government_titles()
        assert titles["ArmamentMinister"] == "Armaments Minister"


def test_get_idea_titles(aod_path):
    if aod_path.exists():
        titles = rhf.get_idea_titles()
        assert titles["SOCIAL_POLICY"] == "Social Policy"


def test_get_province_names(aod_path):
    if aod_path.exists():
        province_names = rhf.get_province_names()
        assert province_names[19] == "London"
        assert province_names[300] == "Berlin"
        assert province_names[606] == "Washington D.C."
