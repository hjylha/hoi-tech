
left0_x = 0.01
left1_x = 0.2
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
    2560: (left3_x + 0.01, 0.235),

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
    2900: (left4_x + 0.02, 0.525),
    2910: (left4_x, 0.49),
    2920: (left4_x + 0.01, 0.455),
    2930: (left4_x + 0.02, 0.42),

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
    3760: (left4_x, 0.45),
    3770: (left4_x, 0.415),
    3780: (left4_x, 0.38),
    3790: (left4_x, 0.345),
    3800: (left4_x, 0.31),

    # battlecruisers
    3630: (left3_x, 0.925),
    3640: (left3_x, 0.89),
    3650: (left3_x, 0.855),
    3660: (left3_x, 0.82),
    3670: (left3_x, 0.785),
    3680: (left3_x, 0.75),
    3690: (left3_x, 0.715),

    # pocket battleships
    3700: (left3_x, 0.63),
    3710: (left3_x, 0.595),

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
    5210: (left0_x + 0.02, 0.915),
    5220: (left0_x + 0.02, 0.88),
    5230: (left0_x + 0.02, 0.845),
    5240: (left0_x + 0.02, 0.81),
    # production planning
    5250: (left0_x, 0.76),
    # army planning
    5260: (left0_x + 0.02, 0.725),
    5270: (left0_x + 0.02, 0.69),
    5280: (left0_x + 0.02, 0.655),
    # naval planning
    5290: (left0_x + 0.02, 0.605),
    5300: (left0_x + 0.02, 0.57),
    5310: (left0_x + 0.02, 0.535),
    # air force planning
    5320: (left0_x + 0.02, 0.485),
    5330: (left0_x + 0.02, 0.45),
    5340: (left0_x + 0.02, 0.415),

    # policy conquest
    5680: (left0_x + 0.02, 0.34),
    5690: (left0_x + 0.02, 0.29),
    5700: (left0_x + 0.02, 0.24),
    # economic theory, taxes, public finance
    5710: (left0_x + 0.02, 0.15),
    5720: (left0_x + 0.01, 0.115),
    5730: (left0_x, 0.08),
    # economy choices
    5740: (left1_x - 0.01, 0.17),
    5750: (left1_x - 0.01, 0.12),
    5760: (left1_x - 0.01, 0.07),
    # keynesian/self-sustainable
    5770: (left2_x - 0.01, 0.16),
    5780: (left2_x - 0.01, 0.06),
    # implementation
    5790: (left2_x + 0.01, 0.11),
    # state control, monetary system
    5800: (left3_x - 0.02, 0.11),
    5810: (left3_x - 0.01, 0.075),
    # employment system, foreign trade
    5820: (left4_x - 0.03, 0.075),
    5830: (left4_x - 0.01, 0.04),

    # basic industry, imp ind, selective
    5010: (left1_x, 0.95),
    5020: (left1_x, 0.9),
    5030: (left1_x + 0.01, 0.865),
    # light industry, consumer
    5040: (left1_x, 0.815),
    5050: (left1_x + 0.01, 0.78),
    # average industry, adv parts
    5060: (left1_x, 0.73),
    5070: (left1_x + 0.01, 0.695),
    # heavy industry, mass prod, high q
    5080: (left1_x, 0.63),
    5090: (left1_x + 0.01, 0.595),
    5100: (left1_x + 0.02, 0.56),
    # chemical industry
    5110: (left2_x - 0.01, 0.9),
    # refined fuel, processed, post-ref
    5120: (left2_x, 0.865),
    5130: (left2_x, 0.83),
    5140: (left2_x, 0.795),
    # special materials, imp synth, thermo
    5150: (left2_x - 0.01, 0.73),
    5160: (left2_x, 0.695),
    5170: (left2_x, 0.66),
    # new compounds, light alloys
    5180: (left2_x - 0.01, 0.595),
    5190: (left2_x, 0.56),
    # boost mining
    5350: (left2_x + 0.01, 0.95),
    # mining and materials
    5360: (left3_x, 0.95),
    5370: (left3_x + 0.02, 0.915),
    5380: (left3_x, 0.865),
    5390: (left3_x + 0.02, 0.83),
    5400: (left3_x, 0.78),
    5410: (left3_x + 0.02, 0.745),
    5420: (left3_x, 0.695),
    5430: (left3_x + 0.02, 0.66),

    # study centers
    5440: (left1_x, 0.49),
    # ind training inst
    5450: (left2_x, 0.49),
    # laboratories
    5460: (left3_x, 0.49),
    # investigation centers
    5470: (left4_x, 0.49),

    # circuits theory, vacuum tubes
    5480: (left1_x, 0.42),
    5490: (left1_x, 0.385),
    # radio frequency
    5590: (left1_x, 0.3),
    5600: (left1_x, 0.265),
    5610: (left1_x, 0.23),
    # electronics
    5500: (left2_x, 0.42),
    5510: (left2_x, 0.385),
    5520: (left2_x, 0.35),
    # radar
    5620: (left2_x, 0.3),
    5630: (left2_x, 0.265),
    5640: (left2_x, 0.23),
    # calculators, tabulating
    5530: (left3_x, 0.43),
    5540: (left4_x, 0.43),
    # initial computers, decoding/encoding
    5550: (left3_x, 0.385),
    5560: (left4_x, 0.385),
    # basic computers, complex calc
    5570: (left3_x, 0.34),
    5580: (left4_x, 0.34),
    # long range radar
    5650: (left3_x + 0.05, 0.23),
    # transistor, integrated circuit
    5940: (left4_x, 0.24),
    5950: (left4_x, 0.205),

    # wartime or peacetime
    5660: (left4_x, 0.7),
    5670: (left4_x, 0.65),

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
    # 19th century
    8010: (left1_x + 0.02, 0.95),

    # sea control
    8020: (left0_x, 0.95),
    8030: (left0_x, 0.915),
    # naval diplomacy
    8090: (left0_x + 0.01, 0.88),
    # commerce defence
    8040: (left0_x + 0.01, 0.845),
    # convoy sailing
    8100: (left1_x, 0.845),
    # port protection/invasion op
    8050: (left0_x + 0.02, 0.81),
    8060: (left0_x + 0.02, 0.76),
    # antisub patrols / naval participation
    8110: (left1_x + 0.01, 0.81),
    8120: (left1_x + 0.01, 0.76),
    # maritime patrol
    8070: (left0_x + 0.01, 0.725),
    8080: (left0_x + 0.01, 0.69),

    # commerce raiding
    8130: (left2_x, 0.95),
    8140: (left2_x, 0.915),
    # convoy harassment
    8150: (left2_x + 0.01, 0.88),
    # diversion force
    8160: (left2_x + 0.01, 0.845),
    # naval minelaying
    8170: (left2_x + 0.02, 0.81),
    8180: (left2_x + 0.02, 0.775),
    # emphasis on navigation training
    8190: (left4_x, 0.95),
    8200: (left4_x + 0.01, 0.915),
    8210: (left4_x + 0.02, 0.88),
    # limited offensive fleet / submarine fleet
    8220: (left3_x, 0.915),
    8230: (left3_x + 0.02, 0.88),
    8240: (left3_x, 0.825),
    8250: (left3_x + 0.02, 0.79),
    8260: (left3_x + 0.02, 0.755),

    # decisive/block enemy ships
    8280: (left0_x + 0.02, 0.62),
    8290: (left0_x + 0.02, 0.56),

    # fleet-in-being
    8270: (left0_x, 0.47),

    # naval firepower
    8320: (left1_x + 0.01, 0.62),
    # escort sub & naval attrition
    8330: (left2_x, 0.655),
    8340: (left2_x, 0.62),
    # command of the sea
    8350: (left3_x, 0.655),
    # large taskforce / balanced fleet
    8360: (left3_x + 0.01, 0.62),
    8370: (left3_x + 0.01, 0.57),
    # naval presence
    8380: (left4_x, 0.595),

    # decoy fleet
    8390: (left1_x + 0.01, 0.56),
    # battlefleet concentration
    8400: (left2_x, 0.56),
    # encounter group
    8410: (left2_x, 0.525),
    8420: (left2_x + 0.01, 0.49),

    # combined army-navy / warfare manouver
    8300: (left0_x + 0.02, 0.40),
    8310: (left0_x + 0.02, 0.28),

    # overseas expansion
    8430: (left1_x + 0.01, 0.42),
    # invasion force, base strike
    8440: (left1_x + 0.02, 0.385),
    8450: (left1_x + 0.02, 0.35),
    # air-naval supremacy / fleet auxiliary carrier
    8460: (left2_x + 0.01, 0.42),
    8500: (left2_x + 0.01, 0.37),
    # fleet auxiliary force
    8470: (left3_x, 0.47),
    8480: (left3_x + 0.01, 0.435),
    8490: (left3_x + 0.02, 0.40),
    # naval superiority
    8510: (left3_x, 0.34),
    8520: (left3_x + 0.01, 0.305),
    8530: (left3_x + 0.02, 0.27),
    # national protection
    8540: (left4_x, 0.355),

    # power projection
    8550: (left0_x, 0.21),
    # rapid decision
    8560: (left0_x + 0.01, 0.175),
    8570: (left0_x + 0.01, 0.14),
    # amphibious operations
    8580: (left0_x + 0.01, 0.105),
    8590: (left0_x + 0.02, 0.07),
    # air-naval supremacy
    8600: (left1_x + 0.01, 0.28),
    # enemy deployments interdiction
    8660: (left2_x - 0.01, 0.28),
    8670: (left2_x, 0.245),
    # fleet defence
    8610: (left1_x + 0.02, 0.21),
    # indirect approach
    8640: (left1_x + 0.02, 0.175),
    # amphibious combined arms
    8620: (left2_x - 0.01, 0.20),
    8630: (left2_x, 0.165),
    # naval power
    8650: (left1_x + 0.02, 0.07),

    # naval intelligence
    8680: (left3_x - 0.03, 0.17),
    # levels
    8690: (left3_x - 0.02, 0.135),
    8700: (left3_x - 0.02, 0.1),
    8710: (left3_x - 0.02, 0.065),

    # naval logistic support
    8720: (left4_x - 0.03, 0.21),
    # naval superiority / area of influence
    8730: (left4_x - 0.02, 0.175),
    8740: (left4_x - 0.02, 0.13),
    # long range operations, continuous navigation
    8750: (left4_x - 0.01, 0.095),
    8760: (left4_x - 0.01, 0.06),

    # AIR DOCTRINES
    # air superiority
    9020: (left0_x, 0.95),
    # air defence
    9060: (left0_x + 0.02, 0.915),
    9070: (left0_x + 0.03, 0.88),
    # luftbery circle
    9100: (left0_x + 0.03, 0.845),
    9110: (left0_x + 0.04, 0.81),
    # frontal attack
    9190: (left0_x + 0.02, 0.77),
    # abschwung
    9200: (left0_x + 0.03, 0.735),
    # kette formation
    9030: (left1_x, 0.915),
    9040: (left1_x + 0.01, 0.88),
    9050: (left1_x + 0.02, 0.845),
    # vic zigzag
    9080: (left1_x + 0.03, 0.81),
    9090: (left1_x + 0.04, 0.775),
    # bomber interception
    9120: (left2_x, 0.915),
    # schräge musik
    9130: (left2_x + 0.01, 0.88),
    9140: (left2_x + 0.02, 0.845),
    # air patrol
    9210: (left3_x, 0.915),
    # freie jagd
    9230: (left3_x + 0.01, 0.88),
    # aerial intruder
    9240: (left3_x + 0.01, 0.845),
    # okhotniki
    9220: (left3_x + 0.01, 0.81),
    # night attack
    9150: (left4_x, 0.915),
    # flare use
    9180: (left4_x + 0.01, 0.88),
    # wilde sau
    9160: (left4_x + 0.01, 0.845),
    9170: (left4_x + 0.02, 0.81),
    
    # air power
    9010: (left0_x - 0.01, 0.635),

    # independent / tactical
    9600: (left1_x - 0.01, 0.65),
    9610: (left1_x - 0.01, 0.6),
    # battle management, central c&c, himmelbett
    9620: (left2_x - 0.02, 0.66),
    9630: (left2_x - 0.02, 0.625),
    9640: (left2_x - 0.02, 0.59),

    # bombing doctrine
    9250: (left0_x, 0.55),

    # strategic bombing
    9260: (left0_x + 0.01, 0.48),
    # close formation
    9270: (left0_x + 0.02, 0.445),
    # concentrated fire
    9280: (left0_x + 0.03, 0.41),
    # escort fighter
    9290: (left0_x + 0.04, 0.375),
    9300: (left0_x + 0.05, 0.34),
    # strategic level
    9310: (left0_x + 0.02, 0.305),
    9320: (left0_x + 0.03, 0.27),
    # concrete objectives
    9330: (left0_x + 0.04, 0.235),
    # carpet bombing
    9340: (left0_x + 0.05, 0.2),
    9350: (left0_x + 0.05, 0.165),
    # level flight
    9360: (left0_x + 0.02, 0.13),
    # differing altitude
    9370: (left0_x + 0.03, 0.095),
    

    # vertical envelopment
    9380: (left1_x + 0.03, 0.48),
    9390: (left1_x + 0.04, 0.445),
    9400: (left1_x + 0.05, 0.41),

    # combined forces
    9580: (left1_x + 0.03, 0.33),
    # deep operations
    9590: (left1_x + 0.04, 0.295),

    # tactical air support
    9410: (left2_x + 0.03, 0.48),
    # support ground operations
    9490: (left2_x + 0.04, 0.445),
    # air interdiction
    9420: (left2_x + 0.04, 0.41),
    # installation attack
    9430: (left2_x + 0.05, 0.375),
    # jackpot
    9440: (left2_x + 0.06, 0.34),
    9450: (left2_x + 0.06, 0.305),
    # naval patrols
    9460: (left2_x + 0.05, 0.27),
    # long range
    9470: (left2_x + 0.06, 0.235),
    9480: (left2_x + 0.06, 0.2),

    # dive bomb
    9500: (left4_x, 0.445),
    9510: (left4_x + 0.01, 0.41),
    # predefined objectives
    9520: (left4_x + 0.01, 0.375),
    9530: (left4_x + 0.02, 0.34),
    # nearby interception
    9540: (left3_x + 0.02, 0.4),
    # hedgehog
    9550: (left3_x + 0.03, 0.365),
    # harrassment
    9560: (left4_x + 0.01, 0.29),
    # offensive corridor
    9570: (left3_x + 0.03, 0.29),

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
    7600: (left4_x, 0.25),


    # POST-WAR
    # INFANTRY
    11890: (left0_x - 0.01, 0.9),
    11770: (left0_x - 0.01, 0.85),
    11870: (left0_x, 0.815),
    11880: (left0_x + 0.01, 0.78),
    11780: (left0_x, 0.745),
    11790: (left0_x + 0.01, 0.71),
    11850: (left0_x + 0.01, 0.675),
    11860: (left0_x + 0.02, 0.64),
    # mot and mech
    11800: (left1_x - 0.03, 0.86),
    11810: (left1_x - 0.02, 0.825),
    11820: (left1_x - 0.02, 0.775),
    11830: (left1_x - 0.01, 0.735),
    11840: (left1_x, 0.7),

    # LAND DOCTRINES
    16810: (left2_x + 0.03, 0.9),
    # massive means + stuff
    16820: (left2_x - 0.04, 0.85),
    16830: (left2_x - 0.04, 0.815),
    16840: (left2_x - 0.04, 0.78),
    # eco forces + stuff
    16850: (left2_x + 0.13, 0.85),
    16860: (left2_x + 0.13, 0.815),
    16870: (left2_x + 0.13, 0.78),
    # counterint/elect counterm
    16880: (left2_x + 0.03, 0.715),
    16890: (left2_x + 0.03, 0.665),
    # combined arms
    16900: (left2_x + 0.05, 0.62),
    # command unit/individual
    16910: (left2_x + 0.07, 0.575),
    16920: (left2_x + 0.07, 0.525),

    # ECONOMY/INDUSTRIAL
    15840: (left0_x - 0.01, 0.55),
    15850: (left0_x, 0.5),
    # free trade / mutual assist
    15860: (left0_x + 0.01, 0.46),
    15870: (left0_x + 0.01, 0.41),
    # labor org + just in time
    15880: (left0_x + 0.01, 0.37),
    15890: (left0_x + 0.02, 0.335),
    # eco restruct, casting, quality, finish
    15900: (left0_x + 0.03, 0.27),
    15910: (left0_x + 0.04, 0.235),
    15920: (left0_x + 0.05, 0.2),
    15930: (left0_x + 0.06, 0.165),
    # laser + microprocessor
    15960: (left0_x + 0.04, 0.1),
    15970: (left0_x + 0.05, 0.065),

    # AIRCRAFT
    14740: (left1_x + 0.03, 0.415),
    # helicopters
    14840: (left1_x + 0.04, 0.38),
    # transports
    14820: (left1_x + 0.04, 0.345),
    # interceptor
    14780: (left1_x + 0.04, 0.31),
    # fighter
    14770: (left1_x + 0.04, 0.275),
    14790: (left1_x + 0.05, 0.24),
    # tac bomber
    14800: (left1_x + 0.04, 0.205),
    14810: (left1_x + 0.05, 0.17),
    # naval bomber
    14830: (left1_x + 0.04, 0.135),
    # strategic bomber
    14750: (left1_x + 0.04, 0.1),
    14760: (left1_x + 0.05, 0.065),

    # AIR DOCTRINES
    19650: (left2_x + 0.02, 0.415),
    # asw helicopters
    19690: (left2_x + 0.03, 0.38),
    # bvr
    19660: (left2_x + 0.03, 0.345),
    19670: (left2_x + 0.04, 0.31),
    19680: (left2_x + 0.05, 0.275),
    # multitasking
    19700: (left2_x + 0.03, 0.24),
    19710: (left2_x + 0.04, 0.205),
    # radar line
    19730: (left2_x + 0.03, 0.17),
    19740: (left2_x + 0.04, 0.135),
    # awacs
    19720: (left2_x + 0.03, 0.1),

    # NAVAL
    13860: (left4_x - 0.06, 0.9),
    # destroyers
    13930: (left4_x - 0.04, 0.85),
    13940: (left4_x - 0.03, 0.815),
    # corvettes
    13950: (left4_x - 0.03, 0.78),
    13970: (left4_x - 0.02, 0.745),
    13960: (left4_x - 0.02, 0.71),
    # frigates
    13870: (left4_x - 0.04, 0.675),
    13880: (left4_x - 0.03, 0.64),
    # cruisers
    13890: (left4_x - 0.04, 0.605),
    13900: (left4_x - 0.03, 0.57),
    13910: (left4_x - 0.02, 0.535),
    # cv
    13920: (left4_x - 0.04, 0.5),

    # NAVAL DOCTRINES
    18770: (left3_x + 0.1, 0.4),
    # depth
    18780: (left3_x + 0.01, 0.33),
    18790: (left3_x + 0.02, 0.295),
    18800: (left3_x + 0.03, 0.26),
    18810: (left3_x + 0.03, 0.225),
    18820: (left3_x + 0.04, 0.19),
    # surface
    18830: (left4_x, 0.33),
    18840: (left4_x + 0.01, 0.295),
    18850: (left4_x + 0.02, 0.26),
    18860: (left4_x + 0.02, 0.225),
    18870: (left4_x + 0.03, 0.19)

}