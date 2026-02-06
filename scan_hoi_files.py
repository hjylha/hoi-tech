
from file_paths import get_tech_path, get_minister_modifier_path, get_ideas_path, get_ministers_path, get_province_rev_path, get_tech_files, get_tech_team_files
from file_paths import get_leaders_files, get_ministers_files, get_all_text_files_paths, get_brigades_files, get_divisions_files
from file_paths import this_files_directory, countries_file
from check_file_paths import AOD_PATH
from read_hoi_files import get_tech_names, read_csv_file, read_txt_file, get_scenario_file_path_for_country, get_minister_and_policy_names, get_government_titles, get_idea_titles
from read_hoi_files import the_encoding, text_encoding, csv_encoding, get_texts_from_files, get_texts_from_files_w_duplicates
from classes import Component, EFFECT_ATTRIBUTES, Effect, MODIFIER_ATTRIBUTES, Modifier, Tech, TechTeam, Leader
from classes import MinisterPersonality, Minister, Idea, get_minister_personality, Model, Brigade, Division
from event import Event, get_event_from_raw_event


def scan_tech_file(filepath, tech_names):
    techs = []

    tech_category = filepath.stem[:filepath.stem.index("_tech")]

    content = read_txt_file(filepath, encoding=csv_encoding)["technology"]

    if tech_category != content["category"]:
        raise Exception(f"Category mismatch: {tech_category} /= {content['category']}")

    for tech in content["application"]:
        try:
            tech_id = int(tech["id"])
        except ValueError as e:
            print(filepath)
            print(f"tech id not int: {tech['id']}")
            raise e
        tech_name_key = tech["Name"]
        tech_name = tech_names[tech_name_key].strip()
        short_tech_name_key = f"SHORT_{tech_name_key}"
        short_tech_name = tech_names[short_tech_name_key].strip()

        requirements = []
        if (reqs := tech.get("required")) is not None:
            for req in reqs:
                if isinstance(req, int):
                    requirements.append(req)
                elif isinstance(req, list):
                    for r in req:
                        requirements.append(r)
                else:
                    print(tech["id"])
                    print(tech["required"])
                    raise Exception(f"Requirements messed up")
        if (opt_reqs := tech.get("OR_required")) is not None:
            requirements.append(opt_reqs)
        if (opt_reqs := tech.get("or_required")) is not None:
            requirements.append(opt_reqs)
        components = []
        for component in tech["component"]:
            components.append(Component(component["type"].lower(), int(component["difficulty"])))
        
        list_of_effects = tech["effects"]["command"]
        if isinstance(list_of_effects, dict):
            effects = [Effect(*[list_of_effects.get(key) for key in EFFECT_ATTRIBUTES])]
        else:
            effects = []
            for effect in list_of_effects:
                if isinstance(effect, str):
                    print(tech["id"])
                    print(effect)
                    raise Exception(f"Effects messed up")
                effect_tuple = Effect(*[effect.get(key) for key in EFFECT_ATTRIBUTES])
                effects.append(effect_tuple)
        techs.append(Tech(tech_id, tech_name, short_tech_name, filepath, tech_category, requirements, components, effects))

    # with open(filepath, "r", encoding = "ISO-8859-1") as f:
    #     filtered_full_text = "\n".join([text.split("#")[0] for text in f.read().split("\n")])
    #     # for tech_text in f.read().split("application =")[1:]:
    #     for tech_text in filtered_full_text.split("application =")[1:]:
    #         try:
    #             tech_id = int(tech_text.split("id =")[1].split("\n")[0].strip(" ="))
    #         except ValueError as e:
    #             print(filepath)
    #             print(tech_text.split("id ")[1].split("\n")[0].strip(" ="))
    #             print(tech_text[:100])
    #             raise e

    #         tech_name_key = tech_text.split("Name =")[1].split("\n")[0].strip(" =")
    #         tech_name = tech_names[tech_name_key].strip()
    #         short_tech_name_key = f"SHORT_{tech_name_key}"
    #         short_tech_name = tech_names[short_tech_name_key]

    #         requirements = []
    #         if "required =" in tech_text:
    #             first_split = tech_text.split("OR_required =")
    #             try:
    #                 for text in first_split[1:]:
    #                     reqs = text.split("\n")[0].strip(" ={}").split(" ")
    #                     reqs = [int(req) for req in reqs if req]
    #                     requirements.append(reqs)
    #             except IndexError:
    #                 pass
    #             # try again
    #             first_split = first_split[0].split("or_required =")
    #             try:
    #                 for text in first_split[1:]:
    #                     reqs = text.split("\n")[0].strip(" ={}").split(" ")
    #                     reqs = [int(req) for req in reqs if req]
    #                     requirements.append(reqs)
    #             except IndexError:
    #                 pass
                
    #             for text0 in first_split:
    #                 try:
    #                     for text in text0.split("required =")[1:]:
    #                         reqs = text.split("\n")[0].strip(" ={}").split(" ")
    #                         reqs = [int(req) for req in reqs if req]
    #                         requirements = requirements + reqs
    #                 except IndexError:
    #                     pass
    #             # reqs = tech_text.split("required =")[1].split("\n")[0].strip(" ={}").split(" ")
    #             # requirements = [int(req) for req in reqs if req]
            
    #         components = []
    #         component_texts = [t.split("}")[0] for t in tech_text.split("component =")[1:]]
    #         for comp_text in component_texts:
    #             try:
    #                 component_type = comp_text.split("type =")[1].split("\n")[0].strip(" =")
    #                 component_difficulty = int(comp_text.split("difficulty =")[1].split("\n")[0].strip(" ="))
    #                 components.append(Component(component_type.lower(), component_difficulty))
    #             except IndexError as e:
    #                 print(filepath)
    #                 print(comp_text)
    #                 print()
    #                 print("component".join(component_texts))
    #                 print(tech_text)
    #                 raise e
            
    #         effects = []
    #         effect_texts = tech_text.split("effects =")[1].split("command")[1:]
    #         effect_texts = [t.split("{")[1].split("}")[0].strip() for t in effect_texts]
    #         for effect_text in effect_texts:
    #             words = effect_text.split(" ")
                
    #             effect = dict()
    #             previous_word = None
    #             equals_between = False
    #             for word in words:
    #                 if equals_between and previous_word is not None:
    #                     if previous_word == "value":
    #                         try:
    #                             effect[previous_word] = int(word)
    #                         except ValueError:
    #                             try:
    #                                 effect[previous_word] = float(word)
    #                             except ValueError:
    #                                 effect[previous_word] = word
    #                     else:
    #                         effect[previous_word] = word
    #                     previous_word = None
    #                     equals_between = False
    #                     continue
    #                 if word == "=":
    #                     equals_between = True
    #                 if not equals_between and word != "=":
    #                     previous_word = word
    #             try:
    #                 effect_tuple = Effect(*[effect.get(key) for key in EFFECT_ATTRIBUTES])
    #             except Exception as e:
    #                 print(effect)
    #                 raise e
    #             effects.append(effect_tuple)

    #         techs.append(Tech(tech_id, tech_name, short_tech_name, tech_category, requirements, components, effects))
    
    return techs


def scan_techs():
    techs = []
    tech_files = get_tech_files(get_tech_path(AOD_PATH))
    tech_names = get_tech_names()

    for tech_file in tech_files:
        techs_in_file = scan_tech_file(tech_file, tech_names)
        techs = techs + techs_in_file
    return techs

def get_tech_dict():
    techs = scan_techs()
    techs = {tech.tech_id: tech for tech in techs}
    # add what each tech allows and deactivates
    for tech_id, tech in techs.items():
        for requirement in tech.requirements:
            if isinstance(requirement, int):
                techs[requirement].allows.add(tech_id)
                continue
            if isinstance(requirement, list):
                for req in requirement:
                    techs[req].allows.add(tech_id)
        for deactivation in tech.get_deactivated_tech():
            techs[deactivation].deactivated_by.add(tech_id)
    # mark post-war tech
    start_index = 0
    post_war_techs = [5840, 1890]
    end_index = len(post_war_techs)
    while end_index > start_index:
        # new_start_index = end_index
        for tech_id in post_war_techs[start_index:end_index]:
            techs[tech_id].is_post_war = 1
            for t_id in techs[tech_id].allows:
                if t_id not in post_war_techs:
                    post_war_techs.append(t_id)
        start_index = end_index
        end_index = len(post_war_techs)
    # post_war_techs = list(techs[5840].allows)
    return techs
            

def scan_tech_team_file(filepath):
    tech_teams = []
    nation_key = filepath.stem[-3:].upper()
    # tech_nation = country_names[nation_key.upper()]
    # tech_nation = country_names.get(nation_key.upper())
    # if tech_nation is None:
    #     tech_nation = nation_key.upper()
    with open(filepath, "r", encoding = text_encoding) as f:
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
                team_name = items[1].strip()
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
                tech_teams.append(TechTeam(team_id, team_name, nation_key, skill, start_year, end_year, specialities, filepath, pic_path))
    
    return tech_teams


def scan_tech_teams():
    tech_teams = []
    team_files = get_tech_team_files(get_tech_path(AOD_PATH))
    # country_names = get_country_names()
    for team_file in team_files:
        teams = scan_tech_team_file(team_file)
        tech_teams = tech_teams + teams

    return tech_teams


def get_tech_teams(country_code):
    # tech_teams = []
    team_filepath = get_tech_path(AOD_PATH) / "teams" / f"teams_{country_code.lower()}.csv"
    return scan_tech_team_file(team_filepath)


def get_correct_modifiers(modifier_dict):
    modifiers = []
    for mod_key in MODIFIER_ATTRIBUTES:
        if modifier_dict.get(mod_key) is not None:
            modifiers.append(modifier_dict[mod_key])
        else:
            for key in modifier_dict.keys():
                if key.startswith(mod_key):
                    modifiers.append(modifier_dict[key])
                    break
            else:
                modifiers.append(None)
    return Modifier(*modifiers)

def ensure_lists_are_lists(should_be_list):
    if isinstance(should_be_list, list):
        return should_be_list
    if should_be_list is None:
        return []
    return [should_be_list]
    

def scan_minister_personalities():
    public_name_dict = get_minister_and_policy_names()
    # minister_titles = get_government_titles()
    minister_modifier_path = get_minister_modifier_path(AOD_PATH)
    personalities = []
    content = read_txt_file(minister_modifier_path)
    m_personalities = content["minister_personalities"]["personality"]
    for personality in m_personalities:
        name = personality["personality_string"]
        # public_name_key = personality["name"]
        public_name = public_name_dict.get(personality["name"].upper())
        position = personality["minister_position"].lower()
        # position = minister_titles[personality["minister_position"]]
        personality_modifiers = ensure_lists_are_lists(personality.get("modifier"))
        modifiers = []
        for modifier in personality_modifiers:
            modifiers.append(get_correct_modifiers(modifier))
        # if personality.get("modifier") is None:
        #     modifiers = []
        # elif isinstance(personality["modifier"], dict):
        #     # modifiers = [Modifier(*[personality["modifier"].get(key) for key in MODIFIER_ATTRIBUTES])]
        #     modifiers = [get_correct_modifiers(personality["modifier"])]
        # else:
        #     modifiers = []
        #     for modifier in personality["modifier"]:
        #         # modifiers.append(Modifier(*[modifier.get(key) for key in MODIFIER_ATTRIBUTES]))
        #         modifiers.append(get_correct_modifiers(modifier))
        personalities.append(MinisterPersonality(name, public_name, position, modifiers))
    return personalities


def scan_ideas():
    public_name_dict = get_minister_and_policy_names()
    # idea_titles = get_idea_titles()
    ideas_path = get_ideas_path(AOD_PATH)
    content = read_txt_file(ideas_path)
    raw_ideas = content["national_ideas"]["national_idea"]
    ideas = []
    for idea in raw_ideas:
        name = idea["personality_string"]
        public_name = public_name_dict.get(idea["name"].upper())
        position = idea["minister_position"]
        gov_types = ensure_lists_are_lists(idea.get("category"))
        idea_modifiers = ensure_lists_are_lists(idea.get("modifier"))
        modifiers = []
        for modifier in idea_modifiers:
            modifiers.append(get_correct_modifiers(modifier))
        ideas.append(Idea(name, public_name, position, modifiers, gov_types=gov_types))
    return ideas


def scan_politics_titles():
    title_dict = get_government_titles()
    more_titles = get_idea_titles()
    for key, item in more_titles.items():
        actual_key = key.replace("_", "")
        if title_dict.get(actual_key) is not None:
            raise Exception(f"Idea title {actual_key}: {item} already in dict")
        title_dict[actual_key] = item
    return {key.lower(): item for key, item in title_dict.items()}


def scan_minister_csv(filepath, minister_personalities):
    csv_content = read_csv_file(filepath)
    ministers = []
    country_code_from_file = None
    for line_num, line in enumerate(csv_content):
        if line_num == 0:
            country_code_from_file = line[0]
            continue
        minister_id = line[0]
        if not minister_id:
            continue
        # minister_position = line[1]
        position = line[1].replace(" ", "").lower()
        # position = line[1]
        # minister_name = line[2]
        # start_year = line[3]
        # minister_ideology = line[4]
        minister_personality_str = line[5]
        minister_personality = get_minister_personality(minister_personalities, minister_personality_str, position)
        # if minister_personality is None:
        #     print(minister_personality_str)
        # minister_loyalty = line[6]
        # minister_pic = line[7]
        ministers.append(Minister(minister_id, line[2], country_code_from_file, position, minister_personality, line[3], line[4], line[6], filepath, line[7]))
    return {country_code_from_file: ministers}

def scan_ministers_for_country(country_code):
    ministers_path = get_ministers_path(country_code, AOD_PATH)
    if not ministers_path.exists():
        print(f"Filepath {ministers_path} not found")
    minister_personalities = scan_minister_personalities()
    minister_dict = scan_minister_csv(ministers_path, minister_personalities)
    return minister_dict[country_code]


def scan_all_ministers(check_unique_ids=False):
    minister_list = []
    minister_files = get_ministers_files(AOD_PATH)
    minister_personalities = scan_minister_personalities()
    for minister_file in minister_files:
        ministers = list(scan_minister_csv(minister_file, minister_personalities).values())[0]
        for minister in ministers:
            minister_list.append(minister)
    if check_unique_ids:
        minister_dict = dict()
        for minister in minister_list:
            if minister_dict.get(minister.m_id) is not None:
                print(f"Minister id {minister.m_id} ({minister.name}) is not unique: {minister.filepath.name}")
            minister_dict[minister.m_id] = minister
        return minister_dict
    return {minister.m_id: minister for minister in minister_list}


def scan_policies_file():
    policy_path = get_province_rev_path(AOD_PATH)
    country_data = read_txt_file(policy_path)["country"]
    policy_dict = dict()
    for country_dict in country_data:
        if "nationalidentity" in country_dict.keys() or "socialpolicy" in country_dict.keys() or "nationalculture" in country_dict.keys():
            country_code = country_dict["tag"]
            if policy_dict.get(country_code) is None:
                policy_dict[country_code] = {
                    "nationalidentity": country_dict.get("nationalidentity"),
                    "socialpolicy": country_dict.get("socialpolicy"),
                    "nationalculture": country_dict.get("nationalculture")
                }
    return policy_dict


def scan_leaders_file(filepath, column_names=None):
    csv_content = read_csv_file(filepath)
    leaders = []
    country_code_from_file = None
    for line_num, line in enumerate(csv_content):
        if line_num == 0:
            column_names_in_file = [item.lower() for item in line]
            if column_names is None:
                column_names = column_names_in_file
            elif column_names != column_names_in_file:
                for col_name, col_name_f in zip(column_names, column_names_in_file):
                    if col_name != col_name_f:
                        print(f"Expected {col_name} = {col_name_f}, but this is not the case in file {filepath.name}")
            country_index = column_names.index("country")
            if country_index != 2:
                print(f"Country is not the third column in file {filepath.name}")
            continue
        if country_code_from_file is None:
            country_code_from_file = line[country_index]
        if line[country_index] != country_code_from_file:
            # raise Exception(f"Not all leaders are from the same country in {filepath}: {line[country_index]} != {country_code_from_file}")
            print(f"Not all leaders are from the same country in {filepath}: {line[country_index]} != {country_code_from_file}")
        leader_dict = {col_name: value for col_name, value in zip(column_names, line)}
        leaders.append(Leader(
            leader_dict["id"],
            leader_dict["name"],
            filepath,
            leader_dict["country"],
            leader_dict["skill"],
            leader_dict["max skill"],
            leader_dict["traits"],
            leader_dict["type"],
            leader_dict["start year"],
            leader_dict["end year"],
            leader_dict["loyalty"],
            leader_dict["experience"],
            leader_dict["ideal rank"],
            leader_dict["rank 3 year"],
            leader_dict["rank 2 year"],
            leader_dict["rank 1 year"],
            leader_dict["rank 0 year"],
            leader_dict["picture"]
        ))

    return leaders

def scan_all_leaders(check_unique_ids=False):
    column_names = ["name", "id", "country", "rank 3 year", "rank 2 year", "rank 1 year", "rank 0 year", "ideal rank", "max skill", "traits", "skill", "experience", "loyalty", "type", "picture", "start year", "end year", "x"]
    leader_dict = {}
    all_leaders = []
    leader_files = get_leaders_files(AOD_PATH)
    for filepath in leader_files:
        try:
            leaders = scan_leaders_file(filepath, column_names)
            for leader in leaders:
                all_leaders.append(leader)
        except KeyError:
            print(f"KeyError IN FILE: {filepath}")
        except IndexError:
            print(f"IndexError IN FILE: {filepath}")
        except TypeError:
            print(f"TypeError IN FILE {filepath}")
    if check_unique_ids:
        for leader in all_leaders:
            if leader_dict.get(leader.leader_id) is not None:
                raise Exception(f"Leader id is not unique: {leader.leader_id}")
            leader_dict[leader.leader_id] = leader
        return leader_dict
    for leader in all_leaders:
        leader_dict[leader.leader_id] = leader
    return leader_dict


def scan_scenario_file(filepath):
    if filepath is None:
        return None
    results = dict()

    results["deactivated"] = []
    results["researched"] = []
    results["blueprints"] = []

    content = read_txt_file(filepath, False)
    results["country_code"] = content["country"]["tag"].upper()
    if content["country"].get("deactivate") is not None:
        results["deactivated"] = content["country"]["deactivate"]
    if content["country"].get("techapps") is not None:
        results["researched"] = content["country"]["techapps"]
    if content["country"].get("blueprints") is not None:
        results["blueprints"] = content["country"]["blueprints"]
    if content["country"].get("research_mod") is not None:
        results["research_speed"] = float(content["country"]["research_mod"]) * 100
    minister_positions = ["headofstate", "headofgovernment", "foreignminister", "armamentminister", "ministerofsecurity", "ministerofintelligence", "chiefofstaff", "chiefofarmy", "chiefofnavy", "chiefofair"]
    for position in minister_positions:
        if content["country"].get(position) is not None:
            results[position] = int(content["country"][position]["id"])
    # if content["country"].get("headofstate") is not None:
    #     results["headofstate"] = content["country"]["headofstate"]["id"]
    # if content["country"].get("headofgovernment") is not None:
    #     results["headofgovernment"] = content["country"]["headofgovernment"]["id"]
    # if content["country"].get("foreignminister") is not None:
    #     results["foreignminister"] = content["country"]["foreignminister"]["id"]
    # if content["country"].get("armamentminister") is not None:
    #     results["armamentminister"] = content["country"]["armamentminister"]["id"]
    # if content["country"].get("ministerofsecurity") is not None:
    #     results["ministerofsecurity"] = content["country"]["ministerofsecurity"]["id"]
    # if content["country"].get("ministerofintelligence") is not None:
    #     results["ministerofintelligence"] = content["country"]["ministerofintelligence"]["id"]
    # if content["country"].get("chiefofstaff") is not None:
    #     results["chiefofstaff"] = content["country"]["chiefofstaff"]["id"]
    # if content["country"].get("chiefofarmy") is not None:
    #     results["chiefofarmy"] = content["country"]["chiefofarmy"]["id"]
    # if content["country"].get("chiefofnavy") is not None:
    #     results["chiefofnavy"] = content["country"]["chiefofnavy"]["id"]
    # if content["country"].get("chiefofair") is not None:
    #     results["chiefofair"] = content["country"]["chiefofair"]["id"]

    # deactivated_tech = []
    # researched_tech = []
    # blueprints = []
    # mode = None
    # stages = "={"
    # with open(filepath, "r", encoding = "ISO-8859-1") as f:
    #     for line in f:
    #         textline = line.split("#")[0].strip()
    #         if not textline:
    #             continue
    #         if "deactivate" in textline:
    #             mode = ["deactivated", 0]
    #             current_list = deactivated_tech
    #         if "techapps" in textline:
    #             mode = ["researched", 0]
    #             current_list = researched_tech
    #         if "blueprints" in textline:
    #             mode = ["blueprints", 0]
    #             current_list = blueprints
            
    #         if mode is not None:
    #             if mode[1] < 2:
    #                 for char in stages[mode[1]:]:
    #                     if char in textline:
    #                         textline = textline.split(char)[1].strip()
    #                         mode[1] += 1
    #             if mode[1] == 2:
    #                 if "}" in textline:
    #                     textline = textline.split("}")[0].strip()
    #                     mode = None
    #                 additions = [int(item.strip()) for item in textline.split(" ") if item]
    #                 current_list += additions

    #         # if mode[0] == "deactivated":
    #         #     textline.split(stages[mode[1]])
            
    #         if "research_mod" in textline:
    #             results["research_speed"] = float(textline.split("=")[1].strip()) * 100
    # results["deactivated"] = deactivated_tech
    # results["researched"] = researched_tech
    # results["blueprints"] = blueprints
    return results

def scan_scenario_file_for_country(country_code):
    filepath = get_scenario_file_path_for_country(country_code)
    return scan_scenario_file(filepath)

def scan_brigades(text_dict=None):
    units = dict()
    unit_types = ("land_unit_type", "naval_unit_type", "air_unit_type")
    filepaths = get_brigades_files(AOD_PATH)
    for filepath in filepaths:
        content = read_txt_file(filepath)
        for i, unit_type in enumerate(unit_types):
            if content.get(unit_type) and content.get(unit_type) == 1:
                l_n_or_a = i
        models = []
        if isinstance(content["model"], dict):
            models.append(Model(content["model"]))
            units[filepath.stem] = Brigade(filepath, Brigade.LAND_NAVAL_OR_AIR[l_n_or_a], models, content.get("locked"), text_dict)
            continue
        for model_dict in content["model"]:
            models.append(Model(model_dict))
        units[filepath.stem] = Brigade(filepath, Brigade.LAND_NAVAL_OR_AIR[l_n_or_a], models, content.get("locked"), text_dict)
    return units

def scan_divisions(text_dict=None):
    units = dict()
    unit_types = ("land_unit_type", "naval_unit_type", "air_unit_type")
    filepaths = get_divisions_files(AOD_PATH)
    for filepath in filepaths:
        content = read_txt_file(filepath)
        for i, unit_type in enumerate(unit_types):
            if content.get(unit_type) and content.get(unit_type) == 1:
                l_n_or_a = i
        models = []
        if isinstance(content["model"], dict):
            models.append(Model(content["model"]))
            units[filepath.stem] = Division(filepath, Division.LAND_NAVAL_OR_AIR[l_n_or_a], models, content.get("allowed_brigades"), content.get("max_speed_step"), text_dict)
            continue
        for model_dict in content["model"]:
            models.append(Model(model_dict))
        units[filepath.stem] = Division(filepath, Division.LAND_NAVAL_OR_AIR[l_n_or_a], models, content.get("allowed_brigades"), content.get("max_speed_step"), text_dict)
    return units


def get_tech_by_id(tech_id, list_of_techs):
    for tech in list_of_techs:
        if tech.tech_id == tech_id:
            return tech
    # print(f"Tech with id {tech_id} not found")
    return

def find_tech_by_name(tech_name, list_of_techs):
    results = []
    for tech in list_of_techs:
        if tech_name == tech.name:
            results.append(tech)
    # print(f"Tech named {tech_name} not found")
    return results


# should this be called ScanScenario?
class FileScanner:
    scenario_file_keys = [
        "name",
        "panel",
        "header",
        "globaldata",
        "history",
        "map",
        "province",
        "sleepevent",
        "include",
        "event"
    ]

    # def __init__(self, scenario_path, text_dict_w_duplicates=None, text_dict=None, tech_dict=None, minister_dict=None, leader_dict=None):
    def __init__(
        self,
        scenario_path,
        text_dict_w_duplicates=None,
        text_dict=None,
        tech_dict=None,
        minister_dict=None,
        leader_dict=None,
        brigade_dict=None,
        division_dict=None
    ):
        self.scenario_path = scenario_path
        self.text_dict_w_duplicates = text_dict_w_duplicates
        self.text_dict = text_dict
        if self.text_dict_w_duplicates is None:
            self.text_dict_w_duplicates =  get_texts_from_files_w_duplicates(get_all_text_files_paths(AOD_PATH))
        if self.text_dict is None:
            self.text_dict = get_texts_from_files(get_all_text_files_paths(AOD_PATH))
        
        self.tech_dict = tech_dict
        self.minister_dict = minister_dict
        self.leader_dict = leader_dict
        self.brigade_dict = brigade_dict
        self.division_dict = division_dict
        # TODO: should these be scanned if None?
        # TODO: how about tech teams?

        # TODO: is it useful to list these here?
        self.scenario_name = None
        self.selectable_countries = None
        self.country_codes = None
        self.include_files = None
        self.event_files = None
        self.event_file_paths = None

        self.event_dict = None
        self.country_dict = None

    def scan_main_scenario_file(self):
        file_content = read_txt_file(self.scenario_path, False)

        self.scenario_name_key = file_content["name"]
        self.scenario_name = self.text_dict.get(self.scenario_name_key)
        if self.scenario_name is None:
            self.scenario_name = self.text_dict.get(self.scenario_name_key.upper())
        if self.scenario_name is None:
            self.scenario_name = self.scenario_name_key

        self.scenario_pic_path = file_content["panel"]

        self.selectable_countries = file_content["header"].get("selectable")
        if self.selectable_countries is None:
            self.selectable_countries = []
        self.selectable_countries = [country_code.upper() for country_code in self.selectable_countries]
        for key in file_content["header"].keys():
            if len(key) == 3 and self.text_dict.get(key.upper()) and key.upper() not in self.selectable_countries:
                self.selectable_countries.append(key.upper())
        
        self.country_codes = self.selectable_countries.copy()

        # is this needed?
        # global_data = file_content["globaldata"]

        self.include_files = file_content["include"]
        if isinstance(self.include_files, str):
            self.include_files = [self.include_files]

        self.event_files = file_content.get("event")
        if isinstance(self.event_files, str):
            self.event_files = [self.event_files]
        if self.event_files is None:
            self.event_files = []

        self.happened_events = file_content.get("history")
        if self.happened_events is None:
            self.happened_events = []
        self.deactivated_events = file_content.get("sleepevent")
        if self.deactivated_events is None:
            self.deactivated_events = []
        
        # are these needed?
        # map_stuff = file_content.get("map")
        # province_stuff = file_content.get("province")

    def get_event_files(self, include_files=None, event_files=None):
        if include_files:
            self.include_files = include_files
        if event_files:
            self.event_files = event_files

        include_key = self.scenario_file_keys[-2]
        event_key = self.scenario_file_keys[-1]

        self.event_file_paths = []
        self.other_files = []
        for event_file_path_str in self.event_files:
            event_file_path = AOD_PATH / event_file_path_str.replace("\\", "/")
            for event_filepath in event_file_path.parent.glob(event_file_path.name, case_sensitive=False):
                if event_filepath.exists():
                    self.event_file_paths.append(event_filepath)
                    break
            else:
                print(f"File {str(event_file_path)} does not exist (key: {event_key})")
        for path_str in self.include_files:
            if event_key in path_str:
                include_event_file_path = AOD_PATH / path_str.replace("\\", "/")
                if include_event_file_path.exists():
                    included_dict = read_txt_file(include_event_file_path)
                    for event_file_path_str in included_dict[event_key]:
                        event_file_path = AOD_PATH / event_file_path_str.replace("\\", "/")
                        for event_filepath in event_file_path.parent.glob(event_file_path.name, case_sensitive=False):
                            if event_filepath.exists():
                                self.event_file_paths.append(event_filepath)
                                break
                        else:
                            print(f"File {str(event_file_path)} does not exist (key: include)")
                else:
                    print(f"Include file {include_event_file_path} does not exist")
            else:
                file_found = False
                other_file_path = AOD_PATH / path_str.replace("\\", "/")
                if other_file_path.exists():
                    self.other_files.append(other_file_path)
                    file_found = True
                    continue
                for filepath in other_file_path.parent.glob(other_file_path.name, case_sensitive=False):
                    if filepath.exists():
                        self.other_files.append(filepath)
                        file_found = True
                        break
                if not file_found:
                    print(f"File {str(other_file_path)} does not exist")

    def scan_events(self, already_scanned_event_files=None, show_empty_files=False, show_issues=False):
        if already_scanned_event_files is None:
            already_scanned_event_files = dict()
        self.event_dict = dict()
        for filepath in self.event_file_paths:
            events = already_scanned_event_files.get(filepath)
            if events is not None:
                for event_id, event in events.items():
                    if self.event_dict.get(event_id) is not None:
                        print(f"ERROR: Event ID already in use before: {event_id} {event.name} [{event.country}]")
                        continue
                    self.event_dict[event_id] = event
                continue
            content = read_txt_file(filepath)
            if isinstance(content, list):
                already_scanned_event_files[filepath] = []
                if show_empty_files:
                    print(f"No events in {filepath}")
                continue
            events_raw = content["event"]
            if isinstance(events_raw, dict):
                events_raw = [events_raw]
            more_events = []
            for event_raw in events_raw:
                event_raw["path"] = filepath
                event = get_event_from_raw_event(event_raw, filepath, self.text_dict)
                more_events.append(event)
                self.event_dict[event.event_id] = event
            already_scanned_event_files[filepath] = more_events

        for ev_id, ev in self.event_dict.items():
            for i, action in enumerate(ev.actions):
                for effect in action.effects:
                    if effect.type and effect.type == "trigger":
                        triggered_event_id = effect.which
                        if self.event_dict.get(triggered_event_id) is None:
                            name_text = ev.name if ev.name else "[no name]"
                            if show_issues:
                                print(f"Event {ev_id} [{ev.country_code}]: {name_text} triggers event {triggered_event_id}, which does not exist.")
                            continue
                        self.event_dict[triggered_event_id].triggered_by.append((ev, i))
                    elif effect.type and effect.type == "sleepevent":
                        deactivated_event_id = effect.which
                        if self.event_dict.get(deactivated_event_id) is None:
                            name_text = ev.name if ev.name else "[no name]"
                            if show_issues:
                                print(f"Event {ev_id} [{ev.country_code}]: {name_text} deactivates event {deactivated_event_id}, which does not exist.")
                            continue
                        self.event_dict[deactivated_event_id].deactivated_by.append((ev, i))
        
        return already_scanned_event_files

    def scan_scenario_files(self, already_scanned_scenario_files=None):
        # if already_scanned_scenario_files is None:
        #     already_scanned_scenario_files = dict()
        self.scenario_file_for_country = dict()
        country_key = "country"
        for filepath in self.other_files:
            content = read_txt_file(filepath)
            if country_key not in content.keys():
                continue
            country_data = content[country_key]
            if isinstance(country_data, dict):
                country_code = country_data["tag"].upper()
                if (old_path := self.scenario_file_for_country.get(country_code)) is not None:
                    print(f"Country {self.text_dict[country_code]} [{country_code}] already has something in {old_path}")
                    print(f"Also has something in {filepath}")
                    continue
                self.scenario_file_for_country[country_code] = filepath
            elif isinstance(country_data, list):
                for country_dict in country_data:
                    country_code = country_dict["tag"].upper()
                    if self.scenario_file_for_country.get(country_code) is not None:
                        print(f"Country {self.text_dict[country_code]} [{country_code}] already has something in {old_path}")
                        print(f"Also has something in {filepath}")
                        continue
                    self.scenario_file_for_country[country_code] = filepath
            else:
                raise Exception(f"Country data in unexpected form in {filepath}")
            # already_scanned_scenario_files.append(filepath)
            
        # return already_scanned_scenario_files
    
    def scan_all_countries(self):
        if self.country_codes is None:
            self.scan_main_scenario_file()
        if self.event_dict is None:
            self.scan_events()
        # TODO: are there countries that have no events and do not exist at the start?
        for event in self.event_dict.values():
            if event.country_code and event.country_code not in self.country_codes:
                self.country_codes.append(event.country_code)
        self.country_dict = {country_code.upper(): self.text_dict[country_code.upper()] for country_code in self.country_codes}

    def scan_techs(self):
        self.tech_dict = get_tech_dict()
    
    def scan_tech_teams(self, list_of_tech_teams=None):
        if list_of_tech_teams is None:
            list_of_tech_teams = scan_tech_teams()
        self.techteam_dict = dict()
        for techteam in list_of_tech_teams:
            if techteam.country_code in self.country_codes:
                self.techteam_dict[techteam.team_id] = techteam
    
    def scan_brigades_and_divisions(self):
        self.brigade_dict = scan_brigades(self.text_dict)
        self.division_dict = scan_divisions(self.text_dict)
    
    def scan_ministers(self):
        self.minister_dict = scan_all_ministers()
    
    def scan_leaders(self):
        self.leader_dict = scan_all_leaders()

    def scan(self, scan_everything=False):
        if self.event_dict is None:
            self.scan_main_scenario_file()
            self.get_event_files()
            self.scan_events()
        self.scan_all_countries()
        self.scan_scenario_files()
        self.scan_tech_teams()
        if scan_everything or self.tech_dict is None:
            self.scan_techs()
        if scan_everything or self.brigade_dict is None or self.division_dict is None:
            self.scan_brigades_and_divisions()
        if scan_everything or self.minister_dict is None:
            self.scan_ministers()
        if scan_everything or self.leader_dict is None:
            self.scan_leaders()


def get_country_data():
    td = get_texts_from_files(get_all_text_files_paths(AOD_PATH))
    td_w_duplicates = get_texts_from_files_w_duplicates(get_all_text_files_paths(AOD_PATH))

    ld = scan_all_leaders()
    md = scan_all_ministers()
    bd = scan_brigades()
    dd = scan_divisions()

    scen_p = sorted(get_scenarios(AOD_PATH), key=lambda p: p.name)
    fss = [FileScanner(scenario_path, td_w_duplicates, td, tech_dict, md, ld, bd, dd) for scenario_path in scen_p]
    for fs in fss:
        fs.scan()
    country_data = []
    for i, fs in enumerate(fss):
        for country_code in fs.country_codes:
            # TODO: lots of stuff
            scenario_file_for_country = fs.scenario_file_for_country.get(country_code)
            # data_row = (scen_p[i].name, fs.name, country_code, td[country_code],)
    return country_data

# countries_file should have rows of form
# scenario_filename;scenario_name;country_tag;country_name;country_inc_filepath;tech_teams_filepath;ministers_filepath
def write_countries_file(countries_data):
    filepath = this_files_directory / countries_file
    column_names = ["scenario_filename", "scenario_name", "country_code", "country_name", "country_scenario_filepath", "techteam_filepath", "ministers_filepath"]
    with open(filepath, "w") as f:
        f.write(f"{';'.join(column_names)}\n")
        for datarow in countries_data:
            row_to_write = [str(item) for item in datarow]
            f.write(f"{';'.join(row_to_write)}\n")

        
        
if __name__ == "__main__":
    import time
    from file_paths import get_scenarios
    
    techs = scan_techs()
    # tech_dict = {t.name: t for t in techs}
    tech_dict = get_tech_dict()
    teams = scan_tech_teams()

    # team_dict = dict()
    # for team in teams:
    #     if team_dict.get(team.team_id) is not None:
    #         print(f"Team id {team.team_id} already in use, before {team.name} [{team.country_code}]")
    #         continue
    #     team_dict[team.team_id] = team
        

    ideas = scan_ideas()
    minister_personalities = scan_minister_personalities()

    td = get_texts_from_files(get_all_text_files_paths(AOD_PATH))
    td_w_duplicates = get_texts_from_files_w_duplicates(get_all_text_files_paths(AOD_PATH))

    ld = scan_all_leaders()
    md = scan_all_ministers()
    bd = scan_brigades()
    dd = scan_divisions()

    scen_p = sorted(get_scenarios(AOD_PATH), key=lambda p: p.name)
    scen_c = [read_txt_file(scenario_path) for scenario_path in scen_p]

    def get_fss():
        start_time = time.time()
        fss = [FileScanner(scenario_path, td_w_duplicates, td, tech_dict, md, ld, bd, dd) for scenario_path in scen_p]
        already_scanned_event_files = None
        for fs in fss:
            print(fs.scenario_path)
            fs.scan()
            # fs.scan_main_scenario_file()
            # fs.get_event_files()
            # already_scanned_event_files = fs.scan_events()
            # fs.scan_all_countries()
            # fs.scan_tech_teams()
        print(f"Time elapsed: {round(time.time() - start_time, 1)} seconds")
        return fss

    fin_path = get_scenario_file_path_for_country("FIN")
    content = read_txt_file(fin_path, False)
    provinces = content["province"]
    fin = content["country"]
