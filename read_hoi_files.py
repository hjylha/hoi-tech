
import os
from pathlib import Path
import csv


this_files_directory = Path(__file__).parent


def get_aod_path():
    if os.name == "nt":
        with open(this_files_directory / "aod_path.txt", "r") as f:
            return Path(f.read().strip())
    with open(this_files_directory / "aod_path_linux.txt", "r") as f:
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

def get_save_game_path():
    aod_path = get_aod_path()
    return aod_path / "scenarios" / "save games"


def change_type_if_necessary(text):
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text.strip('" ')

def get_first_item_from_text(text):
    if text[0] in "{}=":
        return (text[0], text[1:].strip())
    if text[0] == '"':
        item = text[1:].split('"')[0]
        return (item, text[len(item) + 2:].strip())
    if text[0] == "'":
        item = text[1:].split("'")[0]
        return (item, text[len(item) + 2:].strip())
    
    item = text
    for symbol in "{}=":
        if symbol in text:
            item = text.split(symbol)[0].strip()
    item = item.split(" ")[0].strip().split("\t")[0].strip()
    
    return (change_type_if_necessary(item), text[len(item):].strip())


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


def read_csv_file(filepath, check_filetype=False, delimiter=";"):
    if check_filetype and filepath.suffix != ".csv":
        print(f"{filepath} is not a csv file.")
        return
    csv_content_list = None
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        csv_content_list = []
        for line in csv_reader:
            csv_content_list.append([change_type_if_necessary(item) for item in line[:-1]])
        # csv_content_list = [line[:-1] for line in csv_reader]
    return csv_content_list


def read_inside_brackets(opened_file, current_line):
    # while not current_line:
    #     raw_line = opened_file.readline()
    #     if not raw_line:
    #         raise Exception("File has curly brackets mismatch.")
    #     current_line = raw_line.split("#")[0].strip()
    current_list_or_dict = []
    # if current_line[0] == "}":
    #     return [current_list_or_dict, current_line[1:]]
    
    previous_object = None
    previous_key = None
    key_value_counts = dict()
    previous_item = None
    while True:
        while not current_line:
            raw_line = opened_file.readline()
            if not raw_line:
                return [current_list_or_dict, raw_line]
            current_line = raw_line.split("#")[0].strip()
        item, current_line = get_first_item_from_text(current_line)
        if item == "}":
            if not current_list_or_dict:
                return [[previous_item], current_line]
            # if previous_item == "}" or previous_key is not None:
            return [current_list_or_dict, current_line]

        if item == "{":
            new_object, current_line = read_inside_brackets(opened_file, current_line)
            # if previous_text is None:
            #     current_list_or_dict.append(new_object)
            previous_item = "}"
            if previous_key is None:
                current_list_or_dict.append(new_object)
                continue
            
            num_of_values_for_key = key_value_counts.get(previous_key)
            if num_of_values_for_key is None:
                key_value_counts[previous_key] = 1
                current_list_or_dict[previous_key] = new_object
                continue
            if num_of_values_for_key == 1:
                key_value_counts[previous_key] += 1
                current_list_or_dict[previous_key] = [current_list_or_dict[previous_key], new_object]
                continue
            current_list_or_dict[previous_key].append(new_object)
            continue
                
        if item == "=":
            previous_key = previous_item
            previous_item = "="
            if not isinstance(current_list_or_dict, dict):
                current_list_or_dict = dict()
            continue
        if previous_item == "=":
            num_of_values_for_key = key_value_counts.get(previous_key)
            if num_of_values_for_key is None:
                key_value_counts[previous_key] = 1
                current_list_or_dict[previous_key] = item
            elif num_of_values_for_key == 1:
                key_value_counts[previous_key] += 1
                current_list_or_dict[previous_key] = [current_list_or_dict[previous_key], item]
            else:
                current_list_or_dict[previous_key].append(item)
            previous_item = "}"
            continue
        if isinstance(current_list_or_dict, list) and current_list_or_dict:
            current_list_or_dict.append(item)
            previous_item = item
            continue
        if previous_item is None:
            previous_item = item
            continue
        if not isinstance(previous_item, str) or len(previous_item) > 1 or previous_item not in "{}=":
            current_list_or_dict.append(previous_item)
            current_list_or_dict.append(item)
            previous_item = item
            continue
        previous_item = item
        
    # if "}" in current_line:

    # while "}" not in current_line:
    return [current_list_or_dict, current_line[1:].strip()]


# def read_txt_file0(filepath, check_filetype=False):
def read_txt_file(filepath, check_filetype=False):
    if check_filetype and filepath.suffix != ".txt":
        print(f"{filepath} is not a txt file.")
        return
    
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        content, _ = read_inside_brackets(f, "")
    if isinstance(content, list) and len(content) == 1:
        content = content[0]
    return content


# def read_txt_file(filepath, check_filetype=False):
#     if check_filetype and filepath.suffix != ".txt":
#         print(f"{filepath} is not a txt file.")
#         return
#     content = dict()
    
#     with open(filepath, "r", encoding = "ISO-8859-1") as f:
#         nested_keys = []
#         nested_values = []
#         previous_text = None
#         for line in f:
#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
#             while clean_line:
#                 item = clean_line.split(" ")[0].strip().split("\t")[0].strip()
#                 # previous_text = item
#                 # clean_line = clean_line[len(item):].strip()
#                 if item[0] == "{":
#                     item = "{"
#                     # if previous_text == "{":
#                     #     nested_keys.append(None)
#                     #     nested_values.append([])
#                     if previous_text != "=":
#                         # TODO: handle pure list
#                         print(line)
#                         raise Exception(f"{previous_text} {item} can not be handled (at least not yet...)")
#                     # 
#                     # print("{", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     # previous_text = item
#                     previous_text = item
#                     continue
#                 if item[0] == "=":
#                     item = "="
#                     if previous_text in ["{", "=", "}"]:
#                         raise Exception(f"{previous_text} {item} can not be handled")
#                     nested_keys.append(change_type_if_necessary(previous_text))
#                     if previous_text is None:
#                         print(line)
#                     nested_values.append(None)
#                     # 
#                     # print("=", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     previous_text = item
#                     continue
#                 if item[0] == "}":
#                     item = "}"
#                     # 
#                     key = nested_keys.pop()
#                     value = nested_values.pop()

#                     # print()
#                     # print(nested_keys)
#                     # for v in nested_values:
#                     #     print(v)
#                     # print(len(nested_values), "values")

#                     if value is None:
#                         value = [change_type_if_necessary(previous_text)]
#                     # if isinstance(value, list):
#                     #     value.append(change_type_if_necessary(previous_text))
#                     if not nested_keys:
#                         if content.get(key) is None:
#                             content[key] = value
#                         elif isinstance(content[key], list):
#                             content[key].append(value)
#                         else:
#                             content[key] = [content[key], value]
#                     elif nested_values[-1] is None:
#                         nested_values[-1] = {key: value}
#                     elif key in nested_values[-1].keys():
#                         if isinstance(nested_values[-1][key], list):
#                             nested_values[-1][key].append(value)
#                         else:
#                             nested_values[-1][key] = [nested_values[-1][key], value]
#                     else:
#                         nested_values[-1][key] = value

#                     # print("}", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     # previous_text = item
#                     previous_text = None
#                     continue
#                 if "=" in item:
#                     item = item.split("=")[0].strip()
#                 if "}" in item:
#                     item = item.split("}")[0].strip()
#                 if item[0] == '"':
#                     quoted_text = clean_line[1:].split('"')[0]
#                     item = f'"{quoted_text}"'
#                 if previous_text == "=":
#                     key = nested_keys.pop()
#                     value = nested_values.pop()
#                     if value is not None:
#                         raise Exception(f"{value} should be None")
#                     value = change_type_if_necessary(item)
#                     if not nested_keys:
#                         if content.get(key) is None:
#                             content[key] = value
#                         elif isinstance(content[key], list):
#                             content[key].append(value)
#                         else:
#                             content[key] = [content[key], value]
#                     elif nested_values[-1] is None:
#                         nested_values[-1] = {key: value}
#                     elif key in nested_values[-1].keys():
#                         if isinstance(nested_values[-1][key], list):
#                             nested_values[-1][key].append(value)
#                         else:
#                             nested_values[-1][key] = [nested_values[-1][key], value]
#                     else:
#                         nested_values[-1][key] = value
#                     # nested_values[-1] = change_type_if_necessary(item)
#                     # print(previous_text, item)
#                     previous_text = None
#                     clean_line = clean_line[len(item):].strip()
#                     continue
#                 if previous_text is not None and previous_text != "{":
#                     if nested_values[-1] is None:
#                         nested_values[-1] = [change_type_if_necessary(previous_text), change_type_if_necessary(item)]
#                     elif isinstance(nested_values[-1], list):
#                         nested_values[-1].append(change_type_if_necessary(item))
#                     else:
#                         raise Exception(f"{item} and {previous_text} do not seem to go to {nested_values[-1]}")
#                     # print(previous_text, item)
#                     previous_text = item
#                     clean_line = clean_line[len(item):].strip()
#                     continue

#                 # previous_text = item
#                 # print("no conditions", previous_text, item)
#                 previous_text = item
#                 clean_line = clean_line[len(item):].strip()


#                 # stuff
                
#             # if "}" in clean_line:
#     return content


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


def read_difficulty_file():
    difficulty_path = get_difficulty_path()
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

# def read_minister_modifiers():
#     minister_modifier_file = get_minister_modifier_path()
#     personalities_and_modifiers = dict()
#     with open(minister_modifier_file, "r", encoding = "ISO-8859-1") as f:
#         for line in f:

#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
    
#     return personalities_and_modifiers


# def read_ideas():
#     ideas_filepath = get_ideas_path()
#     ideas = dict()
#     with open(ideas_filepath, "r", encoding = "ISO-8859-1") as f:
#         for line in f:

#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
    
#     return ideas


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
    # fill the missing countries
    for country_code in country_codes:
        if country_code.upper() not in country_names.keys():
            country_names[country_code.upper()] = ""
    return country_names


def read_savefile_for_research_order(savefilepath):
    strings_from_file = []
    with open(savefilepath, "r", encoding = "ISO-8859-1") as f:
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
