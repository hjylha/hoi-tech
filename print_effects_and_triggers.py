
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

BUILDING_DICT = {
    "ic": "Industrial Capacity",
    "infrastructure": "Infrastructure",
    "flak": "Anti-Air",
    "nuclear_reactor": "Nuclear Reactor",
    "nuclear_power": "Nuclear Power plant",
    "synthetic_oil": "Synthetic Oil plant",
    "synthetic_rares": "Synthetic Material plant",
    "coastal_fort": "Coastal Fortifications",
    "land_fort": "Land Fortifications",
    "air_base": "Air Base",
    "naval_base": "Naval Base",
    "radar_station": "Radar Station",
    "rocket_test": "Rocket Test Site"
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

def access_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_ACCESS"
    return text_dict[the_key].replace("%s", country_dict[effect.which])

def activate_as_str(effect, text_dict, tech_dict=None, **kwargs):
    if tech_dict is None:
        return
    the_key = "EE_ACTIVATE_TECH"
    return text_dict[the_key].replace("%s", f"{effect.which} {tech_dict[effect.which].name}")

def activate_division_as_str(effect, text_dict, **kwargs):
    pass

def activate_unit_type_as_str(effect, text_dict, **kwargs):
    # unit_dict = {
    #     "infantry": SNAME_INFANTRY
    # }
    the_key = "EE_ACTIVATE_UNIT_TYPE"
    unit_name = get_unit_name(effect.which, text_dict)
    return f"{text_dict[the_key]}: {unit_name}"

def add_corps_as_str(effect, text_dict, **kwargs):
    pass

def add_division_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADD_DIVISION"
    unit_name = get_unit_name(effect.value, text_dict, False)
    model_name = get_model_name(effect.value, effect.when, text_dict)
    return f"{text_dict[the_key].replace("%s", unit_name)} [{model_name}]"

def add_prov_resource_as_str(effect, text_dict, **kwargs):
    resource_dict = {
        "energy": "RESOURCE_ENERGY",
        "metal": "RESOURCE_METAL",
        "oil": "RESOURCE_OIL",
        "rare_materials": "RESOURCE_RARE_MATERIALS",
        "money": "RESOURCE_MONEY",
        "supplies": "RESOURCE_SUPPLY",
        # "manpower": "RESOURCE_MANPOWER"
    }
    the_key = "EE_ADD_PROV_RESOURCE"
    resource = text_dict[resource_dict[effect.where]]
    province = text_dict.get(f"PROV{effect.which}")
    province = province if province else str(effect.which)
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    text = f"{raw_text[0]}{resource}{raw_text[1]}{province}{raw_text[2]}"
    return text.replace("%+.1f\\%%\\n", f"{sign}{effect.value}")

def addcore_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADDCORE"
    province_key = f"PROV{effect.which}"
    # added province id for "clarity"
    return text_dict[the_key].replace("%s", f"{text_dict[province_key]} [{effect.which}]")

def ai_as_str(effect, text_dict, **kwargs):
    pass

def ai_prepare_war_as_str(effect, text_dict, **kwargs):
    pass

def alliance_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_ALL"
    return text_dict[the_key].replace("%s", country_dict[effect.which])

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

def armamentminister_as_str(effect, text_dict, **kwargs):
    pass

def army_detection_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ARMY_DETECTION"
    second_key = f"EE_{effect.which.upper()}"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]} {text_dict[second_key]} {sign}{effect.value} %"

def belligerence_change_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_BELLIGERENCE"
    raw_text = text_dict[the_key].split("%s")
    country = country_dict[effect.which]
    sign = "+" if effect.value > 0 else ""
    text = raw_text[0] + country + raw_text[1] + sign + raw_text[2]
    return text.replace("%.1f\\%", str(effect.value)).replace("\\n", "")

def build_cost_as_str(effect, text_dict, **kwargs):
    # RELATIVE ruins everything
    key1 = "EE_BUILD_COST"
    key2 = "T_IC"
    placeholder_text = f"%s: {text_dict[key1]} %d {text_dict[key2]}"
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(placeholder_text, unit_name, effect.value, True)

def build_division_as_str(effect, text_dict, **kwargs):
	pass

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
    province = text_dict.get(f"PROV{effect.which}")
    province = province if province else str(effect.which)
    return f"{text_dict[the_key].replace("%s", f"{effect.which} {province}")} (if possible)"

def carrier_level_as_str(effect, text_dict, **kwargs):
    the_key = "EE_CARRIER_LEVEL"
    return f"{text_dict[the_key]}: {effect.value}"

def change_policy_as_str(effect, text_dict, **kwargs):
	pass

def chiefofair_as_str(effect, text_dict, **kwargs):
	pass

def chiefofarmy_as_str(effect, text_dict, **kwargs):
	pass

def chiefofnavy_as_str(effect, text_dict, **kwargs):
	pass

def chiefofstaff_as_str(effect, text_dict, **kwargs):
	pass

def civil_war_as_str(effect, text_dict, **kwargs):
	pass

def clrflag_as_str(effect, text_dict, **kwargs):
	pass

def coast_fort_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_COAST_FORT_EFF"
    sign = "+" if effect.value > 0 else ""
    return f"{text_dict[the_key]}: {sign}{effect.value}"

def construct_as_str(effect, text_dict, **kwargs):
    province = text_dict.get(f"PROV{effect.where}")
    province = province if province else str(effect.where)
    building_name = BUILDING_DICT.get(effect.which)
    building_name = building_name if building_name else f"{effect.which}*"
    sign = "+" if effect.value > 0 else ""
    return f"{building_name} in {province}: {sign}{effect.value}"

def control_as_str(effect, text_dict, **kwargs):
	pass

def convoy_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

def damage_division_as_str(effect, text_dict, **kwargs):
	pass

def deactivate_as_str(effect, text_dict, tech_dict=None, **kwargs):
    if tech_dict is None:
        return
    the_key = "EE_DEACTIVATE_TECH"
    return f"{text_dict[the_key]}: \n  {effect.which} {tech_dict[effect.which].name}"

def delete_unit_as_str(effect, text_dict, **kwargs):
	pass

def disorg_division_as_str(effect, text_dict, **kwargs):
	pass

def domestic_change_as_str(effect, text_dict, current_value=None, **kwargs):
    # are these correct?
    slider_dict = {
        "democratic": ["DOMNAME_DEM_L", "DOMNAME_DEM_R"],
        "political_left": ["DOMNAME_POL_L", "DOMNAME_POL_R"],
        "freedom": ["DOMNAME_FRE_L", "DOMNAME_FRE_R"],
        "free_market": ["DOMNAME_FRM_L", "DOMNAME_FRM_R"],
        "professional_army": ["DOMNAME_PRO_L", "DOMNAME_PRO_R"],
        "defense_lobby": ["DOMNAME_DEF_L", "DOMNAME_DEF_R"],
        "interventionism": ["DOMNAME_INT_L", "DOMNAME_INT_R"]
    }
    the_key = "EE_DOMESTIC"
    extra_key = "EE_DOMESTIC_CURRENT"
    direction = 0 if effect.value > 0 else 1
    slider_key = slider_dict[effect.which][direction]
    current_value_str = "?" if current_value is None else str(current_value)
    part1 = text_dict[the_key].replace("%d", str(abs(effect.value))).replace("%s", text_dict[slider_key])
    part2 = text_dict[extra_key].replace("%d", current_value_str)
    return f"{part1} {part2}"

# almost the same?
def set_domestic_as_str(effect, text_dict, **kwargs):
    slider_dict = {
        "democratic": ["DOMNAME_DEM_L", "DOMNAME_DEM_R"],
        "political_left": ["DOMNAME_POL_L", "DOMNAME_POL_R"],
        "freedom": ["DOMNAME_FRE_L", "DOMNAME_FRE_R"],
        "free_market": ["DOMNAME_FRM_L", "DOMNAME_FRM_R"],
        "professional_army": ["DOMNAME_PRO_L", "DOMNAME_PRO_R"],
        "defense_lobby": ["DOMNAME_DEF_L", "DOMNAME_DEF_R"],
        "interventionism": ["DOMNAME_INT_L", "DOMNAME_INT_R"]
    }
    slider = text_dict[slider_dict[effect.which][0]]
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
    # mission_key = f"MISSION_{effect.which.upper()}"
    return text_dict[the_key].replace("%s", text_dict[mission_key])

def end_access_as_str(effect, text_dict, **kwargs):
	pass

def end_guarantee_as_str(effect, text_dict, **kwargs):
	pass

def end_mastery_as_str(effect, text_dict, **kwargs):
	pass

def end_non_aggression_as_str(effect, text_dict, **kwargs):
	pass

def end_puppet_as_str(effect, text_dict, **kwargs):
	pass

def end_trades_as_str(effect, text_dict, **kwargs):
	pass

def energypool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ENERGY_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def escort_pool_as_str(effect, text_dict, **kwargs):
	pass

def extra_tc_as_str(effect, text_dict, **kwargs):
	pass

def foreignminister_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

def headofgovernment_as_str(effect, text_dict, **kwargs):
	pass

def headofstate_as_str(effect, text_dict, **kwargs):
	pass

def hq_supply_eff_as_str(effect, text_dict, **kwargs):
    the_key = "EE_HQ_SUPPLY_EFF"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value} %")

def independence_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

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
	pass

def local_clrflag_as_str(effect, text_dict, **kwargs):
	pass

def local_setflag_as_str(effect, text_dict, **kwargs):
	pass

def make_puppet_as_str(effect, text_dict, **kwargs):
	pass

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
    return text_dict[the_key].replace("%d", str(effect.value))

def min_positioning_as_str(effect, text_dict, **kwargs):
    raw_text = text_dict["EE_MIN_POSITIONING"].replace("%+.1f\\%%\\n", "%d")
    unit_name = get_unit_name(effect.which, text_dict)
    return replace_string_and_number(raw_text, unit_name, effect.value)

def ministerofintelligence_as_str(effect, text_dict, **kwargs):
	pass

def ministerofsecurity_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

def nuclear_carrier_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NUCLEAR_CARRIER_NEW"
    # unit_name = get_unit_name(effect.which, text_dict)
    unit_name = text_dict[f"NAME_{effect.which.upper()}"]
    return text_dict[the_key].replace("%s", unit_name)

def nuke_damage_as_str(effect, text_dict, **kwargs):
    the_key = "EE_NUKE_DAMAGE"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("+", f"{sign}{effect.value} %")

def oilpool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_OIL_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def peace_as_str(effect, text_dict, **kwargs):
	pass

def peacetime_ic_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_PEACETIME_IC_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%.1f\\%%", f"{effect.value} %")

def province_keypoints_as_str(effect, text_dict, **kwargs):
    the_key = "EE_KEYPOINTS"
    province = text_dict.get(f"PROV{effect.which}")
    province = province if province else str(effect.which)
    return replace_string_and_number(text_dict[the_key], province, effect.value)

def province_manpower_as_str(effect, text_dict, **kwargs):
    the_key = "EE_P_MAN"
    sign = "+" if effect.value > 0 else ""
    province = text_dict.get(f"PROV{effect.which}")
    province = province if province else str(effect.which)
    return text_dict[the_key].replace("%s%d", f"{sign}{effect.value}").replace("%s", province)

def province_revoltrisk_as_str(effect, text_dict, **kwargs):
    the_key = "EE_P_RR"
    province = text_dict.get(f"PROV{effect.which}")
    province = province if province else str(effect.which)
    return replace_string_and_number(text_dict[the_key].replace("%s%d", "%d"), province, effect.value)


def rarematerialspool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RARE_MATERIALS_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def regime_falls_as_str(effect, text_dict, **kwargs):
	pass

def relation_change_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_RELATION"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    text = f"{raw_text[0]}{country_dict[effect.which.upper()]}{raw_text[1]}{sign}{raw_text[2]}"
    return text.replace("%d", str(effect.value))

def relative_manpower_as_str(effect, text_dict, **kwargs):
    the_key = "DOMESTIC_PRA_MAN"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value} %")

def remove_division_as_str(effect, text_dict, **kwargs):
	pass

def removecore_as_str(effect, text_dict, **kwargs):
	pass

def research_mod_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RESEARCH_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%.1f\\%%\\n", f"{sign}{effect.value}")

def research_sabotaged_as_str(effect, text_dict, **kwargs):
	pass

def resource_as_str(effect, text_dict, **kwargs):
    # how many things are here?
    resource_dict = {
        "energy": "RESOURCE_ENERGY",
        "metal": "RESOURCE_METAL",
        "oil": "RESOURCE_OIL",
        "rare_materials": "RESOURCE_RARE_MATERIALS",
        "money": "RESOURCE_MONEY",
        "supplies": "RESOURCE_SUPPLY",
        # "manpower": "RESOURCE_MANPOWER"
    }
    the_key = "EE_RESOURCE"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    text = f"{raw_text[0]}{text_dict[resource_dict[effect.which]]}{raw_text[1]}{sign}{raw_text[2]}"
    return text.replace("%.1f\\%%", f"{effect.value} %")

def revolt_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

def set_leader_skill_as_str(effect, text_dict, **kwargs):
	pass

def set_relation_as_str(effect, text_dict, **kwargs):
	pass

def setflag_as_str(effect, text_dict, **kwargs):
	pass

def sleepevent_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_SLEEP"
    raw_text = text_dict[the_key].replace("%s", event_dict[effect.which].name)
    # my own additions
    name_w_quotes = f"'{event_dict[effect.which].name}'"
    add = f" [{event_dict[effect.which].country} {effect.which}]"
    return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]

def sleepleader_as_str(effect, text_dict, **kwargs):
	pass

def sleepminister_as_str(effect, text_dict, **kwargs):
	pass

def sleepteam_as_str(effect, text_dict, **kwargs):
	pass

def steal_tech_as_str(effect, text_dict, **kwargs):
	pass

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
	pass

def task_efficiency_as_str(effect, text_dict, **kwargs):
    the_key = "EE_TASK_EFFICIENCY"
    raw_text = text_dict[the_key].replace("%+.1f\\%%\\n", "%d")
    exceptions = {
        "amphibious_assault": "MISSION_AMPHIBOUS_ASSAULT"
    }
    mission_key = exceptions.get(effect.which)
    mission_key = mission_key if mission_key else f"MISSION_{effect.which.upper()}"
    # mission_key = f"MISSION_{effect.which.upper()}"
    return replace_string_and_number(raw_text, text_dict[mission_key], effect.value)

def transport_pool_as_str(effect, text_dict, **kwargs):
	pass

def trigger_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_TRIGGER"
    raw_text = text_dict[the_key].replace("%s", event_dict[effect.which].name)
    # my own additions
    name_w_quotes = f"'{event_dict[effect.which].name}'"
    add = f" [{event_dict[effect.which].country} {effect.which}]"
    return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]

def visibility_as_str(effect, text_dict, **kwargs):
	pass

def vp_as_str(effect, text_dict, **kwargs):
    the_key = "EE_VP"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s%d", f"{sign}{effect.value}")

def wakeleader_as_str(effect, text_dict, **kwargs):
	pass

def waketeam_as_str(effect, text_dict, **kwargs):
	pass

def war_as_str(effect, text_dict, **kwargs):
	pass


STR_FUNCTION_DICT = {
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
    # "air_attack": air_attack_as_str,
    # "air_defense": air_defense_as_str,
    # "air_detection": air_detection_as_str,
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


def effect_as_str(effect, text_dict, event_dict=None, country_dict=None, tech_dict=None, force_default=False, **kwargs):
    if force_default:
        return effect_as_str_default(effect)
    the_function = STR_FUNCTION_DICT.get(effect.type.lower())
    if the_function is None:
        print("PROBLEM:", effect.type)
    # if the_function is not None:
    #     the_text = the_function(effect, text_dict=text_dict, event_dict=event_dict, country_dict=country_dict, **kwargs)
    the_text = STR_FUNCTION_DICT.get(effect.type.lower())(effect, text_dict=text_dict, event_dict=event_dict, country_dict=country_dict, tech_dict=tech_dict, **kwargs)
    if the_text:
        return the_text
    
    return effect_as_str_default(effect)
    

def print_effect(effect, indent_num, text_dict, event_dict=None, country_dict=None, tech_dict=None, force_default=False, **kwargs):
    print(indent_num * " ", effect_as_str(effect, text_dict, event_dict, country_dict, tech_dict, force_default=force_default, **kwargs))
    

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

# def print_condition(condition, **kwargs):
#     pass


def print_condition(condition, indent_num, indent_add, **kwargs):
    if condition.condition is not None:
        if condition.connective and condition.connective == condition.NOT_STR:
            print(indent_num * " ", f"{condition.NOT_STR} (", end=" ")
        else:
            print(indent_num * " ", end=" ")
        first = True
        for key, value in condition.condition.items():
            if not first:
                print(", ", end="")
            else:
                first = False
            print(f"{key} = {value}", end="")
        if condition.connective and condition.connective == condition.NOT_STR:
            print(" )", end="\n")
        else:
            print()
        return
    if condition.connective:
        print(indent_num * " ", condition.connective)
        for condition in condition.child_conditions:
            condition.print_condition(indent_num + indent_add, indent_add)
    else:
        for condition in condition.child_conditions:
            condition.print_condition(indent_num, indent_add)

def print_trigger(event, indent_num, indent_add, empty_trigger=True, **kwargs):
    if not event.trigger.raw_conditions and empty_trigger:
        print(indent_num * " ", "-")
        return
    if not event.trigger.raw_conditions:
        return
    event.trigger.print_condition(indent_num, 2 * indent_add)

def print_action(action, indent_num, indent_add, text_dict, event_dict, country_dict=None, tech_dict=None, force_default=False, **kwargs):
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
    for effect in action.effects:
        print_effect(effect, indent_num, text_dict, event_dict, country_dict, tech_dict, force_default=force_default, **kwargs)

def print_event(event, aod_path, indent_num, indent_add, text_dict, event_dict, country_dict, tech_dict, force_default=False, **kwargs):
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
    print_trigger(event, indent_num + indent_add, indent_add, empty_trigger=trigger_empty, **kwargs)
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
        print_action(action, indent_num, indent_add, text_dict, event_dict, country_dict, tech_dict, force_default=force_default, **kwargs)
    

def list_tech_effects(tech, text_dict, tech_dict, **kwargs):
    effect_strs = []
    research_speed_change = []
    for effect in tech.effects:
        if effect.type == "research_mod":
            research_speed_change.append(effect_as_str(effect, text_dict))
            continue
        effect_str = effect_as_str(effect, text_dict, tech_dict=tech_dict)
        for eff_str in effect_str.split("\n"):
            effect_strs.append(eff_str)
    return research_speed_change + effect_strs
