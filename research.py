
from read_hoi_files import get_country_names
from classes import GameConstants, HoITime
from scan_hoi_files import scan_minister_personalities, scan_ideas, scan_ministers_for_country
from scan_hoi_files import get_tech_dict, get_tech_teams, scan_policies_file, scan_scenario_file_for_country


class Politics:
    # TODO: year has an effect on available ministers

    def filter_personalities_and_ideas_that_affect_research(self):
        self.tech_minister_personalities = []
        for personality in self.minister_personalities:
            if personality.get_research_bonus():
                self.tech_minister_personalities.append(personality)
        self.tech_ideas = []
        for idea in self.ideas:
            if idea.get_research_bonus():
                self.tech_ideas.append(idea)
    
    def get_tech_personalities_and_ideas_as_dict(self):
        tech_personalities_and_ideas = dict()
        for personality in self.tech_minister_personalities:
            key = personality.position.lower()
            if tech_personalities_and_ideas.get(key) is None:
                tech_personalities_and_ideas[key] = [personality]
            else:
                tech_personalities_and_ideas[key].append(personality)
        for idea in self.tech_ideas:
            key = idea.position.lower()
            if tech_personalities_and_ideas.get(key) is None:
                tech_personalities_and_ideas[key] = [idea]
            else:
                tech_personalities_and_ideas[key].append(idea)
        return tech_personalities_and_ideas
    
    def get_policies_for_checkboxes(self):
        initial_dict = self.get_tech_personalities_and_ideas_as_dict()
        final_dict = dict()
        for key, value in initial_dict.items():
            final_dict[key] = [personality.name for personality in value]
            final_dict[key].append("other")
        return final_dict
    
    def get_minister_personality_or_idea(self, personality_str, position):
        for personality in (self.minister_personalities + self.ideas):
            if personality.name.lower() == personality_str.lower() and personality.position.lower() == "all":
                return personality
            if personality.name.lower() == personality_str.lower() and personality.position.lower() == position.lower():
                return personality
            if personality.name.lower() == personality_str.lower():
                print("Match for", personality.name, "but", personality.position, "!=", position)
                return personality
        else:
            print(f"Minister personality {personality_str} not found")

    def __init__(self):
        self.minister_personalities = scan_minister_personalities()
        self.ideas = scan_ideas()

        self.filter_personalities_and_ideas_that_affect_research()

        self.current_policies = {
            "headofstate": None,
            "headofgovernment": None,
            "foreignminister": None,
            "armamentminister": None,
            "ministerofsecurity": None,
            "ministerofintelligence": None,
            "chiefofstaff": None,
            "chiefofarmy": None,
            "chiefofnavy": None,
            "chiefofair": None,
            "nationalidentity": None,
            "socialpolicy": None,
            "nationalculture": None
        }
        self.available_ministers = []
    
    def scan_available_ministers(self, country_code):
        self.available_ministers = scan_ministers_for_country(country_code)
    
    def get_minister_by_id(self, minister_id):
        for minister in self.available_ministers:
            if minister.m_id == minister_id:
                return minister
    
    def get_sum_of_research_bonuses(self):
        bonuses = dict()
        for minister_or_idea in self.current_policies.values():
            if minister_or_idea is None:
                continue
            for category, value in minister_or_idea.get_research_bonus().items():
                if bonuses.get(category) is None:
                    bonuses[category] = value
                else:
                    bonuses[category] += value
        return bonuses

    def change_minister(self, new_minister):
        self.current_policies[new_minister.position] = new_minister.personality

    def change_idea(self, new_idea):
        self.current_policies[new_idea.position] = new_idea

    def change_ministers(self, ministers_dict, check_position=True):
        for position, minister in ministers_dict.items():
            if check_position and position.lower() != minister.position.lower():
                raise Exception(f"{position} does not match {minister.position} for {minister.name} [{minister.m_id}]")
            self.current_policies[position] = minister.personality
    
    def change_minister_or_idea(self, position, name):
        for pos in self.current_policies.keys():
            if pos == position.lower() and name == "other":
                self.current_policies[pos] = None
            elif pos == position.lower():
                personality = self.get_minister_personality_or_idea(name, pos)
                self.current_policies[pos] = personality

class Research:
    DEFAULT_YEAR = 1933
    DEFAULT_RESEARCH_SPEED = 100
    DEFAULT_DIFFICULTY = "EASY"
    POST_WAR_MODIFICATION = 10_000

    def get_date(self):
        return self.date.date
    
    def get_date_str(self):
        return self.date.get_date()
    
    def get_year(self):
        return self.date.get_year()

    def activate_tech(self, tech_id):
        self.active_techs.add(tech_id)
        self.techs[tech_id].active = 1

    def deactivate_tech(self, tech_id):
        self.deactivated_techs.add(tech_id)
        self.techs[tech_id].deactivate()

    def are_tech_requirements_in_list(self, tech_id, list_of_tech_ids):
        if not self.techs[tech_id].requirements:
            return True
        for req in self.techs[tech_id].requirements:
            if isinstance(req, int):
                if req not in list_of_tech_ids:
                    return False
            if isinstance(req, list):
                for r in req:
                    if r in list_of_tech_ids:
                        break
                else:
                    return False
        return True

    def are_tech_requirements_completed(self, tech_id):
        if not self.techs[tech_id].requirements:
            return True
        for req in self.techs[tech_id].requirements:
            if isinstance(req, int):
                if req not in self.completed_techs:
                    return False
            if isinstance(req, list):
                for r in req:
                    if r in self.completed_techs:
                        break
                else:
                    return False
        return True
    
    def can_tech_be_abandoned(self, tech_id):
        if tech_id not in self.completed_techs:
            return False
        category_num = tech_id // 1000
        if category_num not in [6, 8, 9]:
            return False
        for _, tech in self.research_slots:
            if tech is None:
                continue
            if tech.tech_id // 1000 == category_num:
                return False
        for t_id in self.techs[tech_id].allows:
            cat_num = t_id // 1000
            if cat_num == category_num and t_id in self.completed_techs:
                return False
        # should this check more?
        return True
    
    def can_tech_be_researched(self, tech_id):
        techs_in_research = [tech for _, tech in self.research_slots if tech is not None]
        for tech in techs_in_research:
            if tech_id == tech.tech_id:
                return False
            if tech_id in tech.get_deactivated_tech():
                return False
        if tech_id in self.active_techs:
            return True
        if tech_id in self.completed_techs:
            return False
        if not self.are_tech_requirements_completed(tech_id):
            return False
        for t_id in self.techs[tech_id].deactivated_by:
            if t_id in self.completed_techs:
                return False
        return True

    def filter_teams(self):
        filtered_teams = []
        year = self.get_year()
        for team in self.all_teams:
            if team.start_year <= year and team.end_year > year:
                filtered_teams.append(team)
        self.teams = filtered_teams
    
    def update_active_techs(self):
        self.active_techs = set()
        for tech_id in self.techs.keys():
            if tech_id in self.completed_techs:
                continue
            if tech_id in self.deactivated_techs:
                continue
            if self.are_tech_requirements_completed(tech_id):
                self.activate_tech(tech_id)
    
    def reactivate_tech(self, tech_id, update_tech=True):
        if tech_id not in self.deactivated_techs:
            return
        self.deactivated_techs.remove(tech_id)
        if update_tech:
            self.update_active_techs()


    def clear_all_tech(self):
        self.completed_techs = set()
        self.techs_researching = set()
        # self.active_techs = set()
        self.deactivated_techs = set()
        self.blueprints = set()
        self.update_active_techs()

    def change_minister(self, new_minister_personality):
        self.politics.current_policies[new_minister_personality.position.lower()] = new_minister_personality
    
    def change_minister_or_idea(self, position, name):
        self.politics.change_minister_or_idea(position, name)

    def choose_primary_country(self, country_code):
        self.primary_country = country_code
        self.politics.scan_available_ministers(country_code)
        scenario_data = scan_scenario_file_for_country(country_code)
        if scenario_data is None:
            return
        self.completed_techs = set(scenario_data["researched"])
        self.deactivated_techs = set(scenario_data["deactivated"])
        self.blueprints = set(scenario_data["blueprints"])
        if scenario_data.get("research_speed") is not None:
            self.research_speed = scenario_data["research_speed"]
        
        for possible_position, minister_id in scenario_data.items():
            if possible_position in self.politics.current_policies.keys():
                minister = self.politics.get_minister_by_id(minister_id)
                if minister is None:
                    print(minister_id)
                self.politics.current_policies[possible_position] = minister.personality
        
        policies = scan_policies_file().get(country_code)
        if policies:
            for position, idea_name in policies.items():
                idea = self.politics.get_minister_personality_or_idea(idea_name, position)
                self.politics.current_policies[position] = idea

        for tech_id in self.completed_techs:
            deactivations = self.techs[tech_id].get_deactivated_tech()
            for t_id in deactivations:
                self.deactivated_techs.add(t_id)

        self.update_active_techs()
        # for tech_id in self.techs:
        #     if self.are_tech_requirements_completed(tech_id) and tech_id not in self.completed_techs and tech_id not in self.deactivated_techs:
        #         self.active_techs.add(tech_id)

    def __init__(self, research_speed=None, tech_dict=None, countries=None, year=DEFAULT_YEAR, date=None, num_of_research_slots=5, **kwargs) -> None:
        # if tech_dict is None:
        #     tech_dict = get_tech_dict()
        self.techs = get_tech_dict() if tech_dict is None else tech_dict

        self.primary_country = None

        self.clear_all_tech()

        # self.year = year
        self.date = HoITime(**kwargs) if date is None else date
        self.research_speed = self.DEFAULT_RESEARCH_SPEED

        self.politics = Politics()

        if countries:
            country_code = countries[0]
            self.choose_primary_country(country_code)
            
        # can override research speed
        if research_speed is not None:
            self.research_speed = research_speed
        self.countries = [] if countries is None else countries

        self.all_teams = []
        for country_code in self.countries:
            self.all_teams += get_tech_teams(country_code)
        self.filter_teams()
        # difficulty -1, 0, 1, 2, 3  # not anymore
        # self.difficulty = difficulty
        self.constants = GameConstants(**kwargs)
        # do we need to do anything else with rockets and reactors?
        self.num_of_rocket_sites = 0
        self.reactor_size = 0
        # money issues
        self.teams_get_paid = 1

        self.num_of_research_slots = num_of_research_slots
        self.research_slots = [[None, None] for _ in range(self.num_of_research_slots)]

    def set_date(self, new_date):
        self.date.date = new_date
    
    def reset_date(self):
        self.date.reset_date()
    
    def change_year(self, new_year):
        self.date.change_year(new_year)
        self.filter_teams()

    def get_sum_of_policy_effects(self):
        return self.politics.get_sum_of_research_bonuses()
    
    def get_policy_effect_for_tech_category(self, tech_category):
        effect = 0
        for category, policy_effect in self.get_sum_of_policy_effects().items():
            if category == "all" or category == tech_category:
                effect += policy_effect
        return effect
    
    def get_policy_effect_for_tech(self, tech):
        return self.get_policy_effect_for_tech_category(tech.category)

    def add_country(self, country_code):
        if country_code not in self.countries:
            self.countries.append(country_code)
            self.all_teams += get_tech_teams(country_code)
        if self.primary_country is None:
            self.choose_primary_country(country_code)
        self.filter_teams()

    
    def remove_country(self, country_code):
        self.countries.remove(country_code)
        self.all_teams = [team for team in self.all_teams if team.nation != country_code]
        if self.primary_country == country_code:
            self.primary_country = None
            self.clear_all_tech()
        # is this needed?
        # if self.primary_country is None and self.countries:
        #     self.choose_primary_country(self.countries[0])
        self.filter_teams()
    
    # def change_year(self, new_year):
    #     self.year = new_year
    #     self.filter_teams()
    
    def change_difficulty(self, difficulty_string):
        self.constants.change_difficulty(difficulty_string)

    def find_tech(self, search_term):
        results = []
        for tech in self.techs.values():
            if search_term.lower() in tech.name.lower():
                if search_term == tech.name:
                    results.insert(0, tech)
                    continue
                results.append(tech)
        return results

    def get_tech(self, key):
        if isinstance(key, int):
            return self.techs.get(key)
        if isinstance(key, str):
            for tech in self.techs.values():
                if key == tech.name:
                    return tech
    
    def find_team(self, search_term):
        results = []
        for team in self.teams:
            if search_term.lower() in team.name.lower():
                if search_term == team.name:
                    results.insert(0, team)
                    continue
                results.append(team)
        return results
    
    def get_techs_from_ids(self, tech_ids):
        techs = []
        for t_id in tech_ids:
            if isinstance(t_id, int):
                techs.append(self.techs[t_id])
                continue
            if isinstance(t_id, list):
                techs.append([self.techs[tech_id] for tech_id in t_id])
                continue
            raise Exception(f"Weird item type on a list of techs: {type(t_id)}")
        return techs
            
    
    # this is not going to work
    def get_tech_by_short_name_and_category(self, short_name, category):
        for tech in self.techs.values():
            if tech.short_name == short_name and tech.category == category:
                return tech
    
    # this might not work
    def get_team_by_name_and_country(self, team_name, country_code):
        for team in self.teams:
            if team.name == team_name and team.nation == country_code:
                return team
    
    def get_vacant_research_slots(self):
        vacant_indices = []
        for i, t_n_t in enumerate(self.research_slots):
            if t_n_t[0] is None or t_n_t[1] is None:
                vacant_indices.append(i)
        return vacant_indices

    def update_num_of_research_slots(self):
        new_research_slots = []
        for t_n_t in self.research_slots:
            if t_n_t[0] is not None and t_n_t[1] is not None:
                new_research_slots.append(t_n_t)
        self.research_slots = new_research_slots
        num_of_empty_slots = self.num_of_research_slots - len(self.research_slots)
        if num_of_empty_slots <= 0:
            return
        for _ in range(num_of_empty_slots):
            self.research_slots.append([None, None])
            
    def save_status_to_file(self, path):
        lines = []
        country_line = f"country={','.join(self.countries)}"
        lines.append(country_line)
        difficulty_line = f"difficulty={self.constants.current_difficulty_string}"
        lines.append(difficulty_line)
        year_line = f"year={self.get_year()}"
        lines.append(year_line)
        research_speed_line = f"research_speed={self.research_speed}"
        lines.append(research_speed_line)
        rocket_site_line = f"num_of_rocket_sites={self.num_of_rocket_sites}"
        lines.append(rocket_site_line)
        reactor_size_line = f"reactor_size={self.reactor_size}"
        lines.append(reactor_size_line)
        completed_techs_line = f"completed={','.join([str(t) for t in self.completed_techs])}"
        lines.append(completed_techs_line)
        deactivated_techs_line = f"deactivated={','.join([str(t) for t in self.deactivated_techs])}"
        lines.append(deactivated_techs_line)
        blueprints_line = f"blueprints={','.join([str(t) for t in self.blueprints])}"
        lines.append(blueprints_line)
        money_line = f"has_money={str(self.teams_get_paid)}"
        for position, personality in self.politics.current_policies.items():
            name = "" if personality is None else personality.name
            lines.append(f"{position}={name}")
        with open(path, "w") as f:
            f.write("\n".join(lines))

    def load_status_from_file(self, path):
        if not path.exists():
            return
        self.clear_all_tech()
        country_codes = None
        year = None
        research_speed = None
        completed = None
        deactivated = None
        blueprints = None
        policy_changes = dict()
        with open(path, "r") as f:
            for line in f:
                if "country" in line:
                    country_codes = line.split("=")[1].strip().split(",")
                elif "difficulty" in line:
                    difficulty_string = line.split("=")[1].strip()
                    if difficulty_string in self.constants.difficulty_modifiers.keys():
                        self.constants.change_difficulty(difficulty_string)
                elif "year" in line:
                    try:
                        year = int(line.split("=")[1].strip())
                    except ValueError:
                        pass
                elif "research_speed" in line:
                    try:
                        research_speed = float(line.split("=")[1].strip())
                    except ValueError:
                        pass
                elif "num_of_rocket_sites" in line:
                    try:
                        self.num_of_rocket_sites = int(line.split("=")[1].strip())
                        # print(f"{self.num_of_rocket_sites=}")
                    except ValueError:
                        pass
                elif "reactor_size" in line:
                    try:
                        self.reactor_size = int(line.split("=")[1].strip())
                    except ValueError:
                        pass
                elif "completed" in line:
                    try:
                        completed = [int(tech) for tech in line.split("=")[1].strip().split(",")]
                    except ValueError:
                        pass
                elif "deactivated" in line:
                    try:
                        deactivated = [int(tech) for tech in line.split("=")[1].strip().split(",")]
                    except ValueError:
                        pass
                elif "blueprints" in line:
                    try:
                        blueprints = [int(tech) for tech in line.split("=")[1].strip().split(",")]
                    except ValueError:
                        pass
                elif "has_money" in line:
                    try:
                        self.teams_get_paid = int(line.split("=")[1].strip())
                    except ValueError:
                        pass
                else:
                    for position in self.politics.current_policies:
                        if position in line:
                            policy_changes[position] = line.split("=")[1].strip()
                            # personality_str = line.split("=")[1].strip()
                            # personality = self.politics.get_minister_personality(personality_str, position)
                            # self.politics.current_policies[position] = personality
        if country_codes:
            for country_code in country_codes:
                if country_code:
                    self.add_country(country_code)
        if year:
            self.change_year(year)
        if research_speed:
            self.research_speed = research_speed
        if completed:
            self.completed_techs = set(completed)
        if deactivated:
            self.deactivated_techs = set(deactivated)
        if blueprints:
            self.blueprints = set(blueprints)
        if policy_changes:
            for position, name in policy_changes.items():
                self.change_minister_or_idea(position, name)
        self.update_active_techs()
    

    def get_current_policies_and_effects_for_checkboxes(self):
        policy_dict = dict()
        for position, personality in self.politics.current_policies.items():
            if personality is None:
                policy_dict[position] = ["other", dict()]
            elif (research_bonus := personality.get_research_bonus()):
                policy_dict[position] = [personality.name, research_bonus]
            else:
                policy_dict[position] = ["other", dict()]
        return policy_dict

    def get_post_war_modified_ids(self, tech_ids):
        modified_ids = []
        for t_id in tech_ids:
            if self.techs[t_id].is_post_war:
                t_id += self.POST_WAR_MODIFICATION
            modified_ids.append(t_id)
        return modified_ids
            
    def list_requirements(self, tech, with_post_war_modification=True):
        reqs = []
        for req in tech.requirements:
            if isinstance(req, int):
                if with_post_war_modification and self.techs[req].is_post_war:
                    req += self.POST_WAR_MODIFICATION
                reqs.append(str(req))
                # reqs.append(f"{self.techs[req]}")
            elif isinstance(req, list):
                for t_id in req:
                    if with_post_war_modification and self.techs[t_id].is_post_war:
                        t_id += self.POST_WAR_MODIFICATION
                    reqs.append(f"*{t_id}")
                    # reqs.append(f"*{self.techs[t_id]}")
            else:
                raise Exception(f"Invalid type in requirements: {req}")
        # if with_post_war_modification:
        #     reqs = self.get_post_war_modified_ids(reqs)
        return reqs
    
    def list_deactivations(self, tech, with_post_war_modification=True):
        if with_post_war_modification:
            return self.get_post_war_modified_ids(tech.get_deactivated_tech())
        return tech.get_deactivated_tech()
        # deactivation_ids = tech.get_deactivated_tech()
        # return [f"{self.techs[t_id]}" for t_id in deactivation_ids]

    def list_is_required_in(self, tech, with_post_war_modification=True):
        if with_post_war_modification:
            return self.get_post_war_modified_ids(tech.allows)
        return list(tech.allows)
        # return [f"{self.techs[t_id]}" for t_id in tech.allows]
    
    def list_is_deactivated_by(self, tech, with_post_war_modification=True):
        if with_post_war_modification:
            return self.get_post_war_modified_ids(tech.deactivated_by)
        return list(tech.deactivated_by)

    def list_effects(self, tech):
        # TODO: improve this
        effects = []
        for effect in tech.effects:
            type_part = effect.type if effect.type is not None else ""
            which_part = effect.which if effect.which is not None else ""
            value_part = effect.value if effect.value is not None else ""
            when_part = effect.when if effect.when is not None else ""
            where_part = effect.where if effect.where is not None else ""
            effect_line = f"{type_part}, {which_part}, {value_part}, {when_part}, {where_part}"
            effects.append(effect_line.lower())
        return effects

    def print_active_tech(self):
        for tech_id in self.active_techs:
            print(self.techs[tech_id])

    def complete_tech(self, tech_id, update_active=True, check_requirements=False):
        if check_requirements and (not self.are_tech_requirements_completed(tech_id) or tech_id in self.deactivated_techs):
            print(f"tech {tech_id} cannot be researched")
            return
        self.completed_techs.add(tech_id)
        self.techs[tech_id].researched = 1
        self.research_speed += self.techs[tech_id].get_research_speed_change()
        # just in case
        self.research_speed = round(self.research_speed, 1)

        if tech_id in self.techs_researching:
            self.techs_researching.remove(tech_id)
        if tech_id in self.active_techs:
            self.active_techs.remove(tech_id)
        if tech_id in self.deactivated_techs:
            self.deactivated_techs.remove(tech_id)

        for tech_id in self.techs[tech_id].get_deactivated_tech():
            self.deactivate_tech(tech_id)
        for tech_id in self.techs[tech_id].get_reactivated_tech():
            self.reactivate_tech(tech_id, False)
        
        if update_active:
            self.update_active_techs()
    
    # TODO: fix this
    def find_necessary_requirements(self, tech_id, techs_to_complete=None, multiple_choice=None):
        if tech_id in self.completed_techs:
            return techs_to_complete
        if tech_id in self.deactivated_techs:
            return
        if techs_to_complete is not None and tech_id in techs_to_complete:
            return techs_to_complete
        
        if techs_to_complete is None:
            techs_to_complete = [tech_id]
        elif tech_id not in techs_to_complete:
            techs_to_complete.append(tech_id)
        # techs_to_complete = [tech_id] if techs_to_complete is None else
        multiple_choice = [] if multiple_choice is None else multiple_choice

        new_requirements = self.techs[tech_id].requirements
        while new_requirements:
            new_new_requirements = []
            for t_id in new_requirements:
                if isinstance(t_id, list):
                    multiple_choice.append(t_id)
                    continue
                if isinstance(t_id, int):
                    if t_id in self.deactivated_techs:
                        return
                    if t_id in self.completed_techs or t_id in techs_to_complete:
                        continue
                    techs_to_complete.append(t_id)
                    new_new_requirements += self.techs[t_id].requirements
            new_requirements = new_new_requirements
        
        if not multiple_choice:
            return techs_to_complete
        
        i = 0
        js = [0 for _ in multiple_choice]
        # for i, choice in enumerate(multiple_choice):
        #     for j, t_id in enumerate()
        print(multiple_choice)
        while i < len(multiple_choice):
            go_back = True
            # old_techs_to_complete = techs_to_complete.copy()
            while js[i] < len(multiple_choice[i]):
            # for t_id in multiple_choice[i]:
                # techs_to_complete = old_techs_to_complete.copy()
                techs = self.find_necessary_requirements(multiple_choice[i][js[i]], techs_to_complete, multiple_choice)
                # print(f"{multiple_choice[i][js[i]]}: {techs=}")
                if techs is not None:
                    techs_to_complete = techs
                    go_back = False
                    i += 1
                    if d := (len(multiple_choice) - len(js)) > 0:
                        for _ in range(d):
                            js.append(0)
                    break
                js[i] += 1
            if go_back:
                js[i] = 0
                i -= 1
            if i < 0:
                return

        return techs_to_complete

    def find_sufficient_requirements(self, tech_id):
        if tech_id in self.completed_techs or tech_id in self.deactivated_techs:
            return
        techs_to_complete = set([tech_id])
        new_requirements = self.techs[tech_id].requirements
        while new_requirements:
            new_new_requirements = []
            for t_id in new_requirements:
                if isinstance(t_id, int):
                    if t_id not in self.completed_techs and t_id not in self.deactivated_techs:
                        techs_to_complete.add(t_id)
                        new_new_requirements += self.techs[t_id].requirements
                if isinstance(t_id, list):
                    for te_id in t_id:
                        if te_id not in self.completed_techs and te_id not in self.deactivated_techs:
                            techs_to_complete.add(te_id)
                            new_new_requirements += self.techs[te_id].requirements
            new_requirements = new_new_requirements
        return techs_to_complete

    def complete_until_tech(self, tech_id):
        # techs_to_complete = self.find_necessary_requirements(tech_id)
        if tech_id in self.active_techs:
            self.complete_tech(tech_id, update_active=True)
            return
        techs_to_complete = self.find_sufficient_requirements(tech_id)
        if techs_to_complete is None:
            return
        # techs_to_complete.reverse()
        # techs_to_complete = set(techs_to_complete)
        # print(techs_to_complete)
        steps = [t_id for t_id in techs_to_complete if self.are_tech_requirements_completed(t_id)]
        for t_id in steps:
            techs_to_complete.remove(t_id)
        # step_num = 1
        # reached_goal = False
        while tech_id not in steps:
            found_some = False
            tech_ids_to_remove = []
            for t_id in techs_to_complete:
                if self.are_tech_requirements_in_list(t_id, list(self.completed_techs) + steps) and not any([t in steps for t in self.techs[t_id].deactivated_by]):
                    steps.append(t_id)
                    # techs_to_complete.remove(t_id)
                    tech_ids_to_remove.append(t_id)
                    found_some = True
            if not found_some:
                print(f"Cannot research tech {self.techs[tech_id]}")
                # print(f"{steps=}")
                # print(f"{techs_to_complete=}")
                return
                # raise Exception("Cannot complete tech for some reason")
            for t_id in tech_ids_to_remove:
                techs_to_complete.remove(t_id)
        for t_id in steps:
            self.complete_tech(t_id, update_active=False, check_requirements=True)
        self.update_active_techs()

    def abandon_doctrine(self, tech_id):
        self.completed_techs.remove(tech_id)
        self.blueprints.add(tech_id)
        self.techs[tech_id].researched = 0
        self.research_speed += self.techs[tech_id].get_research_speed_change()
        # just in case
        self.research_speed = round(self.research_speed, 1)
        self.update_active_techs()

    def undo_completed_tech(self, tech_id):
        self.completed_techs.remove(tech_id)
        self.techs[tech_id].researched = 0
        self.research_speed -= self.techs[tech_id].get_research_speed_change()
        # just in case
        self.research_speed = round(self.research_speed, 1)
        self.update_active_techs()
    
    def calculate_1_day_progress_for_research(self, team, tech, research_speed=None):
        if research_speed is None:
            research_speed = self.research_speed
        has_blueprint = int(tech.tech_id in self.blueprints)
        extra_bonus = -100 * self.get_policy_effect_for_tech(tech)
        return team.calculate_1_day_progress_for_tech(tech, research_speed, self.constants, extra_bonus, has_blueprint, self.num_of_rocket_sites, self.reactor_size, self.teams_get_paid)

    def calculate_how_many_days_to_complete(self, team, tech, research_speed=None):
        if research_speed is None:
            research_speed = self.research_speed
        has_blueprint = int(tech.tech_id in self.blueprints)
        extra_bonus = -100 * self.get_policy_effect_for_tech(tech)
        return team.calculate_how_many_days_to_complete(tech, research_speed, self.constants, extra_bonus, has_blueprint, self.num_of_rocket_sites, self.reactor_size, self.teams_get_paid)
    
    def calculate_completion_days_with_improvements(self, team, tech):
        has_blueprint = int(tech.tech_id in self.blueprints)
        extra_bonus = -100 * self.get_policy_effect_for_tech(tech)
        completion_info = team.calculate_detailed_completion_times_for_tech(tech, self.research_speed, self.constants, extra_bonus, has_blueprint, self.num_of_rocket_sites, self.reactor_size, self.teams_get_paid)
        # days_and_research_speeds = [0, 0, 999999]
        days = 0
        unacceptable_lower_bound = -1
        unacceptable_upper_bound = 999_999
        lower_rs = unacceptable_lower_bound
        upper_rs = unacceptable_upper_bound
        for line in completion_info:
            days += line[0]
            if line[1] is not None and line[1][1] > lower_rs:
                lower_rs = line[1][1]
            if line[2] is not None and line[2][1] < upper_rs:
                upper_rs = line[2][1]
        if lower_rs == unacceptable_lower_bound:
            lower_tuple = None
        else:
            lower_tuple = (self.calculate_how_many_days_to_complete(team, tech, lower_rs), lower_rs)
        if upper_rs == unacceptable_upper_bound:
            upper_tuple = None
        else:
            upper_tuple = (self.calculate_how_many_days_to_complete(team, tech, upper_rs), upper_rs)
        return (days, lower_tuple, upper_tuple)

    def pcd(self, team, tech):
        stuff = self.calculate_completion_days_with_improvements(team, tech)
        print(f"{team.name} completes {tech.name} in {stuff[0]} days.")
        print(f"If research speed is {stuff[1][1]}, tech is completed in {stuff[1][0]} days.")
        print(f"If research speed is {stuff[2][1]}, tech is completed in {stuff[2][0]} days.")

    def find_fastest_team(self, tech):
        fastest_team = None
        fastest_time = 999999
        for team in self.teams:
            # ignore teams that are researching
            if team in [t for t, _ in self.research_slots]:
                continue
            days = self.calculate_how_many_days_to_complete(team, tech)
            if days < fastest_time:
                fastest_time = days
                fastest_team = team
        return [fastest_team, fastest_time]

    def sort_teams_for_researching_tech(self, tech):
        team_results = []
        for team in self.teams:
            # ignore teams that are researching
            if team in [t for t, _ in self.research_slots]:
                pass
            # days = team.calculate_how_many_days_to_complete(tech, self.research_speed, self.difficulty, has_blueprint=has_blueprint, num_of_rocket_sites=self.num_of_rocket_sites)
            days = self.calculate_how_many_days_to_complete(team, tech)
            team_results.append([team, days])
        return sorted(team_results, key=lambda x: x[1])
    
    def st(self, tech_id, num_of_teams=5):
        sorted_teams = self.sort_teams_for_researching_tech(self.techs[tech_id])
        print(f"Fastest teams to research tech {self.techs[tech_id]}")
        for line in sorted_teams[:num_of_teams]:
            print(line[1], line[0])
        return sorted_teams

    def sort_teams_for_researching_tech_w_improvements(self, tech, num_of_teams=10):
        sorted_teams = self.sort_teams_for_researching_tech(tech)[:num_of_teams]
        sorted_teams_w_improvements = []
        for team, days_num in sorted_teams:
            days_plus_more = self.calculate_completion_days_with_improvements(team, tech)
            if days_plus_more[0] != days_num:
                raise Exception(f"Tech completion time mismatch: {days_plus_more[0]} /= {days_num}")
            sorted_teams_w_improvements.append([team, days_num, days_plus_more[1], days_plus_more[2]])
        return sorted_teams_w_improvements

    def sort_active_tech_based_on_research_time(self):
        if not self.teams:
            return []
        tech_results = []
        for tech_id in self.active_techs:
            team, days = self.sort_teams_for_researching_tech(self.techs[tech_id])[0]
            tech_results.append([self.techs[tech_id], days, team])
        return sorted(tech_results, key=lambda x: x[1])

    def st2(self, num_of_techs=5):
        if not self.teams:
            return []
        sorted_tech = self.sort_active_techs_based_on_research_time()
        print("Fastest techs to research:")
        for line in sorted_tech[:num_of_techs]:
            # tech, days, team = line
            print(line[1], line[0].name, f"({line[2].name})")
        return sorted_tech
    
    def sort_active_tech_based_on_research_time_and_research_speed(self):
        if not self.teams:
            return []
        tech_results = []
        for tech_id in self.active_techs:
            team, days = self.sort_teams_for_researching_tech(self.techs[tech_id])[0]
            research_speed_change = self.techs[tech_id].get_research_speed_change()
            slope_of_research_speed = research_speed_change / days
            tech_results.append([self.techs[tech_id], 100 * slope_of_research_speed, team])
        return sorted(tech_results, key=lambda x: x[1], reverse=True)

    # approximations
    def calculate_approx_time_comparison_to_complete_tech(self, team, tech):
        has_blueprint = int(tech.tech_id in self.blueprints)
        extra_bonus = -100 * self.get_policy_effect_for_tech(tech)
        return team.calculate_approx_time_comparison_to_complete_tech(tech, self.research_speed, extra_bonus, has_blueprint, self.teams_get_paid)

    def sort_teams_based_on_approx_time(self, tech):
        team_results = []
        for team in self.teams:
            time_comparison = self.calculate_approx_time_comparison_to_complete_tech(team, tech)
            team_results.append([team, time_comparison])
        return sorted(team_results, key=lambda x: x[1])
    
    def sort_active_tech_based_on_approx_time(self):
        if not self.teams:
            return []
        tech_results = []
        for tech_id in self.active_techs:
            team, time_comparison = self.sort_teams_based_on_approx_time(self.techs[tech_id])[0]
            tech_results.append([self.techs[tech_id], time_comparison, team])
        return sorted(tech_results, key=lambda x: x[1])

    def sort_active_tech_based_on_approx_time_and_research_speed(self):
        if not self.teams:
            return []
        # positive_change = []
        # no_change = []
        tech_results = []
        for tech_id in self.active_techs:
            team, time_comparison = self.sort_teams_based_on_approx_time(self.techs[tech_id])[0]
            research_speed_change = self.techs[tech_id].get_research_speed_change()
            # if research_speed_change == 0:
            #     # hopefully nothing positive gets to 10_000 comparison
            #     no_change.append([self.techs[tech_id], 10_000 + time_comparison, team])
            #     continue
            # smaller is better here, though negative is worse than positive
            comparison_value = research_speed_change / (self.research_speed + research_speed_change) / time_comparison
            # if research_speed_change > 0:
            #     positive_change.append([self.techs[tech_id], comparison_value, team])
            #     continue
            tech_results.append([self.techs[tech_id], comparison_value, team])
        # return sorted(positive_change, key= lambda x: x[1]) + sorted(no_change, key=lambda x: x[1]) + sorted(tech_results, key=lambda x: x[1])
        return sorted(tech_results, key=lambda x: x[1], reverse=True)

    def do_research_for_day(self):
        completed_tech_ids = []
        for i, t_n_t in enumerate(self.research_slots):
            team, tech = t_n_t
            if tech is None:
                continue
            progress = self.calculate_1_day_progress_for_research(team, tech)
            tech.update_progress(progress)
            if tech.researched:
                self.complete_tech(tech.tech_id)
                completed_tech_ids.append(tech.tech_id)
                self.research_slots[i] = [None, None]
                if len(self.research_slots) != self.num_of_research_slots:
                    self.update_num_of_research_slots()
        self.date.next_day()
        return completed_tech_ids


if __name__ == "__main__":
    import sys
    country = input("Select country: ")
    country_dict = get_country_names()
    for nation_code, nation in country_dict.items():
        if nation_code == country.upper() or nation.upper() == country.upper():
            country_code = nation_code
            print(f"Selected: {nation_code} {nation}")
            break
    # research_speed = input("Research speed (100 if skipped):")
    # if research_speed:
    #     research_speed = float(research_speed)
    # else:
    #     research_speed = 100

    # r = Research(research_speed, countries=[country_code])
    r = Research(countries=[country_code])
    print("Research speed:", r.research_speed)
    print("Completed:", r.completed_techs)
    print("Deactivated:", r.deactivated_techs)
    print("Blueprints:", r.blueprints)

    pol = r.politics
    curr = r.politics.current_policies

    if len(sys.argv) > 1 and sys.argv[1] == "1":
        import time
        t1_start = time.perf_counter()
        tech_list1 = r.sort_active_tech_based_on_approx_time()
        t1_end = time.perf_counter()
        t1_duration = t1_end - t1_start
        
        t2_start = time.perf_counter()
        tech_list2 = r.sort_active_tech_based_on_research_time()
        t2_end = time.perf_counter()
        t2_duration = t2_end - t2_start

        print(f"Approximate calculation: \t {t1_duration}")
        print(f"Accurate calculation: \t\t {t2_duration}")
        print(f"Approx takes {round(t1_duration / t2_duration, 4)} of accurate calculation's time")
    
    if len(sys.argv) > 2 and sys.argv[2] == "1":

        print()
        sorting = r.sort_active_tech_based_on_approx_time_and_research_speed()
        print("Sorting active tech based on approx research time and research speed inpact (smaller is better, though negative is worse than positive)")
        for tech, value, team in sorting:
            print(f"{tech.name} --- {round(value, 4)} --- ({team.name})")

        print()
        true_sorting = r.sort_active_tech_based_on_research_time_and_research_speed()
        print(f"Sorting active tech according to biggest slope of research speed and time")
        for tech, slope, team in true_sorting:
            print(f"{tech.name} --- {round(slope, 4)} --- ({team.name})")


