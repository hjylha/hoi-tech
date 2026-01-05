
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

def domestic_change_as_str(effect, text_dict, current_value=None):
    # are these correct?
    slider_dict = {
        "democratic": "DOMNAME_DEM_L",
        "political_left": "DOMNAME_DOMNAME_POL_L",
        "freedom": "DOMNAME_FRE_L",
        "free_market": "DOMNAME_FRM_L",
        "professional_army": "DOMNAME_PRO_L",
        "defense_lobby": "DOMNAME_DEF_L",
        "interventionism": "DOMNAME_INT_L"
    }
    the_key = "EE_DOMESTIC"
    extra_key = "EE_DOMESTIC_CURRENT"
    slider_key = slider_dict[effect.which]
    current_value_str = "?" if current_value is None else str(current_value)
    part1 = text_dict[the_key].replace("%d", str(effect.value)).replace("%s", text_dict[slider_key])
    part2 = text_dict[extra_key].replace("%d", current_value_str)
    return f"{part1} {part2}"

def manpowerpool_change_as_str(effect, text_dict):
    the_key = "EE_MANPOWER"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%d", str(effect.value))

def peacetime_ic_change_as_str(effect, text_dict):
    the_key = "EE_PEACETIME_IC_MOD"
    sign = "+" if effect.value > 0 else ""
    return text_dict[the_key].replace("%s", sign).replace("%.1f\\%%", f"{effect.value}%")


def effect_as_str(effect, text_dict, **kwargs):
    if effect.type == "domestic":
        return domestic_change_as_str(effect, text_dict)
    if effect.type == "manpowerpool":
        return manpowerpool_change_as_str(effect, text_dict)
    if effect.type == "peacetime_ic_mod":
        return peacetime_ic_change_as_str(effect, text_dict)
    #TODO: this is my own
    if effect.type == "trigger" and "event_dict" in kwargs:
        return f"Triggers event {effect.which}: {event_dict[effect.which].name}"
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
    

def print_effect(effect, indent_num, text_dict, **kwargs):
    print(indent_num * " ", effect_as_str(effect, text_dict))
    

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

def print_condition(condition, **kwargs):
    pass


def print_condition(condition, indent_num, indent_add):
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

def print_trigger(event, indent_num, indent_add, empty_trigger=True):
    if not event.trigger.raw_conditions and empty_trigger:
        print(indent_num * " ", "-")
        return
    if not event.trigger.raw_conditions:
        return
    event.trigger.print_condition(indent_num, 2 * indent_add)

def print_action(action, indent_num, indent_add, text_dict):
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
        print_effect(effect, indent_num, text_dict)

def print_event(event, aod_path, indent_num, indent_add, text_dict):
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
    print_trigger(event, indent_num + indent_add, indent_add, empty_trigger=trigger_empty)
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
        print_action(action, indent_num, indent_add, text_dict)