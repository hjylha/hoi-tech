
right1_x = 0.14
left1_x = 0.2

right2_x = 0.32
left2_x = 0.4


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