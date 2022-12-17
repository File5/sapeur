import arcade


def create_cells_triangles(row_count, column_count, width, height, color=arcade.color.GRAY):
    point_list = []
    for row in range(row_count):
        for column in range(column_count):
            if row % 2 == 0:
                x = width * column
            else:
                x = width * (column_count - column - 1)
            y = height * row
            if column + 1 == column_count:
                if row % 2 == 0:
                    point_list.extend(((x, y), (x + width, y), (x + width, y + height)))
                else:
                    point_list.extend(((x + width, y), (x, y), (x + width, y + height), (x + width, y + height)))
            else:
                point_list.extend(((x, y), (x + width, y + height), (x + width, y))[::1 if row % 2 == 0 else -1])
    return point_list, [color] * len(point_list)


def create_cells_upper_triangles2(row_count, column_count, width, height, color=arcade.color.WHITE):
    point_list = []
    for row in range(row_count):
        for column in range(column_count):
            if row % 2 == 0:
                x = width * column
            else:
                x = width * (column_count - column - 1)
            y = height * row
            middle_point = (x, y + height)
            if column + 1 == column_count:
                if row % 2 == 0:
                    #point_list.extend(((x + width, y + height), (x, y), middle_point, middle_point))
                    point_list.extend(((x, y), middle_point, (x + width, y + height)))
                    #point_list.extend((middle_point, middle_point, (x + width, y + height), (x, y)))
                else:
                    point_list.extend((middle_point, (x, y), (x + width, y + height)))
            else:
                point_list.extend((middle_point, (x, y), (x + width, y + height))[::1 if row % 2 == 0 else -1])
    return point_list[:12 * 3], [color] * len(point_list)


def create_cells_upper_triangles(row_count, column_count, width, height, color=arcade.color.WHITE):
    point_list = []
    for row in range(row_count):
        for column in range(column_count):
            if row % 2 == 1:
                x = width * column
            else:
                x = width * (column_count - column - 1)
            y = height * row
            middle_point = (x, y + height)
            if column + 1 == column_count:
                if row % 2 == 0:
                    point_list.extend(((x, y), middle_point, (x + width, y + height))[::-1])
                else:
                    point_list.extend((middle_point, (x + width, y + height), (x, y), middle_point, middle_point))
            else:
                point_list.extend((middle_point, (x, y), (x + width, y + height))[::1 if row % 2 == 1 else -1])
    return point_list, [color] * len(point_list)

