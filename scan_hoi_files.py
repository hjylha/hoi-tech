
from read_hoi_files import get_tech_path, get_tech_files, get_tech_team_files, get_minister_modifier_path, get_ideas_path, get_ministers_path, get_policies_path, get_scenario_path_for_country
from read_hoi_files import get_tech_names, read_csv_file, read_txt_file
from classes import Component, EFFECT_ATTRIBUTES, Effect, MODIFIER_ATTRIBUTES, Modifier, Tech, TechTeam
from classes import MinisterPersonality, Minister, Idea, get_minister_personality


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
            tech_name = tech_names[tech_name_key].strip()
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
                # try again
                first_split = tech_text.split("or_required =")
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
    minister_modifier_path = get_minister_modifier_path()
    personalities = []
    content = read_txt_file(minister_modifier_path)
    m_personalities = content["minister_personalities"]["personality"]
    for personality in m_personalities:
        name = personality["personality_string"]
        position = personality["minister_position"].lower()
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
        personalities.append(MinisterPersonality(name, position, modifiers))
    return personalities


def scan_ideas():
    ideas_path = get_ideas_path()
    content = read_txt_file(ideas_path)
    raw_ideas = content["national_ideas"]["national_idea"]
    ideas = []
    for idea in raw_ideas:
        name = idea["personality_string"]
        position = idea["minister_position"]
        gov_types = ensure_lists_are_lists(idea.get("category"))
        idea_modifiers = ensure_lists_are_lists(idea.get("modifier"))
        modifiers = []
        for modifier in idea_modifiers:
            modifiers.append(get_correct_modifiers(modifier))
        ideas.append(Idea(name, position, modifiers, gov_types=gov_types))
    return ideas



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
        # minister_name = line[2]
        # start_year = line[3]
        # minister_ideology = line[4]
        minister_personality_str = line[5]
        minister_personality = get_minister_personality(minister_personalities, minister_personality_str, position)
        # if minister_personality is None:
        #     print(minister_personality_str)
        # minister_loyalty = line[6]
        # minister_pic = line[7]
        ministers.append(Minister(minister_id, line[2], position, minister_personality, line[3], line[4], line[6], line[7]))
    return {country_code_from_file: ministers}

def scan_ministers_for_country(country_code):
    ministers_path = get_ministers_path(country_code)
    if not ministers_path.exists():
        print(f"Filepath {ministers_path} not found")
    minister_personalities = scan_minister_personalities()
    minister_dict = scan_minister_csv(ministers_path, minister_personalities)
    return minister_dict[country_code]


def scan_policies_file():
    policy_path = get_policies_path()
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


def scan_scenario_file(filepath):
    if filepath is None:
        return None
    results = dict()

    results["deactivated"] = []
    results["researched"] = []
    results["blueprints"] = []

    content = read_txt_file(filepath, False)
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
    filepath = get_scenario_path_for_country(country_code)
    return scan_scenario_file(filepath)


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
        

if __name__ == "__main__":
    techs = scan_techs()
    tech_dict = {t.name: t for t in techs}
    teams = scan_tech_teams()

    ideas = scan_ideas()
    minister_personalities = scan_minister_personalities()

    fin_path = get_scenario_path_for_country("FIN")
    content = read_txt_file(fin_path, False)
    provinces = content["province"]
    fin = content["country"]
