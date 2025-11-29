
import os
from pathlib import Path


this_files_directory = Path(__file__).parent
gamepath_in = "aod_path.txt"
gamepath_in_linux = "aod_path_linux.txt"
scenario_file_paths_file = "scenario_file_paths.csv"



def get_aod_path():
    if os.name == "nt":
        with open(this_files_directory / gamepath_in, "r") as f:
            return Path(f.read().strip())
    with open(this_files_directory / gamepath_in_linux, "r") as f:
        return Path(f.read().strip())


def get_tech_path():
    aod_path = get_aod_path()
    tech_path = aod_path / "db" / "tech"
    return tech_path


def get_tech_files(tech_path):
    return tech_path.glob("*_tech.txt")


def get_tech_team_files(tech_path):
    tech_team_path = tech_path / "teams"
    return tech_team_path.glob("teams*.csv")

def get_scenario_paths():
    aod_path = get_aod_path()
    scenario33_path = aod_path / "scenarios" / "1933"
    scenario34_path = aod_path / "scenarios" / "1934"
    return [scenario33_path, scenario34_path]

# this is not always correct
def get_scenario_path_for_country(country_code):
    scenario_directories = get_scenario_paths()
    for sd_path in scenario_directories:
        possible_path = sd_path / f"{country_code.lower()}_{sd_path.stem[-2:]}.inc"
        if possible_path.exists():
            return possible_path

def get_misc_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "misc.txt"

def get_difficulty_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "difficulty.csv"

def get_minister_modifier_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "ministers" / "minister_modifiers.txt"

def get_ideas_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "ideas" / "ideas.txt"

def get_ministers_path(country_code):
    aod_path = get_aod_path()
    return aod_path / "db" / "ministers" / f"ministers_{country_code.lower()}.csv"

def get_policies_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "province_rev.inc"

def get_tech_names_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "tech_names.csv"

def get_country_names_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "world_names.csv"

def get_policy_names_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "new_text.csv"

def get_government_titles_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "text.csv"

def get_idea_titles_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "boostertext.csv"

def get_save_game_path():
    aod_path = get_aod_path()
    return aod_path / "scenarios" / "save games"

def get_save_games():
    save_game_folder = get_save_game_path()
    return save_game_folder.glob("*.eug")
