import fix_imports
from classes import TechTeam


def get_teams_for_testing():
	teams_for_testing = dict()

	teams_for_testing[3842] = TechTeam(3842, 'Nikola Tesla', 'YUG', 9, 1930, 1943, ('mathematics', 'mechanics', 'electronics', 'technical_efficiency'))

	teams_for_testing[3] = TechTeam(3, 'I.G. Farben', 'GER', 9, 1930, 1970, ('chemistry', 'industrial_engineering', 'general_equipment', 'management', 'technical_efficiency'))

	teams_for_testing[900] = TechTeam(900, 'Canadian Enfield Arsenal', 'CAN', 7, 1930, 1970, ('artillery', 'general_equipment', 'training'))

	teams_for_testing[7] = TechTeam(7, 'Krupp', 'GER', 9, 1930, 1970, ('industrial_engineering', 'mechanics', 'technical_efficiency', 'artillery'))

	teams_for_testing[903] = TechTeam(903, 'de Havilland', 'CAN', 7, 1930, 1970, ('aeronautics', 'chemistry', 'electronics', 'technical_efficiency'))

	teams_for_testing[10] = TechTeam(10, 'Messerschmitt', 'GER', 9, 1930, 1970, ('aeronautics', 'rocketry', 'artillery', 'technical_efficiency'))

	teams_for_testing[2702] = TechTeam(2702, 'Stanislaw Ulam', 'POL', 7, 1930, 1938, ('nuclear_physics', 'nuclear_engineering', 'mathematics', 'chemistry'))

	teams_for_testing[143] = TechTeam(143, 'William D. Leahy', 'USA', 5, 1930, 1939, ('large_taskforce_tactics', 'centralized_execution', 'naval_training'))

	teams_for_testing[17] = TechTeam(17, 'Wernher von Braun', 'GER', 9, 1932, 1976, ('rocketry', 'aeronautics', 'technical_efficiency'))

	teams_for_testing[147] = TechTeam(147, 'Holland Smith', 'USA', 5, 1930, 1946, ('small_unit_tactics', 'decentralized_execution', 'training', 'combined_arms_focus'))

	teams_for_testing[1300] = TechTeam(1300, 'Aero', 'FIN', 5, 1930, 1970, ('aeronautics', 'technical_efficiency', 'electronics'))

	teams_for_testing[22] = TechTeam(22, 'Heinz Guderian', 'GER', 9, 1930, 1954, ('combined_arms_focus', 'small_unit_tactics', 'large_unit_tactics', 'decentralized_execution', 'training'))

	teams_for_testing[150] = TechTeam(150, 'John Kenneth Galbraith', 'USA', 7, 1930, 1970, ('mathematics', 'management', 'technical_efficiency'))

	teams_for_testing[2710] = TechTeam(2710, 'Marian Rejewski', 'POL', 7, 1930, 1939, ('mathematics', 'electronics'))

	teams_for_testing[153] = TechTeam(153, 'Studebaker', 'USA', 4, 1930, 1970, ('mechanics', 'rocketry', 'technical_efficiency'))

	teams_for_testing[1305] = TechTeam(1305, 'Carl Mannerheim', 'FIN', 7, 1930, 1970, ('infantry_focus', 'individual_courage', 'small_unit_tactics', 'centralized_execution'))

	teams_for_testing[161] = TechTeam(161, 'Lyman Briggs', 'USA', 5, 1930, 1941, ('management', 'nuclear_engineering', 'nuclear_physics'))

	teams_for_testing[163] = TechTeam(163, 'US Army Ordnance Corps', 'USA', 5, 1930, 1970, ('artillery', 'chemistry', 'electronics', 'general_equipment', 'mechanics'))

	teams_for_testing[7600] = TechTeam(7600, 'Afghan Air Force', 'AFG', 1, 1930, 1970, ('aeronautics', 'aircraft_testing', 'mechanics', 'piloting'))

	teams_for_testing[2901] = TechTeam(2901, 'Carbosin', 'ROM', 4, 1930, 1970, ('industrial_engineering', 'chemistry', 'management'))

	teams_for_testing[2904] = TechTeam(2904, 'Malaxa Works', 'ROM', 5, 1930, 1970, ('mechanics', 'artillery', 'technical_efficiency'))

	teams_for_testing[2910] = TechTeam(2910, 'Horia Macellariu', 'ROM', 2, 1930, 1945, ('submarine_tactics', 'naval_training', 'seamanship', 'centralized_execution'))

	teams_for_testing[2913] = TechTeam(2913, 'Henri Coanda', 'ROM', 5, 1930, 1944, ('rocketry', 'aeronautics', 'technical_efficiency'))

	teams_for_testing[101] = TechTeam(101, 'Christie', 'USA', 5, 1930, 1970, ('mechanics', 'artillery', 'training', 'mathematics'))

	teams_for_testing[2923] = TechTeam(2923, 'Petrobrazi', 'ROM', 7, 1930, 1970, ('chemistry', 'industrial_engineering', 'technical_efficiency'))

	teams_for_testing[108] = TechTeam(108, 'Marmon-Herrington', 'USA', 7, 1930, 1970, ('mechanics', 'technical_efficiency', 'chemistry', 'artillery'))

	teams_for_testing[110] = TechTeam(110, 'New York Naval Yard', 'USA', 7, 1930, 1970, ('naval_engineering', 'technical_efficiency', 'electronics', 'naval_artillery', 'mechanics'))

	teams_for_testing[113] = TechTeam(113, 'Raytheon', 'USA', 7, 1930, 1970, ('electronics', 'mathematics', 'management', 'mechanics'))

	teams_for_testing[114] = TechTeam(114, 'Robert Oppenheimer', 'USA', 9, 1930, 1953, ('nuclear_physics', 'nuclear_engineering', 'mathematics'))

	teams_for_testing[116] = TechTeam(116, 'Springfield Armory', 'USA', 7, 1930, 1970, ('chemistry', 'mechanics', 'artillery', 'general_equipment'))

	teams_for_testing[118] = TechTeam(118, 'Texas Oil Company', 'USA', 9, 1930, 1970, ('industrial_engineering', 'chemistry', 'technical_efficiency'))

	return teams_for_testing


techteams_for_testing = get_teams_for_testing()
