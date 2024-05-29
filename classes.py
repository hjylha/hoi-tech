
from collections import namedtuple


RESEARCH_SPEED_CONSTANT = 2.8

Component = namedtuple("Component", ["type", "difficulty"])
EFFECT_ATTRIBUTES = ["type", "which", "value", "when", "where"]
Effect = namedtuple("Effect", EFFECT_ATTRIBUTES)


def calculate_components_difficulty_multiplier(component, research_speed_modifier):
    return max(1 / 20, 9 * research_speed_modifier / (component.difficulty + 2) / 200)


class Tech:
    COMPONENT_SIZE = 20
    NUM_OF_COMPONENTS = 5

    def __init__(self, tech_id, tech_name, tech_category, requirements, components, effects):
        self.tech_id = tech_id
        self.name = tech_name
        self.category = tech_category
        self.requirements = requirements
        self.components = components
        self.effects = effects
        self.current_component = 0
        self.component_progress = 0
        self.researched = 0
        self.deactivated = 0
        self.active = 0
    
    def __str__(self):
        return f"{self.tech_id} {self.name}"
    
    def to_db_tuple(self):
        return (
            self.tech_id, 
            self.name,
            self.category,
            "; ".join([str(r) for r in self.requirements]),
            "; ".join([",".join([str(i) for i in component]) for component in self.components]),
            "; ".join([",".join([str(a) for a in effect]) for effect in self.effects])
                )
    
    # def get_current_component(self):
    #     return self.progress // self.COMPONENT_SIZE
    
    def update_progress(self, progress_made):
        self.component_progress += progress_made
        if self.component_progress >= self.COMPONENT_SIZE:
            self.component_progress = 0
            self.current_component += 1
            # check if ready?
            if self.current_component >= 5:
                self.researched = 1

    def reset_progress(self):
        self.current_component = 0
        self.component_progress = 0
        self.researched = 0
    
    def get_current_progress(self):
        return self.current_component * self.COMPONENT_SIZE + self.component_progress
    
    def deactivate(self):
        self.possible = 0
        self.reset_progress()
    
    def get_research_speed_change(self):
        for effect in self.effects:
            if effect.type == "research_mod":
                return float(effect.value)
            
    def get_deactivated_tech(self):
        deactivated_tech = []
        for effect in self.effects:
            if effect.type == "deactivate":
                deactivated_tech.append(int(effect.which))
        return deactivated_tech
    
    def calculate_component_difficulty_multiplier(self, component_index, research_speed_modifier):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[component_index].difficulty + 2) / 200)
        return calculate_components_difficulty_multiplier(self.components[component_index], research_speed_modifier)
    
    def calculate_current_difficulty_multiplier(self, research_speed_modifier):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[self.current_component].difficulty + 2) / 9)
        return self.calculate_component_difficulty_multiplier(self.current_component, research_speed_modifier)


class TechTeam:
    def __init__(self, team_id, team_name, team_nation, skill, start_year, end_year, specialities, pic_path=None):
        self.team_id = team_id
        self.name = team_name
        self.nation = team_nation
        self.skill = skill
        self.start_year = start_year
        self.end_year = end_year
        self.specialities = specialities
        if pic_path is None:
            pic_path = "gfx/interface/tech/Team_noimage.bmp"
        self.pic_path = pic_path
        self.researching = 0

    def __str__(self):
        return self.name
        # return f"{self.name} {self.nation}"
    
    def to_db_tuple(self):
        return (
            self.team_id,
            self.name,
            self.nation,
            self.skill,
            self.start_year,
            self.end_year,
            "; ".join(self.specialities),
            self.pic_path
                )
    
    def calculate_1_day_progress_for_component(self, component, research_speed_modifier, has_blueprint=0):
        has_speciality = 0
        component_type = component.type
        if component_type in self.specialities:
            has_speciality = 1
        difficulty_modifier = calculate_components_difficulty_multiplier(component, research_speed_modifier)
        return 0.2 * RESEARCH_SPEED_CONSTANT * 0.1 * (self.skill + 6) * (has_speciality + 1) * (0.7 * has_blueprint + 1) * difficulty_modifier

    def calculate_how_many_days_to_complete(self, tech, research_speed_modifier, has_blueprint=0):
        days_gone = 0
        for component in tech.components:
            daily_progress = self.calculate_1_day_progress_for_component(component, research_speed_modifier, has_blueprint)
            days_to_complete_component = int(20 // daily_progress + 1)
            days_gone += days_to_complete_component
        return days_gone
    
    def calculate_1_day_progress_for_tech(self, tech, research_speed_modifier, has_blueprint=0):
        return self.calculate_1_day_progress_for_component(tech.components[tech.current_component, research_speed_modifier, has_blueprint])
