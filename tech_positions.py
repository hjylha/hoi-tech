
left0_x = 0.01
left1_x = 0.19
left2_x = 0.4
left3_x = 0.61
left4_x = 0.81

tech_positions = {
    # INFANTRY
    # machineguns
    1010: (left0_x, 0.885),
    1020: (left0_x, 0.845),
    1030: (left0_x, 0.805),
    1040: (left0_x, 0.765),
    1050: (left0_x, 0.725),
    1060: (left0_x, 0.685),

    # infantry
    1070: (left1_x, 0.96),
    1080: (left1_x, 0.925),
    1090: (left1_x, 0.885),
    1100: (left1_x, 0.845),
    1110: (left1_x, 0.805),
    1120: (left1_x, 0.765),
    1130: (left1_x, 0.725),
    1140: (left1_x, 0.685),

    # cavalry
    1260: (left0_x, 0.6),
    1270: (left0_x + 0.01, 0.565),
    1280: (left0_x + 0.01, 0.53),
    1290: (left0_x + 0.01, 0.495),
    1760: (left0_x + 0.01, 0.46),

    # light vehicle
    1390: (left0_x - 0.01, 0.31),

    # mechanized
    1440: (left0_x, 0.205),
    1450: (left0_x, 0.17),
    1460: (left0_x, 0.135),
    1470: (left0_x, 0.1),

    # motorized
    1400: (left1_x, 0.205),
    1410: (left1_x, 0.17),
    1420: (left1_x, 0.135),
    1430: (left1_x, 0.1),

    # marines
    1300: (left1_x, 0.6),
    1310: (left1_x, 0.565),
    1320: (left1_x, 0.53),
    1330: (left1_x, 0.495),
    1340: (left1_x, 0.46),

    # specialization and equipment
    1150: (left2_x - 0.01, 0.885),
    1160: (left2_x, 0.83),
    1170: (left2_x + 0.02, 0.795),
    1180: (left2_x, 0.745),
    1190: (left2_x + 0.02, 0.71),
    1200: (left2_x, 0.66),
    1210: (left2_x + 0.02, 0.625),

    # mountain
    1220: (left3_x, 0.93),
    1230: (left3_x, 0.885),
    1240: (left3_x, 0.85),
    1250: (left3_x, 0.815),

    # paratroopers
    1350: (left3_x, 0.74),
    1360: (left3_x + 0.01, 0.705),
    1370: (left3_x + 0.01, 0.67),
    1380: (left3_x + 0.01, 0.635),

    # logistics
    # supply logistics
    1490: (left2_x + 0.02, 0.54),
    # concentrated
    1500: (left2_x + 0.02, 0.47),
    1510: (left2_x + 0.02, 0.435),
    1520: (left2_x + 0.02, 0.395),
    1530: (left2_x + 0.02, 0.36),
    # arsenal logistics
    1480: (left3_x - 0.02, 0.54),
    # dispersed
    1540: (left3_x - 0.02, 0.47),
    1550: (left3_x - 0.02, 0.435),
    1560: (left3_x - 0.02, 0.395),
    1570: (left3_x - 0.02, 0.36),
    # logistic management expert
    1580: (left2_x + 0.1, 0.29),

    # prioritization
    1590: (left4_x, 0.65),
    1600: (left4_x, 0.59),

    1610: (left4_x, 0.5),
    1620: (left4_x, 0.44),

    # commandos
    1630: (left4_x, 0.9),
    1640: (left4_x, 0.86),
    1650: (left4_x, 0.82),
    1660: (left4_x, 0.78),

    # electronic warfare
    1670: (left2_x + 0.01, 0.15),
    # jamming
    1680: (left3_x, 0.12),
    1690: (left3_x + 0.01, 0.085),
    1700: (left3_x + 0.02, 0.05),
    # basic signal detection
    1710: (left3_x, 0.21),
    1720: (left3_x + 0.01, 0.175),
    # detection of communications
    1730: (left4_x, 0.15),
    1740: (left4_x + 0.01, 0.115),
    1750: (left4_x + 0.01, 0.08),

    # ARMOR & ARTILLERY
    # light tanks
    2070: (left0_x, 0.95),
    2080: (left0_x, 0.915),
    2090: (left0_x, 0.88),
    2100: (left0_x, 0.845),
    2110: (left0_x, 0.81),

    # medium tanks
    2120: (left0_x, 0.75),
    2130: (left0_x, 0.715),
    2140: (left0_x, 0.68),
    2150: (left0_x, 0.645),

    # heavy tanks
    2160: (left0_x, 0.58),
    2170: (left0_x, 0.545),
    2180: (left0_x, 0.51),
    2190: (left0_x, 0.475),
    2200: (left0_x, 0.44),

    # prioritizations
    2650: (left0_x, 0.36),
    2660: (left0_x, 0.3),
    2670: (left0_x, 0.24),

    # mechanical parts
    2680: (left0_x, 0.165),
    2690: (left0_x + 0.02, 0.13),
    2700: (left0_x + 0.02, 0.095),
    2710: (left0_x + 0.02, 0.06),

    2720: (left1_x, 0.15),
    2730: (left1_x, 0.1),
    2740: (left1_x, 0.05),

    # fuses
    2040: (left1_x, 0.92),
    2050: (left1_x, 0.885),
    2060: (left1_x, 0.85),

    # guns
    2010: (left1_x, 0.75),
    2020: (left1_x, 0.7),
    2030: (left1_x, 0.65),

    # self-propelled artillery
    2490: (left1_x, 0.545),
    2500: (left1_x, 0.51),
    2510: (left1_x, 0.475),
    2520: (left1_x, 0.44),

    # self-propelled rocket artillery
    2610: (left1_x, 0.35),
    2620: (left1_x, 0.315),
    2630: (left1_x, 0.28),
    2640: (left1_x, 0.245),

    # tank destroyers
    2210: (left2_x, 0.95),
    2220: (left2_x, 0.915),
    2230: (left2_x, 0.88),
    2240: (left2_x, 0.845),

    # heavy anti-air
    2290: (left2_x, 0.75),
    2300: (left2_x, 0.715),
    2310: (left2_x, 0.68),
    2320: (left2_x, 0.645),
    2330: (left2_x, 0.61),

    # light artillery
    2440: (left2_x, 0.545),
    2450: (left2_x, 0.51),
    2460: (left2_x, 0.475),
    2470: (left2_x, 0.44),
    2480: (left2_x, 0.405),

    # rocket artillery
    2570: (left2_x, 0.35),
    2580: (left2_x, 0.315),
    2590: (left2_x, 0.28),
    2600: (left2_x, 0.245),

    # anti-tank guns
    2250: (left3_x, 0.95),
    2260: (left3_x, 0.915),
    2270: (left3_x, 0.88),
    2280: (left3_x, 0.845),

    # light anti-air
    2340: (left3_x, 0.75),
    2350: (left3_x, 0.715),
    2360: (left3_x, 0.68),
    2370: (left3_x, 0.645),
    2380: (left3_x, 0.61),

    # heavy artilley
    2390: (left3_x, 0.545),
    2400: (left3_x, 0.51),
    2410: (left3_x, 0.475),
    2420: (left3_x, 0.44),
    2430: (left3_x, 0.405),

    # cars
    2530: (left3_x, 0.35),
    2540: (left3_x + 0.01, 0.315),

    2550: (left3_x, 0.27),
    2560: (left3_x, 0.235),

    # armor
    2750: (left2_x, 0.15),
    2760: (left2_x + 0.01, 0.1),
    2770: (left2_x + 0.01, 0.05),

    2780: (left3_x, 0.15),
    2790: (left3_x + 0.01, 0.115),
    2800: (left3_x + 0.02, 0.08),
    2810: (left3_x + 0.03, 0.045),

    # special purpose vehicles
    2820: (left4_x - 0.01, 0.95),
    2830: (left4_x, 0.91),
    2840: (left4_x, 0.875),
    2850: (left4_x, 0.84),
    2860: (left4_x, 0.805),
    2870: (left4_x, 0.77),

    # amphibious
    2880: (left4_x - 0.01, 0.6),
    2890: (left4_x, 0.56),
    2900: (left4_x, 0.525),
    2910: (left4_x, 0.49),
    2920: (left4_x, 0.455),
    2930: (left4_x, 0.42),

    # NAVAL
    # battleships
    3120: (left0_x, 0.925),
    3130: (left0_x, 0.89),
    3140: (left0_x, 0.855),
    3150: (left0_x, 0.82),
    3160: (left0_x, 0.785),
    3170: (left0_x, 0.75),
    3180: (left0_x, 0.715),
    3190: (left0_x, 0.68),

    # destroyers
    3200: (left0_x, 0.61),
    3210: (left0_x, 0.575),
    3220: (left0_x, 0.54),
    3230: (left0_x, 0.505),
    3240: (left0_x, 0.47),
    3250: (left0_x, 0.435),
    3260: (left0_x, 0.40),

    # transports
    3270: (left0_x, 0.33),
    3280: (left0_x, 0.295),
    3290: (left0_x, 0.26),
    3300: (left0_x, 0.225),
    3310: (left0_x, 0.19),

    # landing craft
    3720: (left0_x, 0.13),
    3730: (left0_x + 0.01, 0.095),
    3740: (left0_x + 0.01, 0.06),
    3750: (left0_x + 0.02, 0.025),

    # naval guns
    3060: (left1_x, 0.96),
    3070: (left1_x, 0.925),
    3080: (left1_x, 0.89),
    3090: (left1_x, 0.855),
    3100: (left1_x, 0.82),
    3110: (left1_x, 0.785),

    # naval engines
    3010: (left1_x, 0.61),
    3020: (left1_x, 0.575),
    3030: (left1_x, 0.54),
    3040: (left1_x, 0.505),
    3050: (left1_x, 0.47),

    # submarines
    3320: (left1_x, 0.365),
    3330: (left1_x, 0.33),
    3340: (left1_x, 0.295),
    3350: (left1_x, 0.26),
    3360: (left1_x, 0.225),
    3850: (left1_x, 0.19),

    # heavy cruisers
    3370: (left2_x, 0.925),
    3380: (left2_x, 0.89),
    3390: (left2_x, 0.855),
    3400: (left2_x, 0.82),
    3410: (left2_x, 0.785),
    3420: (left2_x, 0.75),
    3430: (left2_x, 0.715),

    # light cruisers
    3440: (left2_x, 0.63),
    3450: (left2_x, 0.595),
    3460: (left2_x, 0.56),
    3470: (left2_x, 0.525),
    3480: (left2_x, 0.49),
    3490: (left2_x, 0.455),

    # carriers
    3500: (left2_x, 0.365),
    3510: (left2_x, 0.33),
    3520: (left2_x, 0.295),
    3530: (left2_x, 0.26),
    3540: (left2_x, 0.225),
    3550: (left2_x, 0.19),
    3560: (left2_x, 0.155),

    # patrol boats
    3760: (left3_x, 0.17),
    3770: (left3_x + 0.01, 0.135),
    3780: (left3_x + 0.02, 0.1),
    3790: (left3_x + 0.03, 0.065),
    3800: (left3_x + 0.04, 0.03),

    # battlecruisers
    3630: (left3_x, 0.925),
    3640: (left3_x, 0.89),
    3650: (left3_x, 0.855),
    3660: (left3_x, 0.82),
    3670: (left3_x, 0.785),
    3680: (left3_x, 0.75),
    3690: (left3_x, 0.715),

    # pocket battleships
    3700: (left3_x, 0.61),
    3710: (left3_x, 0.575),

    # carrier air groups
    3570: (left3_x, 0.365),
    3580: (left3_x, 0.33),
    3590: (left3_x, 0.295),

    # escort carriers
    3600: (left4_x, 0.92),
    3610: (left4_x, 0.885),
    3620: (left4_x, 0.85),
    3810: (left4_x, 0.815),
    3820: (left4_x, 0.78),
    3830: (left4_x, 0.745),
    3840: (left4_x, 0.71),

    # AIRCRAFT
    # fighter plans
    4010: (left0_x, 0.95),
    4020: (left0_x, 0.915),

    # fighter firepower or long range
    4560: (left0_x, 0.8),
    4570: (left0_x, 0.74),

    # bomber plans
    4220: (left0_x, 0.63),
    4230: (left0_x, 0.595),

    # close air support
    4240: (left0_x, 0.5),
    4250: (left0_x, 0.465),
    4260: (left0_x, 0.43),
    4270: (left0_x, 0.395),

    # bombs
    4610: (left0_x, 0.28),
    4620: (left0_x, 0.20),
    4630: (left0_x, 0.165),
    4640: (left0_x + 0.01, 0.13),
    4650: (left1_x - 0.01, 0.28),
    4660: (left1_x - 0.01, 0.245),

    # fighters
    4030: (left1_x, 0.95),
    4040: (left1_x, 0.915),
    4050: (left1_x, 0.88),
    4060: (left1_x, 0.845),
    4070: (left1_x, 0.81),

    # interceptors
    4120: (left1_x, 0.74),
    4130: (left1_x, 0.705),
    4140: (left1_x, 0.67),
    4150: (left1_x, 0.635),
    4160: (left1_x, 0.60),

    # tactical bombers
    4320: (left1_x, 0.5),
    4330: (left1_x, 0.465),
    4340: (left1_x, 0.43),
    4350: (left1_x, 0.395),
    4360: (left1_x, 0.36),

    # night fighters
    4080: (left2_x, 0.915),
    4090: (left2_x, 0.88),
    4100: (left2_x, 0.845),
    4110: (left2_x, 0.81),

    # escort fighters
    4170: (left2_x, 0.74),
    4180: (left2_x, 0.705),
    4190: (left2_x, 0.67),
    4200: (left2_x, 0.635),
    4210: (left2_x, 0.60),

    # strategic bombers
    4370: (left2_x, 0.5),
    4380: (left2_x, 0.465),
    4390: (left2_x, 0.43),
    4400: (left2_x, 0.395),
    4410: (left2_x, 0.36),

    # surveillance
    4670: (left2_x, 0.28),
    # hydroplanes
    4680: (left2_x, 0.20),
    4690: (left2_x, 0.165),
    # more surveillance
    4700: (left3_x, 0.28),
    4710: (left3_x, 0.245),
    4720: (left3_x, 0.21),
    4730: (left3_x, 0.175),

    # rockey theory
    4470: (left3_x, 0.9),
    4480: (left3_x, 0.865),
    4490: (left3_x, 0.83),
    4500: (left3_x, 0.795),
    4510: (left3_x, 0.76),

    # jet engines
    4520: (left3_x, 0.7),
    4530: (left3_x, 0.665),
    4540: (left3_x, 0.63),
    4550: (left3_x, 0.595),

    # naval bombers
    4420: (left3_x, 0.5),
    4430: (left3_x, 0.465),
    4440: (left3_x, 0.43),
    4450: (left3_x, 0.395),
    4460: (left3_x, 0.36),

    # bomber defence, range or firepower
    4580: (left4_x, 0.75),
    4590: (left4_x, 0.7),
    4600: (left4_x, 0.65),

    # transports
    4280: (left4_x, 0.5),
    4290: (left4_x, 0.465),
    4300: (left4_x, 0.43),
    4310: (left4_x, 0.395),

    # INDUSTRY
    # war industry
    5200: (left0_x, 0.95),
    # mobilization
    5210: (left0_x + 0.01, 0.9),
    5220: (left0_x + 0.01, 0.865),
    5230: (left0_x + 0.01, 0.83),
    5240: (left0_x + 0.01, 0.795),
    # production planning
    5250: (left0_x, 0.75),
    # army planning
    5260: (left0_x + 0.01, 0.7),
    5270: (left0_x + 0.01, 0.665),
    5280: (left0_x + 0.01, 0.63),
    # naval planning
    5290: (left0_x + 0.01, 0.58),
    5300: (left0_x + 0.01, 0.545),
    5310: (left0_x + 0.01, 0.51),
    # air force planning
    5320: (left0_x + 0.01, 0.46),
    5330: (left0_x + 0.01, 0.425),
    5340: (left0_x + 0.01, 0.39),

    # policy conquest
    5680: (left0_x + 0.01, 0.3),
    5690: (left0_x + 0.01, 0.25),
    5700: (left0_x + 0.01, 0.2),

    # economic theory, taxes, public finance
    5710: (left0_x, 0.15),
    5720: (left0_x + 0.01, 0.1),
    5730: (left0_x + 0.01, 0.065),

    # industry
    5010: (left1_x, 0.95),
    5020: (left1_x, 0.9),
    5030: (left1_x, 0.865),
    # light industry
    5040: (left1_x, 0.815),
    5050: (left1_x, 0.78),
    # average industry
    5060: (left1_x, 0.73),
    5070: (left1_x, 0.695),
    # heavy industry
    5080: (left1_x, 0.645),
    5090: (left1_x, 0.61),
    5100: (left1_x, 0.575),

    # study centers
    5440: (left1_x, 0.525),
    5450: (left1_x, 0.49),

    # circuits theory and vacuum tubes
    5480: (left1_x, 0.4),
    5490: (left1_x, 0.365),

    # radio frequency
    5590: (left1_x, 0.3),
    5600: (left1_x, 0.265),
    5610: (left1_x, 0.23),

    # economy choices
    5740: (left1_x - 0.01, 0.17),
    5750: (left1_x - 0.01, 0.12),
    5760: (left1_x - 0.01, 0.07),

    # boost mining
    5350: (left2_x, 0.95),

    # chemical industry
    5110: (left2_x, 0.9),
    5120: (left2_x, 0.865),
    5130: (left2_x, 0.83),
    5140: (left2_x, 0.795),

    # special materials
    5150: (left2_x, 0.73),
    5160: (left2_x, 0.695),
    5170: (left2_x, 0.66),

    # new compounds
    5180: (left2_x, 0.61),
    5190: (left2_x, 0.575),

    # laboratories
    5460: (left2_x, 0.525),
    5470: (left2_x, 0.49),

    # electronics
    5500: (left2_x, 0.42),
    5510: (left2_x, 0.385),
    5520: (left2_x, 0.35),

    # radar
    5620: (left2_x, 0.3),
    5630: (left2_x, 0.265),
    5640: (left2_x, 0.23),

    # keynesian/self-sustainable
    5770: (left2_x - 0.01, 0.16),
    5780: (left2_x - 0.01, 0.06),
    # implementation
    5790: (left2_x + 0.01, 0.11),

    # mining and materials
    5360: (left3_x, 0.95),
    5370: (left3_x + 0.01, 0.915),
    5380: (left3_x, 0.865),
    5390: (left3_x + 0.01, 0.83),
    5400: (left3_x, 0.78),
    5410: (left3_x + 0.01, 0.745),
    5420: (left3_x, 0.695),
    5430: (left3_x + 0.01, 0.66),

    # calculators
    5530: (left3_x, 0.525),
    5540: (left3_x, 0.49),
    # initial computers
    5550: (left3_x, 0.42),
    5560: (left3_x, 0.385),
    # basic computers
    5570: (left3_x, 0.335),
    5580: (left3_x, 0.3),
    # long range radar
    5650: (left3_x, 0.23),

    # more economic stuff
    5800: (left3_x, 0.18),
    5810: (left3_x, 0.145),
    5820: (left3_x, 0.11),
    5830: (left3_x, 0.075),

    # wartime or peacetime
    5660: (left4_x, 0.6),
    5670: (left4_x, 0.55),

    # LAND DOCTRINES
    # bewegungskrieg
    6020: (left0_x, 0.88),
    6030: (left0_x, 0.845),
    6040: (left0_x, 0.81),
    6050: (left0_x, 0.775),
    6060: (left0_x, 0.74),
    6070: (left0_x, 0.705),
    6080: (left0_x, 0.67),

    # defence principles
    6280: (left0_x + 0.01, 0.6),
    6290: (left0_x + 0.01, 0.55),
    6300: (left0_x + 0.01, 0.515),
    6310: (left0_x + 0.01, 0.48),

    # WW1 thought
    6500: (left0_x, 0.39),
    # levels
    6510: (left0_x + 0.02, 0.35),
    6520: (left0_x + 0.02, 0.315),
    6530: (left0_x + 0.02, 0.28),

    # centralized
    6560: (left0_x, 0.23),
    6570: (left0_x + 0.02, 0.195),
    # truppenführung
    6580: (left0_x, 0.145),
    6590: (left0_x + 0.02, 0.11),
    # revisionist
    6600: (left0_x, 0.06),
    6610: (left0_x + 0.02, 0.025),

    # WW1 Doctrine
    6010: (left1_x + 0.02, 0.96),

    # rapid deployment
    6090: (left1_x, 0.88),
    6100: (left1_x, 0.845),
    6110: (left1_x, 0.81),
    6120: (left1_x, 0.775),
    6130: (left1_x, 0.74),
    # mechanized ops
    6140: (left1_x, 0.67),

    # elastic/static defence
    6320: (left1_x, 0.6),
    6420: (left1_x, 0.55),
    # planning, fortifications
    6430: (left1_x, 0.49),
    6440: (left1_x + 0.01, 0.455),

    # decisive battle / operational art
    6540: (left1_x + 0.01, 0.34),
    6550: (left1_x + 0.01, 0.29),

    # concentrated
    6620: (left1_x, 0.205),
    6630: (left1_x + 0.01, 0.17),
    # C3I
    6640: (left1_x, 0.12),
    6650: (left1_x + 0.01, 0.085),
    # guerrilla
    6660: (left1_x, 0.035),
    6670: (left1_x + 0.01, 0),

    # deep attack
    6150: (left2_x, 0.88),
    6160: (left2_x, 0.845),
    6170: (left2_x, 0.81),
    6180: (left2_x, 0.775),

    # pre-planned attack
    6190: (left3_x, 0.88),
    6200: (left3_x, 0.845),
    6210: (left3_x, 0.81),
    6220: (left3_x, 0.775),

    # armoured ops
    6270: (left2_x + 0.1, 0.70),

    # strategic envelopment
    6230: (left4_x, 0.88),
    6240: (left4_x, 0.845),
    6250: (left4_x, 0.81),
    6260: (left4_x, 0.775),

    # fire & retreat, defence in depth
    6330: (left2_x, 0.63),
    6370: (left2_x, 0.58),
    # strategic demo
    6340: (left4_x, 0.58),
    6350: (left4_x, 0.545),
    6360: (left4_x, 0.51),
    # counterattack
    6380: (left3_x, 0.58),
    6390: (left3_x, 0.545),
    6400: (left3_x, 0.51),
    # strategic withdrawal
    6410: (left3_x + 0.1, 0.44),

    # trench warfare
    6450: (left2_x, 0.49),
    6460: (left2_x + 0.01, 0.455),
    6470: (left2_x + 0.02, 0.42),
    6480: (left2_x + 0.02, 0.385),
    # sturmtruppen
    6490: (left2_x + 0.03, 0.35),

    # small units
    6680: (left2_x - 0.01, 0.25),
    6690: (left2_x, 0.215),
    # patrols
    6770: (left2_x + 0.01, 0.155),
    6780: (left2_x + 0.02, 0.12),
    # ambush
    6790: (left2_x + 0.01, 0.08),
    6800: (left2_x + 0.02, 0.045),

    # infantry tactics
    6700: (left3_x, 0.155),
    6710: (left3_x + 0.01, 0.12),
    6720: (left3_x + 0.01, 0.07),
    # penetration/contact
    6730: (left3_x + 0.02, 0.03),
    # shoot and escape
    6740: (left4_x, 0.155),
    6750: (left4_x + 0.01, 0.12),
    6760: (left4_x + 0.02, 0.085),

    # NAVAL DOCTRINES
    # sea control
    8020: (left0_x, 0.95),
    8030: (left0_x, 0.915),
    8040: (left0_x, 0.88),
    # port protection/invasion op
    8050: (left0_x + 0.01, 0.83),
    8060: (left0_x + 0.01, 0.78),
    # maritime patrol
    8070: (left0_x, 0.73),
    8080: (left0_x, 0.695),

    # fleet-in-being
    8270: (left0_x, 0.6),
    # decisive/block enemy ships
    8280: (left0_x + 0.01, 0.56),
    8290: (left0_x + 0.01, 0.47),

    # combined army-navy / warfare manouver
    8300: (left0_x + 0.01, 0.37),
    8310: (left0_x + 0.01, 0.28),

    # power projection
    8550: (left0_x, 0.19),
    8560: (left0_x + 0.01, 0.155),
    8570: (left0_x + 0.01, 0.12),

    # amphibious operations
    8580: (left0_x, 0.05),
    8590: (left0_x + 0.01, 0.015),

    # 19th century
    8010: (left1_x, 0.95),

    # naval diplomacy
    8090: (left1_x, 0.9),
    # convoy sailing
    8100: (left1_x, 0.86),
    # antisub patrols / naval participation
    8110: (left1_x + 0.01, 0.81),
    8120: (left1_x + 0.01, 0.76),

    # naval firepower
    8320: (left1_x, 0.68),
    8330: (left1_x + 0.01, 0.645),
    8340: (left1_x + 0.01, 0.61),

    # decoy fleet
    8390: (left1_x, 0.5),
    8400: (left1_x + 0.01, 0.465),

    # overseas expansion
    8430: (left1_x, 0.42),
    8440: (left1_x, 0.385),
    8450: (left1_x, 0.35),

    # air-naval supremacy
    8600: (left1_x, 0.28),
    # fleet defence
    8610: (left1_x + 0.01, 0.23),
    # amphibious combined arms
    8620: (left1_x + 0.01, 0.18),
    8630: (left1_x + 0.02, 0.145),
    # indirect approach
    8640: (left1_x, 0.1),
    # naval power
    8650: (left1_x + 0.02, 0.015),

    # commerce raiding
    8130: (left2_x, 0.95),
    8140: (left2_x + 0.01, 0.915),
    8150: (left2_x + 0.01, 0.88),

    # diversion force
    8160: (left2_x, 0.83),
    # naval minelaying
    8170: (left2_x + 0.01, 0.78),
    8180: (left2_x + 0.01, 0.745),

    # command of the sea
    8350: (left2_x, 0.68),
    # large taskforce / balanced fleet
    8360: (left2_x + 0.01, 0.63),
    8370: (left2_x + 0.01, 0.58),

    # encounter group
    8410: (left2_x, 0.5),
    8420: (left2_x + 0.01, 0.465),

    # air-naval supremacy / fleet auxiliary carrier
    8460: (left2_x, 0.41),
    8500: (left2_x, 0.35),

    # enemy deployments interdiction
    8660: (left2_x, 0.23),
    8670: (left2_x + 0.01, 0.195),

    # emphasis on navigation training
    8190: (left3_x, 0.95),
    8200: (left3_x + 0.01, 0.915),
    8210: (left3_x + 0.01, 0.88),
    # limited offensive fleet / submarine fleet
    8220: (left3_x, 0.8),
    8230: (left3_x + 0.01, 0.765),
    8240: (left3_x, 0.715),
    8250: (left3_x + 0.01, 0.68),
    8260: (left3_x + 0.01, 0.645),

    # naval presence
    8380: (left3_x, 0.59),

    # fleet auxiliary force
    8470: (left3_x, 0.45),
    8480: (left3_x + 0.01, 0.415),
    8490: (left3_x + 0.02, 0.38),
    # naval superiority
    8510: (left3_x, 0.33),
    8520: (left3_x + 0.01, 0.295),
    8530: (left3_x + 0.02, 0.26),
    # national protection
    8540: (left4_x, 0.355),

    # naval intelligence
    8680: (left4_x - 0.01, 0.9),
    # levels
    8690: (left4_x + 0.01, 0.865),
    8700: (left4_x + 0.01, 0.83),
    8710: (left4_x + 0.01, 0.795),

    # naval logistic support
    8720: (left4_x - 0.01, 0.72),
    # naval superiority / area of influence
    8730: (left4_x, 0.67),
    8740: (left4_x, 0.62),
    # long range operations, continuous navigation
    8750: (left4_x + 0.01, 0.57),
    8760: (left4_x + 0.01, 0.535),

    # AIR DOCTRINES
    # kette formation
    9030: (left0_x, 0.95),
    9040: (left0_x + 0.01, 0.915),
    9050: (left0_x + 0.01, 0.88),
    # air defence
    9060: (left0_x + 0.01, 0.8),
    9070: (left0_x + 0.02, 0.765),

    # air superiority
    9020: (left0_x, 0.66),

    # air power
    9010: (left0_x - 0.01, 0.6),

    # bombing doctrine
    9250: (left0_x, 0.54),
    # strategic bombing
    9260: (left0_x + 0.01, 0.48),
    # vertical envelopment
    9380: (left0_x + 0.01, 0.4),
    9390: (left0_x + 0.02, 0.365),
    9400: (left0_x + 0.03, 0.33),
    # tactical air support
    9410: (left0_x +0.01, 0.23),
    # air interdiction
    9420: (left0_x + 0.02, 0.18),
    # installation attack
    9430: (left0_x + 0.02, 0.13),
    # jackpot
    9440: (left0_x + 0.03, 0.08),
    9450: (left0_x + 0.03, 0.045),

    # vic zigzag
    9080: (left1_x, 0.91),
    9090: (left1_x + 0.01, 0.875),
    # luftbery circle
    9100: (left1_x, 0.825),
    9110: (left1_x + 0.01, 0.79),

    # independent / tactical
    9600: (left1_x - 0.01, 0.625),
    9610: (left1_x - 0.01, 0.575),

    # close formation
    9270: (left1_x, 0.48),
    # strategic level
    9310: (left1_x, 0.43),
    9320: (left1_x + 0.01, 0.395),
    # level flight
    9360: (left1_x, 0.34),
    # combined forces
    9580: (left1_x, 0.29),
    # support ground operations
    9490: (left1_x, 0.23),
    # naval patrols
    9460: (left1_x, 0.13),
    # long range
    9470: (left1_x + 0.01, 0.075),
    9480: (left1_x + 0.02, 0.04),

    # bomber interception
    9120: (left2_x, 0.95),
    # night attack
    9150: (left2_x, 0.83),
    # frontal attack
    9190: (left2_x, 0.75),
    # air patrol
    9210: (left2_x, 0.7),

    # battle management, central c&c, himmelbett
    9620: (left2_x - 0.02, 0.617),
    9630: (left2_x - 0.02, 0.582),
    9640: (left2_x - 0.02, 0.547),

    # concentrated fire
    9280: (left2_x + 0.01, 0.48),
    # concrete objectives
    9330: (left2_x + 0.01, 0.395),
    # differing altitude
    9370: (left2_x, 0.34),
    # deep operations
    9590: (left2_x + 0.01, 0.29),
    # dive bomb
    9500: (left2_x, 0.25),
    9510: (left2_x + 0.01, 0.215),
    # nearby interception
    9540: (left2_x, 0.15),
    # hedgehog
    9550: (left2_x + 0.01, 0.08),

    # schräge musik
    9130: (left3_x, 0.95),
    9140: (left3_x + 0.01, 0.915),
    # wilde sau
    9160: (left3_x, 0.865),
    9170: (left3_x + 0.01, 0.83),
    # flare use
    9180: (left3_x, 0.785),
    # abschwung
    9200: (left3_x, 0.74),
    # okhotniki
    9220: (left3_x, 0.69),
    # freie jagd
    9230: (left3_x, 0.65),
    # aerial intruder
    9240: (left3_x, 0.61),

    # escort fighter
    9290: (left3_x, 0.48),
    9300: (left3_x + 0.01, 0.445),
    # carpet bombing
    9340: (left3_x, 0.395),
    9350: (left3_x, 0.36),
    
    # predefined objectives
    9520: (left3_x, 0.25),
    9530: (left3_x + 0.01, 0.215),
    # harrassment
    9560: (left3_x, 0.15),
    # offensive corridor
    9570: (left3_x, 0.05),

    # SECRET WEAPONS
    # atomic theories
    7010: (left0_x, 0.9),
    7020: (left0_x + 0.01, 0.865),
    7030: (left0_x + 0.02, 0.83),
    7040: (left0_x + 0.03, 0.795),
    # particle physics
    7050: (left0_x, 0.745),
    7060: (left0_x + 0.01, 0.71),
    7070: (left0_x + 0.02, 0.675),
    # neutron
    7080: (left0_x, 0.625),
    7090: (left0_x + 0.01, 0.59),
    7100: (left0_x + 0.02, 0.555),
    # experimental reactor
    7110: (left0_x, 0.505),
    7120: (left0_x + 0.01, 0.47),
    # nuclear reactor
    7130: (left0_x, 0.42),
    7140: (left0_x + 0.01, 0.385),

    # nuclear waste bomb
    7150: (left0_x, 0.28),
    7160: (left0_x + 0.01, 0.245),
    7170: (left0_x + 0.02, 0.21),
    7180: (left0_x + 0.03, 0.175),

    # nuclear battleship, cruiser, carrier, submarine
    7190: (left2_x, 0.95),
    7200: (left2_x, 0.89),
    7210: (left2_x, 0.83),
    7220: (left2_x, 0.77),

    # rocket interceptors
    7230: (left2_x, 0.7),
    7240: (left2_x + 0.01, 0.665),
    # turbojet interceptors
    7250: (left2_x, 0.61),
    7260: (left2_x + 0.01, 0.575),

    # turbojet tac, str, naval, cas, cag
    7270: (left2_x, 0.51),
    7280: (left2_x, 0.455),
    7290: (left2_x, 0.40),
    7300: (left2_x, 0.345),
    7310: (left2_x, 0.29),

    # air-to-surface, surface-to-air missile
    7320: (left2_x, 0.23),
    7330: (left2_x, 0.17),

    # main battle tank
    7500: (left1_x, 0.085),
    7510: (left1_x, 0.05),
    7520: (left2_x, 0.05),
    7530: (left2_x, 0.015),

    # flying bomb -- icbm
    7340: (left3_x, 0.77),
    7350: (left3_x + 0.01, 0.735),
    7360: (left3_x + 0.01, 0.7),
    7370: (left3_x + 0.01, 0.665),
    # space recon
    7570: (left3_x + 0.01, 0.62),

    # turbojet fighter
    7380: (left3_x, 0.54),
    7390: (left3_x + 0.01, 0.505),

    # air cavalry
    7400: (left3_x, 0.4),

    # electronic computers
    7410: (left3_x, 0.3),
    7420: (left3_x, 0.265),
    7430: (left3_x, 0.23),
    7440: (left3_x, 0.195),

    # radar
    7540: (left3_x, 0.09),
    7550: (left3_x + 0.01, 0.055),
    7560: (left3_x + 0.02, 0.02),

    # satellites
    7460: (left4_x, 0.85),
    7470: (left4_x + 0.01, 0.815),
    7480: (left4_x + 0.02, 0.78),
    7490: (left4_x + 0.03, 0.745),

    # more missiles
    7610: (left4_x, 0.61),
    7620: (left4_x, 0.56),
    7630: (left4_x, 0.51),

    # submarines
    7580: (left4_x, 0.35),
    7590: (left4_x, 0.3),
    7600: (left4_x, 0.25)


}