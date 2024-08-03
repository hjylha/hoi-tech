
import os
from pathlib import Path
import csv


def get_aod_path():
    if os.name == "nt":
        with open("aod_path.txt", "r") as f:
            return Path(f.read().strip())
    with open("aod_path_linux.txt", "r") as f:
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

def get_scenario_path_for_country(country_code):
    scenario_directories = get_scenario_paths()
    for sd_path in scenario_directories:
        possible_path = sd_path / f"{country_code.lower()}_{sd_path.stem[-2:]}.inc"
        if possible_path.exists():
            return possible_path

def get_misc_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "misc.txt"

def get_minister_modifier_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "ministers" / "minister_modifiers.txt"

def get_ideas_path():
    aod_path = get_aod_path()
    return aod_path / "db" / "ideas" / "ideas.txt"

def get_ministers_path(country_code):
    aod_path = get_aod_path()
    return aod_path / "db" / "ministers" / f"ministers_{country_code.lower()}.csv"

def get_tech_names_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "tech_names.csv"

def get_country_names_path():
    aod_path = get_aod_path()
    return aod_path / "config" / "world_names.csv"


def change_type_if_necessary(text):
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text.strip('" ')


def read_name_file(filepath, language="English"):
    names = dict()
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        for i, line in enumerate(f):
            if i == 0:
                language_index = line.split(";").index(language)
                continue
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue
            # key, name = clean_line[0], clean_line[language_index]
            names[clean_line[0]] = clean_line[language_index]
    return names

def read_names_from_file(search_terms, filepath, language="English"):
    names = dict()
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
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


def read_csv_file(filepath, check_filetype=True):
    if check_filetype and filepath.suffix != ".csv":
        print(f"{filepath} is not a csv file.")
        return
    csv_content_list = None
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        csv_reader = csv.reader(f, delimiter=";")
        csv_content_list = []
        for line in csv_reader:
            csv_content_list.append([change_type_if_necessary(item) for item in line[:-1]])
        # csv_content_list = [line[:-1] for line in csv_reader]
    return csv_content_list


def read_txt_file(filepath, check_filetype=True):
    if check_filetype and filepath.suffix != ".txt":
        print(f"{filepath} is not a txt file.")
        return
    content = dict()
    
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        nested_keys = []
        nested_values = []
        previous_text = None
        for line in f:
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue
            while clean_line:
                item = clean_line.split(" ")[0].strip()
                # previous_text = item
                # clean_line = clean_line[len(item):].strip()
                if item[0] == "{":
                    item = "{"
                    if previous_text != "=":
                        raise Exception(f"{previous_text} {item} can not be handled (at least not yet...)")
                    # 
                    # print("{", previous_text, item)
                    clean_line = clean_line[1:].strip()
                    # previous_text = item
                    previous_text = None
                    continue
                if item[0] == "=":
                    item = "="
                    if previous_text in ["{", "=", "}"]:
                        raise Exception(f"{previous_text} {item} can not be handled")
                    nested_keys.append(change_type_if_necessary(previous_text))
                    nested_values.append(None)
                    # 
                    # print("=", previous_text, item)
                    clean_line = clean_line[1:].strip()
                    previous_text = item
                    continue
                if item[0] == "}":
                    item = "}"
                    # 
                    key = nested_keys.pop()
                    value = nested_values.pop()

                    # print()
                    # print(nested_keys)
                    # for v in nested_values:
                    #     print(v)
                    # print(len(nested_values), "values")

                    if value is None:
                        value = [change_type_if_necessary(previous_text)]
                    # if isinstance(value, list):
                    #     value.append(change_type_if_necessary(previous_text))
                    if not nested_keys:
                        if content.get(key) is None:
                            content[key] = value
                        elif isinstance(content[key], list):
                            content[key].append(value)
                        else:
                            content[key] = [content[key], value]
                    elif nested_values[-1] is None:
                        nested_values[-1] = {key: value}
                    elif key in nested_values[-1].keys():
                        if isinstance(nested_values[-1][key], list):
                            nested_values[-1][key].append(value)
                        else:
                            nested_values[-1][key] = [nested_values[-1][key], value]
                    else:
                        nested_values[-1][key] = value

                    # print("}", previous_text, item)
                    clean_line = clean_line[1:].strip()
                    # previous_text = item
                    previous_text = None
                    continue
                if "=" in item:
                    item = item.split("=")[0].strip()
                if "}" in item:
                    item = item.split("}")[0].strip()
                if item[0] == '"':
                    quoted_text = clean_line[1:].split('"')[0]
                    item = f'"{quoted_text}"'
                if previous_text == "=":
                    key = nested_keys.pop()
                    value = nested_values.pop()
                    if value is not None:
                        raise Exception(f"{value} should be None")
                    value = change_type_if_necessary(item)
                    if not nested_keys:
                        if content.get(key) is None:
                            content[key] = value
                        elif isinstance(content[key], list):
                            content[key].append(value)
                        else:
                            content[key] = [content[key], value]
                    elif nested_values[-1] is None:
                        nested_values[-1] = {key: value}
                    elif key in nested_values[-1].keys():
                        if isinstance(nested_values[-1][key], list):
                            nested_values[-1][key].append(value)
                        else:
                            nested_values[-1][key] = [nested_values[-1][key], value]
                    else:
                        nested_values[-1][key] = value
                    # nested_values[-1] = change_type_if_necessary(item)
                    # print(previous_text, item)
                    previous_text = None
                    clean_line = clean_line[len(item):].strip()
                    continue
                if previous_text is not None:
                    if nested_values[-1] is None:
                        nested_values[-1] = [change_type_if_necessary(previous_text), change_type_if_necessary(item)]
                    elif isinstance(nested_values[-1], list):
                        nested_values[-1].append(change_type_if_necessary(item))
                    else:
                        raise Exception(f"{item} and {previous_text} do not seem to go to {nested_values[-1]}")
                    # print(previous_text, item)
                    previous_text = item
                    clean_line = clean_line[len(item):].strip()
                    continue

                # previous_text = item
                # print("no conditions", previous_text, item)
                previous_text = item
                clean_line = clean_line[len(item):].strip()


                # stuff
                
            # if "}" in clean_line:
    return content



def read_misc_file():
    misc_filepath = get_misc_path()
    # misc_content = dict()
    # content_types = ["economy", "combat", "research"]
    # with open(misc_filepath, "r", encoding = "ISO-8859-1") as f:
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

def get_blueprint_bonus_and_tech_speed_modifier():
    misc_content = read_misc_file()
    return misc_content["research"][0], misc_content["research"][5]


def read_minister_modifiers():
    minister_modifier_file = get_minister_modifier_path()
    personalities_and_modifiers = dict()
    with open(minister_modifier_file, "r", encoding = "ISO-8859-1") as f:
        for line in f:

            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue
    
    return personalities_and_modifiers


def read_ideas():
    ideas_filepath = get_ideas_path()
    ideas = dict()
    with open(ideas_filepath, "r", encoding = "ISO-8859-1") as f:
        for line in f:

            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue
    
    return ideas


def get_tech_names():
    # aod_path = get_aod_path()
    # tech_names_path = aod_path / "config" / "tech_names.csv"
    tech_names_path = get_tech_names_path()
    tech_names = dict()
    with open(tech_names_path, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            names = line.split(";")
            if names[0]:
                tech_names[names[0]] = names[1]
    return tech_names


def get_country_names():
    # aod_path = get_aod_path()

    tech_team_files = get_tech_team_files(get_tech_path())
    country_codes = [filepath.stem[-3:].upper() for filepath in tech_team_files]

    # country_names_path = aod_path / "config" / "world_names.csv"
    country_names_path = get_country_names_path()
    country_names = dict()
    with open(country_names_path, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            names = line.split(";")
            if names[0].upper() in country_codes:
                country_names[names[0].upper()] = names[1]
    return country_names

