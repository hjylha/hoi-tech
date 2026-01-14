
import os
from pathlib import Path

import file_paths as fp


def get_folder_example():
    if os.name == "nt":
        return "C:\\games\\arsenalofdemocracy"
    return "~/Games/ArsenalOfDemocracy"


def is_aod_filepath_ok(aod_filepath):
    if not aod_filepath.exists():
        return False
    if not fp.get_db_folder_path(aod_filepath).exists():
        return False
    if not fp.get_config_folder_path(aod_filepath).exists():
        return False
    scenario_folder = fp.get_scenarios_folder_path(aod_filepath)
    if not scenario_folder.exists():
        return False
    default_scenario_path = scenario_folder / fp.DEFAULT_SCENARIO
    if not default_scenario_path.exists():
        return False
    if not fp.get_tech_path(aod_filepath).exists():
        return False
    if not fp.get_misc_path(aod_filepath).exists():
        return False
    if not fp.get_difficulty_path(aod_filepath).exists():
        return False
    if not fp.get_ministers_folder_path(aod_filepath).exists():
        return False
    if not fp.get_minister_modifier_path(aod_filepath).exists():
        return False
    if not fp.get_ideas_path(aod_filepath).exists():
        return False
    if not fp.get_policies_path(aod_filepath).exists():
        return False
    if not fp.get_tech_names_path(aod_filepath).exists():
        return False
    return True


def create_aod_path_file(aod_filepath):
    gamepath_file = fp.get_gamepath_filepath()
    with open(gamepath_file, "w") as f:
        f.write(str(aod_filepath))


def ask_for_aod_path():
    while True:
        possible_aod_path_str = input(f"\nWrite (or paste) the path to the main Iron Cross folder \n  (for example {get_folder_example()}):\n").strip()
        if possible_aod_path_str.startswith("~"):
            possible_aod_path_str = possible_aod_path_str.replace("~", os.getenv("HOME"))
        possible_aod_path = Path(possible_aod_path_str)
        if is_aod_filepath_ok(possible_aod_path):
            return possible_aod_path
        print(f"{possible_aod_path} does not seem to be a correct path.")
        yes_or_no = input("Do you want to try again (Y/N)? [Default: Y] ")
        if yes_or_no.lower().startswith("n"):
            return


def make_sure_aod_path_is_known():
    try:
        aod_path = fp.get_aod_path()
        if is_aod_filepath_ok(aod_path):
            return True
    except FileNotFoundError:
        pass
    aod_path = ask_for_aod_path()
    if aod_path:
        create_aod_path_file(aod_path)
        print(f"Iron Cross folder saved: {aod_path}")
        return True
    return False


is_it_ok = make_sure_aod_path_is_known()
if is_it_ok:
    print(f"Iron Cross located in folder: {fp.get_aod_path()}")
else:
    raise Exception("Things are very bad, at least when it comes to knowing where Iron Cross files are.")

AOD_PATH = fp.get_aod_path()
