
from collections import namedtuple
import math

from read_hoi_files import get_blueprint_bonus_and_tech_speed_modifier

# should this be read from game files?
# RESEARCH_SPEED_CONSTANT = 2.8
# BLUEPRINT_BONUS = 1.7
BLUEPRINT_BONUS, RESEARCH_SPEED_CONSTANT = get_blueprint_bonus_and_tech_speed_modifier()

Component = namedtuple("Component", ["type", "difficulty"])
EFFECT_ATTRIBUTES = ["type", "which", "value", "when", "where"]
Effect = namedtuple("Effect", EFFECT_ATTRIBUTES)
MODIFIER_ATTRIBUTES = ["type", "value", "option", "extra", "modifier_effect"]
Modifier = namedtuple("Modifier", MODIFIER_ATTRIBUTES)


def calculate_components_difficulty_multiplier(component, research_speed_modifier, game_difficulty, total_extra_bonus):
    return max(1 , (1 - game_difficulty / 10) * research_speed_modifier * 100 / (100 - total_extra_bonus) / (component.difficulty + 2) )


def get_modifiers_tech_effects(modifier):
    if modifier.type == "tech_group_mod":
        return (modifier.value, modifier.modifier_effect)


class Tech:
    COMPONENT_SIZE = 20
    NUM_OF_COMPONENTS = 5

    def __init__(self, tech_id, tech_name, short_name, tech_category, requirements, components, effects):
        self.tech_id = tech_id
        self.name = tech_name
        self.short_name = short_name
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
        return 0
            
    def get_deactivated_tech(self):
        deactivated_tech = []
        for effect in self.effects:
            if effect.type == "deactivate":
                deactivated_tech.append(int(effect.which))
        return deactivated_tech
    
    def calculate_component_difficulty_multiplier(self, component_index, research_speed_modifier, game_difficulty, total_extra_bonus):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[component_index].difficulty + 2) / 200)
        return calculate_components_difficulty_multiplier(self.components[component_index], research_speed_modifier, game_difficulty, total_extra_bonus)
    
    def calculate_current_difficulty_multiplier(self, research_speed_modifier, game_difficulty, total_extra_bonus):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[self.current_component].difficulty + 2) / 9)
        return self.calculate_component_difficulty_multiplier(self.current_component, research_speed_modifier, game_difficulty, total_extra_bonus)


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
    
    def format_name_and_country(self):
        return f"[{self.nation}] {self.name}"
    
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
    
    def calculate_1_day_progress_for_component(
            self,
            component,
            research_speed_modifier,
            game_difficulty,
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0
            ):
        has_speciality = 0
        component_type = component.type
        if component_type in self.specialities:
            has_speciality = 1
        difficulty_modifier = calculate_components_difficulty_multiplier(
            component,
            research_speed_modifier,
            game_difficulty,
            total_extra_bonus
            )
        skill_issue = 0.1 * (self.skill + 6) * (has_speciality + 1)
        if component_type == "rocketry":
            skill_issue += num_of_rocket_sites
        if component_type == "nuclear_physics" or component_type == "nuclear_engineering":
            skill_issue += math.sqrt(reactor_size)
        return 0.01 * RESEARCH_SPEED_CONSTANT * skill_issue * ((BLUEPRINT_BONUS - 1) * has_blueprint + 1) * difficulty_modifier

    def calculate_how_many_days_to_complete(
            self,
            tech,
            research_speed_modifier,
            game_difficulty,
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0
            ):
        days_gone = 0
        for component in tech.components:
            daily_progress = self.calculate_1_day_progress_for_component(
                component,
                research_speed_modifier,
                game_difficulty,
                total_extra_bonus,
                has_blueprint,
                num_of_rocket_sites,
                reactor_size)
            days_to_complete_component = math.ceil(20 / daily_progress)
            days_gone += days_to_complete_component
        return days_gone
    
    def calculate_1_day_progress_for_tech(
            self,
            tech,
            research_speed_modifier,
            game_difficulty,
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0
            ):
        return self.calculate_1_day_progress_for_component(
            tech.components[tech.current_component],
            research_speed_modifier,
            game_difficulty,
            total_extra_bonus,
            has_blueprint,
            num_of_rocket_sites,
            reactor_size)


class MinisterOrIdea:
    def __init__(self, name, position, modifiers):
        self.name = name
        self.position = position
        self.modifiers = modifiers

    def get_research_bonus(self):
        research_bonus_dict = dict()
        for modifier in self.modifiers:
            if (effect := get_modifiers_tech_effects(modifier)):
            # category, value = get_modifiers_tech_effects(modifier)
                category, value = effect
                category = category if category else "all"
                if research_bonus_dict.get(category) is None:
                    research_bonus_dict[category] = value
                    continue
                research_bonus_dict[category] += value
        return research_bonus_dict


class MinisterPersonality(MinisterOrIdea):
    def __init__(self, *args):
        super().__init__(*args)

    # def get_research_bonus(self):
    #     research_bonus_dict = dict()
    #     for modifier in self.modifiers:
    #         category, value = get_modifiers_tech_effects(modifier)
    #         category = category if category else "all"
    #         if research_bonus_dict.get(category) is None:
    #             research_bonus_dict[category] = value
    #             continue
    #         research_bonus_dict[category] += value
    #     return research_bonus_dict


def get_minister_personality(minister_personalities, personality_str, position="all"):
    for personality in minister_personalities:
        if personality.name.lower() == personality_str.lower() and personality.position == "all":
            return personality
        if personality.name.lower() == personality_str.lower() and personality.position == position:
            return personality
        if personality.name.lower() == personality_str.lower():
            print("Match for", personality.name, "but", personality.position, "!=", position)
            return personality
    else:
        print(f"Minister personality {personality_str} not found")


class Minister:
    # def get_modifiers(self):
    #     modifiers = []

    #     return modifiers

    def __init__(self, minister_id, name, position, personality, start_year, ideology, loyalty, pic_path=None):
        self.m_id = minister_id
        self.name = name
        self.position = position
        self.personality = personality
        self.start_year = start_year
        self.ideology = ideology
        self.loyalty = loyalty
        self.pic_path = pic_path
        if self.pic_path is None:
            self.pic_path = "gfx/interface/pics/Unknown.bmp"
        # self.modifiers = self.get_modifiers()
    
    def get_research_bonus(self):
        if self.personality is None:
            return dict()
        return self.personality.get_research_bonus()


class Idea(MinisterOrIdea):
    def __init__(self, *args, gov_types=None):
        super().__init__(*args)
        self.gov_types = gov_types if gov_types else []

    # def get_research_bonus(self):
    #     research_bonus_dict = dict()
    #     for modifier in self.modifiers:
    #         category, value = get_modifiers_tech_effects(modifier)
    #         category = category if category else "all"
    #         if research_bonus_dict.get(category) is None:
    #             research_bonus_dict[category] = value
    #             continue
    #         research_bonus_dict[category] += value
    #     return research_bonus_dict

# class NationalIdentity(Idea):
#     pass

# class SocialPolicy(Idea):
#     pass

# class NationalCulture(Idea):
#     pass
