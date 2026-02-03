
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
    NUM_OF_DECIMALS = 6

    def __init__(self, team_id, team_name, team_nation, skill, start_year, end_year, specialities, filepath, pic_path=None):
        self.team_id = team_id
        self.name = team_name
        # TODO: changes needed
        self.nation = team_nation
        self.country = team_nation
        self.skill = max(min(skill, self.MAX_SKILL), self.MIN_SKILL)
        self.start_year = start_year
        self.end_year = end_year
        self.specialities = specialities
        self.filepath = filepath
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
        daily_progress = round(daily_progress, self.NUM_OF_DECIMALS)
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
            daily_progress = round(daily_progress, self.NUM_OF_DECIMALS)
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
            one_day_progress = round(one_day_progress, self.NUM_OF_DECIMALS)
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

    def __init__(self, minister_id, name, country_code, position, personality, start_year, ideology, loyalty, filepath, pic_path=None):
        self.m_id = minister_id
        self.name = name
        self.country_code = country_code
        self.country = country_code
        self.position = position
        self.personality = personality
        self.start_year = start_year
        self.ideology = ideology
        self.loyalty = loyalty
        self.filepath = filepath
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


class Leader:
    # from hoi2.paradoxwikis.com/Leader_Traits
    trait_list = [
        "Logistics Wizard",
        "Defensive Doctrine",
        "Offensive Doctrine",
        "Winter Specialist",
        "Trickster",
        "Engineer",
        "Fortress Buster",
        "Panzer Leader",
        "Commando",
        "Old Guard",
        "Sea Wolf",
        "Blockade Runner",
        "Superior Tactician",
        "Spotter",
        "Tank Buster",
        "Carpet Bomber",
        "Night Flyer",
        "Fleet Destroyer",
        "Desert Fox",
        "Jungle Rat",
        "Urban Warfare Specialist",
        "Ranger",
        "Mountaineer",
        "Hills Fighter",
        "Counter Attacker",
        "Assaulter",
        "Encircler",
        "Ambusher",
        "Disciplined",
        "Elastic Defence Specialist",
        "Blitzer"
    ]
    
    def get_traits_from_trait_num(self, trait_num):
        if trait_num == 0:
            return []
        trait_indices = []
        num_to_divide = trait_num
        index_exponent = 4 * len(str(trait_num))
        while num_to_divide >= 1:
            divider = pow(2, index_exponent)
            if divider <= num_to_divide:
                trait_indices.append(index_exponent)
                num_to_divide -= divider
            index_exponent -= 1
        return tuple([self.trait_list[i] for i in trait_indices[::-1]])

    def __init__(self, leader_id, name, filepath, country_code, skill, max_skill, trait_num, l_n_or_a, start_year, end_year, loyalty, exp, ideal_rank, r3_year, r2_year, r1_year, r0_year, pic_path=None):
        self.leader_id = leader_id
        self.name = name
        self.filepath = filepath
        self.country_code = country_code
        # TODO: change
        self.country = country_code
        self.skill = skill
        self.max_skill = max_skill
        try:
            self.traits = self.get_traits_from_trait_num(trait_num)
        except TypeError as e:
            self.traits = []
            print("TypeError detected with trait_num:")
            print(f"{leader_id=}")
            print(f"{name=}")
            print(f"{country_code=}")
            print(f"{trait_num=}")
            raise TypeError(e)
        self.land_naval_or_air = l_n_or_a
        self.start_year = start_year
        self.end_year = end_year
        self.loyalty = loyalty
        self.experience = exp
        self.ideal_rank = ideal_rank
        self.rank_years = [r0_year, r1_year, r2_year, r3_year]
        self.pic_path = pic_path
        if self.pic_path is None:
            self.pic_path = "gfx/interface/pics/Unknown.bmp"
    
    def print_leader_info(self):
        pass


class Model:
    MODEL_KEYS = (
        "airattack",
        "airdefence",
        "airdetectioncapability",
        "artillery_bombardment",
        "buildtime",
        "convoyattack",
        "cost",
        "defaultorganisation",
        "defensiveness",
        "distance",
        "fuelconsumption",
        "hardattack",
        "manpower",
        "max_oil_stock",
        "max_supply_stock",
        "maxspeed",
        "morale",
        "navalattack",
        "range",
        "seaattack",
        "seadefence",
        "shorebombardment",
        "softattack",
        "softness",
        "speed_cap_aa",
        "speed_cap_art",
        "speed_cap_at",
        "speed_cap_eng",
        "strategicattack",
        "subattack",
        "subdetectioncapability",
        "supplyconsumption",
        "suppression",
        "surfacedefence",
        "surfacedetectioncapability",
        "toughness",
        "transportcapability"
        "transportweight",
        "upgrade_cost_factor",
        "upgrade_time_factor",
        "visibility",
    )

    def __init__(self, model_dict):
        self.name = ""

        self.build_time = model_dict.get("buildtime")
        self.cost = model_dict["cost"]
        self.manpower = model_dict.get("manpower")
        self.upgrade_cost_factor = model_dict.get("upgrade_cost_factor")
        self.upgrade_time_factor = model_dict.get("upgrade_time_factor")
        
        self.fuel_consumption = model_dict.get("fuelconsumption")
        self.supply_consumption = model_dict.get("supplyconsumption")
        self.max_oil_stock = model_dict.get("max_oil_stock")
        self.max_supply_stock = model_dict.get("max_supply_stock")

        self.default_organization = model_dict.get("defaultorganisation")
        self.morale = model_dict.get("morale")

        self.air_attack = model_dict.get("airattack")
        self.air_defence = model_dict.get("airdefence")
        self.air_detection_capability = model_dict.get("airdetectioncapability")
        self.artillery_bombardment = model_dict.get("artillery_bombardment")
        self.convoy_attack = model_dict.get("convoyattack")
        self.defensiveness = model_dict.get("defensiveness")
        self.distance = model_dict.get("distance")
        self.hard_attack = model_dict.get("hardattack")
        self.max_speed = model_dict.get("maxspeed")
        self.naval_attack = model_dict.get("navalattack")
        self.range = model_dict.get("range")
        self.sea_attack = model_dict.get("seaattack")
        self.sea_defence = model_dict.get("seadefence")
        self.shore_bombardment = model_dict.get("shorebombardment")
        self.soft_attack = model_dict.get("softattack")
        self.softness = model_dict.get("softness")
        self.speed_cap_aa = model_dict.get("speed_cap_aa")
        self.speed_cap_art = model_dict.get("speed_cap_art")
        self.speed_cap_at = model_dict.get("speed_cap_at")
        self.speed_cap_eng = model_dict.get("speed_cap_eng")
        self.strategic_attack = model_dict.get("strategicattack")
        self.sub_attack = model_dict.get("subattack")
        self.sub_detection_capability = model_dict.get("subdetectioncapability")
        self.suppression = model_dict.get("suppression")
        self.surface_defence = model_dict.get("surfacedefence")
        self.surface_detection_capability = model_dict.get("surfacedetectioncapability")
        self.toughness = model_dict.get("toughness")
        self.transport_capability = model_dict.get("transportcapability")
        self.transport_weight = model_dict.get("transportweight")
        self.visibility = model_dict.get("visibility")
        

class Brigade:
    LAND_NAVAL_OR_AIR = (
        "land",
        "naval",
        "air"
    )

    DIVISION_NUMBERS = {
        "infantry": 0,
        "cavalry": 1,
        "motorized": 2,
        "mechanized": 3,
        "light_armor": 4,
        "armor": 5,
        "paratrooper": 6,
        "marine": 7,
        "bergsjaeger": 8,
        "garrison": 9,
        "hq": 10,
        "militia": 11,
        "multi_role": 12,
        "interceptor": 13,
        "strategic_bomber": 14,
        "tactical_bomber": 15,
        "naval_bomber": 16,
        "cas": 17,
        "transport_plane": 18,
        "flying_bomb": 19,
        "flying_rocket": 20,
        "battleship": 21,
        "light_cruiser": 22,
        "heavy_cruiser": 23,
        "battlecruiser": 24,
        "destroyer": 25,
        "carrier": 26,
        "escort_carrier": 27,
        "submarine": 28,
        "nuclear_submarine": 29,
        "transport": 30
    }

    BRIGADE_NUMBERS = {
        "artillery": 1,
        "sp_artillery": 2,
        "rocket_artillery": 3,
        "sp_rct_artillery": 4,
        "anti_tank": 5,
        "tank_destroyer": 6,
        "light_armor_brigade": 7,
        "heavy_armor": 8,
        "super_heavy_armor": 9,
        "armored_car": 10,
        "anti_air": 11,
        "police": 12,
        "engineer": 13,
        "cag": 14,
        "escort": 15,
        "naval_asw": 16,
        "naval_anti_air_s": 17,
        "naval_radar_s": 18,
        "naval_fire_controll_s": 19,
        "naval_improved_hull_s": 20,
        "naval_torpedoes_s": 21,
        "naval_anti_air_l": 22,
        "naval_radar_l": 23,
        "naval_fire_controll_l": 24,
        "naval_improved_hull_l": 25,
        "naval_torpedoes_l": 26,
        "naval_mines": 27,
        "naval_sa_l": 28,
        "naval_spotter_l": 29,
        "naval_spotter_s": 30,
        "b_u1": 31,
        "b_u2": 32,
        "b_u3": 33,
        "b_u4": 34,
        "b_u5": 35,
        "b_u6": 36,
        "b_u7": 37,
        "b_u8": 38,
        "b_u9": 39,
        "b_u10": 40,
        "b_u11": 41,
        "b_u12": 42,
        "b_u13": 43,
        "b_u14": 44
    }

    def get_unit_name(self, unit_key, text_dict, do_short=True):
        if unit_key == "none":
            return
        if not do_short:
            exceptions = {
                "anti_air": "NAME_ANTIAIR",
                "anti_tank": "NAME_ANTITANK",
                "light_armor_brigade": "NAME_LIGHT_ARMOR_BRI",
                "sp_rct_artillery": "NAME_SP_ROCKET_ARTILLERY",
                "land": "WHICH_TYPE_LAND",
                "air": "WHICH_TYPE_AIR",
                "naval": "WHICH_TYPE_NAVAL"
            }
            the_key = exceptions.get(unit_key)
            if the_key is None:
                the_key = f"NAME_{unit_key.upper()}"
            if text_dict.get(the_key) is None:
                print(f"no name found corresponding to {unit_key}")
                return unit_key
            return text_dict[the_key]
        exceptions = {
            "anti_air": "SNAME_ANTIAIR",
            "anti_tank": "SNAME_ANTITANK",
            "light_armor_brigade": "SNAME_LIGHT_ARMOR_BRI",
            "sp_rct_artillery": "SNAME_SP_ROCKET_ARTILLERY",
            "land": "WHICH_TYPE_LAND",
            "air": "WHICH_TYPE_AIR",
            "naval": "WHICH_TYPE_NAVAL"
        }
        the_key = exceptions.get(unit_key)
        if the_key is None:
            the_key = f"SNAME_{unit_key.upper()}"
        if text_dict.get(the_key) is None:
            print(f"No name found corresponding to {unit_key}")
            return unit_key
        return text_dict[the_key]

    def get_model_name(self, unit_key, model_num, text_dict):
        if unit_key == "none":
            return
        try:
            model_key = f"MODEL_{self.DIVISION_NUMBERS[unit_key.lower()]}_{model_num}"
        except KeyError:
            try:
                model_key = f"BRIG_MODEL_{self.BRIGADE_NUMBERS[unit_key.lower()]}_{model_num}"
            except KeyError:
                print(f"No model name found corresponding to {unit_key} model {model_num}")
                return f"{unit_key} {model_num}"
        
        return text_dict[model_key]


    def __init__(self, filepath, land_naval_or_air, models, locked=None, text_dict=None):
        self.filepath = filepath
        self.name_key = filepath.stem
        if text_dict:
            self.name = self.get_unit_name(self.name_key, text_dict, do_short=False)
            self.short_name = self.get_unit_name(self.name_key, text_dict, do_short=True)
        
        self.unit_type = land_naval_or_air
        
        self.locked = True if locked else False

        self.models = []
        for i, model in enumerate(models):
            if text_dict:
                model.name = self.get_model_name(self.name_key, i, text_dict)
            self.models.append(model)

class Division(Brigade):

    def __init__(self, filepath, land_naval_or_air, models, allowed_brigades=None, max_speed_step=None, text_dict=None):
        super().__init__(filepath, land_naval_or_air, models, text_dict=text_dict)

        self.max_speed_step = max_speed_step

        self.allowed_brigades = allowed_brigades
        if self.allowed_brigades is None:
            self.allowed_brigades = []


class UnitModifiers:
    pass
