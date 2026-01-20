
import pytest

import fix_imports
import file_paths as fp


@pytest.fixture
def aod_path():
    return fp.get_aod_path()

def test_get_aod_path(aod_path):
    assert aod_path.exists()


def test_get_db_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_db_folder_path(aod_path).exists()


def test_get_config_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_config_folder_path(aod_path).exists()


def test_get_scenarios_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_scenarios_folder_path(aod_path).exists()


def test_get_tech_path(aod_path):
    if aod_path.exists():
        assert fp.get_tech_path(aod_path).exists()


def test_get_tech_files(aod_path):
    if aod_path.exists():
        tech_path = fp.get_tech_path(aod_path)
        industry_tech_path = tech_path / "industry_tech.txt"
        tech_files = fp.get_tech_files(tech_path)
        assert industry_tech_path in tech_files


def test_get_tech_team_files(aod_path):
    if aod_path.exists():
        tech_path = fp.get_tech_path(aod_path)
        uk_tech_teams_path = tech_path / "teams" / "teams_eng.csv"
        tech_team_files = fp.get_tech_team_files(tech_path)
        assert uk_tech_teams_path in tech_team_files


def test_get_scenario_paths(aod_path):
    if aod_path.exists():
        path_33, path_34 = fp.get_scenario_paths(aod_path)
        assert path_33.exists()
        assert path_34.exists()


def test_get_scenario_path_for_country(aod_path):
    if aod_path.exists():
        for code in ("AFG", "ENG", "FIN", "ITA", "SOV", "USA"):
            assert fp.get_scenario_path_for_country(code, aod_path).exists()


def test_get_misc_path(aod_path):
    if aod_path.exists():
        assert fp.get_misc_path(aod_path).exists()


def test_get_difficulty_path(aod_path):
    if aod_path.exists():
        assert fp.get_difficulty_path(aod_path).exists()


def test_get_ministers_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_ministers_folder_path(aod_path).exists()


def test_get_minister_modifier_path(aod_path):
    if aod_path.exists():
        assert fp.get_minister_modifier_path(aod_path).exists()


def test_get_ideas_path(aod_path):
    if aod_path.exists():
        assert fp.get_ideas_path(aod_path).exists()


def test_get_ministers_path(aod_path):
    if aod_path.exists():
        for code in ("AFG", "ENG", "FIN", "ITA", "SOV", "USA"):
            assert fp.get_ministers_path(code, aod_path).exists()


def test_get_ministers_files(aod_path):
    if aod_path.exists():
        ministers_folder_path = fp.get_ministers_folder_path(aod_path)
        uk_ministers = ministers_folder_path / "ministers_eng.csv"
        assert uk_ministers in fp.get_ministers_files(aod_path)


def test_get_province_rev_path(aod_path):
    if aod_path.exists():
        assert fp.get_province_rev_path(aod_path).exists()


def test_get_leaders_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_leaders_folder_path(aod_path).exists()


def test_get_leaders_files(aod_path):
    if aod_path.exists():
        leaders_folder_path = fp.get_leaders_folder_path(aod_path)
        swe_leaders = leaders_folder_path / "sweden.csv"
        leaders_files = list(fp.get_leaders_files(aod_path))
        assert swe_leaders in leaders_files
        assert len(leaders_files) >= 100


def test_get_units_folder_path(aod_path):
    if aod_path.exists():
        assert fp.get_units_folder_path(aod_path).exists()


def test_get_divisions_files(aod_path):
    if aod_path.exists():
        units_folder_path = fp.get_units_folder_path(aod_path)
        infantry_file = units_folder_path / "divisions" / "infantry.txt"
        division_files = list(fp.get_divisions_files(aod_path))
        assert infantry_file in division_files
        assert len(division_files) >= 30


def test_get_brigades_files(aod_path):
    if aod_path.exists():
        units_folder_path = fp.get_units_folder_path(aod_path)
        artillery_file = units_folder_path / "brigades" / "artillery.txt"
        brigade_files = list(fp.get_brigades_files(aod_path))
        assert artillery_file in brigade_files
        assert len(brigade_files) >= 50


def test_get_unit_modifiers_filepath(aod_path):
    if aod_path.exists():
        assert fp.get_unit_modifiers_filepath(aod_path).exists()


def test_get_tech_names_path(aod_path):
    if aod_path.exists():
        assert fp.get_tech_names_path(aod_path).exists()


def test_get_country_names_path(aod_path):
    if aod_path.exists():
        assert fp.get_country_names_path(aod_path).exists()


def test_get_policy_names_path(aod_path):
    if aod_path.exists():
        assert fp.get_policy_names_path(aod_path).exists()


def test_get_government_titles_path(aod_path):
    if aod_path.exists():
        assert fp.get_government_titles_path(aod_path).exists()


def test_get_idea_titles_path(aod_path):
    if aod_path.exists():
        assert fp.get_idea_titles_path(aod_path).exists()


def test_get_province_names_path(aod_path):
    if aod_path.exists():
        assert fp.get_province_names_path(aod_path).exists()


def test_get_event_text_paths(aod_path):
    if aod_path.exists():
        paths = fp.get_event_text_paths(aod_path)
        for filepath in paths:
            assert filepath.exists()


def test_get_all_text_files_paths(aod_path):
    if aod_path.exists():
        paths = fp.get_all_text_files_paths(aod_path)
        assert len(paths) == 18
        assert aod_path / "config" / "text.csv" in paths
        assert aod_path / "config" / "Additional" / "addon.csv" in paths
        for filepath in paths:
            assert filepath.exists()

def test_get_save_game_path(aod_path):
    if aod_path.exists():
        assert fp.get_save_game_path(aod_path).exists()


def test_get_scenarios(aod_path):
    if aod_path.exists():
        default_scenario_path = fp.get_scenarios_folder_path(aod_path) / fp.DEFAULT_SCENARIO
        assert default_scenario_path in fp.get_scenarios(aod_path)
