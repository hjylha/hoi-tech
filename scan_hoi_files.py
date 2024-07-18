
import os
from pathlib import Path

from classes import Component, EFFECT_ATTRIBUTES, Effect, Tech, TechTeam


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


def get_tech_names():
    aod_path = get_aod_path()
    tech_names_path = aod_path / "config" / "tech_names.csv"
    tech_names = dict()
    with open(tech_names_path, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            names = line.split(";")
            if names[0]:
                tech_names[names[0]] = names[1]
    return tech_names


def get_country_names():
    aod_path = get_aod_path()

    tech_team_files = get_tech_team_files(get_tech_path())
    country_codes = [filepath.stem[-3:].upper() for filepath in tech_team_files]

    country_names_path = aod_path / "config" / "world_names.csv"
    country_names = dict()
    with open(country_names_path, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            names = line.split(";")
            if names[0].upper() in country_codes:
                country_names[names[0].upper()] = names[1]
    return country_names


def scan_tech_file(filepath, tech_names):
    techs = []

    tech_category = filepath.stem[:filepath.stem.index("_tech")]

    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        filtered_full_text = "\n".join([text.split("#")[0] for text in f.read().split("\n")])
        # for tech_text in f.read().split("application =")[1:]:
        for tech_text in filtered_full_text.split("application =")[1:]:
            try:
                tech_id = int(tech_text.split("id =")[1].split("\n")[0].strip(" ="))
            except ValueError as e:
                print(filepath)
                print(tech_text.split("id ")[1].split("\n")[0].strip(" ="))
                print(tech_text[:100])
                raise e

            tech_name_key = tech_text.split("Name =")[1].split("\n")[0].strip(" =")
            tech_name = tech_names[tech_name_key]
            short_tech_name_key = f"SHORT_{tech_name_key}"
            short_tech_name = tech_names[short_tech_name_key]

            requirements = []
            if "required =" in tech_text:
                first_split = tech_text.split("OR_required =")
                try:
                    for text in first_split[1:]:
                        reqs = text.split("\n")[0].strip(" ={}").split(" ")
                        reqs = [int(req) for req in reqs if req]
                        requirements.append(reqs)
                except IndexError:
                    pass
                
                for text0 in first_split:
                    try:
                        for text in text0.split("required =")[1:]:
                            reqs = text.split("\n")[0].strip(" ={}").split(" ")
                            reqs = [int(req) for req in reqs if req]
                            requirements = requirements + reqs
                    except IndexError:
                        pass
                # reqs = tech_text.split("required =")[1].split("\n")[0].strip(" ={}").split(" ")
                # requirements = [int(req) for req in reqs if req]
            
            components = []
            component_texts = [t.split("}")[0] for t in tech_text.split("component =")[1:]]
            for comp_text in component_texts:
                try:
                    component_type = comp_text.split("type =")[1].split("\n")[0].strip(" =")
                    component_difficulty = int(comp_text.split("difficulty =")[1].split("\n")[0].strip(" ="))
                    components.append(Component(component_type.lower(), component_difficulty))
                except IndexError as e:
                    print(filepath)
                    print(comp_text)
                    print()
                    print("component".join(component_texts))
                    print(tech_text)
                    raise e
            
            effects = []
            effect_texts = tech_text.split("effects =")[1].split("command")[1:]
            effect_texts = [t.split("{")[1].split("}")[0].strip() for t in effect_texts]
            for effect_text in effect_texts:
                words = effect_text.split(" ")
                
                effect = dict()
                previous_word = None
                equals_between = False
                for word in words:
                    if equals_between and previous_word is not None:
                        if previous_word == "value":
                            try:
                                effect[previous_word] = int(word)
                            except ValueError:
                                try:
                                    effect[previous_word] = float(word)
                                except ValueError:
                                    effect[previous_word] = word
                        else:
                            effect[previous_word] = word
                        previous_word = None
                        equals_between = False
                        continue
                    if word == "=":
                        equals_between = True
                    if not equals_between and word != "=":
                        previous_word = word
                try:
                    effect_tuple = Effect(*[effect.get(key) for key in EFFECT_ATTRIBUTES])
                except Exception as e:
                    print(effect)
                    raise e
                effects.append(effect_tuple)

            techs.append(Tech(tech_id, tech_name, short_tech_name, tech_category, requirements, components, effects))
    
    return techs




def scan_techs():
    techs = []
    tech_files = get_tech_files(get_tech_path())
    tech_names = get_tech_names()

    for tech_file in tech_files:
        techs_in_file = scan_tech_file(tech_file, tech_names)
        techs = techs + techs_in_file
    
    return techs


def scan_tech_team_file(filepath):
    tech_teams = []
    nation_key = filepath.stem[-3:].upper()
    # tech_nation = country_names[nation_key.upper()]
    # tech_nation = country_names.get(nation_key.upper())
    # if tech_nation is None:
    #     tech_nation = nation_key.upper()
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            items = line.split(";")
            if items[0].strip():
                try:
                    team_id = int(items[0].strip())
                except ValueError:
                    if nation_key.lower() != items[0].strip().lower():
                        print(line)
                        print(len(items[0]))
                        raise Exception(f"{nation_key} is not {items[0]}")
                    continue
                team_name = items[1]
                pic_path = f"gfx/interface/pics/{items[2]}.bmp"
                skill = int(items[3])
                start_year = int(items[4])
                end_year = int(items[5])
            
                specialities = []
                for spec in items[6:]:
                    if spec and spec.lower() not in specialities:
                        specialities.append(spec.lower())
                    else:
                        break
                tech_teams.append(TechTeam(team_id, team_name, nation_key, skill, start_year, end_year, specialities, pic_path))
    
    return tech_teams


def scan_tech_teams():
    tech_teams = []
    team_files = get_tech_team_files(get_tech_path())
    # country_names = get_country_names()
    for team_file in team_files:
        teams = scan_tech_team_file(team_file)
        tech_teams = tech_teams + teams

    return tech_teams


def get_tech_teams(country_code):
    # tech_teams = []
    team_filepath = get_tech_path() / "teams" / f"teams_{country_code.lower()}.csv"
    return scan_tech_team_file(team_filepath)

def scan_scenario_file(filepath):
    if filepath is None:
        return None
    results = dict()
    deactivated_tech = []
    researched_tech = []
    blueprints = []
    mode = None
    stages = "={"
    with open(filepath, "r", encoding = "ISO-8859-1") as f:
        for line in f:
            textline = line.split("#")[0].strip()
            if not textline:
                continue
            if "deactivate" in textline:
                mode = ["deactivated", 0]
                current_list = deactivated_tech
            if "techapps" in textline:
                mode = ["researched", 0]
                current_list = researched_tech
            if "blueprints" in textline:
                mode = ["blueprints", 0]
                current_list = blueprints
            
            if mode is not None:
                if mode[1] < 2:
                    for char in stages[mode[1]:]:
                        if char in textline:
                            textline = textline.split(char)[1].strip()
                            mode[1] += 1
                if mode[1] == 2:
                    if "}" in textline:
                        textline = textline.split("}")[0].strip()
                        mode = None
                    additions = [int(item.strip()) for item in textline.split(" ") if item]
                    current_list += additions

            # if mode[0] == "deactivated":
            #     textline.split(stages[mode[1]])
            
            if "research_mod" in textline:
                results["research_speed"] = float(textline.split("=")[1].strip()) * 100
    results["deactivated"] = deactivated_tech
    results["researched"] = researched_tech
    results["blueprints"] = blueprints
    return results

def scan_scenario_file_for_country(country_code):
    filepath = get_scenario_path_for_country(country_code)
    return scan_scenario_file(filepath)


def find_tech(tech_id, list_of_techs):
    for tech in list_of_techs:
        if tech.tech_id == tech_id:
            return tech
    print(f"Tech with id {tech_id} not found")
    return


if __name__ == "__main__":
    techs = scan_techs()
    tech_dict = {t.name: t for t in techs}
    teams = scan_tech_teams()
