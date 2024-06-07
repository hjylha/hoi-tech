
from scan_hoi_files import get_country_names, scan_techs, get_tech_teams, scan_scenario_file_for_country


class Research:
    DEFAULT_YEAR = 1933
    DEFAULT_RESEARCH_SPEED = 100
    DEFAULT_DIFFICULTY = 0

    def are_tech_requirements_completed(self, tech_id):
        if not self.techs[tech_id].requirements:
            return True
        for req in self.techs[tech_id].requirements:
            if isinstance(req, int):
                if req in self.completed_techs:
                    continue
                return False
            if isinstance(req, list):
                for r in req:
                    if r in self.completed_techs:
                        continue
                return False
        return True

    def filter_teams(self):
        filtered_teams = []
        for team in self.all_teams:
            if team.start_year <= self.year and team.end_year >= self.year:
                filtered_teams.append(team)
        self.teams = filtered_teams


    def clear_all_tech(self):
        self.completed_techs = set()
        self.techs_researching = set()
        self.active_techs = set()
        self.deactivated_techs = set()
        self.blueprints = set()

    def choose_primary_country(self, country_code):
        self.primary_country = country_code
        scenario_data = scan_scenario_file_for_country(country_code)
        if scenario_data is None:
            return
        self.completed_techs = set(scenario_data["researched"])
        self.deactivated_techs = set(scenario_data["deactivated"])
        self.blueprints = set(scenario_data["blueprints"])
        self.research_speed = scenario_data["research_speed"]

        for tech_id in self.techs:
            if self.are_tech_requirements_completed(tech_id) and tech_id not in self.completed_techs and tech_id not in self.deactivated_techs:
                self.active_techs.add(tech_id)


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
    
    def get_tech_by_short_name_and_category(self, short_name, category):
        for tech in self.techs.values():
            if tech.short_name == short_name and tech.category == category:
                return tech
    
    def print_active_tech(self):
        for tech_id in self.active_techs:
            print(self.techs[tech_id])

    def activate_tech(self, tech_id):
        self.active_techs.add(tech_id)
        self.techs[tech_id].active = 1

    def deactivate_tech(self, tech_id):
        self.deactivated_techs.add(tech_id)
        self.techs[tech_id].deactivate()

    def complete_tech(self, completed_tech_id):
        self.completed_techs.add(completed_tech_id)
        self.techs[completed_tech_id].researched = 1
        self.research_speed += self.techs[completed_tech_id].get_research_speed_change()

        if completed_tech_id in self.techs_researching:
            self.techs_researching.remove(completed_tech_id)
        if completed_tech_id in self.active_techs:
            self.active_techs.remove(completed_tech_id)
        if completed_tech_id in self.deactivated_techs:
            self.deactivated_techs.remove(completed_tech_id)

        for tech_id in self.techs[completed_tech_id].get_deactivated_tech():
            self.deactivate_tech(tech_id)
        
        for tech_id in self.techs:
            if self.are_tech_requirements_completed(tech_id):
                if not(tech_id in self.completed_techs or tech_id in self.deactivated_techs):
                    self.activate_tech(tech_id)
    
    def undo_completed_tech(self, tech_id):
        self.completed_techs.remove(tech_id)
        self.techs[tech_id].researched = 0
        self.research_speed -= self.techs[tech_id].get_research_speed_change() 
        # OTHER STUFF????????
        if self.are_tech_requirements_completed(tech_id):
            self.activate_tech(tech_id)
    
    def sort_teams_for_researching_tech(self, tech):
        # check blueprint
        has_blueprint = int(tech.tech_id in self.blueprints)

        team_results = []
        for team in self.teams:
            days = team.calculate_how_many_days_to_complete(tech, self.research_speed, self.difficulty, has_blueprint)
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


