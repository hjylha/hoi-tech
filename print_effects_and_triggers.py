
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

def access_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_ACCESS"
    return text_dict[the_key].replace("%s", country_dict[effect.which])

def addcore_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ADDCORE"
    province_key = f"PROV{effect.which}"
    # added province id for "clarity"
    return text_dict[the_key].replace("%s", f"{text_dict[province_key]} [{effect.which}]")

def alliance_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_ALL"
    return text_dict[the_key].replace("%s", country_dict[effect.which])

def belligerence_change_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_BELLIGERENCE"
    raw_text = text_dict[the_key].split("%s")
    country = country_dict[effect.which]
    sign = "+" if effect.value > 0 else ""
    text = raw_text[0] + country + raw_text[1] + sign + raw_text[2]
    return text.replace("%.1f\\%", str(effect.value)).replace("\\n", "")

def dissent_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_DISSENT"
    return text_dict[the_key].replace("%d", str(effect.value))

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

def energypool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_ENERGY_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def manpowerpool_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MANPOWER"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%d", str(effect.value))

def metalpool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_METAL_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def money_as_str(effect, text_dict, **kwargs):
    the_key = "EE_MONEY"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%+.1f", f"{sign}{effect.value}")

def oilpool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_OIL_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def peacetime_ic_change_as_str(effect, text_dict, **kwargs):
    the_key = "EE_PEACETIME_IC_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%.1f\\%%", f"{effect.value}%")

def rarematerialspool_as_str(effect, text_dict, **kwargs):
    the_key = "EE_RARE_MATERIALS_POOL"
    return text_dict[the_key].replace("%d", str(effect.value))

def relation_change_as_str(effect, text_dict, country_dict=None, **kwargs):
    if country_dict is None:
        return
    the_key = "EE_RELATION"
    sign = "+" if effect.value > 0 else ""
    raw_text = text_dict[the_key].split("%s")
    text = f"{raw_text[0]}{country_dict[effect.which]}{raw_text[1]}{sign}{raw_text[2]}"
    return text.replace("%d", str(effect.value))

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
    return text.replace("%.1f\\%%", f"{effect.value}%")

def sleepevent_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_SLEEP"
    raw_text = text_dict[the_key].replace("%s", event_dict[effect.which].name)
    # my own additions
    name_w_quotes = f"'{event_dict[effect.which].name}'"
    add = f" [{event_dict[effect.which].country} {effect.which}]"
    return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]

def trigger_as_str(effect, text_dict, event_dict=None, **kwargs):
    if event_dict is None:
        return
    the_key = "EE_TRIGGER"
    raw_text = text_dict[the_key].replace("%s", event_dict[effect.which].name)
    # my own additions
    name_w_quotes = f"'{event_dict[effect.which].name}'"
    add = f" [{event_dict[effect.which].country} {effect.which}]"
    return raw_text[:raw_text.index(name_w_quotes) + len(name_w_quotes)] + add + raw_text[raw_text.index(name_w_quotes) + len(name_w_quotes):]


def effect_as_str(effect, text_dict, event_dict=None, country_dict=None, force_default=False, **kwargs):
    if force_default:
        return effect_as_str_default(effect)
    function_dict = {
        "access": access_as_str,
        "addcore": addcore_as_str,
        "alliance": alliance_as_str,
        "belligerence": belligerence_change_as_str,
        "dissent": dissent_change_as_str,
        "domestic": domestic_change_as_str,
        "energypool": energypool_as_str,
        "manpowerpool": manpowerpool_change_as_str,
        "metalpool": metalpool_as_str,
        "money": money_as_str,
        "oilpool": oilpool_as_str,
        "peacetime_ic_mod": peacetime_ic_change_as_str,
        "rarematerialspool": rarematerialspool_as_str,
        "relation": relation_change_as_str,
        "resource": resource_as_str,
        "set_domestic": set_domestic_as_str,
        "sleepevent": sleepevent_as_str,
        "trigger": trigger_as_str
    }
    the_function = function_dict.get(effect.type.lower())
    if the_function is not None:
        return the_function(effect, text_dict=text_dict, event_dict=event_dict, country_dict=country_dict, **kwargs)
    
    return effect_as_str_default(effect)
    

def print_effect(effect, indent_num, text_dict, event_dict=None, country_dict=None, force_default=False, **kwargs):
    print(indent_num * " ", effect_as_str(effect, text_dict, event_dict, country_dict, force_default, **kwargs))
    

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

def print_action(action, indent_num, indent_add, text_dict, event_dict, country_dict=None, force_default=False, **kwargs):
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
        print_effect(effect, indent_num, text_dict, event_dict, country_dict, force_default, **kwargs)

def print_event(event, aod_path, indent_num, indent_add, text_dict, event_dict, country_dict, force_default=False, **kwargs):
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
        print_action(action, indent_num, indent_add, text_dict, event_dict, country_dict, force_default, **kwargs)