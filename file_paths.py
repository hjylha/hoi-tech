
import os
from pathlib import Path


this_files_directory = Path(__file__).parent
gamepath_in = "aod_path.txt"
gamepath_in_linux = "aod_path_linux.txt"
scenario_file_paths_file = "scenario_file_paths.csv"

DEFAULT_SCENARIO = "1933.eug"


def get_gamepath_filepath():
    if os.name == "nt":
        return this_files_directory / gamepath_in
    return this_files_directory / gamepath_in_linux

def get_aod_path():
    gamepath_in_file = get_gamepath_filepath()
    with open(gamepath_in_file, "r") as f:
        return Path(f.read().strip())


def get_db_folder_path(aod_path):
    return aod_path / "db"

def get_config_folder_path(aod_path):
    return aod_path / "config"

def get_scenarios_folder_path(aod_path):
    return aod_path / "scenarios"

def get_tech_path(aod_path):
    return get_db_folder_path(aod_path) / "tech"


def get_tech_files(tech_path):
    return tech_path.glob("*_tech.txt")


def get_tech_team_files(tech_path):
    tech_team_path = tech_path / "teams"
    return tech_team_path.glob("teams*.csv")

def get_scenario_paths(aod_path):
    scenario_folder_path = get_scenarios_folder_path(aod_path)
    scenario33_path = scenario_folder_path / "1933"
    scenario34_path = scenario_folder_path / "1934"
    return [scenario33_path, scenario34_path]

# this is not always correct
def get_scenario_path_for_country(country_code, aod_path):
    scenario_directories = get_scenario_paths(aod_path)
    for sd_path in scenario_directories:
        possible_path = sd_path / f"{country_code.lower()}_{sd_path.stem[-2:]}.inc"
        if possible_path.exists():
            return possible_path

def get_misc_path(aod_path):
    return get_db_folder_path(aod_path) / "misc.txt"

def get_difficulty_path(aod_path):
    return get_db_folder_path(aod_path) / "difficulty.csv"

def get_ministers_folder_path(aod_path):
    return get_db_folder_path(aod_path) / "ministers"

def get_minister_modifier_path(aod_path):
    return get_ministers_folder_path(aod_path) / "minister_modifiers.txt"

def get_ideas_path(aod_path):
    return get_db_folder_path(aod_path) / "ideas" / "ideas.txt"

def get_ministers_path(country_code, aod_path):
    return get_ministers_folder_path(aod_path) / f"ministers_{country_code.lower()}.csv"

def get_ministers_files(aod_path):
    return get_ministers_folder_path(aod_path).glob("ministers_*.csv")

def get_policies_path(aod_path):
    return get_db_folder_path(aod_path) / "province_rev.inc"

def get_tech_names_path(aod_path):
    return get_config_folder_path(aod_path) / "tech_names.csv"

def get_country_names_path(aod_path):
    return get_config_folder_path(aod_path) / "world_names.csv"

def get_policy_names_path(aod_path):
    return get_config_folder_path(aod_path) / "new_text.csv"

def get_government_titles_path(aod_path):
    return get_config_folder_path(aod_path) / "text.csv"

def get_idea_titles_path(aod_path):
    return get_config_folder_path(aod_path) / "boostertext.csv"

def get_province_names_path(aod_path):
    return get_config_folder_path(aod_path) / "province_names.csv"

def get_event_text_paths(aod_path):
    config_path = get_config_folder_path(aod_path)
    return [
        config_path / "doomsdaytext.csv",
        config_path / "event_text.csv",
        config_path / "boostertext.csv",
        config_path / "modtext.csv",
        config_path / "new_text.csv",
        config_path / "extra_text.csv",
        config_path / "Additional" / "addon.csv"
    ]

def get_all_text_files_paths(aod_path):
    config_path = get_config_folder_path(aod_path)
    paths = list(config_path.glob("**/*.csv", case_sensitive=False))
    return paths

def get_save_game_path(aod_path):
    return get_scenarios_folder_path(aod_path) / "save games"

def get_save_games(aod_path):
    save_game_folder = get_save_game_path(aod_path)
    return save_game_folder.glob("*.eug")

def get_scenarios(aod_path):
    scenario_folder = get_scenarios_folder_path(aod_path)
    return scenario_folder.glob("*.eug")
