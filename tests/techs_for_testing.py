import fix_imports
from classes import Component, Effect, Tech


def get_techs_for_testing():
	techs_for_testing = dict()

	components = (Component('naval_engineering', 6), Component('naval_engineering', 6), Component('naval_artillery', 6), Component('electronics', 6), Component('technical_efficiency', 6))
	effects = (Effect('new_model', 'submarine', 1, None, None), Effect('activate_unit_type', 'naval_torpedoes_s', None, None, None), Effect('new_model', 'naval_torpedoes_s', 0, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[3330] = Tech(3330, 'Coastal Submarine', 'Coastal', 'techs_for_testing.py', 'naval', [3320], components, effects)

	components = (Component('mathematics', 2), Component('electronics', 2), Component('electronics', 2), Component('mechanics', 2), Component('technical_efficiency', 2))
	effects = (Effect('intelligence', 'us', 4, None, None), Effect('intelligence', 'them', -2, None, None), Effect('surprise', 'naval', 2, None, None), Effect('surprise', 'land', 2, None, None), Effect('surprise', 'air', 2, None, None), Effect('army_detection', 'us', 4, None, None), Effect('army_detection', 'them', -2, None, None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[1670] = Tech(1670, 'Electronic Warfare', 'Electronic Warfare', 'techs_for_testing.py', 'infantry', [], components, effects)

	components = (Component('mathematics', 2), Component('naval_engineering', 2), Component('naval_engineering', 2), Component('electronics', 2), Component('naval_training', 2))
	effects = (Effect('max_organization', 'transport', 7, None, None), Effect('speed', 'transport', 2, 'on_upgrade', None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[3720] = Tech(3720, 'Landing Craft Support', 'Landing Craft Sup', 'techs_for_testing.py', 'naval', [], components, effects)

	components = (Component('aeronautics', 6), Component('aeronautics', 6), Component('chemistry', 6), Component('mechanics', 6), Component('technical_efficiency', 6))
	effects = (Effect('activate_unit_type', 'strategic_bomber', None, None, None), Effect('new_model', 'strategic_bomber', 0, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[4370] = Tech(4370, 'Basic Strategic Bomber', 'Basic Strat. Bomber', 'techs_for_testing.py', 'aircraft', [4230], components, effects)

	components = (Component('mathematics', 5), Component('mathematics', 5), Component('artillery', 5), Component('mechanics', 5), Component('training', 5))
	effects = (Effect('activate_unit_type', 'light_armor', None, None, None), Effect('new_model', 'light_armor', 0, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[2070] = Tech(2070, 'Light Tank Prototypes', 'Light Prototypes', 'techs_for_testing.py', 'armor', [2010], components, effects)

	components = (Component('small_unit_tactics', 2), Component('small_unit_tactics', 2), Component('individual_courage', 2), Component('infantry_focus', 2), Component('training', 2))
	effects = (Effect('attrition_mod', None, 5, None, None), Effect('morale', 'land', 1, None, None), Effect('research_mod', None, 0.3, None, None))
	techs_for_testing[6680] = Tech(6680, 'Small Units Doctrine', 'Small Units', 'techs_for_testing.py', 'land_doctrines', [], components, effects)

	components = (Component('mathematics', 10), Component('mathematics', 10), Component('mechanics', 10), Component('chemistry', 10), Component('aeronautics', 10))
	effects = (Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[4520] = Tech(4520, 'Jet Engine Concepts', 'Jet Concepts', 'techs_for_testing.py', 'aircraft', [], components, effects)

	components = (Component('nuclear_engineering', 18), Component('naval_engineering', 18), Component('nuclear_physics', 18), Component('nuclear_engineering', 18), Component('naval_engineering', 18))
	effects = (Effect('new_model', 'carrier', 9, None, None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[7210] = Tech(7210, 'Nuclear Carrier Vessel Propulsion', 'Nuclear Carrier', 'techs_for_testing.py', 'secret_weapons', [3560, 7140], components, effects)

	components = (Component('centralized_execution', 4), Component('fighter_tactics', 4), Component('bomber_tactics', 4), Component('combined_arms_focus', 4), Component('aircraft_testing', 4))
	effects = (Effect('max_organization', 'interceptor', 3, None, None), Effect('morale', 'interceptor', 3, None, None), Effect('max_organization', 'tactical_bomber', 3, None, None), Effect('morale', 'tactical_bomber', 3, None, None), Effect('research_mod', None, 0.8, None, None))
	techs_for_testing[9010] = Tech(9010, 'Air Power Doctrine', 'Air Power', 'techs_for_testing.py', 'air_doctrines', [], components, effects)

	components = (Component('rocketry', 5), Component('mechanics', 5), Component('mechanics', 5), Component('chemistry', 5), Component('training', 5))
	effects = (Effect('activate_unit_type', 'sp_rct_artillery', None, None, None), Effect('new_model', 'sp_rct_artillery', 0, None, None), Effect('soft_attack', 'mechanized', 1, 'on_upgrade', None), Effect('soft_attack', 'light_armor', 1, 'on_upgrade', None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[2610] = Tech(2610, 'Self-Propelled Rocket Artillery Prototypes', 'techs_for_testing.py', 'Self-Prop. Rocket', 'armor', [2570, 2090], components, effects)

	components = (Component('aeronautics', 4), Component('aeronautics', 4), Component('artillery', 4), Component('mechanics', 4), Component('technical_efficiency', 4))
	effects = (Effect('new_model', 'multi_role', 1, None, None), Effect('new_model', 'interceptor', 1, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[4020] = Tech(4020, 'Interceptor/Fighter Prototypes', 'Int./Fighter Prototypes', 'techs_for_testing.py', 'aircraft', [4010], components, effects)

	components = (Component('artillery', 8), Component('general_equipment', 8), Component('general_equipment', 8), Component('training', 8), Component('artillery', 8))
	effects = (Effect('new_model', 'infantry', 1, None, None), Effect('activate_unit_type', 'garrison', None, None, None), Effect('new_model', 'garrison', 0, None, None), Effect('new_model', 'militia', 1, None, None), Effect('activate_unit_type', 'b_u7', None, None, None), Effect('new_model', 'b_u7', 0, None, None), Effect('enable_task', 'amphibious_assault', None, None, None), Effect('research_mod', None, 1, None, None))
	techs_for_testing[1080] = Tech(1080, 'Post-WWI Infantry', 'Post-WWI', 'techs_for_testing.py', 'infantry', [1070], components, effects)

	components = (Component('aeronautics', 4), Component('aeronautics', 4), Component('mechanics', 4), Component('electronics', 4), Component('technical_efficiency', 4))
	effects = (Effect('activate_unit_type', 'transport_plane', None, None, None), Effect('new_model', 'transport_plane', 0, None, None), Effect('paradrop_attack', 'paratrooper', 2, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[4280] = Tech(4280, 'Basic Air Transport', 'Basic Air Transport', 'techs_for_testing.py', 'aircraft', [4230], components, effects)

	components = (Component('aeronautics', 2), Component('aeronautics', 2), Component('electronics', 2), Component('aircraft_testing', 2), Component('piloting', 2))
	effects = (Effect('surface_detection', 'multi_role', 1, 'on_upgrade', None), Effect('air_detection', 'multi_role', 1, 'on_upgrade', None), Effect('air_detection', 'interceptor', 1, 'on_upgrade', None), Effect('surface_detection', 'interceptor', 1, 'on_upgrade', None), Effect('air_detection', 'escort', 1, 'on_upgrade', None), Effect('surface_detection', 'escort', 1, 'on_upgrade', None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[4670] = Tech(4670, 'Light Surveillance Aircraft', 'Light Surveillance', 'techs_for_testing.py', 'aircraft', [], components, effects)

	components = (Component('aeronautics', 5), Component('aeronautics', 5), Component('artillery', 5), Component('electronics', 5), Component('technical_efficiency', 5))
	effects = (Effect('new_model', 'multi_role', 2, None, None), Effect('scrap_model', 'multi_role', 0, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[4030] = Tech(4030, 'Basic Fighter', 'Basic Fighter', 'techs_for_testing.py', 'aircraft', [4020], components, effects)

	components = (Component('mathematics', 4), Component('mathematics', 4), Component('mathematics', 4), Component('management', 4), Component('mathematics', 4))
	effects = (Effect('research_mod', None, 2, None, None))
	techs_for_testing[5440] = Tech(5440, 'Study Centers', 'Study Centers', 'techs_for_testing.py', 'industry', [], components, effects)

	components = (Component('rocketry', 18), Component('rocketry', 18), Component('aeronautics', 18), Component('electronics', 18), Component('technical_efficiency', 18))
	effects = (Effect('info_may_cause', '7250', None, None, None), Effect('info_may_cause', '7380', None, None, None), Effect('research_mod', None, 1.3, None, None))
	techs_for_testing[4550] = Tech(4550, 'Standard Jet Engine', 'Standard Engine', 'techs_for_testing.py', 'aircraft', [4540, 5070], components, effects)

	components = (Component('small_taskforce_tactics', 4), Component('small_taskforce_tactics', 4), Component('centralized_execution', 4), Component('seamanship', 4), Component('naval_training', 4))
	effects = (Effect('deactivate', '8130', None, None, None), Effect('allow_convoy_escorts', None, None, None, None), Effect('max_positioning', 'battleship', 0.1, None, None), Effect('min_positioning', 'battleship', 0.06, None, None), Effect('max_positioning', 'battlecruiser', 0.08, None, None), Effect('min_positioning', 'battlecruiser', 0.04, None, None), Effect('max_positioning', 'heavy_cruiser', 0.1, None, None), Effect('min_positioning', 'heavy_cruiser', 0.06, None, None), Effect('research_mod', None, 0.8, None, None))
	techs_for_testing[8020] = Tech(8020, 'Sea Control Doctrine', 'Sea Control', 'techs_for_testing.py', 'naval_doctrines', [8010], components, effects)

	components = (Component('mathematics', 4), Component('mechanics', 4), Component('chemistry', 4), Component('technical_efficiency', 4), Component('management', 4))
	effects = (Effect('speed', 'light_armor', 3, 'on_upgrade', None), Effect('speed', 'armor', 3, 'on_upgrade', None), Effect('deactivate', '2660', None, None, None), Effect('deactivate', '2670', None, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[2650] = Tech(2650, 'Prioritize Speed', 'Prioritize Speed', 'techs_for_testing.py', 'armor', [], components, effects)

	components = (Component('training', 2), Component('general_equipment', 2), Component('training', 2), Component('artillery', 2), Component('electronics', 2))
	effects = (Effect('defensiveness', 'bergsjaeger', 2, 'on_upgrade', None), Effect('defensiveness', 'paratrooper', 2, 'on_upgrade', None), Effect('defensiveness', 'marine', 2, 'on_upgrade', None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[1630] = Tech(1630, 'Commando Units', 'Commando Units', 'techs_for_testing.py', 'infantry', [], components, effects)

	components = (Component('small_unit_tactics', 4), Component('mathematics', 4), Component('mechanics', 4), Component('artillery', 4), Component('training', 4))
	effects = (Effect('defensiveness', 'land', 1, 'on_upgrade', None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[2530] = Tech(2530, 'Armoured Car Prototypes', 'Armoured Car', 'techs_for_testing.py', 'armor', [], components, effects)

	components = (Component('centralized_execution', 4), Component('electronics', 4), Component('electronics', 4), Component('management', 4), Component('technical_efficiency', 4))
	effects = (Effect('task_efficiency', 'naval_port_strike', 0.05, None, None), Effect('task_efficiency', 'naval_airbase_strike', 0.05, None, None), Effect('task_efficiency', 'asw', 0.05, None, None), Effect('task_efficiency', 'convoy_raiding', 0.05, None, None), Effect('convoy_def_eff', None, 0.05, None, None), Effect('research_mod', None, 0.8, None, None))
	techs_for_testing[8680] = Tech(8680, 'Naval Intelligence Doctrine', 'Naval Intelligence', 'techs_for_testing.py', 'naval_doctrines', [], components, effects)

	components = (Component('nuclear_physics', 12), Component('chemistry', 12), Component('chemistry', 12), Component('nuclear_engineering', 12), Component('mechanics', 12))
	effects = (Effect('enable_task', 'nuke', None, None, None), Effect('max_reactor_size', None, 6, None, None), Effect(None, None, None, None, None), Effect('nuclear_carrier', 'flying_bomb', None, None, None), Effect('nuclear_carrier', 'flying_rocket', None, None, None), Effect('nuke_damage', None, 30, None, None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[7150] = Tech(7150, 'Nuclear Waste Bomb', 'Nuclear Waste Bomb', 'techs_for_testing.py', 'secret_weapons', [7140], components, effects)

	components = (Component('mathematics', 4), Component('mathematics', 4), Component('artillery', 4), Component('mechanics', 4), Component('training', 4))
	effects = (Effect('allow_building', 'flak', None, None, None), Effect('AA_batteries', None, 13, None, None), Effect('activate_unit_type', 'naval_anti_air_s', None, None, None), Effect('new_model', 'naval_anti_air_s', 0, None, None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[2290] = Tech(2290, 'Heavy Anti-Air Prototypes', 'Heavy Anti-Air', 'techs_for_testing.py', 'armor', [2010], components, effects)

	components = (Component('artillery', 4), Component('artillery', 4), Component('artillery', 4), Component('mechanics', 4), Component('artillery', 4))
	effects = (Effect('urban_attack', 'infantry', 1, None, None), Effect('urban_attack', 'motorized', 1, None, None), Effect('urban_attack', 'paratrooper', 1, None, None), Effect('soft_attack', 'infantry', 1, 'on_upgrade', None), Effect('soft_attack', 'bergsjaeger', 1, 'on_upgrade', None), Effect('soft_attack', 'garrison', 1, 'on_upgrade', None), Effect('defensiveness', 'garrison', 2, 'on_upgrade', None), Effect('soft_attack', 'marine', 1, 'on_upgrade', None), Effect('soft_attack', 'paratrooper', 1, 'on_upgrade', None), Effect('soft_attack', 'motorized', 1, 'on_upgrade', None), Effect('soft_attack', 'mechanized', 1, 'on_upgrade', None), Effect('research_mod', None, 0.7, None, None))
	techs_for_testing[1010] = Tech(1010, 'Basic Sub-Machine Gun', 'Basic SMG', 'techs_for_testing.py', 'infantry', [], components, effects)

	components = (Component('small_unit_tactics', 2), Component('centralized_execution', 2), Component('individual_courage', 2), Component('technical_efficiency', 2), Component('training', 2))
	effects = (Effect('urban_defense', 'militia', 14, None, None), Effect('urban_defense', 'infantry', 14, None, None), Effect('urban_defense', 'garrison', 14, None, None), Effect('urban_defense', 'paratrooper', 14, None, None), Effect('urban_defense', 'marine', 14, None, None), Effect('urban_defense', 'bergsjaeger', 14, None, None), Effect('urban_defense', 'motorized', 14, None, None), Effect('urban_defense', 'cavalry', 14, None, None), Effect('urban_defense', 'mechanized', 7, None, None), Effect('urban_defense', 'light_armor', 7, None, None), Effect('urban_defense', 'armor', 7, None, None), Effect('research_mod', None, 0.3, None, None))
	techs_for_testing[6770] = Tech(6770, 'Patrols Doctrine', 'Patrols', 'techs_for_testing.py', 'land_doctrines', [6690], components, effects)

	components = (Component('mathematics', 2), Component('mechanics', 2), Component('mechanics', 2), Component('mechanics', 2), Component('technical_efficiency', 2))
	effects = (Effect('speed', 'light_armor', 1, 'on_upgrade', None), Effect('speed', 'armor', 1, 'on_upgrade', None), Effect('research_mod', None, 0.5, None, None))
	techs_for_testing[2680] = Tech(2680, 'Basic Mechanical Components', 'Basic Mechanical', 'techs_for_testing.py', 'armor', [], components, effects)

	return techs_for_testing

techs_for_testing = get_techs_for_testing()
