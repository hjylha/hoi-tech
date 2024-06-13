
right1_x = 0.14
left1_x = 0.2

right2_x = 0.32
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
    ((right1_x, 0.905, left2_x, 0.905), True)

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
