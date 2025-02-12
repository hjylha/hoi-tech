
# from pathlib import Path

import pytest

import fix_imports
import read_hoi_files as rhf


@pytest.fixture
def aod_path():
    return rhf.get_aod_path()


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


def test_get_policy_names_path(aod_path):
    if aod_path.exists():
        assert rhf.get_policy_names_path().exists()


def test_get_government_titles_path(aod_path):
    if aod_path.exists():
        assert rhf.get_government_titles_path().exists()


def test_get_idea_titles_path(aod_path):
    if aod_path.exists():
        assert rhf.get_idea_titles_path().exists()


def test_get_save_game_path(aod_path):
    if aod_path.exists():
        assert rhf.get_save_game_path().exists()


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
