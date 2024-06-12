import math

def get_arrow_points(x1, y1, x2, y2, length=0.02):
    if x1 == x2 and y1 == y2:
        return (x1, y1, x1, y1, x1, y1)
    mid_point = ((x1 + x2) / 2, (y1 + y2) / 2)
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    direction = ((x2 - x1) / dist, (y2 - y1) / dist)
    normal_direction = (-direction[1], direction[0])

    new_x1 = mid_point[0] + length * direction[0]
    new_y1 = mid_point[1] + length * direction[1]

    new_x2 = mid_point[0] + length * normal_direction[0]
    new_y2 = mid_point[1] + length * normal_direction[1]

    new_x3 = mid_point[0] - length * normal_direction[0]
    new_y3 = mid_point[1] - length * normal_direction[1]

    return new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x1, new_y1


def round_points(points, num_of_decimals):
    return [round(num, num_of_decimals) for num in points]


def get_rounded_arrow_points(x1, y1, x2, y2, length=0.006, num_of_decimals=4):
    arrow_points = get_arrow_points(x1, y1, x2, y2, length)
    return round_points(arrow_points, num_of_decimals)


def scale_arrows(size, origin, points):
    x_multiplier, y_multiplier = size
    x0, y0 = origin
    scaled_points = []
    for i, point in enumerate(points):
        if i & 2 == 1:
            scaled_points.append(x0 + x_multiplier * point)
        else:
            scaled_points.append(y0 + y_multiplier * point)
    return scaled_points
