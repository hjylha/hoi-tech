
from scan_hoi_files import get_country_names, scan_techs, get_tech_teams, scan_scenario_file_for_country


class Research:
    DEFAULT_YEAR = 1933
    DEFAULT_RESEARCH_SPEED = 100
    DEFAULT_DIFFICULTY = 0

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
                found = False
                for r in req:
                    if r in list_of_tech_ids:
                        found = True
                        break
                if not found:
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
                found = False
                for r in req:
                    if r in self.completed_techs:
                        found = True
                if not found:
                    return False
        return True

    def filter_teams(self):
        filtered_teams = []
        for team in self.all_teams:
            if team.start_year <= self.year and team.end_year >= self.year:
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


    def clear_all_tech(self):
        self.completed_techs = set()
        self.techs_researching = set()
        # self.active_techs = set()
        self.deactivated_techs = set()
        self.blueprints = set()
        self.update_active_techs()

    def choose_primary_country(self, country_code):
        self.primary_country = country_code
        scenario_data = scan_scenario_file_for_country(country_code)
        if scenario_data is None:
            return
        self.completed_techs = set(scenario_data["researched"])
        self.deactivated_techs = set(scenario_data["deactivated"])
        self.blueprints = set(scenario_data["blueprints"])
        if scenario_data.get("research_speed") is not None:
            self.research_speed = scenario_data["research_speed"]

        for tech_id in self.completed_techs:
            deactivations = self.techs[tech_id].get_deactivated_tech()
            for t_id in deactivations:
                self.deactivated_techs.add(t_id)

        self.update_active_techs()
        # for tech_id in self.techs:
        #     if self.are_tech_requirements_completed(tech_id) and tech_id not in self.completed_techs and tech_id not in self.deactivated_techs:
        #         self.active_techs.add(tech_id)


    def __init__(self, research_speed=None, difficulty=DEFAULT_DIFFICULTY, list_of_techs=None, countries=None, year=DEFAULT_YEAR) -> None:
        if list_of_techs is None:
            list_of_techs = scan_techs()
        self.techs = {tech.tech_id: tech for tech in list_of_techs}

        self.primary_country = None

        self.clear_all_tech()

        self.year = year
        self.research_speed = self.DEFAULT_RESEARCH_SPEED

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
        # difficulty does nothing for now, 0 = normal
        self.difficulty = difficulty

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
        self.filter_teams()
    
    def change_year(self, new_year):
        self.year = new_year
        self.filter_teams()

    def find_tech(self, search_term):
        results = []
        for tech in self.techs.values():
            if search_term.upper() in tech.name.upper():
                results.append(tech)
        return results

    def get_tech(self, key):
        if isinstance(key, int):
            return self.techs.get(key)
        if isinstance(key, str):
            for tech in self.techs.values():
                if key == tech.name:
                    return tech
    
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
            
    def list_requirements(self, tech):
        reqs = []
        for req in tech.requirements:
            if isinstance(req, int):
                reqs.append(f"{self.techs[req]}")
            elif isinstance(req, list):
                for t_id in req:
                    reqs.append(f"*{self.techs[t_id]}")
            else:
                raise Exception(f"Invalid type in requirements: {req}")
        return reqs
    
    def list_deactivations(self, tech):
        deactivation_ids = tech.get_deactivated_tech()
        return [f"{self.techs[t_id]}" for t_id in deactivation_ids]

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

    def complete_tech(self, completed_tech_id, update_active=True):
        self.completed_techs.add(completed_tech_id)
        self.techs[completed_tech_id].researched = 1
        self.research_speed += self.techs[completed_tech_id].get_research_speed_change()
        # just in case
        self.research_speed = round(self.research_speed, 1)

        if completed_tech_id in self.techs_researching:
            self.techs_researching.remove(completed_tech_id)
        if completed_tech_id in self.active_techs:
            self.active_techs.remove(completed_tech_id)
        if completed_tech_id in self.deactivated_techs:
            self.deactivated_techs.remove(completed_tech_id)

        for tech_id in self.techs[completed_tech_id].get_deactivated_tech():
            self.deactivate_tech(tech_id)
        
        if update_active:
            self.update_active_techs()
    
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
        while i < len(multiple_choice):
            go_back = True
            while js[i] < len(multiple_choice[i]):
            # for t_id in multiple_choice[i]:
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

    def complete_until_tech(self, tech_id):
        techs_to_complete = self.find_necessary_requirements(tech_id)
        if techs_to_complete is None:
            return
        techs_to_complete.reverse()
        # print(techs_to_complete)
        for t_id in techs_to_complete:
            self.complete_tech(t_id, update_active=False)
        self.update_active_techs()

    def undo_completed_tech(self, tech_id):
        self.completed_techs.remove(tech_id)
        self.techs[tech_id].researched = 0
        self.research_speed -= self.techs[tech_id].get_research_speed_change()
        # just in case
        self.research_speed = round(self.research_speed, 1)
        self.update_active_techs()
    
    def sort_teams_for_researching_tech(self, tech):
        # check blueprint
        has_blueprint = int(tech.tech_id in self.blueprints)

        team_results = []
        for team in self.teams:
            days = team.calculate_how_many_days_to_complete(tech, self.research_speed, self.difficulty, has_blueprint=has_blueprint)
            team_results.append([team, days])
        return sorted(team_results, key=lambda x: x[1])
    
    def st(self, tech_id, num_of_teams=5):
        sorted_teams = self.sort_teams_for_researching_tech(self.techs[tech_id])
        print(f"Fastest teams to research tech {self.techs[tech_id]}")
        for line in sorted_teams[:num_of_teams]:
            print(line[1], line[0])
        return sorted_teams


    
if __name__ == "__main__":
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


