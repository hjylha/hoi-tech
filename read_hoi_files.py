
import csv

import file_paths as fp
import read_files as rf
from check_file_paths import AOD_PATH


DEFAULT_SCENARIO = "1933.eug"

the_encoding = "utf-8"
text_encoding = "ISO-8859-1"
csv_encoding = "cp1252"
# special_encoding = "cp1251"


def read_name_file(filepath, language="English", language_index=1, encoding=text_encoding, show_errors=False):
    names = dict()
    with open(filepath, "r", encoding = encoding) as f:
        language_confirmed = False
        new_line = f.readline()
        while new_line:
            line = new_line.strip()
            if not language_confirmed:
                try:
                    language_index = line.split(";").index(language)
                    language_confirmed = True
                    new_line = f.readline()
                    continue
                except ValueError:
                    pass
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                new_line = f.readline()
                continue
            items = clean_line.split(";")
            if names.get(items[0]) is not None and names[items[0]] != items[language_index]:
                if show_errors:
                    print(f"PROBLEM: key {items[0]} is already in file {filepath.name}")
            names[items[0]] = items[language_index]
            new_line = f.readline()

        # for i, line in enumerate(f):
        #     if i == 0:
        #         language_index = line.split(";").index(language)
        #         continue
        #     clean_line = line.split("#")[0].strip()
        #     if not clean_line:
        #         continue
        #     # key, name = clean_line[0], clean_line[language_index]
        #     names[clean_line[0]] = clean_line[language_index]
    return names

def read_name_file_w_duplicates(filepath, names=None, language="English", language_index=1, encoding=text_encoding):
    if names is None:
        names = dict()
    with open(filepath, "r", encoding = encoding) as f:
        language_confirmed = False
        new_line = f.readline()
        while new_line:
            line = new_line.strip()
            if not language_confirmed:
                try:
                    language_index = line.split(";").index(language)
                    language_confirmed = True
                    new_line = f.readline()
                    continue
                except ValueError:
                    pass
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                new_line = f.readline()
                continue
            items = clean_line.split(";")
            key = items[0]
            name = items[language_index]
            if names.get(key) is None:
                names[key] = [(name, filepath)]
            else:
                names[key].append((name, filepath))
            new_line = f.readline()

    return names

# TODO: FIX
def read_names_from_file(search_terms, filepath, language="English", encoding=text_encoding):
    names = dict()
    with open(filepath, "r", encoding = encoding) as f:
        for i, line in enumerate(f):
            if i == 0:
                language_index = line.split(";").index(language)
                continue
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue
            if clean_line[0] in search_terms:
                names[clean_line[0]] = clean_line[language_index]
            if len(names) == len(search_terms):
                return names
    return names


def read_csv_file(filepath, check_filetype=False, delimiter=";", encoding=csv_encoding):
    return rf.read_csv_file(filepath, encoding, check_filetype=check_filetype, delimiter=delimiter)


def read_txt_file(filepath, check_filetype=False, encoding=text_encoding):
    return rf.read_txt_file(filepath, encoding, check_filetype=check_filetype)


def read_misc_file(aod_path=AOD_PATH):
    misc_filepath = fp.get_misc_path(aod_path)
    # misc_content = dict()
    # content_types = ["economy", "combat", "research"]
    # with open(misc_filepath, "r", encoding = the_encoding) as f:
    #     current_type = None
    #     for line in f:
    #         clean_line = line.split("#")[0].strip()
    #         if clean_line == "":
    #             continue
    #         for t in content_types:
    #             if t in clean_line:
    #                 misc_content[t] = []
    #                 current_type = t
    #                 break
    #         else:
    #             if "}" in clean_line:
    #                 current_type = None
    #                 continue
    #             try:
    #                 item = int(clean_line)
    #             except ValueError:
    #                 item = float(clean_line)
    #             misc_content[current_type].append(item)
    return read_txt_file(misc_filepath)

def get_blueprint_bonus_and_tech_speed_modifier(aod_path=AOD_PATH):
    misc_content = read_misc_file(aod_path)
    return misc_content["research"][0], misc_content["research"][5]


def read_difficulty_file(aod_path=AOD_PATH):
    difficulty_path = fp.get_difficulty_path(aod_path)
    data = read_csv_file(difficulty_path)
    important_rows = []
    starts = ["CATEGORY", "HUMAN", "RESEARCH"]
    starts_index = 0
    starting_string = starts[starts_index]
    row_num = 0
    while starts_index < 3:
        row_as_list = data[row_num]
        if starting_string == row_as_list[0]:
            starts_index += 1
            important_rows.append(row_as_list[1:6])
            if starts_index == 3:
                break
            starting_string = starts[starts_index]
        row_num += 1
    return {diff: int(modifier) for diff, modifier in zip(important_rows[0], important_rows[2])}


def get_country_codes_from_scenario_files(aod_path=AOD_PATH):
    scenario_paths = dict()
    path33, path34 = fp.get_scenario_paths(aod_path)
    paths33 = path33.glob("*.inc")
    paths34 = path34.glob("*.inc")
    for p in paths33:
        content = read_txt_file(p)
        try:
            country_code = content["country"]["tag"]
            if scenario_paths.get(country_code) is None:
                scenario_paths[country_code] = p.name
                continue
            print(f"Country code {country_code} already found before {p}")
        except KeyError as e:
            print("Key Error with contents in file", p)
            # raise e
    for p in paths34:
        content = read_txt_file(p)
        try:
            country_code = content["country"]["tag"]
            if scenario_paths.get(country_code) is None:
                scenario_paths[country_code] = p.name
                continue
            print(f"Country code {country_code} already found before {p}")
        except KeyError as e:
            print("Key Error with contents in file", p)
            # raise e
    return scenario_paths


def write_scenario_file_paths_to_file(filepath_dict):
    with open(fp.this_files_directory / fp.scenario_file_paths_file, "w", encoding = the_encoding) as f:
        for country_code, filename in filepath_dict.items():
            f.write(f"{country_code};{filename}\n")

def read_scenario_file_paths_from_file():
    filepath = fp.this_files_directory / fp.scenario_file_paths_file
    if not filepath.exists():
        scenario_paths = get_country_codes_from_scenario_files()
        write_scenario_file_paths_to_file(scenario_paths)
    scenario_paths = dict()
    with open(filepath, "r", encoding = the_encoding) as f:
        for line in f:
            try:
                country_code, path_str = line.strip().split(";")
                scenario_paths[country_code] = Path(path_str)
            except ValueError:
                pass
    return scenario_paths

def get_scenario_file_path_for_country(country_code):
    filepath = fp.this_files_directory / fp.scenario_file_paths_file
    if not filepath.exists():
        scenario_paths = get_country_codes_from_scenario_files()
        write_scenario_file_paths_to_file(scenario_paths)
    scenario_file_directories = fp.get_scenario_paths(AOD_PATH)
    with open(filepath, "r", encoding = the_encoding) as f:
        for line in f:
            try:
                country_code_candidate, path_str = line.strip().split(";")
                if country_code_candidate.upper() == country_code.upper():
                    for directory in scenario_file_directories:
                        path = directory / path_str
                        if path.exists():
                            return path
                    # return Path(path_str)
            except ValueError:
                pass


# def read_minister_modifiers():
#     minister_modifier_file = get_minister_modifier_path()
#     personalities_and_modifiers = dict()
#     with open(minister_modifier_file, "r", encoding = the_encoding) as f:
#         for line in f:

#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
    
#     return personalities_and_modifiers


# def read_ideas():
#     ideas_filepath = get_ideas_path()
#     ideas = dict()
#     with open(ideas_filepath, "r", encoding = the_encoding) as f:
#         for line in f:

#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
    
#     return ideas


def get_tech_names(aod_path=AOD_PATH):
    # aod_path = get_aod_path()
    # tech_names_path = aod_path / "config" / "tech_names.csv"
    tech_names_path = fp.get_tech_names_path(aod_path)
    tech_names = dict()
    with open(tech_names_path, "r", encoding = csv_encoding) as f:
        for line in f:
            names = line.split(";")
            if names[0]:
                tech_names[names[0]] = names[1]
    return tech_names


def get_country_names(aod_path=AOD_PATH, country_codes=None):
    # aod_path = get_aod_path()
    if country_codes is None:
        tech_team_files = fp.get_tech_team_files(fp.get_tech_path(aod_path))
        country_codes = [filepath.stem[-3:].upper() for filepath in tech_team_files]

    # country_names_path = aod_path / "config" / "world_names.csv"
    country_names_path = fp.get_country_names_path(aod_path)
    country_names = dict()
    with open(country_names_path, "r", encoding = csv_encoding) as f:
        for line in f:
            names = line.split(";")
            if names[0].upper() in country_codes:
                country_names[names[0].upper()] = names[1]
    # fill the missing countries
    for country_code in country_codes:
        if country_code.upper() not in country_names.keys():
            country_names[country_code.upper()] = ""
    return country_names


def get_minister_and_policy_names(aod_path=AOD_PATH):
    policy_name_file = fp.get_policy_names_path(aod_path)
    policy_and_minister_names = dict()
    with open(policy_name_file, "r", encoding = csv_encoding) as f:
        for line in f:
            names = line.split("#")[0].split(";")
            key = names[0].upper()
            if "NAME_POLICY" in key or "NPERSONALITY" in key:
                policy_and_minister_names[key] = names[1]
    return policy_and_minister_names


def format_title(title_w_all_caps_and_underscores):
    words = [word.lower().capitalize() for word in title_w_all_caps_and_underscores.split("_")]
    return "".join(words)


def get_government_titles(aod_path=AOD_PATH):
    titles_in_file = fp.get_government_titles_path(aod_path)
    # title_dict = {"all": "all"}
    title_dict = dict()
    start_text = "HOIG_"
    with open(titles_in_file, "r", encoding = text_encoding) as f:
        for line in f:
            if start_text in line:
                items = line.strip().split(";")
                key = format_title(items[0].split(start_text)[1])
                title_dict[key] = items[1]
    return title_dict

def get_idea_titles(aod_path=AOD_PATH):
    titles_in_file = fp.get_idea_titles_path(aod_path)
    title_dict = dict()
    start_text = "HOINI_"
    with open(titles_in_file, "r", encoding = text_encoding) as f:
        for line in f:
            if start_text in line:
                items = line.strip().split(";")
                key = items[0].split(start_text)[1]
                title_dict[key] = items[1]
    return title_dict

def get_province_names(aod_path=AOD_PATH):
    names_in_file = fp.get_province_names_path(aod_path)
    return {int(k[4:]): name for k, name in read_name_file(names_in_file).items()}


def read_savefile_for_research_order(savefilepath):
    strings_from_file = []
    with open(savefilepath, "r", encoding = text_encoding) as f:
        for line in f:
            if "has developed" in line:
                strings_from_file.append(line.strip().split("=")[1].strip().strip('"'))
    tech_n_team_n_time = []
    for s in strings_from_file:
        time0, time, rest = s.split(":")
        time = (":".join([time0, time])).strip()
        team, tech = rest.strip().split(" has developed ")
        team = team.strip()
        tech = tech.strip(" '.")
        tech_n_team_n_time.append((tech, team, time))
    return tech_n_team_n_time


def read_scenario_file_for_events(scenario_file_name, aod_path=AOD_PATH):
    event_file_paths = []
    scenario_file_path = fp.get_scenarios_folder_path(aod_path) / scenario_file_name
    scenario_dict = read_txt_file(scenario_file_path)
    event_key = "event"
    include_key = "include"
    if isinstance(scenario_dict[event_key], str):
        event_file_path = aod_path / scenario_dict[event_key].replace("\\", "/")
        for event_filepath in event_file_path.parent.glob(event_file_path.name, case_sensitive=False):
            if event_filepath.exists():
                event_file_paths.append(event_filepath)
                break
        else:
            print(f"File {str(event_file_path)} does not exist (1)")
    if isinstance(scenario_dict[event_key], list):
        for event_file_path_str in scenario_dict[event_key]:
            event_file_path = aod_path / event_file_path_str.replace("\\", "/")
            for event_filepath in event_file_path.parent.glob(event_file_path.name, case_sensitive=False):
                if event_filepath.exists():
                    event_file_paths.append(event_filepath)
                    break
            else:
                print(f"File {str(event_file_path)} does not exist (2)")
    for path_str in scenario_dict[include_key]:
        if event_key in path_str:
            include_event_file_path = aod_path / path_str.replace("\\", "/")
            if include_event_file_path.exists():
                included_dict = read_txt_file(include_event_file_path)
                for event_file_path_str in included_dict[event_key]:
                    event_file_path = aod_path / event_file_path_str.replace("\\", "/")
                    for event_filepath in event_file_path.parent.glob(event_file_path.name, case_sensitive=False):
                        if event_filepath.exists():
                            event_file_paths.append(event_filepath)
                            break
                    else:
                        print(f"File {str(event_file_path)} does not exist (3)")
            else:
                print(f"Include file {include_event_file_path} does not exist")
    return event_file_paths


def get_texts_from_files(list_of_filepaths):
    text_dict = dict()
    for filepath in list_of_filepaths:
        texts = read_name_file(filepath)
        for key, text in texts.items():
            # empty string should probably not be a key
            if key:
                text_dict[key] = text
    return text_dict

def get_texts_from_files_w_duplicates(list_of_filepaths):
    text_dict = dict()
    for filepath in list_of_filepaths:
        text_dict = read_name_file_w_duplicates(filepath, text_dict)
    return text_dict

def get_all_texts_from_files():
    return get_texts_from_files(fp.get_all_text_files_paths(AOD_PATH))


def get_event_texts(list_of_keys):
    event_dict = dict()

    return event_dict
