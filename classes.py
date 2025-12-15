
from collections import namedtuple
import math

from read_hoi_files import get_blueprint_bonus_and_tech_speed_modifier, read_difficulty_file

# should this be read from game files?
# RESEARCH_SPEED_CONSTANT = 2.8
# BLUEPRINT_BONUS = 1.7
BLUEPRINT_BONUS, RESEARCH_SPEED_CONSTANT = get_blueprint_bonus_and_tech_speed_modifier()

# GameConstants = namedtuple("GameConstants", ["speed_modifier", "blueprint_bonus"])
Component = namedtuple("Component", ["type", "difficulty"])
EFFECT_ATTRIBUTES = ["type", "which", "value", "when", "where"]
Effect = namedtuple("Effect", EFFECT_ATTRIBUTES)
MODIFIER_ATTRIBUTES = ["type", "value", "option", "extra", "modifier_effect"]
Modifier = namedtuple("Modifier", MODIFIER_ATTRIBUTES)

INDENT_SPACES = 2


class GameConstants:
    # is difficulty needed here?
    DEFAULT_DIFFICULTY = "EASY"

    def overwrite_difficulty_modifier(self, difficulty_modifier):
        self.current_difficulty = difficulty_modifier

    def __init__(self, research_speed_constant=None, blueprint_bonus=None, difficulty_modifiers=None, current_difficulty=None, current_difficulty_string=None) -> None:
        if research_speed_constant is None or blueprint_bonus is None:
            blueprint_bonus, research_speed_constant = get_blueprint_bonus_and_tech_speed_modifier()
        self.research_speed_constant = research_speed_constant
        self.blueprint_bonus = blueprint_bonus
        # you can overwrite difficulty modifier
        if current_difficulty is not None:
            self.overwrite_difficulty_modifier(current_difficulty)
            return
        if difficulty_modifiers is None:
            difficulty_modifiers = read_difficulty_file()
        self.difficulty_modifiers = difficulty_modifiers
        if current_difficulty_string is None:
            current_difficulty_string = self.DEFAULT_DIFFICULTY
        self.current_difficulty_string = current_difficulty_string
        self.current_difficulty = self.difficulty_modifiers[self.current_difficulty_string]
        
    
    def change_difficulty(self, difficulty_string):
        self.current_difficulty_string = difficulty_string
        self.current_difficulty = self.difficulty_modifiers[self.current_difficulty_string]
    
    def get_research_multiplier(self, has_blueprint):
        return round(0.01 * self.research_speed_constant * ((self.blueprint_bonus - 1) * has_blueprint + 1), 4)


class HoITime:
    # day 0 = 1.1.1933
    DEFAULT_START_YEAR = 1933
    DEFAULT_START_DAY = 30
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    DAYS_IN_MONTH = 30
    DAYS_IN_YEAR = len(MONTHS) * DAYS_IN_MONTH

    def __init__(self, date=DEFAULT_START_DAY, **kwargs):
        self.date = date

    def reset_date(self):
        self.date = self.DEFAULT_START_DAY

    def get_year(self, date=None):
        date = self.date if date is None else date
        return self.DEFAULT_START_YEAR + date // self.DAYS_IN_YEAR
    
    # HH:MM month day, year -> date
    def date_str_to_date(self, date_str):
        _, month, day0, year = date_str.split(" ")
        day = int(day0.strip(","))
        year = int(year)
        month_num = self.MONTHS.index(month[:3])
        return (year - self.DEFAULT_START_YEAR) * self.DAYS_IN_YEAR + month_num * self.DAYS_IN_MONTH + day - 1
    
    def date_to_date_str(self, date):
        year = self.get_year(date)
        month = self.MONTHS[date // self.DAYS_IN_MONTH % len(self.MONTHS)]
        day = date % self.DAYS_IN_MONTH + 1
        return f"{day} {month} {year}"
    
    def get_date(self):
        return self.date_to_date_str(self.date)
    
    def change_year(self, new_year):
        self.date += (new_year - self.get_year()) * self.DAYS_IN_YEAR
    
    def next_day(self):
        self.date += 1


class TriggerConditions:

    def __init__(self, conditions):
        pass

    def print_conditions(self):
        pass


class Trigger:
    indent = INDENT_SPACES

    def __init__(self, trigger_dict):
        self.conditions = trigger_dict

    def print_trigger(self, indent_num=indent, empty_trigger=True):
        if not self.conditions and empty_trigger:
            print(indent_num * " ", "-")
            return
        if not self.conditions:
            return
        if isinstance(self.conditions, dict):
            for key, item in self.conditions.items():
                if key.upper() in ["NOT", "AND", "OR"]:
                    print(indent_num * " ", key.upper())
                    indent_num += self.indent
                    if isinstance(item, dict):
                        for k, it in item.items():
                            print(indent_num * " ", k, "=", it)
                    elif isinstance(item, list):
                        for it in item:
                            print(indent_num * " ", it)
                    indent_num -= self.indent
                    continue
                print(indent_num * " ", key, "=", item)
            return
        if isinstance(self.conditions, list):
            for item in self.conditions:
                print(indent_num * " ", item)
            return
        print(f"PROBLEM: trigger is of type {type(self.conditions)}")


class Action:
    indent = INDENT_SPACES

    def __init__(self, action_key, name_key, name="", ai_chance=None, effects=None):
        self.action_key = action_key
        self.name_key = name_key
        self.name = name

        self.ai_chance = ai_chance

        effects = [] if not effects else effects
        if isinstance(effects, dict):
            effects = [effects]
        self.effects = []
        for effect in effects:
            self.effects.append(Effect(effect.get("type"), effect.get("which"), effect.get("value"), effect.get("when"), effect.get("where")))
        
    def __str__(self):
        return f"{self.action_key}: {self.name}"
    
    def print_action(self, ordinal=1, indent_num=indent):
        print(indent_num * " ", f"{ordinal}.", self.name)
        indent_num += self.indent
        if self.ai_chance is not None:
            print(indent_num * " ", f"AI chance: {self.ai_chance} %")
        print(indent_num * " ", "Effects:")
        indent_num += self.indent
        if not self.effects:
            print(indent_num * " ", "-")
            return
        for effect in self.effects:
            text_parts = []
            type_part = f"type = {effect.type}" if effect.type is not None else ""
            text_parts.append(type_part)
            which_part = f"which = {effect.which}" if effect.which is not None else ""
            text_parts.append(which_part)
            value_part = f"value = {effect.value}" if effect.value is not None else ""
            text_parts.append(value_part)
            when_part = f"when = {effect.when}" if effect.when is not None else ""
            text_parts.append(when_part)
            where_part = f"where = {effect.where}" if effect.where is not None else ""
            text_parts.append(where_part)
            text_parts = [t for t in text_parts if t]
            # effect_line = f"{type_part}, {which_part}, {value_part}, {when_part}, {where_part}"
            print(indent_num * " ", ", ".join(text_parts))


def get_actions(list_of_action_dicts, text_dict):
    actions = []
    key_to_action_key = "action_key"
    key_to_name_key = "name"
    key_to_ai_chance = "ai_chance"
    key_to_effects = "command"
    for action in list_of_action_dicts:
        action_key = action[key_to_action_key]
        name_key = action.get(key_to_name_key)
        name = text_dict.get(name_key)
        name = "" if name is None else name
        ai_chance = action.get(key_to_ai_chance)
        effects = action.get(key_to_effects)
        actions.append(Action(action_key, name_key, name, ai_chance, effects))
    return actions


# just some approximate value to use in time = difficulty / skill
def get_approx_difficulty(tech_difficulty, research_speed_modifier, total_extra_bonus):
    return (tech_difficulty + 2) * (1 - 0.01 * total_extra_bonus) / research_speed_modifier


def get_game_difficulty_multiplier(game_difficulty_modifier):
    return round(1 + 0.01 * game_difficulty_modifier, 4)


# not actually correct, but this should avoid dividing by zero
def get_policy_modifier(total_extra_bonus):
    extra_bonus = min(99.99, total_extra_bonus)
    return round(0.01 * (100 - extra_bonus), 4)


def get_tech_difficulty_modifier(component):
    return component.difficulty + 2


def get_components_difficulty_modifiers(component, game_difficulty_modifier, total_extra_bonus):
    return get_tech_difficulty_modifier(component), get_game_difficulty_multiplier(game_difficulty_modifier), get_policy_modifier(total_extra_bonus)


# 1 / base difficulty from the game, up to scaling
def calculate_components_difficulty_multiplier(component, research_speed_modifier, game_difficulty_modifier, total_extra_bonus):
    extra_bonus = min(99.99, total_extra_bonus)
    return min(200, max(1 , 100 * (1 + 0.01 * game_difficulty_modifier) * research_speed_modifier / (100 - extra_bonus) / (component.difficulty + 2) ))


def calculate_components_difficulty_multiplier_from_modifiers(research_speed_modifier, tech_difficulty_modifier, game_difficulty_multiplier, policy_modifier):
    return min(200, max(1, research_speed_modifier * game_difficulty_multiplier / tech_difficulty_modifier / policy_modifier))


def calculate_1_day_progress_from_multipliers(game_constants, skill_multiplier, difficulty_multiplier, has_blueprint):
    return game_constants.get_research_multiplier(has_blueprint) * skill_multiplier * difficulty_multiplier


def get_modifiers_tech_effects(modifier):
    if modifier.type == "tech_group_mod":
        return (modifier.value, modifier.modifier_effect)


class Tech:
    COMPONENT_SIZE = 20
    NUM_OF_COMPONENTS = 5

    def __init__(self, tech_id, tech_name, short_name, tech_category, requirements, components, effects, allows=None, deactivated_by=None, is_post_war=0):
        self.tech_id = tech_id
        self.name = tech_name
        self.short_name = short_name
        self.category = tech_category
        self.requirements = requirements
        self.components = components
        self.effects = effects
        self.allows = set() if allows is None else set(allows)
        self.deactivated_by = set() if deactivated_by is None else set(deactivated_by)
        self.is_post_war = is_post_war 
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
    
    def get_reactivated_tech(self):
        reactivated_tech = []
        for effect in self.effects:
            if effect.type == "activate":
                reactivated_tech.append(int(effect.which))
        return reactivated_tech
    
    def calculate_component_difficulty_multiplier(self, component_index, research_speed_modifier, game_difficulty, total_extra_bonus):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[component_index].difficulty + 2) / 200)
        return calculate_components_difficulty_multiplier(self.components[component_index], research_speed_modifier, game_difficulty, total_extra_bonus)
    
    def calculate_current_difficulty_multiplier(self, research_speed_modifier, game_difficulty, total_extra_bonus):
        # return max(1 / 20, 9 * research_speed_modifier / (self.components[self.current_component].difficulty + 2) / 9)
        return self.calculate_component_difficulty_multiplier(self.current_component, research_speed_modifier, game_difficulty, total_extra_bonus)


class TechTeam:
    MIN_SKILL = 1
    MAX_SKILL = 10

    def __init__(self, team_id, team_name, team_nation, skill, start_year, end_year, specialities, pic_path=None):
        self.team_id = team_id
        self.name = team_name
        self.nation = team_nation
        self.skill = max(min(skill, self.MAX_SKILL), self.MIN_SKILL)
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

    def get_num_of_specials(self, tech):
        specials = 0
        for comp in tech.components:
            if comp.type in self.specialities:
                specials += 1
        return specials
    
    def get_skill_multiplier_for_component(self, component, num_of_rocket_sites=0, reactor_size=0, has_money=1):
        has_speciality = 0
        if component.type in self.specialities:
            has_speciality = 1
        skill_issue = 0.1 * (self.skill * has_money + 6) * (has_speciality + 1)
        if component.type == "rocketry":
            skill_issue += num_of_rocket_sites
        if component.type == "nuclear_physics" or component.type == "nuclear_engineering":
            skill_issue += math.sqrt(reactor_size)
        return skill_issue
    
    def calculate_approx_time_comparison_to_complete_tech(
            self, 
            tech, 
            research_speed_modifier,
            total_extra_bonus=0, 
            has_blueprint=0,
            has_money=1):
        num_of_specials = self.get_num_of_specials(tech)
        # difficulty_multiplier = tech.components[0].difficulty + 2
        difficulty_multiplier = get_approx_difficulty(tech.components[0].difficulty, research_speed_modifier, total_extra_bonus)
        skill_multiplier = self.skill + 6 if has_money else 6
        return difficulty_multiplier * (10 - num_of_specials)  / skill_multiplier / (1 + (BLUEPRINT_BONUS - 1) * has_blueprint)

    def calculate_1_day_progress_for_component(
            self,
            component,
            research_speed_modifier,
            game_constants = GameConstants(),
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0,
            has_money = 1
            ):
        skill_issue = self.get_skill_multiplier_for_component(component, num_of_rocket_sites, reactor_size, has_money)
        difficulty_modifier = calculate_components_difficulty_multiplier(
            component,
            research_speed_modifier,
            game_constants.current_difficulty,
            total_extra_bonus
            )
        return 0.01 * game_constants.research_speed_constant * skill_issue * ((game_constants.blueprint_bonus - 1) * has_blueprint + 1) * difficulty_modifier

    def calculate_how_many_days_to_complete_component(
        self,
        component,
        research_speed_modifier,
        game_constants = GameConstants(),
        total_extra_bonus = 0,
        has_blueprint = 0,
        num_of_rocket_sites = 0,
        reactor_size = 0,
        has_money = 1
    ):
        daily_progress = self.calculate_1_day_progress_for_component(
                component,
                research_speed_modifier,
                game_constants,
                total_extra_bonus,
                has_blueprint,
                num_of_rocket_sites,
                reactor_size,
                has_money)
        return math.ceil(20 / daily_progress)

    def calculate_how_many_days_to_complete(
            self,
            tech,
            research_speed_modifier,
            game_constants = GameConstants(),
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0,
            has_money = 1
            ):
        days_gone = 0
        for component in tech.components:
            daily_progress = self.calculate_1_day_progress_for_component(
                component,
                research_speed_modifier,
                game_constants,
                total_extra_bonus,
                has_blueprint,
                num_of_rocket_sites,
                reactor_size,
                has_money)
            days_to_complete_component = math.ceil(20 / daily_progress)
            days_gone += days_to_complete_component
        return days_gone
    
    def calculate_1_day_progress_for_tech(
            self,
            tech,
            research_speed_modifier,
            game_constants = GameConstants(),
            total_extra_bonus = 0,
            has_blueprint=0,
            num_of_rocket_sites = 0,
            reactor_size = 0,
            has_money = 1
            ):
        return self.calculate_1_day_progress_for_component(
            tech.components[tech.current_component],
            research_speed_modifier,
            game_constants,
            total_extra_bonus,
            has_blueprint,
            num_of_rocket_sites,
            reactor_size,
            has_money)

    def calculate_detailed_completion_times_for_tech(self, tech, research_speed_modifier, game_constants=GameConstants(), total_extra_bonus=0, has_blueprint=0, num_of_rocket_sites=0, reactor_size=0, has_money=1):
        results = []
        for component in tech.components:
            component_result = []
            c_n_bp = game_constants.get_research_multiplier(has_blueprint)
            skill_issue = self.get_skill_multiplier_for_component(component, num_of_rocket_sites, reactor_size, has_money)
            tdm, gdm, pm = get_components_difficulty_modifiers(component, game_constants.current_difficulty, total_extra_bonus)
            difficulty_multiplier = calculate_components_difficulty_multiplier_from_modifiers(research_speed_modifier, tdm, gdm, pm)
            one_day_progress = calculate_1_day_progress_from_multipliers(game_constants, skill_issue, difficulty_multiplier, has_blueprint)
            days_to_complete_component = math.ceil(tech.COMPONENT_SIZE / one_day_progress)
            component_result.append(days_to_complete_component)

            lower_difficulty_multiplier = tech.COMPONENT_SIZE / (days_to_complete_component) / c_n_bp / skill_issue
            if lower_difficulty_multiplier < 1 or lower_difficulty_multiplier > 200:
                component_result.append(None)
            else:
                lower_research_speed = lower_difficulty_multiplier * tdm * pm / gdm
                rs = round(math.ceil(lower_research_speed * 10) * 0.1 - 0.1, 1)
                component_result.append((days_to_complete_component + 1, rs))
            if days_to_complete_component == 1:
                component_result.append(None)
                results.append(tuple(component_result))
                continue
            higher_difficulty_multiplier = tech.COMPONENT_SIZE / (days_to_complete_component - 1) / c_n_bp / skill_issue
            if higher_difficulty_multiplier > 200 or higher_difficulty_multiplier < 1:
                component_result.append(None)
                results.append(tuple(component_result))
                continue
            higher_research_speed = higher_difficulty_multiplier * tdm * pm / gdm
            rs = round(math.ceil(higher_research_speed * 10) * 0.1, 1)
            component_result.append((days_to_complete_component - 1, rs))
            results.append(tuple(component_result))
        return tuple(results)


class MinisterOrIdea:
    def __init__(self, name, public_name, position, modifiers):
        self.name = name
        self.public_name = public_name
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


def get_minister_personality(minister_personalities, personality_str, position="all", show_issues=False):
    if not personality_str:
        return
    for personality in minister_personalities:
        if (personality.name.lower() == personality_str.lower() or personality.public_name.lower() == personality_str.lower()) and personality.position == "all":
            return personality
        if (personality.name.lower() == personality_str.lower() or personality.public_name.lower() == personality_str.lower()) and personality.position == position:
            return personality
        if personality.name.lower() == personality_str.lower():
            if show_issues:
                print("Match for", personality.name, "but", personality.position, "!=", position)
            return personality
        if personality.public_name.lower() == personality_str.lower():
            if show_issues:
                print("Match for", personality.public_name, "but", personality.position, "!=", position)
            return personality
    else:
        if show_issues:
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


class Event:
    indent = INDENT_SPACES
    EVENT_KEYS = [
        "id",
        "random",
        "invention",
        "country",
        "trigger",
        "name",
        "desc",
        "style",
        "date",
        "offset",
        "deathdate",
        "persistent",
        "picture",
        "action_a",
        "action_b",
        "action_c",
        "action_d",
        "action_e"
    ]

    def __init__(
        self,
        filepath,
        event_id,
        name_key,
        name,
        actions,
        is_random=False,
        is_invention=False,
        country_code=None,
        country=None,
        trigger=None,
        desc_key=None,
        description="",
        style=0,
        picture="",
        date=None,
        offset=None,
        deathdate=None,
        is_persistent=False,
        notes="",
        triggered_by=None
    ):
        self.event_id = event_id
        self.filepath = filepath
        self.name_key = name_key
        self.name = name
        self.desc_key = desc_key
        self.description = description

        self.country_code = country_code
        self.country = country

        self.is_random = is_random
        self.is_invention = is_invention
        self.is_persistent = is_persistent

        self.trigger = trigger
        self.triggered_by = [] if triggered_by is None else triggered_by

        self.date = date
        self.offset = offset
        self.deathdate = deathdate

        self.actions = actions

        self.notes = notes

        self.style = style
        self.picture = picture
    
    # def set_triggered_by(self, trigger_event_id, trigger_action_key):
    #     self.triggered_by = (trigger_event_id, trigger_action_key)
    
    def __str__(self):
        return f"{self.event_id} [{self.country_code}]: {self.name}"

    def print_event(self, aod_path, indent_num=0):
        print(f"{indent_num * ' '} {self.event_id}: {self.name}")
        if self.country:
            print(f"{indent_num * ' '} Country: {self.country}")
        if self.is_invention:
            print(f"{indent_num * ' '} Invention event")
        if self.is_random:
            print(f"{indent_num * ' '} Random event")
        
        path_str = str(self.filepath)[len(str(aod_path)) + 1:]
        print(f"{indent_num * ' '} In file: {path_str}")

        print()
        print(indent_num * ' ', "Trigger:")
        trigger_empty = True
        if self.triggered_by:
            trigger_empty = False
            print((indent_num + self.indent) * " ", "Triggered by:")
            for trigger_event_id, trigger_action_key in self.triggered_by:
                print((indent_num + 2 * self.indent) * " ", f"event {trigger_event_id},", "action", trigger_action_key)
        self.trigger.print_trigger(indent_num=indent_num + self.indent, empty_trigger=trigger_empty)
        print()

        if self.date:
            print(indent_num * ' ', "Date:")
            print(indent_num * ' ', self.date["day"], self.date["month"], self.date["year"])
        if self.offset is not None:
            print(f"{indent_num * ' '} Offset: {self.offset}")
        if self.deathdate:
            print(indent_num * ' ', "Deathdate:")
            print(indent_num * ' ', event["deathdate"]["day"], event["deathdate"]["month"], event["deathdate"]["year"])
        
        if self.is_persistent:
            print(indent_num * ' ', "Persistent event")

        print()
        print(f"{indent_num * ' '} Description:")
        print(indent_num * ' ', self.description)

        print()
        print(indent_num * ' ', "Possible Actions:")
        for i, action in enumerate(self.actions):
            action.print_action(ordinal=i+1, indent_num=indent_num + self.indent)


def suggest_events_based_on_search_words(search_text, event_dict):
    try:
        event_id = int(search_text)
        if event_dict.get(event_id) is not None:
            return [event_dict[event_id]]
    except ValueError:
        pass
    search_text = search_text.lower()
    name_starts = []
    name_other = []
    desc_starts = []
    desc_other = []
    action_things = []
    for event_id, event in event_dict.items():
        if event.name.lower().startswith(search_text):
            name_starts.append(event)
            continue
        if search_text in event.name.lower():
            name_other.append(event)
            continue
        if event.description is None:
            continue
        if event.description.lower().startswith(search_text):
            desc_starts.append(event)
            continue
        if search_text in event.description.lower():
            desc_other.append(event)
            continue
        for action in event.actions:
            if not action.name:
                continue
            if search_text in action.name.lower():
                action_things.append(event)
                break
    suggestions = name_starts + name_other + desc_starts + desc_other + action_things
    
    return suggestions
