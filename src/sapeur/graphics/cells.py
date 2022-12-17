import arcade


def create_cells_triangles(row_count, column_count, width, height, upper=False, color=arcade.color.GRAY):
    point_list = []
    upper_m = 1 if upper else 0
    upper_r = -1 if upper else 1
    for row in range(row_count):
        for column in range(column_count):
            if row % 2 == upper_m:
                x = width * column
            else:
                x = width * (column_count - column - 1)
            y = height * row
            if upper:
                middle_point = (x, y + height)
            else:
                middle_point = (x + width, y)
            if column + 1 == column_count:
                if row % 2 == 0:
                    point_list.extend(((x, y), middle_point, (x + width, y + height))[::upper_r])
                else:
                    if upper:
                        point_list.extend((middle_point, (x + width, y + height), (x, y), middle_point, middle_point))
                    else:
                        point_list.extend((middle_point, (x, y), (x + width, y + height), (x + width, y + height)))
            else:
                if upper:
                    point_list.extend((middle_point, (x, y), (x + width, y + height))[::1 if row % 2 == 1 else -1])
                else:
                    point_list.extend(((x, y), (x + width, y + height), middle_point)[::1 if row % 2 == 0 else -1])
    return point_list, [color] * len(point_list)


def create_cells_rectangles(
        sprite_list, rect_grid,
        row_count, column_count, width, height, imargin,
        color=arcade.color.DARK_GRAY):
    for row in range(row_count):
        for column in range(column_count):
            # Do the math to figure out where the box is
            x = (width) * column + width // 2
            y = (height) * row + height // 2
            rect = arcade.SpriteSolidColor(width - imargin * 2, height - imargin * 2, arcade.color.WHITE)
            rect.center_x = x
            rect.center_y = y
            rect.color = color
            rect_grid[row][column] = rect
            sprite_list.append(rect)
