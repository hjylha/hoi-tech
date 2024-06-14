
right1_x = 0.14
left1_x = 0.21

right2_x = 0.33
left2_x = 0.41

right3_x = 0.53
left3_x = 0.62

right4_x = 0.74
left4_x = 0.82


infantry_lines = [
    # machineguns -> infantry
    ((right1_x, 0.9, left1_x, 0.9), True),
    ((right1_x, 0.86, left1_x, 0.86), True),
    ((right1_x, 0.82, left1_x, 0.82), True),
    ((right1_x, 0.78, left1_x, 0.78), True),
    ((right1_x, 0.74, left1_x, 0.74), True),
    ((right1_x, 0.7, left1_x, 0.7), True),
    # basic inf -> specialized units
    ((right2_x, 0.9, left2_x, 0.9), True),
    # specialized -> mnt 2
    ((0.52, 0.9, 0.62, 0.9), True),
    # specilized -> equipment
    ((0.4, 0.885, 0.4, 0.845), True),
    ((0.41, 0.845, 0.4, 0.845, 0.4, 0.76), False),
    ((0.41, 0.76, 0.4, 0.76, 0.4, 0.675, 0.41, 0.675), False),
    # motorized -> mechanized
    ((left1_x, 0.22, right1_x, 0.22), True),
    ((left1_x, 0.185, right1_x, 0.185), True),
    ((left1_x, 0.15, right1_x, 0.15), True),
    ((left1_x, 0.115, right1_x, 0.115), True),
    # light vehicle -> mechanized
    ((0.08, 0.31, 0.08, 0.24), True),
    # arsenal log -> supply log
    ((0.6, 0.555, 0.55, 0.555), True),
    # arsenal log -> concentrated & dispersed
    ((0.6, 0.54, 0.55, 0.505), True),
    ((0.67, 0.54, 0.67, 0.505), True),
    # log savings & frontline supply -> management expert
    ((0.53, 0.36, 0.53, 0.325), True),
    ((0.62, 0.36, 0.62, 0.325), True),
    # EW -> signal detection & jamming
    ((0.54, 0.17, 0.62, 0.225), True),
    ((0.54, 0.165, 0.62, 0.135), True),
    # high freq -> detection
    ((0.75, 0.19, 0.82, 0.17), True),
    ((0.76, 0.07, 0.82, 0.165), True)
]

infantry_deact_lines = [
    # prioritizations
    (0.88, 0.65, 0.88, 0.62),
    (0.88, 0.5, 0.88, 0.47),
    # concentrated vs dispersed logistics
    (0.55, 0.485, 0.6, 0.485),
    # winter/desert/jungle II
    (0.55, 0.795, 0.55, 0.66)
]

armor_lines = [
    # at guns -> tds
    ((left3_x, 0.965, right3_x, 0.965), True),
    ((left3_x, 0.93, right3_x, 0.93), True),
    ((left3_x, 0.895, right3_x, 0.895), True),
    ((left3_x, 0.86, right3_x, 0.86), True),
    # heavy aa -> light aa
    ((right3_x, 0.765, left3_x, 0.765), True),
    # light art -> sp art
    ((left2_x, 0.56, right2_x, 0.56), True),
    ((left2_x, 0.525, right2_x, 0.525), True),
    ((left2_x, 0.49, right2_x, 0.49), True),
    ((left2_x, 0.455, right2_x, 0.455), True),
    # rocket art -> sp r-art
    ((left2_x, 0.365, right2_x, 0.365), True),
    ((left2_x, 0.33, right2_x, 0.33), True),
    ((left2_x, 0.295, right2_x, 0.295), True),
    ((left2_x, 0.26, right2_x, 0.26), True),
    # mech parts -> hq-balanced-mass
    ((right1_x + 0.02, 0.145, right1_x + 0.03, 0.145, right1_x + 0.03, 0.11), False),
    ((right1_x + 0.02, 0.11, right1_x + 0.03, 0.11, right1_x + 0.03, 0.075, right1_x + 0.02, 0.075), False),
    ((right1_x + 0.03, 0.145, left1_x, 0.165), True),
    ((right1_x + 0.03, 0.11, left1_x, 0.11), True),
    ((right1_x + 0.03, 0.075, left1_x, 0.065), True),
    # welded armor -> heavy/light armor
    ((left2_x, 0.15, left2_x, 0.12), True),
    ((left2_x + 0.01, 0.12, left2_x, 0.12, left2_x, 0.07, left2_x + 0.01, 0.07), False),
    # light/heavy -> light sloped armor
    ((right3_x + 0.01, 0.12, right3_x + 0.02, 0.12, right3_x + 0.02, 0.07, right3_x + 0.01, 0.07), False),
    ((right3_x + 0.02, 0.095, left3_x, 0.165), True)
]

armor_deact_lines = [
    # speed-power-balanced
    (0.08, 0.36, 0.08, 0.275),
    # quality-balanced-mass
    (0.26, 0.15, 0.26, 0.07),
    # heavy/light armor
    (0.48, 0.1, 0.48, 0.08)
]

naval_lines = [
    # engines -> destroyers
    ((left1_x, 0.625, right1_x, 0.625), True),
    ((left1_x, 0.59, right1_x, 0.59), True),
    ((left1_x, 0.555, right1_x, 0.555), True),
    # 138khp -> imp cv & 250khp -> adv cv
    ((right2_x, 0.525, left2_x, 0.28), True),
    ((right2_x, 0.49, left2_x, 0.245), True),
    # guns -> bb
    ((left1_x, 0.94, right1_x, 0.94), True),
    ((left1_x, 0.87, right1_x, 0.87), True),
    ((left1_x, 0.835, right1_x, 0.835), True),
    ((left1_x, 0.8, right1_x, 0.73), True),
    # guns -> ca
    ((right2_x, 0.94, left2_x, 0.94), True),
    ((right2_x, 0.905, left2_x, 0.905), True)

]

naval_deact_lines = []

aircraft_lines = [
    # fighter prototypes -> fighter, interceptor, escort
    ((right1_x, 0.93, left1_x - 0.02, 0.93), True),
    ((left1_x, 0.965, left1_x - 0.02, 0.965, left1_x - 0.02, 0.79, left1_x + 0.06, 0.79), False),
    ((left1_x + 0.06, 0.775, left1_x + 0.06, 0.79, left2_x + 0.06, 0.79, left2_x + 0.06, 0.755), False),
    # avg fighter -> basic night fighter & adv ftr -> adv night ftr
    ((right2_x, 0.93, left2_x, 0.93), True),
    ((right2_x, 0.865, left2_x, 0.865), True),
    # bomber prototypes -> cas, tac, str, nav, tra
    ((0.08, 0.595, 0.08, 0.55), True),
    ((0.08, 0.535, 0.08, 0.55, left1_x + 0.06, 0.55), False),
    ((left1_x + 0.06, 0.535, left1_x + 0.06, 0.55, left2_x + 0.06, 0.55), False),
    ((left2_x + 0.06, 0.535, left2_x + 0.06, 0.55, left3_x + 0.06, 0.55), False),
    ((left3_x + 0.06, 0.535, left3_x + 0.06, 0.55, left4_x + 0.06, 0.55, left4_x + 0.06, 0.535), False),
    # basic bombs -> 500kg & he
    ((0.08, 0.28, 0.08, 0.235), True),
    ((right1_x, 0.295, left1_x, 0.295), True),
    # light surveillance -> hydroplanes & basic surveillance
    ((0.48, 0.28, 0.48, 0.235), True),
    ((right3_x, 0.295, left3_x, 0.295), True)
]

aircraft_deact_lines = [
    # fighter firepower/long-range
    (0.08, 0.8, 0.08, 0.775),
    # bonber defence/range/firepower
    (0.88, 0.75, 0.88, 0.685)
]

industry_lines = [
    # rf -> radar
    ((right2_x, 0.315, left2_x, 0.315), True),
    ((right2_x, 0.28, left2_x, 0.28), True),
    ((right2_x, 0.245, left2_x, 0.245), True)
]

industry_deact_lines = [
    # industry/mining/conquest
    (0.09, 0.3, 0.09, 0.235),
    # liberal/military/marxist
    (left1_x + 0.05, 0.17, left1_x + 0.05, 0.105),
    # keynesian/self-sustainable
    (left2_x - 0.01, 0.16, left2_x - 0.01, 0.095),
    # peacetime/wartime
    (left4_x + 0.06, 0.6, left4_x + 0.06, 0.58)
]

land_doct_lines = [
    # WW1 doct -> all things
    ((left1_x + 0.08, 0.96, left1_x + 0.08, 0.93), True),
    ((0.08, 0.915, 0.08, 0.93, left1_x + 0.06, 0.93), False),
    ((left1_x + 0.06, 0.915, left1_x + 0.06, 0.93, left2_x + 0.06, 0.93), False),
    ((left2_x + 0.06, 0.915, left2_x + 0.06, 0.93, left3_x + 0.06, 0.93), False),
    ((left3_x + 0.06, 0.915, left3_x + 0.06, 0.93, left4_x + 0.06, 0.93, left4_x + 0.06, 0.915), False),
    # def principles -> deep ops
    ((0.09, 0.6, 0.09, 0.585), False),
    # def principles -> elastic/static
    ((right1_x + 0.01, 0.615, left1_x - 0.02, 0.615), True),
    ((left1_x, 0.615, left1_x - 0.02, 0.615, left1_x - 0.02, 0.57, left1_x, 0.57), False),
    # levels -> decisive/op art
    ((right1_x + 0.02, 0.365, right1_x + 0.03, 0.365, right1_x + 0.03, 0.33), False),
    ((right1_x + 0.02, 0.33, right1_x + 0.03, 0.33, right1_x + 0.03, 0.295, right1_x + 0.02, 0.295), False),
    ((right1_x + 0.03, 0.355, left1_x + 0.01, 0.355), True),
    ((right1_x + 0.03, 0.305, left1_x + 0.01, 0.305), True),
    # kampfgruppen/motorized -> mechanized
    ((right1_x, 0.685, left1_x, 0.685), True),
    ((left1_x + 0.06, 0.74, left1_x + 0.06, 0.705), True),
    # large unit/inf assault -> armoured ops
    ((right3_x - 0.02, 0.775, right3_x - 0.01, 0.735), True),
    ((left3_x + 0.02, 0.775, left3_x + 0.01, 0.735), True),
    # WW1 thought -> centralized planning
    ((0.02, 0.39, 0.02, 0.265), True),
    # massive forces -> conc art, auftrags -> c3i, foreign -> guerrilla
    ((right1_x + 0.02, 0.22, left1_x, 0.22), True),
    ((right1_x + 0.02, 0.135, left1_x, 0.135), True),
    ((right1_x + 0.02, 0.05, left1_x, 0.05), True),
    # elastic -> fire&retreat + defindepth
    ((right2_x, 0.615, left2_x - 0.02, 0.615), True),
    ((left2_x, 0.645, left2_x - 0.02, 0.645, left2_x - 0.02, 0.595, left2_x, 0.595), False),
    # static -> planning, trench
    ((right2_x, 0.565, right2_x + 0.05, 0.565), True),
    ((right2_x, 0.51, left2_x, 0.51), False),
    ((right2_x + 0.05, 0.565, right2_x + 0.05, 0.51), False),
    # defindepth -> counterattack
    ((right3_x, 0.595, left3_x, 0.595), True),
    # fire&retreat -> strategic demo
    ((right3_x, 0.645, left4_x + 0.06, 0.645), True),
    ((left4_x + 0.06, 0.645, left4_x + 0.06, 0.615), False),
    # rapid react/central def -> start withdraw
    ((right4_x - 0.02, 0.51, right4_x - 0.01, 0.475), True),
    ((left4_x + 0.02, 0.51, left4_x + 0.01, 0.475), True),
    # einheit -> patrols & ambush
    ((left2_x, 0.215, left2_x, 0.17), True),
    ((left2_x + 0.01, 0.17, left2_x, 0.17, left2_x, 0.1, left2_x + 0.01, 0.1), False),
    # einheit -> inf tactics & shoot&escape
    ((right3_x, 0.23, left3_x + 0.06, 0.23), True),
    ((left3_x + 0.06, 0.19, left3_x + 0.06, 0.23, left4_x + 0.06, 0.23, left4_x + 0.06, 0.19), False)
]

land_doct_deact_lines = [
    # bewegungskrieg/rapid/deep/pre-planned/envelopment
    (right1_x, 0.895, left4_x, 0.895),
    # centralized/truppenführung/revisionist
    (0.02, 0.23, 0.02, 0.095),
    # elastic/static defence
    (left1_x + 0.06, 0.6, left1_x + 0.06, 0.585),
    # decisive/op art
    (left1_x + 0.07, 0.34, left1_x + 0.07, 0.325),
    # counterfire/scorched
    (right4_x, 0.56, left4_x, 0.56),
    # officer/subordinate
    (left3_x + 0.07, 0.12, left3_x + 0.07, 0.105)
]

naval_doct_lines = [
    # 19th century -> sea control & ommerce raiding
    ((left1_x + 0.02, 0.965, right1_x, 0.965), True),
    ((right2_x + 0.02, 0.965, left2_x, 0.965), True),
    # commerce def -> convoy sailing
    ((right1_x + 0.01, 0.86, left1_x, 0.86), True),
    # commerce raiding -> emphasis on nav
    ((right3_x, 0.965, left4_x, 0.965), True),
    # sealane interdiction -> lin off / submarine
    ((right3_x, 0.93, left3_x - 0.01, 0.93), True),
    ((left3_x, 0.93, left3_x - 0.01, 0.93, left3_x - 0.01, 0.845, left3_x, 0.845), False),
    # decisive battle -> naval firepower
    ((right1_x + 0.02, 0.635, left1_x + 0.01, 0.635), True),
    # naval firepower -> escort sub + naval attrition
    ((right2_x + 0.01, 0.635, left2_x - 0.01, 0.635), True),
    ((left2_x, 0.67, left2_x - 0.01, 0.67, left2_x - 0.01, 0.635, left2_x, 0.635), False),
    # escort sub + naval attrition -> command of the sea
    ((right3_x, 0.67, right3_x + 0.01, 0.67, right3_x + 0.01, 0.635, right3_x, 0.635), False),
    ((right3_x + 0.01, 0.67, left3_x, 0.67), True),
    # large taskforce / balanced -> naval presence
    ((right4_x + 0.01, 0.635, right4_x + 0.02, 0.635, right4_x + 0.02, 0.58, right4_x + 0.01, 0.58), False),
    ((right4_x + 0.02, 0.61, left4_x, 0.61), True),
    # block enemy ships -> decoy fleet
    ((right1_x + 0.02, 0.575, left1_x + 0.01, 0.575), True),
    # decoy fleet -> battlefleet concentration
    ((right2_x + 0.01, 0.575, left2_x, 0.575), True),
    # fleet-in-being -> decisive/block
    ((0.02, 0.505, 0.02, 0.605), True),
    ((0.04, 0.635, 0.02, 0.635, 0.02, 0.575, 0.04, 0.575), False),
    # fleet-in-being -> combined army-navy / warfare manoeuvres
    ((0.02, 0.47, 0.02, 0.4), True),
    ((0.04, 0.415, 0.02, 0.415, 0.02, 0.3, 0.04, 0.3), False),
    # comb army-navy -> overseas exp
    ((right1_x + 0.02, 0.425, left1_x + 0.01, 0.425), True),
    # overseas exp -> air naval / fleet aux
    ((right2_x + 0.01, 0.435, left2_x, 0.435), True),
    ((left2_x + 0.01, 0.435, left2_x, .435, left2_x, 0.385, left2_x + 0.01, 0.385), False),
    # air naval supr -> fleet aux force
    ((right3_x + 0.01, 0.435, left3_x, 0.485), True),
    # fleet aux cv -> naval superiority
    ((right3_x + 0.01, 0.39, left3_x, 0.355), True),
    # small taskforce, concentrated forces -> national protection
    ((right4_x + 0.02, 0.415, left4_x, 0.375), True),
    ((right4_x + 0.02, 0.29, left4_x, 0.37), True),
    # warfare manoeuvres -> power projection, air-naval supr
    ((0.1, 0.28, 0.1, 0.245), True),
    ((right1_x + 0.02, 0.295, left1_x + 0.01, 0.295), True),
    # air-naval supr -> enemy deployments
    ((right2_x + 0.01, 0.295, left2_x - 0.01, 0.295), True),
    # power projection, air-naval -> fleet def, indirect approach
    ((right1_x, 0.23, left1_x + 0.01, 0.23), True),
    ((left1_x + 0.01, 0.28, left1_x + 0.01, 0.23), True),
    ((left1_x + 0.02, 0.23, left1_x + 0.01, 0.23, left1_x + 0.01, 0.195, left1_x + 0.02, 0.195), False),
    # fleet def -> amphibious comb arms
    ((right2_x + 0.02, 0.22, left2_x, 0.22), True),
    # mass amp op, inderct app, naval av -> naval power
    ((right1_x + 0.02, 0.09, left1_x + 0.02, 0.09), True),
    ((left1_x + 0.08, 0.175, left1_x + 0.08, 0.105), True),
    ((left2_x + 0.03, 0.165, right2_x, 0.105), True)
]

naval_doct_deact_lines = [
    # port prot / invasion ops
    (0.1, 0.81, 0.1, 0.795),
    # antisub patrols / naval participation
    (left1_x + 0.07, 0.81, left1_x + 0.07, 0.795),
    # lim off fleet / submarine fleet
    (left3_x, 0.915, left3_x, 0.86),
    # decisive battle / block enemy ships
    (0.1, 0.62, 0.1, 0.595),
    # large taskforce / balanced
    (left3_x + 0.07, 0.62, left3_x + 0.07, 0.605),
    # air-naval supr / fleet aux cv
    (left2_x + 0.07, 0.42, left2_x + 0.07   , 0.405),
    # comb army-navy / warfare man
    (0.1, 0.4, 0.1, 0.315),
    # naval superiority / area of influence
    (left4_x + 0.05, 0.175, left4_x + 0.05, 0.165)
]

air_doct_lines = [
    # air power -> air superiority
    ((0.02, 0.67, 0.02, 0.95), True),
    # air superiority -> kette, bomber intercept, air patrol, night attack
    ((right1_x, 0.965, left1_x + 0.07, 0.965), True),
    ((left1_x + 0.07, 0.95, left1_x + 0.07, 0.965, left2_x + 0.07, 0.965), False),
    ((left2_x + 0.07, 0.95, left2_x + 0.07, 0.965, left3_x + 0.07, 0.965), False),
    ((left3_x + 0.07, 0.95, left3_x + 0.07, 0.965, left4_x + 0.07, 0.965, left4_x + 0.07, 0.95), False),
    # air power -> independent/tactical
    ((right1_x - 0.01, 0.65, left1_x - 0.02, 0.65), True),
    ((left1_x - 0.01, 0.665, left1_x - 0.02, 0.665, left1_x - 0.02, 0.62, left1_x - 0.01, 0.62), False),
    # independent/tactical -> battlemana, centralc&c, himmelbett
    ((right2_x - 0.01, 0.665, right2_x, 0.665, right2_x, 0.62, right2_x - 0.01, 0.62), False),
    ((right2_x, 0.66, left2_x - 0.02, 0.675), True),
    ((right2_x, 0.64, left2_x - 0.02, 0.64), True),
    ((right2_x, 0.62, left2_x - 0.02, 0.61), True),
    # air power -> bombing
    ((0.07, 0.635, 0.07, 0.585), True),
    # bombing -> strategic, vertical, tactical
    ((0.07, 0.55, 0.07, 0.53), True),
    ((0.07, 0.515, 0.07, 0.53, left1_x + 0.08, 0.53), False),
    ((left1_x + 0.08, 0.515, left1_x + 0.08, 0.53, left2_x + 0.08, 0.53, left2_x + 0.08, 0.515), False),
    # support ground ops -> nearby intercept, dive bombing
    ((right3_x + 0.04, 0.46, left3_x + 0.07, 0.46), True),
    ((left3_x + 0.07, 0.435, left3_x + 0.07, 0.46, left4_x, 0.46), False),
    # nearby intercept, predefined -> harassment
    ((right4_x + 0.02, 0.43, left4_x + 0.01, 0.31), True),
    ((left4_x + 0.01, 0.375, left4_x + 0.01, 0.325), True),
    # hedgehog, harassment -> offesive corridor
    ((left3_x + 0.08, 0.365, left3_x + 0.08, 0.325), True),
    ((left4_x + 0.01, 0.305, right4_x + 0.03, 0.305), True),
    # strategic, supp ground, air interdict -> ombined forces
    ((right1_x + 0.01, 0.5, left1_x + 0.05, 0.365), True),
    ((left2_x + 0.04, 0.46, left2_x + 0.03, 0.46, left2_x + 0.03, 0.43, left2_x + 0.04, 0.43), False),
    ((left2_x + 0.03, 0.445, right2_x + 0.03, 0.365), True)

]

air_doct_deact_lines = [
    # independent / tactical
    (left1_x + 0.06, 0.65, left1_x + 0.06, 0.635)
]
