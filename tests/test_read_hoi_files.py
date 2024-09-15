
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


def test_get_save_game_path(aod_path):
    if aod_path.exists():
        assert rhf.get_save_game_path().exists()
