
import os
from pathlib import Path


this_files_directory = Path(__file__).parent
gamepath_in = "aod_path.txt"
gamepath_in_linux = "aod_path_linux.txt"
scenario_file_paths_file = "scenario_file_paths.csv"

DEFAULT_SCENARIO = "1933.eug"



def get_aod_path():
    if os.name == "nt":
        with open(this_files_directory / gamepath_in, "r") as f:
            return Path(f.read().strip())
    with open(this_files_directory / gamepath_in_linux, "r") as f:
        return Path(f.read().strip())

def get_db_folder_path():
    return get_aod_path() / "db"

def get_config_folder_path():
    return get_aod_path() / "config"

def get_scenarios_folder_path():
    return get_aod_path() / "scenarios"

def get_tech_path():
    return get_db_folder_path() / "tech"


def get_tech_files(tech_path):
    return tech_path.glob("*_tech.txt")


def get_tech_team_files(tech_path):
    tech_team_path = tech_path / "teams"
    return tech_team_path.glob("teams*.csv")

def get_scenario_paths():
    scenario_folder_path = get_scenarios_folder_path()
    scenario33_path = scenario_folder_path / "1933"
    scenario34_path = scenario_folder_path / "1934"
    return [scenario33_path, scenario34_path]

# this is not always correct
def get_scenario_path_for_country(country_code):
    scenario_directories = get_scenario_paths()
    for sd_path in scenario_directories:
        possible_path = sd_path / f"{country_code.lower()}_{sd_path.stem[-2:]}.inc"
        if possible_path.exists():
            return possible_path

def get_misc_path():
    return get_db_folder_path() / "misc.txt"

def get_difficulty_path():
    return get_db_folder_path() / "difficulty.csv"

def get_ministers_folder_path():
    return get_db_folder_path() / "ministers"

def get_minister_modifier_path():
    return get_ministers_folder_path() / "minister_modifiers.txt"

def get_ideas_path():
    return get_db_folder_path() / "ideas" / "ideas.txt"

def get_ministers_path(country_code):
    return get_ministers_folder_path() / f"ministers_{country_code.lower()}.csv"

def get_ministers_files():
    return get_ministers_folder_path().glob("ministers_*.csv")

def get_policies_path():
    return get_db_folder_path() / "province_rev.inc"

def get_tech_names_path():
    return get_config_folder_path() / "tech_names.csv"

def get_country_names_path():
    return get_config_folder_path() / "world_names.csv"

def get_policy_names_path():
    return get_config_folder_path() / "new_text.csv"

def get_government_titles_path():
    return get_config_folder_path() / "text.csv"

def get_idea_titles_path():
    return get_config_folder_path() / "boostertext.csv"

def get_save_game_path():
    return get_scenarios_folder_path() / "save games"

def get_save_games():
    save_game_folder = get_save_game_path()
    return save_game_folder.glob("*.eug")

def get_scenarios():
    scenario_folder = get_scenarios_folder_path()
    return scenario_folder.glob("*.eug")
