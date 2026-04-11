
from collections import Counter

from classes import Effect
from event import Condition

# Effect types (capitalization hopefully does not matter)
# aa_batteries
# abomb_production
# access
# activate
# activate_division
# activate_unit_type
# add_corps
# add_division
# add_prov_resource
# addcore
# ai
# ai_prepare_war
# air_attack
# air_defense
# air_detection
# alliance
# allow_building
# allow_convoy_escorts
# allow_dig_in
# ambush
# armamentminister
# army_detection
# assault
# attrition_mod
# belligerence
# blizzard_attack
# blizzard_defense
# blizzard_move
# breakthrough
# build_cost
# build_division
# build_time
# building_eff_mod
# building_prod_mod
# capital
# carrier_level
# change_policy
# chiefofair
# chiefofarmy
# chiefofnavy
# chiefofstaff
# civil_war
# clrflag
# coast_fort_eff
# construct
# control
# convoy
# convoy_def_eff
# convoy_prod_mod
# counterattack
# country
# damage_division
# deactivate
# defensiveness
# delay
# delete_unit
# desert_attack
# desert_defense
# desert_move
# disorg_division
# dissent
# domestic
# double_nuke_prod
# enable_task
# encirclement
# end_access
# end_guarantee
# end_mastery
# end_non_aggression
# end_puppet
# end_trades
# energypool
# escort_pool
# extra_tc
# foreignminister
# forest_defense
# fort_attack
# free_energy
# free_ic
# free_metal
# free_money
# free_oil
# free_rare_materials
# free_supplies
# frozen_attack
# frozen_defense
# frozen_move
# fuel_consumption
# gain_tech
# ground_def_eff
# guarantee
# hard_attack
# headofgovernment
# headofstate
# hill_attack
# hill_defense
# hill_move
# hq_supply_eff
# independence
# industrial_modifier
# industrial_multiplier
# info_may_cause
# inherit
# intelligence
# jungle_attack
# jungle_defense
# jungle_move
# land_fort_eff
# leave_alliance
# local_clrflag
# local_setflag
# make_puppet
# manpowerpool
# max_amphib_mod
# max_organization
# max_positioning
# max_reactor_size
# metalpool
# min_positioning
# ministerofintelligence
# ministerofsecurity
# money
# morale
# mountain_attack
# mountain_defense
# mountain_move
# muddy_move
# naval_attack
# naval_defense
# new_model
# night_attack
# night_defense
# night_move
# non_aggression
# nuclear_carrier
# nuke_damage
# oilpool
# paradrop_attack
# peace
# peacetime_ic_mod
# province_keypoints
# province_manpower
# province_revoltrisk
# radar_eff
# rain_attack
# rain_defense
# rain_move
# range
# rarematerialspool
# regime_falls
# relation
# relative_manpower
# remove_division
# removecore
# repair_mod
# research_mod
# research_sabotaged
# resource
# revolt
# river_attack
# sce_frequency
# scrap_model
# secedeprovince
# set_domestic
# set_leader_skill
# set_relation
# setflag
# shore_attack
# sleepevent
# sleepleader
# sleepminister
# sleepteam
# snow_attack
# snow_defense
# snow_move
# soft_attack
# speed
# steal_tech
# storm_attack
# storm_defense
# storm_move
# strategic_attack
# supplies
# supply_consumption
# supply_dist_mod
# surface_detection
# surprise
# swamp_attack
# swamp_defense
# swamp_move
# switch_allegiance
# tactical_withdrawal
# task_efficiency
# tc_mod
# tc_occupied_mod
# transport_pool
# trickleback_mod
# trigger
# urban_attack
# urban_defense
# urban_move
# visibility
# vp
# wakeleader
# waketeam
# war

RESOURCES_LIST = (
    "oil",
    "metal",
    "energy",
    "rare_materials",
    "supplies",
    # TODO: should money and manpower be in this list?
    "money",
    "manpower"
)

BUILDING_DICT = {
    "ic": "Industrial Capacity",
    "infrastructure": "Infrastructure",
    "flak": "Anti-Air",
    "nuclear_reactor": "Nuclear Reactor",
    "nuclear_power": "Nuclear Power plant",
    "synthetic_oil": "Synthetic Oil plant",
    "synthetic_rares": "Synthetic Material plant",
    "coastal_fort": "Coastal Fort",
    "land_fort": "Land Fort",
    "air_base": "Air Base",
    "naval_base": "Naval Base",
    "radar_station": "Radar Station",
    "rocket_test": "Rocket Test Site"
}

IDEOLOGY_DICT = {
    "FA": "CATEGORY_FASCIST",
    "ML": "CATEGORY_MARKET_LIBERAL",
    "PA": "CATEGORY_PATERNAL_AUTOCRAT",
    "NS": "CATEGORY_NATIONAL_SOCIALIST",
    "LE": "CATEGORY_LENINIST",
    "ST": "CATEGORY_STALINIST",
    "SD": "CATEGORY_SOCIAL_DEMOCRAT",
    "SC": "CATEGORY_SOCIAL_CONSERVATIVE",
    "SL": "CATEGORY_SOCIAL_LIBERAL",
    "LWR": "CATEGORY_LEFT_WING_RADICAL"
}

SLIDER_DICT = {
    "democratic": ["DOMNAME_DEM_L", "DOMNAME_DEM_R"],
    "political_left": ["DOMNAME_POL_L", "DOMNAME_POL_R"],
    "freedom": ["DOMNAME_FRE_L", "DOMNAME_FRE_R"],
    "free_market": ["DOMNAME_FRM_L", "DOMNAME_FRM_R"],
    "professional_army": ["DOMNAME_PRO_L", "DOMNAME_PRO_R"],
    "defense_lobby": ["DOMNAME_DEF_L", "DOMNAME_DEF_R"],
    "interventionism": ["DOMNAME_INT_L", "DOMNAME_INT_R"]
    }

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

def get_tech_category_name(category, text_dict):
    if "_" in category:
        category_str = "".join([i[0] for i in category.split("_")])
        the_key = f"TECH_{category_str.upper()}_NAME"
    # if "doctrine" in category:
    #     the_key = f"TECH_{category[0].upper()}D_NAME"
    else:
        the_key = f"TECH_{category.upper()}_NAME"
    return text_dict[the_key]

def get_resource_name(resource, text_dict):
    if resource == "supplies":
        the_key = "RESOURCE_SUPPLY"
    else:
        the_key = f"RESOURCE_{resource.upper()}"
    return text_dict[the_key]

def get_resources(num):
    resource_indices = []
    num_to_divide = num
    index_exponent = 4 * len(str(num))
    while num_to_divide >= 1:
        divider = pow(2, index_exponent)
        if divider <= num_to_divide:
            resource_indices.append(index_exponent)
            num_to_divide -= divider
        index_exponent -= 1
    return tuple([RESOURCES_LIST[i] for i in resource_indices[::-1]])

def get_unit_name(unit_key, text_dict, do_short=True):
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
    return text_dict[the_key]

def get_model_name(unit_key, model_num, text_dict):
    try:
        model_key = f"MODEL_{DIVISION_NUMBERS[unit_key.lower()]}_{model_num}"
    except KeyError:
        model_key = f"BRIG_MODEL_{BRIGADE_NUMBERS[unit_key.lower()]}_{model_num}"
    return text_dict[model_key]

def get_province(province_num, text_dict):
    province = text_dict.get(f"PROV{province_num}")
    if province is not None:
        return province
    return province_num

def get_country(country_code, text_dict):
    if isinstance(country_code, int):
        return country_code
    country = text_dict.get(country_code.upper())
    if country is not None:
        return country
    return country_code

def replace_string_and_number(original_text, replacement_text, replacement_number, percentage=False):
    pct = " %" if percentage else ""
    sign = "+" if replacement_number > 0 else ""
    return original_text.replace("%s", replacement_text).replace("%d", f"{sign}{replacement_number}{pct}")


def unit_stat_boosts_as_str(effect, text_dict, **kwargs):
    exceptions = {
        "defensiveness": "EE_GROUND_DEFENSE",
        "max_organization": "EE_MAX_ORG"
    }
    the_key = exceptions.get(effect.type)
    if the_key is None:
        the_key = f"EE_{effect.type.upper()}"
    unit_name = get_unit_name(effect.which, text_dict)
    sign = "+" if effect.value > 0 else ""
    when_part = effect.when if effect.when else ""
    on_upgrade = text_dict.get(f"EE_{when_part.upper()}")
    on_upgrade = on_upgrade if on_upgrade else ""
    return f"{unit_name}: {text_dict[the_key]} {sign}{effect.value} {on_upgrade}"

def unit_stat_pct_boost_as_str(effect, text_dict, **kwargs):
    the_key = f"EE_{effect.type.upper()}"
    unit_name = get_unit_name(effect.which, text_dict)
    sign = "+" if effect.value > 0 else ""
    when_part = effect.when if effect.when else ""
    on_upgrade = text_dict.get(f"EE_{when_part.upper()}")
    on_upgrade = on_upgrade if on_upgrade else ""
    return f"{unit_name}: {text_dict[the_key]} {sign}{effect.value} % {on_upgrade}"

def change_as_str(effect, text_dict, **kwargs):
    the_key = f"EE_{effect.type.upper()}"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def pct_change_as_str(effect, text_dict, **kwargs):
    the_key = f"EE_{effect.type.upper()}"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value} %")

def pct_change_as_str_w_plus(effect, text_dict, **kwargs):
    the_key = f"EE_{effect.type.upper()}"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%+.1f\\%%\\n", f"{sign}{effect.value} %")


def free_resources_as_str(effect, text_dict, **kwargs):
    exceptions = {
        "free_rare_materials": "EE_FREE_RAREMAT"
    }
    the_key = exceptions.get(effect.type)
    the_key = the_key if the_key else f"EE_{effect.type.upper()}"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%+.0f", f"{sign}{effect.value}")


def effect_as_str_default(effect, **kwargs):
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
    return ", ".join(text_parts)

def aa_batteries_as_str(effect, text_dict, **kwargs):
    the_key = "EE_AA_BATTERIES"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {sign}{effect.value}"

def abomb_production_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ABOMB_ALLOWED"
    return text_dict[the_key]

def access_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ACCESS"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def activate_as_str(effect, text_dict, tech_dict=None, **kwargs):
    if tech_dict is None:
        return
    the_key = "EE_ACTIVATE_TECH"
    return text_dict[the_key].replace("%s", f"{effect.which} {tech_dict[effect.which].name}")

def activate_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ACTIVATE_DIVISION"
    province = get_province(effect.where, text_dict)
    province = str(province) if isinstance(province, int) else f"{province} [{effect.where}]"
    # TODO: find out what this means (and what about effect.when)
    division_info = f"[type: {effect.which}, id: {effect.value}]"
    raw_text = text_dict[the_key].split("%s")
    return f"{raw_text[0]}{division_info}{raw_text[1]}{province}{raw_text[2]}"

def activate_unit_type_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ACTIVATE_UNIT_TYPE"
    unit_name = get_unit_name(effect.which, text_dict)
    return f"{text_dict[the_key]}: {unit_name}"

def add_corps_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADD_CORPS"
    corps_name = effect.which
    province = get_province(effect.where, text_dict)
    raw_text = text_dict[the_key].split("%s")
    bonus_text = f"value: {effect.value}, when: {effect.when}"
    return f"{raw_text[0]}{corps_name}{raw_text[1]}{province}{raw_text[2]} [{bonus_text}]"

def add_division_as_str(effect, text_dict, **kwargs):
    # TODO: THERE IS SOME WEIRDNESS WITH add_division
    the_key = "EE_ADD_DIVISION"
    unit_name = get_unit_name(effect.value, text_dict, False)
    division_name_text = ""
    if effect.which:
        division_name_text = f" [{effect.which}]"
    
    brigade_text = ""
    redo_brigade_text = False
    if effect.where is not None:
        try:
            brigade_name = get_unit_name(effect.where, text_dict)
            brigade_text = f" with {brigade_name}"
        except KeyError:
            redo_brigade_text = True
        except AttributeError:
            redo_brigade_text = True
    if redo_brigade_text:
        brigade_text = f" with UNKNOWN BRIGADE {effect.where}"
        
    if effect.when is not None:
        try:
            model_name = get_model_name(effect.value, effect.when, text_dict)
            model_text = f" [{model_name}{brigade_text}]"
        except KeyError:
            model_text = f" [UNKNOWN MODEL {effect.when}{brigade_text}]"
    else:
        model_text = f"[UNKNOWN MODEL{brigade_text}]"
    return f"{text_dict[the_key].replace("%s", unit_name)}{division_name_text}{model_text}"

def add_prov_resource_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADD_PROV_RESOURCE"
    resource = get_resource_name(effect.where, text_dict)
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    text = f"{raw_text[0]}{resource}{raw_text[1]}{province_text}{raw_text[2]}"
    return text.replace("%+.1f\\%%\\n", f"{sign}{effect.value}")

def addcore_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADDCORE"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return text_dict[the_key].replace("%s", f"{province_text} [{effect.which}]")

def ai_as_str(effect, text_dict, **kwargs):
    # TODO: is this it?
    return f"{effect.type.upper()}: {effect.which}"

def ai_prepare_war_as_str(effect, text_dict, **kwargs):
    # TODO: what does this do anyway?
    country = text_dict[effect.which.upper()]
    return f"AI prepares for war: {country}"

def alliance_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ALL"
    return text_dict[the_key].replace("%s", text_dict[effect.which.upper()])

def allow_building_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ALLOW_BUILDING"
    building_name = BUILDING_DICT.get(effect.which)
    building_name = building_name if building_name else f"{effect.which}*"
    return text_dict[the_key].replace("%s", building_name)

def allow_convoy_escorts_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ALLOW_CONVOY_ESCORTS"
    return text_dict[the_key]

def allow_dig_in_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ALLOW_DIG_IN"
    return text_dict[the_key]

def armamentminister_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_ARMMIN"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def army_detection_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ARMY_DETECTION"
    second_key = f"EE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value} %"

def belligerence_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_BELLIGERENCE"
    raw_text = text_dict[the_key].split("%s")
    if effect.which is None:
        country = "[Current country]"
    else:
        country = text_dict[effect.which.upper()]
    sign = "+" if effect.value > 0 else ""
    text = raw_text[0] + country + raw_text[1] + sign + raw_text[2]
    return text.replace("%.1f\\%%\\n", str(effect.value))

def build_cost_as_str(effect, text_dict, **kwargs):
    # RELATIVE ruins everything
    key1 = "EE_BUILD_COST"
    key2 = "T_IC"
    placeholder_text = f"%s: {text_dict[key1]} %d {text_dict[key2]}"
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(placeholder_text, unit_name, effect.value, True)

def build_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_BUILD_DIVISION"
    unit_name = get_unit_name(effect.which, text_dict)
    return text_dict[the_key].replace("%s", unit_name)

def build_time_as_str(effect, text_dict, **kwargs):
    key1 = "EE_BUILD_TIME"
    key2 = "T_DAYS"
    placeholder_text = f"%s: {text_dict[key1]} %d {text_dict[key2]}"
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(placeholder_text, unit_name, effect.value, True)

def building_eff_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_BUILDING_EFF_MOD"
    building_name = BUILDING_DICT[effect.which]
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", building_name).replace("%+.1f\\%%\\n", f"{sign}{effect.value} %")

def building_prod_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_BUILDING_PROD_MOD"
    some_text = text_dict[the_key].replace("%+.1f\\%%\\n", "%d %")
    building_name = BUILDING_DICT.get(effect.which)
    building_name = building_name if building_name else f"{effect.which}*"
    return replace_string_and_number(some_text, building_name, effect.value)

def capital_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CAPITAL"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return f"{text_dict[the_key].replace("%s", f"{effect.which} {province_text}")} (if possible)"

def carrier_level_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CARRIER_LEVEL"
    return f"{text_dict[the_key]}: {effect.value}"

def change_policy_as_str(effect, text_dict, current_value=None, **kwargs):
    the_key = "EE_DOMESTIC"
    extra_key = "EE_DOMESTIC_CURRENT"
    direction = 0 if effect.value > 0 else 1
    slider_key = SLIDER_DICT[effect.which][direction]
    current_value_str = "?" if current_value is None else str(current_value)
    part1 = text_dict[the_key].replace("%d", str(abs(effect.value))).replace("%s", text_dict[slider_key])
    part2 = text_dict[extra_key].replace("%d", current_value_str)
    return f"{part1} {part2}"

def chiefofair_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_CAIR"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def chiefofarmy_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_CARMY"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def chiefofnavy_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_CNAVY"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def chiefofstaff_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_STAFF"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def civil_war_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CIVIL_WAR"
    new_country = text_dict[effect.which.upper()]
    return f"{text_dict[the_key]} [opponent: {new_country}]"

def clrflag_as_str(effect, text_dict, **kwargs):
    return f"Clear flag [{effect.type}]: {effect.which}"

def coast_fort_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_COAST_FORT_EFF"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]}: {sign}{effect.value}"

def construct_as_str(effect, text_dict, **kwargs):
    province = get_province(effect.where, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.where}]"
    building_name = BUILDING_DICT.get(effect.which)
    building_name = building_name if building_name else f"{effect.which}*"
    sign = "+" if effect.value > 0 else ""
    return f"{building_name} in {province}: {sign}{effect.value}"

def control_as_str(effect, text_dict, **kwargs):
    # TODO: how is this different from secedeprovince?
    return f"{secedeprovince_as_str(effect, text_dict, **kwargs)} [control]"

def convoy_as_str(effect, text_dict, **kwargs):
    the_key = "EE_N_CONVOY"
    province_from = get_province(effect.which, text_dict)
    province_to = get_province(effect.value, text_dict)
    # TODO: how does effect.when translate to resources?
    resources = ", ".join(get_resource_name(res, text_dict) for res in get_resources(effect.when))
    raw_text = text_dict[the_key].split("%s")
    return f"{raw_text[0]}{resources}{raw_text[1]}{province_from}{raw_text[2]}{province_to}{raw_text[3]}"


def convoy_def_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CONVOY_DEF_EFF"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]}: {sign}{effect.value}"

def convoy_prod_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CONVOY_PROD_MOD"
    sign = "+" if effect.value > 0 else ""
    name = f"Convoy {effect.which.capitalize()}"
    return text_dict[the_key].replace("%s", name).replace("%+.1f\\%%\\n", f"{sign}{effect.value} %")

def country_as_str(effect, text_dict, **kwargs):
    the_key = "EE_TAG"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def damage_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_DAMAGE_DIVISION"
    raw_text = text_dict[the_key].replace("%s%d\\%%", "%d")
    # TODO: find out what this means
    the_unit_info = f"[type: {effect.which}, id: {effect.value}]"
    return replace_string_and_number(raw_text, the_unit_info, -effect.where, percentage=True)

def deactivate_as_str(effect, text_dict, tech_dict=None, **kwargs):
    if tech_dict is None:
        return
    the_key = "EE_DEACTIVATE_TECH"
    return f"{text_dict[the_key]}: \n  {effect.which} {tech_dict[effect.which].name}"

def delete_unit_as_str(effect, text_dict, **kwargs):
    the_key = "EE_DELETE_UNIT"
    # TODO: is there anything more to this?
    return text_dict[the_key].replace("%s", str(effect.which))

def disorg_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_DISORG_DIVISION"
    raw_text = text_dict[the_key].replace("%s%d\\%%", "%d")
    # TODO: is effect.which sufficient?
    return replace_string_and_number(raw_text, str(effect.which), -effect.where, percentage=True)

def domestic_change_as_str(effect, text_dict, current_value=None, **kwargs):
    the_key = "EE_DOMESTIC"
    extra_key = "EE_DOMESTIC_CURRENT"
    direction = 0 if effect.value > 0 else 1
    slider_key = SLIDER_DICT[effect.which][direction]
    current_value_str = "?" if current_value is None else str(current_value)
    part1 = text_dict[the_key].replace("%d", str(abs(effect.value))).replace("%s", text_dict[slider_key])
    part2 = text_dict[extra_key].replace("%d", current_value_str)
    return f"{part1} {part2}"

# almost the same?
def set_domestic_as_str(effect, text_dict, **kwargs):
    slider = text_dict[SLIDER_DICT[effect.which][0]]
    # the game does not seem to use this
    the_key = "EE_SET_DOMESTIC"
    return text_dict[the_key].replace("%s", slider).replace("%d", str(effect.value))

def double_nuke_prod_as_str(effect, text_dict, **kwargs):
    return text_dict["EE_NUKE_PROD"]

def enable_task_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ENABLE_TASK"
    exceptions = {
        "amphibious_assault": "MISSION_AMPHIBOUS_ASSAULT"
    }
    mission_key = exceptions.get(effect.which)
    mission_key = mission_key if mission_key else f"MISSION_{effect.which.upper()}"
    return text_dict[the_key].replace("%s", text_dict[mission_key])

def end_access_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_ACCESS"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def end_guarantee_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_GUARANTEE"
    raw_text = text_dict[the_key].split("%s")
    country1 = text_dict[effect.which.upper()]
    country2 = text_dict[effect.where.upper()]
    return f"{raw_text[0]}{country1}{raw_text[1]}{country2}{raw_text[2]}"

def end_mastery_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_MASTERY"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def end_non_aggression_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_NON_AGGRESSION"
    raw_text = text_dict[the_key]
    country1 = text_dict[effect.which.upper()]
    country2 = text_dict[effect.where.upper()]
    return f"{raw_text[0]}{country1}{raw_text[1]}{country2}{raw_text[2]}"

def end_puppet_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_PUPPET"
    return text_dict[the_key]

def end_trades_as_str(effect, text_dict, **kwargs):
    the_key = "EE_END_TRADES"
    raw_text = text_dict[the_key]
    country1 = text_dict[effect.which.upper()]
    country2 = text_dict[effect.where.upper()]
    return f"{raw_text[0]}{country1}{raw_text[1]}{country2}{raw_text[2]}"

def energypool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ENERGY_POOL"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def escort_pool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ESCORT_POOL"
    country = text_dict[effect.which.upper()]
    return replace_string_and_number(text_dict[the_key], country, effect.value)

def extra_tc_as_str(effect, text_dict, **kwargs):
    raw_text = change_as_str(effect, text_dict, **kwargs)
    return raw_text.replace("%s", "")

def foreignminister_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_FGNMIN"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def gain_tech_as_str(effect, text_dict, tech_dict=None, **kwargs):
    the_key = "EE_GAIN_TECH"
    the_tech = tech_dict.get(effect.which)
    if not the_tech:
        return text_dict[the_key].replace("'%s'", str(effect.which))
    return text_dict[the_key].replace("'%s'", f"{the_tech.tech_id} {the_tech.name}")

def ground_def_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_GROUND_DEF_EFF"
    return f"{text_dict[the_key]}: {effect.value}"

def guarantee_as_str(effect, text_dict, **kwargs):
    the_key = "EE_GUARANTEE"
    country1 = text_dict[effect.which.upper()]
    country2 = text_dict[effect.where.upper()]
    raw_text = text_dict[the_key].split("%s")
    return f"{raw_text[0]}{country1}{raw_text[1]}{country2}{raw_text[2]}"

def headofgovernment_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_HOG"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def headofstate_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_HOS"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def hq_supply_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_HQ_SUPPLY_EFF"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value} %")

def independence_as_str(effect, text_dict, **kwargs):
    # TODO: does effect.value do anything?
    the_key = "EE_INDY"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def industrial_modifier_as_str(effect, text_dict, **kwargs):
    the_key = "EE_INDUSTRIAL_MODIFIER"
    second_key = f"EE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value} %"

def industrial_multiplier_as_str(effect, text_dict, **kwargs):
    the_key = "EE_INDUSTRIAL_MULTIPLIER"
    second_key = f"EE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value}"

def info_may_cause_as_str(effect, text_dict, tech_dict=None, **kwargs):
    the_key = "EE_INFO_MAY_CAUSE"
    return text_dict[the_key].replace("'%s'", f"{effect.which} {tech_dict[effect.which].name}")

def inherit_as_str(effect, text_dict, **kwargs):
    the_key = "EE_INHERIT"
    return text_dict[the_key].replace("%s", text_dict[effect.which.upper()])

def intelligence_as_str(effect, text_dict, **kwargs):
    the_key = "EE_INTELLIGENCE"
    second_key = f"EE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value} %"

def land_fort_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_LAND_FORT_EFF"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]}: {sign}{effect.value}"

def leave_alliance_as_str(effect, text_dict, **kwargs):
    the_key = "EE_LEAVE_ALLIANCE"
    return text_dict[the_key]

def local_clrflag_as_str(effect, text_dict, **kwargs):
	return f"Clear flag [{effect.type}]: {effect.which}"

def local_setflag_as_str(effect, text_dict, **kwargs):
	return f"Set flag [{effect.type}]: {effect.which}"

def make_puppet_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MAKE_PUPPET"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def manpowerpool_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MANPOWER"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%d", str(effect.value))

def max_amphib_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MAX_AMPHIB_MOD"
    return text_dict[the_key].replace("%.0f\\n", str(effect.value))

def max_positioning_as_str(effect, text_dict, **kwargs):
    raw_text = text_dict["EE_MAX_POSITIONING"].replace("%+.1f\\%%\\n", "%d")
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(raw_text, unit_name, effect.value)

def max_reactor_size_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MAX_REACTOR_SIZE"
    return f"{text_dict[the_key]} {effect.value}"

def metalpool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_METAL_POOL"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def min_positioning_as_str(effect, text_dict, **kwargs):
    raw_text = text_dict["EE_MIN_POSITIONING"].replace("%+.1f\\%%\\n", "%d")
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(raw_text, unit_name, effect.value)

def ministerofintelligence_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_INTMIN"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def ministerofsecurity_as_str(effect, text_dict, minister_dict=None, **kwargs):
    the_key = "EE_SECMIN"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def money_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MONEY"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%+.1f", f"{sign}{effect.value}")

def new_model_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NEW_MODEL"
    unit_name = get_unit_name(effect.which, text_dict)
    model_name = get_model_name(effect.which, effect.value, text_dict)
    return f"{unit_name}: {text_dict[the_key]}: {model_name}"

def non_aggression_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NON_AGGRESSION"
    raw_text = text_dict[the_key]
    country1 = text_dict[effect.which.upper()]
    country2 = text_dict[effect.where.upper()]
    return f"{raw_text[0]}{country1}{raw_text[1]}{country2}{raw_text[2]}"

def nuclear_carrier_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NUCLEAR_CARRIER_NEW"
    unit_name = text_dict[f"NAME_{effect.which.upper()}"]
    return text_dict[the_key].replace("%s", unit_name)

def nuke_damage_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NUKE_DAMAGE"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("+", f"{sign}{effect.value} %")

def oilpool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_OIL_POOL"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def peace_as_str(effect, text_dict, **kwargs):
    # TODO: does effect.value do anything?
    the_key = "EE_PEACE"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)

def peacetime_ic_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_PEACETIME_IC_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%.1f\\%%", f"{effect.value} %")

def province_keypoints_as_str(effect, text_dict, **kwargs):
    the_key = "EE_KEYPOINTS"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return replace_string_and_number(text_dict[the_key], province_text, effect.value)

def province_manpower_as_str(effect, text_dict, **kwargs):
    the_key = "EE_P_MAN"
    sign = "+" if effect.value > 0 else ""
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return text_dict[the_key].replace("%s%d", f"{sign}{effect.value}").replace("%s", province_text)

def province_revoltrisk_as_str(effect, text_dict, **kwargs):
    the_key = "EE_P_RR"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return replace_string_and_number(text_dict[the_key].replace("%s%d", "%d"), province_text, effect.value)

def rarematerialspool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RARE_MATERIALS_POOL"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def regime_falls_as_str(effect, text_dict, **kwargs):
    the_key = "EE_REGIME_FALLS"
    return text_dict[the_key]

def relation_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RELATION"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    try:
        country = text_dict[effect.which.upper()]
    except AttributeError:
        country = f"[{effect.which}]"
    text = f"{raw_text[0]}{country}{raw_text[1]}{sign}{raw_text[2]}"
    return text.replace("%d", str(effect.value))

def relative_manpower_as_str(effect, text_dict, **kwargs):
    the_key = "DOMESTIC_PRA_MAN"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value} %")

def remove_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_REMOVE_DIVISION"
    # TODO: find out what this actually means
    the_unit_info = f"[type: {effect.which}, id: {effect.value}]"
    return text_dict[the_key].replace("%s", the_unit_info)

def removecore_as_str(effect, text_dict, **kwargs):
    the_key = "EE_REMCORE"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return text_dict[the_key].replace("%s", f"{province_text}")

def research_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RESEARCH_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value}")

def research_sabotaged_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RESEARCH_SABOTAGED"
    return text_dict[the_key]

def resource_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RESOURCE"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    resource = get_resource_name(effect.which, text_dict)
    text = f"{raw_text[0]}{resource}{raw_text[1]}{sign}{raw_text[2]}"
    return text.replace("%.1f\\%%", f"{effect.value} %")

def revolt_as_str(effect, text_dict, **kwargs):
    the_key = "EE_N_REVOLT"
    province = get_province(effect.which, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.which}]"
    return text_dict[the_key].replace("%s", province_text)

def sce_frequency_as_str(effect, text_dict, **kwargs):
    the_key = "EE_HQ_COMBAT_EVENT_CHANCE"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%+.1f\\n", f"{sign}{effect.value}")

def scrap_model_as_str(effect, text_dict, **kwargs):
    the_key = "EE_SCRAP_MODEL"
    unit_name = get_unit_name(effect.which, text_dict)
    model_name = get_model_name(effect.which, effect.value, text_dict)
    raw_text = text_dict[the_key].split("%s")
    return f"{raw_text[0]}{unit_name}{raw_text[1]}{model_name}{raw_text[2]}"

def secedeprovince_as_str(effect, text_dict, **kwargs):
    # TODO: how is this different from control?
    the_key = "EE_SECEDE"
    raw_text = text_dict[the_key].split("%s")
    province = get_province(effect.value, text_dict)
    province_text = str(province) if isinstance(province, int) else f"{province} [{effect.value}]"
    country = text_dict[effect.which.upper()]
    return f"{raw_text[0]}{province_text}{raw_text[1]}{country}{raw_text[2]} (if possible)"

def set_leader_skill_as_str(effect, text_dict, leader_dict=None, **kwargs):
    leader_id = effect.which
    if leader_dict:
        leader_name = leader_dict.get(leader_id).name if leader_dict.get(leader_id) else ""
    else:
        leader_name = ""
    new_skill = effect.value
    return f"Skill of leader {leader_name} [{leader_id}] is set to {new_skill}"

def set_relation_as_str(effect, text_dict, **kwargs):
    the_key = "EE_SET_RELATION"
    country = text_dict[effect.which.upper()]
    return replace_string_and_number(text_dict[the_key], country, effect.value)

def setflag_as_str(effect, text_dict, **kwargs):
    return f"Set flag [{effect.type}]: {effect.which}"

def sleepevent_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_SLEEP"
    try:
        the_event = event_dict[effect.which]
        raw_text = text_dict[the_key].replace("%s", the_event.name)
        # my own additions
        name_w_quotes = f"'{the_event.name}'"
        add = f" [{the_event.country} {effect.which}]"
        return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]
    except KeyError:
        return text_dict[the_key].replace("'%s' Event", f"Event {effect.which} [EVENT NOT FOUND]")
    

def sleepleader_as_str(effect, text_dict, leader_dict=None, **kwargs):
    the_key = "EE_SLEADER"
    leader_id = effect.which
    if leader_dict:
        leader_name = leader_dict.get(leader_id).name if leader_dict.get(leader_id) else ""
    else:
        leader_name = ""
    return text_dict[the_key].replace("%s", f"{leader_name} [{leader_id}]")

def sleepminister_as_str(effect, text_dict, minister_dict, **kwargs):
    the_key = "EE_SMINISTER"
    minister_id = effect.which
    if minister_dict:
        minister_name = minister_dict.get(minister_id).name if minister_dict.get(minister_id) else ""
    else:
        minister_name = ""
    return text_dict[the_key].replace("%s", f"{minister_name} [{minister_id}]")

def sleepteam_as_str(effect, text_dict, techteam_dict=None, **kwargs):
    the_key = "EE_STEAM"
    team_id = effect.which
    if techteam_dict:
        team_name = techteam_dict.get(team_id).name if techteam_dict.get(team_id) else ""
    else:
        team_name = ""
    return text_dict[the_key].replace("%s", f"{team_name} [{team_id}]")

def steal_tech_as_str(effect, text_dict, **kwargs):
    the_key = "EE_STEAL_TECH"
    country = str(effect.which)
    if not isinstance(effect.which, int):
        country = text_dict[effect.which.upper()]
    
    raw_text = text_dict[the_key].replace("'%s'", "?")
    return raw_text.replace("%s", country)

def supplies_as_str(effect, text_dict, **kwargs):
    the_key = "EE_SUPPLY_POOL"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%d", f"{sign}{effect.value}")

def surprise_as_str(effect, text_dict, **kwargs):
    the_key = "EE_SURPRISE"
    second_key = f"WHICH_TYPE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value} %"

def switch_allegiance_as_str(effect, text_dict, **kwargs):
    # TODO: is there something better?
    the_key = "EE_SWITCH_ALLEGIANCE"
    the_unit = effect.which
    country = text_dict[effect.where.upper()]
    raw_text = text_dict[the_key].split("%s")
    return f"{raw_text[0]}{the_unit}{raw_text[1]}{country}{raw_text[2]}"

def task_efficiency_as_str(effect, text_dict, **kwargs):
    the_key = "EE_TASK_EFFICIENCY"
    raw_text = text_dict[the_key].replace("%+.1f\\%%\\n", "%d")
    exceptions = {
        "amphibious_assault": "MISSION_AMPHIBOUS_ASSAULT"
    }
    mission_key = exceptions.get(effect.which)
    mission_key = mission_key if mission_key else f"MISSION_{effect.which.upper()}"
    return replace_string_and_number(raw_text, text_dict[mission_key], effect.value)

def transport_pool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_TRANSPORT_POOL"
    country = text_dict[effect.which.upper()]
    return replace_string_and_number(text_dict[the_key], country, effect.value)

def trigger_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_TRIGGER"
    try:
        the_event = event_dict[effect.which]
        raw_text = text_dict[the_key].replace("%s", the_event.name)
        # my own additions
        name_w_quotes = f"'{the_event.name}'"
        add = f" [{the_event.country} {effect.which}]"
        return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]
    except KeyError:
        return text_dict[the_key].replace("'%s' Event", f"Event {effect.which} [EVENT NOT FOUND]")

def vp_as_str(effect, text_dict, **kwargs):
    the_key = "EE_VP"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%d", f"{sign}{effect.value}")

def wakeleader_as_str(effect, text_dict, leader_dict=None, **kwargs):
    the_key = "EE_WAKE_LEADER"
    leader_id = effect.which
    if leader_dict:
        leader_name = leader_dict.get(leader_id).name if leader_dict.get(leader_id) else ""
    else:
        leader_name = ""
    return text_dict[the_key].replace("%s", f"{leader_name} [{leader_id}]")

def waketeam_as_str(effect, text_dict, techteam_dict, **kwargs):
    the_key = "EE_WTEAM"
    team_id = effect.which
    if techteam_dict:
        team_name = techteam_dict.get(team_id).name if techteam_dict.get(team_id) else ""
    else:
        team_name = ""
    return text_dict[the_key].replace("%s", f"{team_name} [{team_id}]")

def war_as_str(effect, text_dict, **kwargs):
    the_key = "EE_WAR"
    country = text_dict[effect.which.upper()]
    return text_dict[the_key].replace("%s", country)


STR_FUNCTION_DICT_FOR_EFFECTS = {
    "aa_batteries": aa_batteries_as_str,
    "abomb_production": abomb_production_as_str,
    "access": access_as_str,
    "activate": activate_as_str,
    "activate_division": activate_division_as_str,
    "activate_unit_type": activate_unit_type_as_str,
    "add_corps": add_corps_as_str,
    "add_division": add_division_as_str,
    "add_prov_resource": add_prov_resource_as_str,
    "addcore": addcore_as_str,
    "ai": ai_as_str,
    "ai_prepare_war": ai_prepare_war_as_str,
    "air_attack": unit_stat_boosts_as_str,
    "air_defense": unit_stat_boosts_as_str,
    "air_detection": unit_stat_boosts_as_str,
    "alliance": alliance_as_str,
    "allow_building": allow_building_as_str,
    "allow_convoy_escorts": allow_convoy_escorts_as_str,
    "allow_dig_in": allow_dig_in_as_str,
    "ambush": pct_change_as_str,
    "armamentminister": armamentminister_as_str,
    "army_detection": army_detection_as_str,
    "assault": pct_change_as_str,
    "attrition_mod": pct_change_as_str,
    "belligerence": belligerence_change_as_str,
    "blizzard_attack": unit_stat_pct_boost_as_str,
    "blizzard_defense": unit_stat_pct_boost_as_str,
    "blizzard_move": unit_stat_pct_boost_as_str,
    "breakthrough": pct_change_as_str,
    "build_cost": build_cost_as_str,
    "build_division": build_division_as_str,
    "build_time": build_time_as_str,
    "building_eff_mod": building_eff_mod_as_str,
    "building_prod_mod": building_prod_mod_as_str,
    "capital": capital_as_str,
    "carrier_level": carrier_level_as_str,
    "change_policy": change_policy_as_str,
    "chiefofair": chiefofair_as_str,
    "chiefofarmy": chiefofarmy_as_str,
    "chiefofnavy": chiefofnavy_as_str,
    "chiefofstaff": chiefofstaff_as_str,
    "civil_war": civil_war_as_str,
    "clrflag": clrflag_as_str,
    "coast_fort_eff": coast_fort_eff_as_str,
    "construct": construct_as_str,
    "control": control_as_str,
    "convoy": convoy_as_str,
    "convoy_def_eff": convoy_def_eff_as_str,
    "convoy_prod_mod": convoy_prod_mod_as_str,
    "counterattack": pct_change_as_str,
    "country": country_as_str,
    "damage_division": damage_division_as_str,
    "deactivate": deactivate_as_str,
    "defensiveness": unit_stat_boosts_as_str,
    "delay": pct_change_as_str,
    "delete_unit": delete_unit_as_str,
    "desert_attack": unit_stat_pct_boost_as_str,
    "desert_defense": unit_stat_pct_boost_as_str,
    "desert_move": unit_stat_pct_boost_as_str,
    "disorg_division": disorg_division_as_str,
    "dissent": change_as_str,
    "domestic": domestic_change_as_str,
    "double_nuke_prod": double_nuke_prod_as_str,
    "enable_task": enable_task_as_str,
    "encirclement": pct_change_as_str,
    "end_access": end_access_as_str,
    "end_guarantee": end_guarantee_as_str,
    "end_mastery": end_mastery_as_str,
    "end_non_aggression": end_non_aggression_as_str,
    "end_puppet": end_puppet_as_str,
    "end_trades": end_trades_as_str,
    "energypool": energypool_as_str,
    "escort_pool": escort_pool_as_str,
    "extra_tc": extra_tc_as_str,
    "foreignminister": foreignminister_as_str,
    "forest_defense": unit_stat_pct_boost_as_str,
    "fort_attack": unit_stat_pct_boost_as_str,
    "free_energy": free_resources_as_str,
    "free_ic": free_resources_as_str,
    "free_metal": free_resources_as_str,
    "free_money": free_resources_as_str,
    "free_oil": free_resources_as_str,
    "free_rare_materials": free_resources_as_str,
    "free_supplies": free_resources_as_str,
    "frozen_attack": unit_stat_pct_boost_as_str,
    "frozen_defense": unit_stat_pct_boost_as_str,
    "frozen_move": unit_stat_pct_boost_as_str,
    "fuel_consumption": unit_stat_boosts_as_str,
    "gain_tech": gain_tech_as_str,
    "ground_def_eff": ground_def_eff_as_str,
    "guarantee": guarantee_as_str,
    "hard_attack": unit_stat_boosts_as_str,
    "headofgovernment": headofgovernment_as_str,
    "headofstate": headofstate_as_str,
    "hill_attack": unit_stat_pct_boost_as_str,
    "hill_defense": unit_stat_pct_boost_as_str,
    "hill_move": unit_stat_pct_boost_as_str,
    "hq_supply_eff": hq_supply_eff_as_str,
    "independence": independence_as_str,
    "industrial_modifier": industrial_modifier_as_str,
    "industrial_multiplier": industrial_multiplier_as_str,
    "info_may_cause": info_may_cause_as_str,
    "inherit": inherit_as_str,
    "intelligence": intelligence_as_str,
    "jungle_attack": unit_stat_pct_boost_as_str,
    "jungle_defense": unit_stat_pct_boost_as_str,
    "jungle_move": unit_stat_pct_boost_as_str,
    "land_fort_eff": land_fort_eff_as_str,
    "leave_alliance": leave_alliance_as_str,
    "local_clrflag": local_clrflag_as_str,
    "local_setflag": local_setflag_as_str,
    "make_puppet": make_puppet_as_str,
    "manpowerpool": manpowerpool_change_as_str,
    "max_amphib_mod": max_amphib_mod_as_str,
    "max_organization": unit_stat_boosts_as_str,
    "max_positioning": max_positioning_as_str,
    "max_reactor_size": max_reactor_size_as_str,
    "metalpool": metalpool_as_str,
    "min_positioning": min_positioning_as_str,
    "ministerofintelligence": ministerofintelligence_as_str,
    "ministerofsecurity": ministerofsecurity_as_str,
    "money": money_as_str,
    "morale": unit_stat_boosts_as_str,
    "mountain_attack": unit_stat_pct_boost_as_str,
    "mountain_defense": unit_stat_pct_boost_as_str,
    "mountain_move": unit_stat_pct_boost_as_str,
    "muddy_move": unit_stat_pct_boost_as_str,
    "naval_attack": unit_stat_boosts_as_str,
    "naval_defense": unit_stat_boosts_as_str,
    "new_model": new_model_as_str,
    "night_attack": unit_stat_pct_boost_as_str,
    "night_defense": unit_stat_pct_boost_as_str,
    "night_move": unit_stat_pct_boost_as_str,
    "non_aggression": non_aggression_as_str,
    "nuclear_carrier": nuclear_carrier_as_str,
    "nuke_damage": nuke_damage_as_str,
    "oilpool": oilpool_as_str,
    "paradrop_attack": unit_stat_pct_boost_as_str,
    "peace": peace_as_str,
    "peacetime_ic_mod": peacetime_ic_change_as_str,
    "province_keypoints": province_keypoints_as_str,
    "province_manpower": province_manpower_as_str,
    "province_revoltrisk": province_revoltrisk_as_str,
    "radar_eff": pct_change_as_str_w_plus,
    "rain_attack": unit_stat_pct_boost_as_str,
    "rain_defense": unit_stat_pct_boost_as_str,
    "rain_move": unit_stat_pct_boost_as_str,
    "range": unit_stat_boosts_as_str,
    "rarematerialspool": rarematerialspool_as_str,
    "regime_falls": regime_falls_as_str,
    "relation": relation_change_as_str,
    "relative_manpower": relative_manpower_as_str,
    "remove_division": remove_division_as_str,
    "removecore": removecore_as_str,
    "repair_mod": pct_change_as_str,
    "research_mod": research_mod_as_str,
    "research_sabotaged": research_sabotaged_as_str,
    "resource": resource_as_str,
    "revolt": revolt_as_str,
    "river_attack": unit_stat_pct_boost_as_str,
    "sce_frequency": sce_frequency_as_str,
    "scrap_model": scrap_model_as_str,
    "secedeprovince": secedeprovince_as_str,
    "set_domestic": set_domestic_as_str,
    "set_leader_skill": set_leader_skill_as_str,
    "set_relation": set_relation_as_str,
    "setflag": setflag_as_str,
    "shore_attack": unit_stat_pct_boost_as_str,
    "sleepevent": sleepevent_as_str,
    "sleepleader": sleepleader_as_str,
    "sleepminister": sleepminister_as_str,
    "sleepteam": sleepteam_as_str,
    "snow_attack": unit_stat_pct_boost_as_str,
    "snow_defense": unit_stat_pct_boost_as_str,
    "snow_move": unit_stat_pct_boost_as_str,
    "soft_attack": unit_stat_boosts_as_str,
    "speed": unit_stat_boosts_as_str,
    "steal_tech": steal_tech_as_str,
    "storm_attack": unit_stat_pct_boost_as_str,
    "storm_defense": unit_stat_pct_boost_as_str,
    "storm_move": unit_stat_pct_boost_as_str,
    "strategic_attack": unit_stat_boosts_as_str,
    "supplies": supplies_as_str,
    "supply_consumption": unit_stat_boosts_as_str,
    "supply_dist_mod": pct_change_as_str,
    "surface_detection": unit_stat_boosts_as_str,
    "surprise": surprise_as_str,
    "swamp_attack": unit_stat_pct_boost_as_str,
    "swamp_defense": unit_stat_pct_boost_as_str,
    "swamp_move": unit_stat_pct_boost_as_str,
    "switch_allegiance": switch_allegiance_as_str,
    "tactical_withdrawal": pct_change_as_str,
    "task_efficiency": task_efficiency_as_str,
    "tc_mod": pct_change_as_str,
    "tc_occupied_mod": pct_change_as_str,
    "transport_pool": transport_pool_as_str,
    "trickleback_mod": pct_change_as_str,
    "trigger": trigger_as_str,
    "urban_attack": unit_stat_pct_boost_as_str,
    "urban_defense": unit_stat_pct_boost_as_str,
    "urban_move": unit_stat_pct_boost_as_str,
    "visibility": unit_stat_boosts_as_str,
    "vp": vp_as_str,
    "wakeleader": wakeleader_as_str,
    "waketeam": waketeam_as_str,
    "war": war_as_str
}


def effect_as_str(effect, text_dict, event_dict=None, tech_dict=None, leader_dict=None, minister_dict=None, techteam_dict=None, force_default=False, **kwargs):
    if force_default:
        return effect_as_str_default(effect)
    the_function = STR_FUNCTION_DICT_FOR_EFFECTS.get(effect.type.lower())
    if the_function is None:
        print("PROBLEM:", effect.type)
    # if the_function is not None:
    #     the_text = the_function(effect, text_dict=text_dict, event_dict=event_dict, **kwargs)
    the_text = the_function(effect, text_dict=text_dict, event_dict=event_dict, tech_dict=tech_dict, leader_dict=leader_dict, minister_dict=minister_dict, techteam_dict=techteam_dict, **kwargs)
    if the_text:
        return the_text
    
    return effect_as_str_default(effect)
    

def print_effect(effect, indent_num, text_dict, event_dict=None, tech_dict=None, leader_dict=None, minister_dict=None, techteam_dict=None, force_default=False, **kwargs):
    print(indent_num * " ", effect_as_str(effect, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, force_default=force_default, **kwargs))


# Minister personality (and policy and idea) modifiers
# accept_alliance_mod
# combat_mod
# defend_land_mod
# detect_convoy_mod
# detect_fleet_mod
# diplomatic_action_mod
# diplomatic_cost_mod
# dissent_mod
# division_extra_mod
# division_type_mod
# do_war_bell_mod
# foreign_ic_mod
# foreign_mp_mod
# intel_diff_mod
# intelligence_mod
# morale_mod
# mp_growth_mod
# org_mod
# peace_bell_rate_mod
# production_category_mod
# province_project_mod
# resource_mod
# retooling_time_mod
# supply_consumption_mod
# tc_mod
# tech_group_mod
# unit_intel_mod
# unit_speed_mod
# war_bell_rate_mod

def get_pct_effect_str(modifier):
    effect = int(modifier.modifier_effect * 100)
    sign = "+" if effect > 0 else ""
    return f"{sign}{effect} %"

def mod_pct_change_as_str(key, modifier, text_dict, text_to_replace="%s%d\\%%\\n"):
    return text_dict[key].replace(text_to_replace, get_pct_effect_str(modifier))

def get_text_and_pct(key, modifier, text_dict):
    return f"- {text_dict[key]}: {get_pct_effect_str(modifier)}"

def modifier_as_str_default(modifier, text_dict=None, **kwargs):
    text_parts = []
    type_part = f"type = {modifier.type}" if modifier.type is not None else ""
    text_parts.append(type_part)
    value_part = f"value = {modifier.value}" if modifier.value is not None else ""
    text_parts.append(value_part)
    option_part = f"option = {modifier.option}" if modifier.option is not None else ""
    text_parts.append(option_part)
    extraa_part = f"extra = {modifier.extra}" if modifier.extra is not None else ""
    text_parts.append(extraa_part)
    modifier_effect_part = f"modifier_effect = {modifier.modifier_effect}" if modifier.modifier_effect is not None else ""
    text_parts.append(modifier_effect_part)
    option1_part = f"option1 = {modifier.option1}" if modifier.option1 is not None else ""
    text_parts.append(option1_part)
    option2_part = f"option2 = {modifier.option2}" if modifier.option2 is not None else ""
    text_parts.append(option2_part)
    division_part = f"division = {modifier.division}" if modifier.division is not None else ""
    text_parts.append(division_part)
    text_parts = [t for t in text_parts if t]
    # effect_line = f"{type_part}, {which_part}, {value_part}, {when_part}, {where_part}"
    return ", ".join(text_parts)

def accept_alliance_mod_as_str(modifier, text_dict):
    # TODO: Check this
    the_key = None
    if modifier.value is not None:
        key_dict = {
            # 0: "ALLIANCE_W_ALL",
            # 1: "ALLIANCE_W_CLOSE_DICTATORSHIPS",
            # 2: "ALLIANCE_W_CLOSE_DEMOCRACIES",
            # this should be correct
            3: "ALLIANCE_W_CLOSE_IDEOLOGY"
        }
        the_key = key_dict.get(modifier.value)
        if the_key is None:
            the_key = modifier_as_str_default(modifier)
        
    elif modifier.option1 is not None:
        key_dict = {
            0: "ALLIANCE_W_DICTATORSHIPS",
            1: "ALLIANCE_W_DEMOCRACIES"
        }
        the_key = key_dict[modifier.option1]
    if the_key is None:
        the_key = "ALLIANCE_W_ALL"
    return mod_pct_change_as_str(the_key, modifier, text_dict)

def colonial_ic_mod_as_str(modifier, text_dict):
    the_key = "T_COLONIAL_IC"
    return get_text_and_pct(the_key, modifier, text_dict)

def colonial_mp_mod_as_str(modifier, text_dict):
    the_key = "T_COLONIAL_MP"
    return get_text_and_pct(the_key, modifier, text_dict)

def combat_mod_as_str(modifier, text_dict):
    if modifier.division is not None:
        division_name = get_unit_name(modifier.division, text_dict, do_short=False)
    elif modifier.extra is not None:
        division_name = get_unit_name(modifier.extra, text_dict, do_short=False)
    the_key = "OFF_COMBAT_MODIFIER" if modifier.option1 == 1 else "DEF_COMBAT_MODIFIER"
    return f"- {division_name} {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def defend_land_mod_as_str(modifier, text_dict):
    the_key = "DEF_COMBAT_MODIFIER"
    return f"- {text_dict[the_key]} (Land): {get_pct_effect_str(modifier)}"

def detect_convoy_mod_as_str(modifier, text_dict):
    the_key = "NAVAL_DETECTION"
    the_key2 = "PRODIW_CO"
    return f"- {text_dict[the_key]} ({text_dict[the_key2]}): {get_pct_effect_str(modifier)}"

def detect_fleet_mod_as_str(modifier, text_dict):
    the_key = "NAVAL_DETECTION"
    return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def diplomatic_action_mod_as_str(modifier, text_dict):
    # TODO: option1 ???
    if modifier.value is not None:
        exceptions = {
            "offer_trade_agreement": "DIP_OFFER_TA"
        }
        the_key = exceptions.get(modifier.value)
        if the_key is None:
            the_key = f"DIP_{modifier.value.upper()}"
        action_text = text_dict[the_key]
    else:
        action_text = "Diplomatic actions"
    chance_str = text_dict["T_CHANCE"]
    return f"- {action_text}: {get_pct_effect_str(modifier)} {chance_str}"

def diplomatic_cost_mod_as_str(modifier, text_dict):
    # TODO: lots of other possibilities
    if modifier.value is None:
        the_key = "DIPLO_COST"
        return mod_pct_change_as_str(the_key, modifier, text_dict)
    exceptions = {
        "offer_trade_agreement": "DIP_OFFER_TA"
    }
    the_key = exceptions.get(modifier.value)
    if the_key is None:
        the_key = f"DIP_{modifier.value.upper()}"
    gov_text = ""
    if modifier.option1 is not None:
        gov_text = f" ({text_dict['GOV_SAME']})" if modifier.option1 == 1 else f" ({text_dict['GOV_OTHER']})"
    return f"- {text_dict[the_key]}{gov_text}: {get_pct_effect_str(modifier)}"

def dissent_mod_as_str(modifier, text_dict):
    the_key = "DISSENT_GROWTH"
    return mod_pct_change_as_str(the_key, modifier, text_dict)

def division_extra_mod_as_str(modifier, text_dict):
    the_key = "T_CONSTRUCTION"
    if modifier.value is not None:
        division_name = get_unit_name(modifier.value, text_dict, do_short=False)
    elif modifier.extra is not None:
        division_name = get_unit_name(modifier.extra, text_dict, do_short=False)
    return f"- {division_name} {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def division_type_mod_as_str(modifier, text_dict):
    if modifier.value is None and modifier.extra is None:
        the_key = "UNIT_COST"
        return mod_pct_change_as_str(the_key, modifier, text_dict)
    the_key = "T_CONSTRUCTION"
    if modifier.value is not None:
        division_name = get_unit_name(modifier.value, text_dict, do_short=False)
    elif modifier.extra is not None:
        division_name = get_unit_name(modifier.extra, text_dict, do_short=False)
    return f"- {division_name} {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def do_war_bell_mod_as_str(modifier, text_dict):
    the_key = f"DOW_BELLIGERENCE"
    return mod_pct_change_as_str(the_key, modifier, text_dict)

def foreign_ic_mod_as_str(modifier, text_dict):
    the_key = "T_FOREIGN_IC_USE"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def foreign_mp_mod_as_str(modifier, text_dict):
    the_key = "T_FOREIGN_MANPOWER_USE"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def intel_diff_mod_as_str(modifier, text_dict):
    the_key = "T_INTEL_DIFF"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def intelligence_mod_as_str(modifier, text_dict):
    exceptions = {
        "send_spy": "SPY_INCREASE_INTELLIGENCE_FOUNDING",
        "steal_blueprint": "SPY_STEAL_TECH"
    }
    the_key = exceptions.get(modifier.value)
    if the_key is None:
        the_key = f"SPY_{modifier.value.upper()}"
    chance_str = text_dict["T_CHANCE"]
    try:
        operation = text_dict[the_key]
    except KeyError as e:
        print(modifier)
        raise e
    return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)} {chance_str}"

def leader_xp_mod_as_str(modifier, text_dict):
    the_key = "T_LEADER_XP"
    return get_text_and_pct(the_key, modifier, text_dict)

def military_salaries_mod_as_str(modifier, text_dict):
    the_key = "T_MILITARY_SALARIES"
    return get_text_and_pct(the_key, modifier, text_dict)

def morale_mod_as_str(modifier, text_dict):
    the_key = "ORG_REGAIN"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def mp_growth_mod_as_str(modifier, text_dict):
    the_key = "MANPOWER_GROWTH"
    effect = int(modifier.modifier_effect * 100) - 100
    sign = "+" if effect > 0 else ""
    effect_str = f"{sign}{effect} %"
    return f"- {text_dict[the_key]}: {effect_str} [Value in file: {modifier.modifier_effect}]"

def org_mod_as_str(modifier, text_dict):
    the_key = "UNIT_ORG"
    return mod_pct_change_as_str(the_key, modifier, text_dict)

def peace_bell_rate_mod_as_str(modifier, text_dict):
    the_key = "PEACE_BELLIGERENCE"
    sign = "+" if modifier.modifier_effect > 0 else ""
    return text_dict[the_key].replace("%s%.1f", f"{sign}{modifier.modifier_effect}").replace("\\n", "")

def production_category_mod_as_str(modifier, text_dict):
    # THIS WILL HAVE PROBLEMS
    value_dict = {
        "production": "T_IC",
        "supply": "EE_SUPPLIES",
        "consumer": "CG_NEED",
        "upgrade": "UPGRADE_COST",
        "infrastructure": "INFRA_REBUILD_COST"
    }
    return f"- {text_dict[value_dict[modifier.value]]}: {get_pct_effect_str(modifier)}"

def province_project_mod_as_str(modifier, text_dict):
    the_key = "T_CONSTRUCTION"
    return f"- {BUILDING_DICT[modifier.value]} {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def remote_placement_min_ic_mod_as_str(modifier, text_dict):
    the_key = "T_REMOTE_PLACEMENT_MIN_IC"
    return get_text_and_pct(the_key, modifier, text_dict)

def resource_mod_as_str(modifier, text_dict):
    # TODO:
    # print(modifier)
    if modifier.value is not None:
        the_key = f"{modifier.value.upper()}_PRODUCTION"
        return text_dict[the_key].replace("%s%d\\%%\\n", str(get_pct_effect_str(modifier)))
    return f"- Resources: {get_pct_effect_str(modifier)}"
    # if modifier.value == "money":
    #     the_key = "MONEY_PRODUCTION"
    # elif modifier.value == "oil":
    #     the_key = "OIL_PRODUCTION"
    # else:
    #     return

def retooling_time_mod_as_str(modifier, text_dict):
    the_key = "T_RETOOLING_TIME"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def stand_ground_dissent_mod_as_str(modifier, text_dict):
    the_key = "T_STAND_GROUND_DISSENT"
    return get_text_and_pct(the_key, modifier, text_dict)

def supply_consumption_mod_as_str(modifier, text_dict):
    the_key = "EE_SUPPLY_CONSUMPTION"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def tc_mod_as_str(modifier, text_dict):
    the_key = "TC_BONUS"
    return mod_pct_change_as_str(the_key, modifier, text_dict)

def tech_group_mod_as_str(modifier, text_dict):
    category = ""
    if modifier.value is not None:
        category = f"{get_tech_category_name(modifier.value, text_dict)} "
    research_str = "research"
    if not category:
        research_str = research_str.capitalize()
    return f"- {category}{research_str}: {get_pct_effect_str(modifier)} [Note: negative is faster]"

def unit_intel_mod_as_str(modifier, text_dict):
    the_key = "T_ARMY_INTELLIGENCE"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def unit_speed_mod_as_str(modifier, text_dict):
    the_key = "LAND_UNIT_SPEED"
    return get_text_and_pct(the_key, modifier, text_dict)
    # return f"- {text_dict[the_key]}: {get_pct_effect_str(modifier)}"

def war_bell_rate_mod_as_str(modifier, text_dict):
    the_key = "WAR_BELLIGERENCE"
    sign = "+" if modifier.modifier_effect > 0 else ""
    return text_dict[the_key].replace("%s%.1f", f"{sign}{modifier.modifier_effect}").replace("\\n", "")

STR_FUNCTION_DICT_FOR_MODIFERS = {
    "accept_alliance_mod": accept_alliance_mod_as_str,
    "colonial_ic_mod": colonial_ic_mod_as_str,
    "colonial_mp_mod": colonial_mp_mod_as_str,
    "combat_mod": combat_mod_as_str,
    "defend_land_mod": defend_land_mod_as_str,
    "detect_convoy_mod": detect_convoy_mod_as_str,
    "detect_fleet_mod": detect_fleet_mod_as_str,
    "diplomatic_action_mod": diplomatic_action_mod_as_str,
    "diplomatic_cost_mod": diplomatic_cost_mod_as_str,
    "dissent_mod": dissent_mod_as_str,
    "division_extra_mod": division_extra_mod_as_str,
    "division_type_mod": division_type_mod_as_str,
    "do_war_bell_mod": do_war_bell_mod_as_str,
    "foreign_ic_mod": foreign_ic_mod_as_str,
    "foreign_mp_mod": foreign_mp_mod_as_str,
    "intel_diff_mod": intel_diff_mod_as_str,
    "intelligence_mod": intelligence_mod_as_str,
    "leader_xp_mod": leader_xp_mod_as_str,
    "military_salaries_mod": military_salaries_mod_as_str,
    "morale_mod": morale_mod_as_str,
    "mp_growth_mod": mp_growth_mod_as_str,
    "org_mod": org_mod_as_str,
    "peace_bell_rate_mod": peace_bell_rate_mod_as_str,
    "production_category_mod": production_category_mod_as_str,
    "province_project_mod": province_project_mod_as_str,
    "remote_placement_min_ic_mod": remote_placement_min_ic_mod_as_str,
    "resource_mod": resource_mod_as_str,
    "retooling_time_mod": retooling_time_mod_as_str,
    "stand_ground_dissent_mod": stand_ground_dissent_mod_as_str,
    "supply_consumption_mod": supply_consumption_mod_as_str,
    "tc_mod": tc_mod_as_str,
    "tech_group_mod": tech_group_mod_as_str,
    "unit_intel_mod": unit_intel_mod_as_str,
    "unit_speed_mod": unit_speed_mod_as_str,
    "war_bell_rate_mod": war_bell_rate_mod_as_str
}

def modifier_as_str(modifier, text_dict, force_default=False, **kwargs):
    if force_default:
        return modifier_as_str_default(modifier)
    the_function = STR_FUNCTION_DICT_FOR_MODIFERS.get(modifier.type.lower())
    if the_function is None:
        print("PROBLEM with modifier type:", modifier.type)
        return modifier_as_str_default(modifier)
    modifier_str = the_function(modifier, text_dict, **kwargs)
    if modifier_str is None:
        return modifier_as_str_default(modifier)
    return modifier_str

def print_modifier(modifier, indent_num, text_dict, force_default=False, **kwargs):
    print(" " * indent_num, modifier_as_str(modifier, text_dict, force_default=force_default, **kwargs))

# Trigger keys: (AI/ai)
# AI
# Event
# InCabinet
# access
# ai
# alliance
# attack
# atwar
# axis
# battlecruiser
# battleship
# belligerence
# can_change_policy
# carrier
# cas
# comintern
# control
# country
# day
# destroyer
# dissent
# domestic
# energy
# escort_carrier
# event
# exists
# flag
# garrison
# government
# guarantee
# headofgovernment
# headofstate
# hq
# ic
# ideology
# incabinet
# infantry
# intel_diff
# interceptor
# is_tech_active
# ispuppet
# land_percentage
# leader
# light_armor
# local_flag
# lost_IC
# lost_VP
# lost_national
# lost_vp
# major
# manpower
# marine
# mechanized
# metal
# minister
# month
# motorized
# multi_role
# naval_bomber
# non_aggression
# oil
# owned
# paratrooper
# puppet
# random
# rare_materials
# relation
# strategic_bomber
# submarine
# supplies
# tactical_bomber
# technology
# transport
# transport_plane
# under_attack
# vp
# war
# year

def condition_as_str_default(condition, text_dict, **kwargs):
    condition_as_str = ""
    conditions_as_str = [f"{key}={value}" for key, value in condition.items()]
    return "  ".join(conditions_as_str)

def faction_cond_as_str(condition, text_dict, **kwargs):
    faction, value = list(condition.items())[0]
    # TODO: I don't know what else this could be?
    return f"{faction.capitalize()} has at least {value} victory points [I don't know what else this could mean]"

def resource_cond_as_str(condition, text_dict, **kwargs):
    the_key = list(condition.keys())[0]
    value = list(condition.values())[0]
    resource_name = get_resource_name(the_key, text_dict)
    return f"Country has at least {value} {resource_name}"

def division_cond_as_str(condition, text_dict, **kwargs):
    unit_key = list(condition.keys())[0]
    unit_name = get_unit_name(unit_key, text_dict, do_short=False)
    detail_dict = list(condition.values())[0]
    country_key = "country"
    value_key = "value"
    country = get_country(detail_dict[country_key], text_dict)
    value = detail_dict[value_key]
    # TODO: is this actually what this means?
    return f"{country} has at least {value} {unit_name}"

def access_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["access"]["country"]
    country0 = text_dict[countries[0]]
    country1 = text_dict[countries[1]]
    return f"{country0} has granted military access to {country1}"

def ai_cond_as_str(condition, text_dict, **kwargs):
    yes_or_no = list(condition.values())[0]
    if yes_or_no.lower() == "yes":
        return "Country is controlled by AI player"
    if yes_or_no.lower() == "no":
        return "Country is controlled by human player"
    country = text_dict[yes_or_no.upper()]
    if len(yes_or_no) == 3 and country:
        return f"{country} is controlled by AI player" 
    raise Exception(f"MASSIVE ERROR=with ai: {condition}")

def alliance_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["alliance"]["country"]
    country0 = get_country(countries[0], text_dict)
    country1 = get_country(countries[1], text_dict)
    return f"Alliance between {country0} and {country1}"

def attack_cond_as_str(condition, text_dict, **kwargs):
    country_code = list(condition.values())[0]
    country = get_country(country_code, text_dict)
    # TODO: who attacks who?
    return f"Attack {country} [or {country} attacks?]"

def atwar_cond_as_str(condition, text_dict, **kwargs):
    value = condition["atwar"].lower()
    if value == "yes":
        return "Country is at war"
    if value == "no":
        return "Country is at peace"
    country = text_dict.get(value.upper())
    if len(value) == 3 and country:
        return f"{country} is at war"
    raise Exception(f"MASSIVE ERROR=with atwar: {condition}")

def axis_cond_as_str(condition, text_dict, **kwargs):
    pass

def battlecruiser_cond_as_str(condition, text_dict, **kwargs):
    pass

def battleship_cond_as_str(condition, text_dict, **kwargs):
    pass

def belligerence_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = condition["belligerence"]
    country = get_country(detail_dict["country"], text_dict)
    lower_value = condition["belligerence"]["value"]
    return f"Belligerence of {country} is at least {lower_value}"

def can_change_policy_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    slider_type_key = detail_dict["type"]
    slider_name = SLIDER_DICT[slider_type_key][0]
    value = detail_dict["value"]
    return f"Country can change {slider_name} by {value}"

def carrier_cond_as_str(condition, text_dict, **kwargs):
    pass

def cas_cond_as_str(condition, text_dict, **kwargs):
    pass

def comintern_cond_as_str(condition, text_dict, **kwargs):
    pass

def control_cond_as_str(condition, text_dict, **kwargs):
    province_key = "province"
    data_key = "data"
    detail_dict = list(condition.values())[0]
    province_num = detail_dict[province_key]
    province = get_province(province_num, text_dict)
    if data_key in detail_dict.keys():
        country_code = detail_dict[data_key]
        country = get_country(country_code, text_dict)
    else:
        country = "Country"
    return f"{country} controls province {province} [{province_num}]"

def country_cond_as_str(condition, text_dict, **kwargs):
    # TODO: what is this condition actually?
    country_code = list(condition.values())[0]
    country = get_country(country_code, text_dict)
    return f"Country is {country}"

def day_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    # TODO: whatever does this mean
    return f"Day is at least {value}"

def destroyer_cond_as_str(condition, text_dict, **kwargs):
    pass

def dissent_cond_as_str(condition, text_dict, **kwargs):
    dissent, value = list(condition.items())[0]
    return f"Country has at least {value} {dissent}"

def domestic_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    slider_type_key = detail_dict["type"]
    slider_name = SLIDER_DICT[slider_type_key][0]
    value = detail_dict["value"]
    # TODO: is this correct?
    return f"{slider_name} is at least {value}"

def escort_carrier_cond_as_str(condition, text_dict, **kwargs):
    pass

def event_cond_as_str(condition, text_dict, event_dict, **kwargs):
    event_id = list(condition.values())[0]
    event = event_dict.get(event_id)
    if event is not None:
        return f"Event {event_id} '{event.name}' has happened"
    return f"Event {event_id} has happened [BUT THIS EVENT DOES NOT EXIST]"

def exists_cond_as_str(condition, text_dict, **kwargs):
    country = get_country(condition["exists"], text_dict)
    return f"Country {country} exists"

def flag_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    return f"Flag: {value}"

def garrison_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country_code = detail_dict["country"]
    country = get_country(country_code, text_dict)
    province_num = detail_dict["province"]
    province = get_province(province_num, text_dict)
    size = detail_dict["size"]
    gar_type = detail_dict.get("type")
    gar_type = f"{gar_type} " if gar_type else ""
    division_type = "divisions"
    is_area = detail_dict.get("area")
    area = ""
    if is_area:
        area = f" (area: {is_area})"
    return f"{country} has at least {size} {gar_type}{division_type} in {province} [{province_num}]{area}"

def government_cond_as_str(condition, text_dict, **kwargs):
    government_type = list(condition.values())[0]
    return f"Country has {government_type} government"

def guarantee_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["guarantee"]["country"]
    country0 = get_country(countries[0], text_dict)
    country1 = get_country(countries[1], text_dict)
    return f"{country0} aguarantees the independence of {country1}"

def headofgovernment_cond_as_str(condition, text_dict, minister_dict=None, **kwargs):
    the_key, value = list(condition.items())[0]
    if minister_dict:
        minister_name = minister_dict.get(value).name if minister_dict.get(value) else ""
    else:
        minister_name = ""
    return f"Head of Government: {minister_name} [{value}]"

def headofstate_cond_as_str(condition, text_dict, minister_dict=None, **kwargs):
    the_key, value = list(condition.items())[0]
    if minister_dict:
        minister_name = minister_dict.get(value).name if minister_dict.get(value) else ""
    else:
        minister_name = ""
    return f"Head of State: {minister_name} [{value}]"

def hq_cond_as_str(condition, text_dict, **kwargs):
    pass

def ic_cond_as_str(condition, text_dict, **kwargs):
    the_key = list(condition.keys())[0]
    value = list(condition.values())[0]
    # TODO: this is most likely 'at least'
    return f"Country has at least (?) {value} {BUILDING_DICT[the_key]}"

def ideology_cond_as_str(condition, text_dict, **kwargs):
    the_key = list(condition.keys())[0]
    ideology_type_key = list(condition.values())[0]
    # exception
    if ideology_type_key.startswith("na"):
        ideology_type_key = "national_socialist"
    ideology = text_dict[f"CATEGORY_{ideology_type_key.upper()}"]
    return f"{the_key.capitalize()} of the country is {ideology}"

def incabinet_cond_as_str(condition, text_dict, minister_dict=None, **kwargs):
    value = list(condition.values())[0]
    if minister_dict:
        minister_name = minister_dict.get(value).name if minister_dict.get(value) else ""
    else:
        minister_name = ""
    return f"Minister {minister_name} [{value}] is in cabinet"

def infantry_cond_as_str(condition, text_dict, **kwargs):
    pass

def intel_diff_cond_as_str(condition, text_dict, **kwargs):
    value = condition["intel_diff"]
    # TODO: at least or at most?
    return f"Intel difference is at least (?) {value}"

def interceptor_cond_as_str(condition, text_dict, **kwargs):
    pass

def is_tech_active_cond_as_str(condition, text_dict, tech_dict, **kwargs):
    tech_id = condition["is_tech_active"]
    tech = tech_dict[tech_id]
    return f"Technology {tech_id} '{tech.name}' is active"

def ispuppet_cond_as_str(condition, text_dict, **kwargs):
    country_code = list(condition.values())[0]
    country = get_country(country_code, text_dict)
    return f"{country} is a puppet country"

def land_percentage_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country_code = detail_dict["country"]
    country = get_country(country_code, text_dict)
    value = detail_dict["value"]
    return f"{country} has at least {value} land percentage [I don't know what this means]"

def leader_cond_as_str(condition, text_dict, leader_dict=None, **kwargs):
    the_key, value = list(condition.items())[0]
    if leader_dict:
        leader_name = leader_dict.get(value).name if leader_dict.get(value) else ""
    else:
        leader_name = ""
    return f"Leader: {leader_name} [{value}]"

def light_armor_cond_as_str(condition, text_dict, **kwargs):
    pass

def local_flag_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    return f"Local flag: {value}"

def lost_ic_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country = get_country(detail_dict["country"], text_dict)
    value = detail_dict["value"]
    # TODO: percentage or actual points?
    return f"{country} has lost at least {value} IC [is this percentage?]"

def lost_national_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country = get_country(detail_dict["country"], text_dict)
    value = detail_dict["value"]
    # TODO: is this correct?
    return f"{country} has lost at least {value} % of national provinces"

def lost_vp_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country = get_country(detail_dict["country"], text_dict)
    value = detail_dict["value"]
    # TODO: percentage or actual points?
    return f"{country} has lost at least {value} victory points [is this percentage?]"

def major_cond_as_str(condition, text_dict, **kwargs):
    yes_or_no = list(condition.values())[0]
    if yes_or_no.lower() == "yes":
        return "Country is a major power (?)"
    if yes_or_no.lower() == "no":
        return "Country is not a major power (?)"
    raise Exception(f"MASSIVE ERROR=with major: {condition}")

def manpower_cond_as_str(condition, text_dict, **kwargs):
    pass

def marine_cond_as_str(condition, text_dict, **kwargs):
    pass

def mechanized_cond_as_str(condition, text_dict, **kwargs):
    pass

def minister_cond_as_str(condition, text_dict, minister_dict=None, **kwargs):
    the_key, value = list(condition.items())[0]
    if minister_dict:
        minister_name = minister_dict.get(value).name if minister_dict.get(value) else ""
    else:
        minister_name = ""
    return f"Minister: {minister_name} [{value}]"

def month_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    # TODO: whatever does this mean
    return f"Month is at least {value}"

def motorized_cond_as_str(condition, text_dict, **kwargs):
    pass

def multi_role_cond_as_str(condition, text_dict, **kwargs):
    pass

def naval_bomber_cond_as_str(condition, text_dict, **kwargs):
    pass

def non_aggression_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["non_aggression"]["country"]
    country0 = get_country(countries[0], text_dict)
    country1 = get_country(countries[1], text_dict)
    return f"Non-aggression pact between {country0} and {country1}"

def owned_cond_as_str(condition, text_dict, **kwargs):
    province_key = "province"
    data_key = "data"
    detail_dict = list(condition.values())[0]
    province_num = detail_dict[province_key]
    province = get_province(province_num, text_dict)
    if data_key in detail_dict.keys():
        country_code = detail_dict[data_key]
        country = get_country(country_code, text_dict)
    else:
        country = "Country"
    return f"{country} owns province {province} [{province_num}]"

def paratrooper_cond_as_str(condition, text_dict, **kwargs):
    pass

def puppet_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["puppet"]["country"]
    country0 = get_country(countries[0], text_dict)
    country1 = get_country(countries[1], text_dict)
    return f"{country0} is a puppet of {country1}"

def random_cond_as_str(condition, text_dict, **kwargs):
    return f"Random: {list(condition.values())[0]} %"

def relation_cond_as_str(condition, text_dict, **kwargs):
    detail_dict = list(condition.values())[0]
    country_code = detail_dict["which"]
    country = get_country(country_code, text_dict)
    value = detail_dict["value"]
    # TODO: this is probably correct
    return f"Our relation with {country} is at least {value}"

def strategic_bomber_cond_as_str(condition, text_dict, **kwargs):
    pass

def submarine_cond_as_str(condition, text_dict, **kwargs):
    pass

def tactical_bomber_cond_as_str(condition, text_dict, **kwargs):
    pass

def technology_cond_as_str(condition, text_dict, tech_dict, **kwargs):
    tech_id = condition["technology"]
    tech = tech_dict[tech_id]
    return f"Country has the technology {tech_id} '{tech.name}'"

def transport_cond_as_str(condition, text_dict, **kwargs):
    pass

def transport_plane_cond_as_str(condition, text_dict, **kwargs):
    pass

def under_attack_cond_as_str(condition, text_dict, **kwargs):
    country_code = list(condition.values())[0]
    country = get_country(country_code, text_dict)
    return f"{country} is under attack"

def vp_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    # TODO: is this actually how this works?
    return f"Country has at least {value} victory points"

def war_cond_as_str(condition, text_dict, **kwargs):
    countries = condition["war"]["country"]
    country0 = get_country(countries[0], text_dict)
    country1 = get_country(countries[1], text_dict)
    return f"War between {country0} and {country1}"

def year_cond_as_str(condition, text_dict, **kwargs):
    value = list(condition.values())[0]
    # TODO: this should be correct
    return f"Year is at least {value}"


STR_FUNCTION_DICT_FOR_CONDITIONS = {
    "access": access_cond_as_str,
    "ai": ai_cond_as_str,
    "alliance": alliance_cond_as_str,
    "attack": attack_cond_as_str,
    "atwar": atwar_cond_as_str,
    "axis": faction_cond_as_str,
    "battlecruiser": division_cond_as_str,
    "battleship": division_cond_as_str,
    "belligerence": belligerence_cond_as_str,
    "can_change_policy": can_change_policy_cond_as_str,
    "carrier": division_cond_as_str,
    "cas": division_cond_as_str,
    "comintern": faction_cond_as_str,
    "control": control_cond_as_str,
    "country": country_cond_as_str,
    "day": day_cond_as_str,
    "destroyer": division_cond_as_str,
    "dissent": dissent_cond_as_str,
    "domestic": domestic_cond_as_str,
    "energy": resource_cond_as_str,
    "escort_carrier": division_cond_as_str,
    "event": event_cond_as_str,
    "exists": exists_cond_as_str,
    "flag": flag_cond_as_str,
    "garrison": garrison_cond_as_str,
    "government": government_cond_as_str,
    "guarantee": guarantee_cond_as_str,
    "headofgovernment": headofgovernment_cond_as_str,
    "headofstate": headofstate_cond_as_str,
    "hq": division_cond_as_str,
    "ic": ic_cond_as_str,
    "ideology": ideology_cond_as_str,
    "incabinet": incabinet_cond_as_str,
    "infantry": division_cond_as_str,
    "intel_diff": intel_diff_cond_as_str,
    "interceptor": division_cond_as_str,
    "is_tech_active": is_tech_active_cond_as_str,
    "ispuppet": ispuppet_cond_as_str,
    "land_percentage": land_percentage_cond_as_str,
    "leader": leader_cond_as_str,
    "light_armor": division_cond_as_str,
    "local_flag": local_flag_cond_as_str,
    "lost_ic": lost_ic_cond_as_str,
    "lost_national": lost_national_cond_as_str,
    "lost_vp": lost_vp_cond_as_str,
    "major": major_cond_as_str,
    "manpower": resource_cond_as_str,
    "marine": division_cond_as_str,
    "mechanized": division_cond_as_str,
    "metal": resource_cond_as_str,
    "minister": minister_cond_as_str,
    "month": month_cond_as_str,
    "motorized": division_cond_as_str,
    "multi_role": division_cond_as_str,
    "naval_bomber": division_cond_as_str,
    "non_aggression": non_aggression_cond_as_str,
    "oil": resource_cond_as_str,
    "owned": owned_cond_as_str,
    "paratrooper": division_cond_as_str,
    "puppet": puppet_cond_as_str,
    "random": random_cond_as_str,
    "rare_materials": resource_cond_as_str,
    "relation": relation_cond_as_str,
    "strategic_bomber": division_cond_as_str,
    "submarine": division_cond_as_str,
    "supplies": resource_cond_as_str,
    "tactical_bomber": division_cond_as_str,
    "technology": technology_cond_as_str,
    "transport": division_cond_as_str,
    "transport_plane": division_cond_as_str,
    "under_attack": under_attack_cond_as_str,
    "vp": vp_cond_as_str,
    "war": war_cond_as_str,
    "year": year_cond_as_str,
}

def condition_as_str(condition, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, force_default=False, **kwargs):
    if force_default:
        return condition_as_str_default(condition, text_dict, **kwargs)
    if len(condition.keys()) > 1:
        print("PROBLEM: too many keys", f"({', '.join(condition.condition.keys())})")
    the_key = list(condition.keys())[0].lower()
    the_function = STR_FUNCTION_DICT_FOR_CONDITIONS[the_key]
    if the_function is None:
        print("PROBLEM:", the_key)
    the_text = the_function(condition, text_dict, event_dict=event_dict, tech_dict=tech_dict, leader_dict=leader_dict, minister_dict=minister_dict, techteam_dict=techteam_dict, **kwargs)
    if the_text:
        return the_text
    return condition_as_str_default(condition, text_dict, **kwargs)


def print_condition(condition, indent_num, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, **kwargs):
    if condition.condition is not None:
        if condition.connective and condition.connective == condition.NOT_STR:
            print(indent_num * " ", f"{condition.NOT_STR} (", end=" ")
        else:
            print(indent_num * " ", end=" ")
        first = True
        for key, value in condition.condition.items():
            if not first:
                print("THIS SHOULD NOT BE HERE!!!! problem condition:", condition.condition)
                print(", ", end="")
            else:
                first = False
            # print(f"{key} = {value}", end="")
            print(condition_as_str(condition.condition, text_dict, event_dict=event_dict, tech_dict=tech_dict, leader_dict=leader_dict, minister_dict=minister_dict, techteam_dict=techteam_dict), end="")
        if condition.connective and condition.connective == condition.NOT_STR:
            print(" )", end="\n")
        else:
            print()
        return
    if condition.connective:
        print(indent_num * " ", condition.connective)
        for cond in condition.child_conditions:
            print_condition(cond, indent_num + indent_add, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict)
            # cond.print_condition(indent_num + indent_add, indent_add)
    else:
        for cond in condition.child_conditions:
            print_condition(cond, indent_num + indent_add, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict)
            # cond.print_condition(indent_num, indent_add)

def print_trigger(event, indent_num, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, empty_trigger=True, **kwargs):
    if not event.trigger.raw_conditions and empty_trigger:
        print(indent_num * " ", "-")
        return
    if not event.trigger.raw_conditions:
        return
    print_condition(event.trigger, indent_num, 2 * indent_add, text_dict, event_dict=event_dict, tech_dict=tech_dict, leader_dict=leader_dict, minister_dict=minister_dict, techteam_dict=techteam_dict, **kwargs)
    # event.trigger.print_condition(indent_num, 2 * indent_add)

def print_action(action, indent_num, indent_add, text_dict, event_dict, tech_dict=None, leader_dict=None, minister_dict=None, techteam_dict=None, force_default=False, max_num_of_duplicate_effects=5, **kwargs):
    if action.name:
        print(indent_num * " ", f"({action.action_key})", action.name)
    elif action.name_key:
        print(indent_num * " ", f"({action.action_key})", action.name_key, " [name in file]")
    else:
        print(indent_num * " ", f"({action.action_key})", " [no name]")
    indent_num += indent_add
    if action.ai_chance is not None:
        print(indent_num * " ", f"AI chance: {action.ai_chance} %")
    
    if not action.effects:
        print(indent_num * " ", "Effects:")
        indent_num += indent_add
        print(indent_num * " ", "-")
        return
    print(indent_num * " ", f"Effects ({len(action.effects)}):")
    indent_num += indent_add
    effects_as_str = [effect_as_str(effect, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, force_default=force_default, **kwargs) for effect in action.effects]
    counts = Counter(effects_as_str)
    skip_duplicates = {key: False for key, num in counts.items() if num > max_num_of_duplicate_effects}
    for effect_str in effects_as_str:
        if skip_duplicates.get(effect_str):
            continue
        if effect_str in skip_duplicates:
            skip_duplicates[effect_str] = True
            print(max(indent_num - 1, 0) * " ", f"{counts[effect_str]} times the following:")
        print(indent_num * " ", effect_str)

def print_event(event, aod_path, indent_num, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, force_default=False, max_num_of_duplicate_effects=5, **kwargs):
    if event.name:
        print(f"{indent_num * ' '} {event.event_id}: {event.name}")
    else:
        print(f"{indent_num * ' '} {event.event_id}: {event.name_key}  [name in file]")
    if event.country:
        print(f"{indent_num * ' '} Country: {event.country}")
    if event.is_invention:
        print(f"{indent_num * ' '} Invention event")
    if event.is_random:
        print(f"{indent_num * ' '} Random event")
    
    path_str = str(event.filepath)[len(str(aod_path)) + 1:]
    print(f"{indent_num * ' '} In file: {path_str}")

    print()
    print(indent_num * ' ', "Trigger:")
    trigger_empty = True
    if event.triggered_by:
        trigger_empty = False
        print((indent_num + indent_add) * " ", "Triggered by:")
        for trigger_event, action_index in event.triggered_by:
            text_about_event = f"event {trigger_event.event_id} [{trigger_event.country}]: {trigger_event.name}"
            text_about_action = f"action '{trigger_event.actions[action_index].name}' [{trigger_event.actions[action_index].action_key}]"
            print((indent_num + 2 * indent_add) * " ", f"{text_about_event}, {text_about_action}")
    # event.trigger.print_trigger(indent_num + indent_add, indent_add, empty_trigger=trigger_empty)
    print_trigger(event, indent_num + indent_add, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, empty_trigger=trigger_empty, **kwargs)
    print()

    if event.deactivated_by:
        print(indent_num * " ", "Deactivated by:")
        for deactivating_event, action_index in event.deactivated_by:
            text_about_event = f"event {deactivating_event.event_id} [{deactivating_event.country}]: {deactivating_event.name}"
            text_about_action = f"action '{deactivating_event.actions[action_index].name}' [{deactivating_event.actions[action_index].action_key}]"
            print((indent_num + 2 * indent_add) * " ", f"{text_about_event}, {text_about_action}")

    print()

    if event.date:
        print(indent_num * ' ', "Date:")
        print(indent_num * ' ', event.date["day"], event.date["month"], event.date["year"])
    if event.offset is not None:
        print(f"{indent_num * ' '} Offset: {event.offset}")
    if event.deathdate:
        print(indent_num * ' ', "Deathdate:")
        print(indent_num * ' ', event.deathdate["day"], event.deathdate["month"], event.deathdate["year"])
    
    if event.is_persistent:
        print(indent_num * ' ', "Persistent event")

    print()
    print(f"{indent_num * ' '} Description:")
    if event.description:
        print(indent_num * ' ', event.description)
    else:
        print(indent_num * ' ', "-")

    print()
    print(indent_num * ' ', "Possible Actions:")
    for action in event.actions:
        # action.print_action(indent_num + indent_add, indent_add)
        print_action(action, indent_num, indent_add, text_dict, event_dict, tech_dict, leader_dict, minister_dict, techteam_dict, force_default=force_default, **kwargs)
    

def list_tech_effects(tech, text_dict, tech_dict, force_default=False, **kwargs):
    effect_strs = []
    research_speed_change = []
    for effect in tech.effects:
        if effect.type == "research_mod":
            research_speed_change.append(effect_as_str(effect, text_dict, force_default=force_default))
            continue
        effect_str = effect_as_str(effect, text_dict, tech_dict=tech_dict, force_default=force_default)
        for eff_str in effect_str.split("\n"):
            effect_strs.append(eff_str)
    return research_speed_change + effect_strs

def get_component_name(component_type, text_dict, force_default=False):
    if force_default:
        return component_type
    key = f"RT_{component_type.upper()}"
    return text_dict[key]

def print_tech(tech, indent_num=2, indent_add=2, text_dict=None, tech_dict=None, force_default=False):
    if text_dict is None or tech_dict is None:
        force_default = True
    print(" " * indent_num, f"{tech.tech_id}: {tech.name}")
    if force_default:
        print(" " * indent_num, f"Category: {tech.category}")
    else:
        print(" " * indent_num, f"Category: {get_tech_category_name(tech.category, text_dict)}")
    print(" " * indent_num, "Components:")
    for component in tech.components:
        print(" " * (indent_num + indent_add), get_component_name(component.type, text_dict, force_default=force_default), f"(Difficulty: {component.difficulty})")

    print(" " * indent_num, "Requirements:")
    if not tech.requirements:
        print(" " * (indent_num + indent_add), "-")
    for requirement in tech.requirements:
        if isinstance(requirement, int):
            if force_default:
                print(" " * (indent_num + indent_add), requirement)
                continue
            print(" " * (indent_num + indent_add), f"[{requirement}] {tech_dict[requirement].name}")
            continue
        print(" " * (indent_num + indent_add), "One of the following:")
        for option in requirement:
            if force_default:
                print(" " * (indent_num + indent_add), option)
                continue
            print(" " * (indent_num + 2 * indent_add), f"[{option}] {tech_dict[option].name}")

    print(" " * indent_num, "Allows:")
    if not tech.allows:
        print(" " * (indent_num + indent_add), "-")
    for tech_id in tech.allows:
        if force_default:
            print(" " * (indent_num + indent_add), tech_id)
            continue
        print(" " * (indent_num + indent_add), f"[{tech_id}] {tech_dict[tech_id].name}")

    print(" " * indent_num, "Deactivated by:")
    if not tech.deactivated_by:
        print(" " * (indent_num + indent_add), "-")
    for tech_id in tech.deactivated_by:
        if force_default:
            print(" " * (indent_num + indent_add), tech_id)
            continue
        print(" " * (indent_num + indent_add), f"[{tech_id}] {tech_dict[tech_id].name}")

    print(" " * indent_num, "Effects:")
    list_of_effects = list_tech_effects(tech, text_dict, tech_dict, force_default=force_default)
    for effect_str in list_of_effects:
        print(" " * (indent_num + 2 * indent_add), effect_str)
    # for effect in tech.effects:
    #     effect_str = " ".join([f"{eff}={value}" for eff, value in zip(EFFECT_ATTRIBUTES, effect) if value is not None])
    #     print(" " * (indent_num + 2 * indent_add), effect_str)
    print(" " * indent_num, f"In file: {tech.filepath}")


def print_tech_team(techteam, indent_num=2, indent_add=2, text_dict=None, force_default=False):
    if text_dict is None:
        force_default = True
    print(" " * indent_num, f"{techteam.team_id}: {techteam.name}")
    print(" " * indent_num, f"Country: {techteam.country}")
    print(" " * indent_num, f"Skill {techteam.skill}")
    print(" " * indent_num, "Specialities:")
    if not techteam.specialities:
        print(" " * (indent_num + indent_add), "-")
    for speciality in techteam.specialities:
        print(" " * (indent_num + indent_add), get_component_name(speciality, text_dict, force_default=force_default))
    print(" " * indent_num, f"Start year: {techteam.start_year}  End year: {techteam.end_year}")
    print(" " * indent_num, f"In file: {techteam.filepath}")


def print_minister(minister, indent_num=2, indent_add=2, text_dict=None, force_default=False):
    if text_dict is None:
        force_default = True
    print(" " * indent_num, f"{minister.m_id}: {minister.name}")
    print(" " * indent_num, f"Country: {minister.country}")
    print(" " * indent_num, f"Position: {minister.readable_positions[minister.position]}")

    print(" " * indent_num, f"Personality:", end=" ")
    if minister.personality is None:
        print("-")
    else:
        print(minister.personality.public_name)
        indent_num += 2 * indent_add
        print(" " * indent_num, "Modifiers:")
        indent_num += indent_add
        for modifier in minister.personality.modifiers:
            print_modifier(modifier, indent_num, text_dict, force_default=force_default)
            # modifier_str = " ".join([f"{mod}={value}" for mod, value in zip(MODIFIER_ATTRIBUTES, modifier) if value is not None])
            # print(" " * (indent_num + 2 * indent_add), modifier_str)
        indent_num -= 3 * indent_add
    print(" " * indent_num, f"Start year: {minister.start_year}")
    if force_default:
        print(" " * indent_num, f"Ideology: {ideology}")
    else:
        print(" " * indent_num, f"Ideology: {text_dict[IDEOLOGY_DICT[minister.ideology]]}")
    print(" " * indent_num, f"Loyalty: {minister.loyalty}")
    print(" " * indent_num, f"Filepath: {minister.filepath}")


def print_idea(idea, indent_num=2, indent_add=2, text_dict=None, force_default=False):
    if text_dict is None:
        force_default = True
    print(" " * indent_num, f"{idea.public_name}")
    print(" " * indent_num, f"Position: {idea.position}")
    print(" " * indent_num, "Modifiers:")
    indent_num += indent_add
    if not idea.modifiers:
        print(" " * indent_num, "-")
    for modifier in idea.modifiers:
        print_modifier(modifier, indent_num, text_dict, force_default=force_default)
    indent_num -= indent_add
    print(" " * indent_num, "Government types:")
    indent_num += indent_add
    for gov_type in idea.gov_types:
        print(" " * indent_num, gov_type)


def print_province(province, indent_num=2, indent_add=2, text_dict=None, force_default=False):
    name_text = "[NO NAME]" if not province.name else province.name
    print(" " * indent_num, f"{province.prov_id}: {name_text}")
    print()
    print(" " * indent_num, f"Area: {province.area}")
    print(" " * indent_num, f"Region: {province.region}")
    print(" " * indent_num, f"Continent: {province.continent}")
    print()
    has_beaches = "Yes" if province.has_beaches == 1 else "No"
    print(" " * indent_num, f"Has beaches: {has_beaches}")
    port_allowed = "Yes" if province.port_allowed == 1 else "No"
    print(" " * indent_num, f"Can have a port: {port_allowed}")
    if province.port_allowed == 1:
        port_seazone = text_dict.get(f"PROV{province.port_seazone}")
        port_seazone_str = "" if port_seazone is None else f" {port_seazone}"
        print(" " * indent_num, f"Port seazone: [{province.port_seazone}]{port_seazone_str}")
    print()
    print(" " * indent_num, "Stats based on province.csv (ignoring revolt risk, tech, peacetime and policy effects):")
    things = ["Infrastructure", "Manpower", "Province efficiency", "Industrial Capacity", "Energy", "Metal", "Rare Materials", "Oil"]
    wordlength = 20
    print(" " * indent_num, f"{things[0]}:{' ' * (wordlength - len(things[0]))} {province.infra}")
    print(" " * indent_num, f"{things[1]}:{' ' * (wordlength - len(things[1]))} {province.mp}")
    print(" " * indent_num, f"{things[2]}:{' ' * (wordlength - len(things[2]))} {round(province.get_efficiency() * 100, 2)} %")
    values = [
        (province.get_ic(), province.ic, province.get_ic_w_max_infra()),
        (province.get_energy(), province.energy, province.get_energy_w_max_infra()),
        (province.get_metal(), province.metal, province.get_metal_w_max_infra()),
        (province.get_rares(), province.rares, province.get_rares_w_max_infra()),
        (province.get_oil(), province.oil, province.get_oil_w_max_infra())
    ]
    value_lengths = (6, 18, 23)
    for thing_name, value in zip(things[3:], values):
        some_text = f"{thing_name}:{' ' * (wordlength - len(thing_name))}"
        value_text = f"{round(value[0], 2)}"
        value_text = value_text + " " * (value_lengths[0] - len(value_text))
        base_text = f"[Base value: {value[1]}]"
        # base_text = base_text + " " * (value_lengths[1] - len(base_text))
        max_text = f"({round(value[2], 2)} with 200 infra)"
        max_text = max_text + " " * (value_lengths[2] - len(max_text))
        print(" " * indent_num, f"{some_text} {value_text} {max_text} {base_text}")
    # print(" " * indent_num, f"{things[3]}:{' ' * (wordlength - len(things[3]))} {round(province.get_ic(), 2)} \t[Base value: {province.ic}]")
    # print(" " * indent_num, f"{things[4]}:{' ' * (wordlength - len(things[4]))} {round(province.get_energy(), 2)} \t[Base value: {province.energy}]")
    # print(" " * indent_num, f"{things[5]}:{' ' * (wordlength - len(things[5]))} {round(province.get_metal(), 2)} \t[Base value: {province.metal}]")
    # print(" " * indent_num, f"{things[6]}:{' ' * (wordlength - len(things[6]))} {round(province.get_rares(), 2)} \t[Base value: {province.rares}]")
    # print(" " * indent_num, f"{things[7]}:{' ' * (wordlength - len(things[7]))} {round(province.get_oil(), 2)} \t[Base value: {province.oil}]")
