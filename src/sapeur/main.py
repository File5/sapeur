"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.
"""
import arcade
import arcade.gui

from time import time

from sapeur.graphics.cells import create_cells_triangles, create_cells_rectangles
from sapeur.graphics.cells import create_empty_cell, create_pressed_cell, create_text_cell
from sapeur.graphics.textures import FlagSSprite, GeneralIconsTextureSheet, BombSprite
from sapeur.model.field import MinesweeperField
from sapeur.utils.array import GridList

# Set how many rows and columns we will have
ROW_COUNT = 9
COLUMN_COUNT = 9

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = WIDTH

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 0
IMARGIN = 5

TOP_SECTION_HEIGHT = 50

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN + TOP_SECTION_HEIGHT


class TopSection(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int, field: MinesweeperField, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

        self.field = field

    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.general_icons = GeneralIconsTextureSheet()
        self.bomb_sprite = BombSprite(self.general_icons)
        self.bomb_sprite.width = WIDTH
        self.bomb_sprite.height = HEIGHT
        self.bomb_sprite.center_x = self.left + 10 + WIDTH // 2
        self.bomb_sprite.center_y = self.bottom + TOP_SECTION_HEIGHT // 2
        self.bomb_counter = arcade.gui.UILabel(
            self.left + 20 + WIDTH, self.bottom + 10,
            width=100,
            text="10", font_name="Kenney Future", font_size=20, text_color=arcade.color.BLACK
        )
        self.timer = arcade.gui.UILabel(
            self.right - 110, self.bottom + 10,
            width=100,
            text="0", font_name="Kenney Future", font_size=20, text_color=arcade.color.BLACK,
            align="right"
        )
        self.manager.add(self.bomb_counter)
        self.manager.add(self.timer)
        self.start_time = time()

    def on_update(self, delta_time: float):
        self.bomb_counter.text = str(self.field.mine_count - self.field.flag_count)
        self.timer.text = str(int(time() - self.start_time))

    def on_draw(self):
        arcade.start_render()
        #arcade.draw_point(self.left + 10, self.top + 10, arcade.color.RED, 10)
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, arcade.color.DARK_GRAY)
        self.bomb_sprite.draw()
        self.manager.draw()
        # arcade.draw_lrtb_rectangle_outline(
        #     self.bomb_counter.left, self.bomb_counter.right, self.bomb_counter.top, self.bomb_counter.bottom, arcade.color.MAGENTA, 1
        # )
        # arcade.draw_lrtb_rectangle_outline(
        #     self.bomb_sprite.left, self.bomb_sprite.right, self.bomb_sprite.top, self.bomb_sprite.bottom, arcade.color.CYAN, 1
        # )


class FieldSection(arcade.Section):

    def __init__(self, left: int, bottom: int, width: int, height: int, field: MinesweeperField, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)
        self.rect_grid = GridList(COLUMN_COUNT, ROW_COUNT)
        self.opened_grid = GridList(COLUMN_COUNT, ROW_COUNT)
        self.text_grid = GridList(COLUMN_COUNT, ROW_COUNT)
        self.flag_grid = GridList(COLUMN_COUNT, ROW_COUNT)

        self.field = field

    def setup(self):
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(arcade.create_triangles_filled_with_colors(
            *create_cells_triangles(ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, color=arcade.color.GRAY)
        ))
        self.shape_list.append(arcade.create_triangles_filled_with_colors(
            *create_cells_triangles(ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, upper=True, color=arcade.color.WHITE)
        ))
        self.sprite_list = arcade.SpriteList()
        create_cells_rectangles(
            self.sprite_list, self.rect_grid,
            ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, IMARGIN,
            color=arcade.color.DARK_GRAY
        )
        self.open_shape_list = arcade.ShapeElementList()
        self.text_sprite_list = arcade.SpriteList()
        self.pressed_cell = None
        self.pressed_shape_list = None
        self.user_sprite_list = arcade.SpriteList()

    def on_draw(self):
        """
        Render the screen.
        """

        # Draw the grid
        self.shape_list.draw()
        self.sprite_list.draw()
        self.open_shape_list.draw()
        self.text_sprite_list.draw()
        if self.pressed_shape_list:
            self.pressed_shape_list.draw()
        self.user_sprite_list.draw()
        arcade.draw_text(f"FPS: {arcade.get_fps():.2f}", 10, 20, arcade.color.RED, 14)

    def _create_pressed_cell(self):
        row, column = self.pressed_cell
        if self.field.user_grid[row, column] == 0:
            pressed_cell = create_pressed_cell(
                WIDTH, HEIGHT, WIDTH * column + WIDTH // 2, HEIGHT * row + HEIGHT // 2
            )
            self.pressed_shape_list = pressed_cell
        else:
            self.pressed_shape_list = None

    def _create_opened_cell(self, row, column):
        opened_cell = create_empty_cell(
            WIDTH, HEIGHT, WIDTH * column + WIDTH // 2, HEIGHT * row + HEIGHT // 2
        )
        self.opened_grid[row, column] = opened_cell
        for shape in opened_cell:
            self.open_shape_list.append(shape)

    def _remove_opened_cell(self, row, column):
        opened_cell = self.opened_grid[row, column]
        if opened_cell is not None:
            self.opened_grid[row, column] = None
            for shape in opened_cell:
                self.open_shape_list.remove(shape)

    def _create_text_cell(self, row, column, cell_content):
        text = str(cell_content)
        text_sprite = create_text_cell(WIDTH * column + WIDTH // 2, HEIGHT * row + HEIGHT // 2, text)
        self.text_grid[row, column] = text_sprite
        self.text_sprite_list.append(text_sprite)

    def _remove_text_cell(self, row, column):
        text_sprite = self.text_grid[row, column]
        if text_sprite:
            self.text_grid[row, column] = None
            self.text_sprite_list.remove(text_sprite)

    def _update_opened_cells(self):
        for row in range(self.field.user_grid.height):
            for column in range(self.field.user_grid.width):
                if self.field.user_grid[row, column] == 1:
                    opened_cell = self.opened_grid[row, column]
                    if opened_cell is None:
                        self._create_opened_cell(row, column)
                        cell_content = self.field.content_grid[row, column]
                        if cell_content != 0:
                            text = str(cell_content)
                            text_sprite = create_text_cell(WIDTH * column + WIDTH // 2, HEIGHT * row + HEIGHT // 2, text)
                            self.text_grid[row, column] = text_sprite
                            self.text_sprite_list.append(text_sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        # Change the x/y screen coordinates to grid coordinates
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)

        if row < ROW_COUNT and column < COLUMN_COUNT:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.pressed_cell = (row, column)
                self._create_pressed_cell()

    def on_mouse_motion(self, x, y, dx, dy):
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)

        if self.pressed_cell and self.pressed_cell != (row, column):
            self.pressed_cell = (row, column)
            self._create_pressed_cell()

    def on_left_mouse_release(self, column, row):
        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the location between 1 and 0.
            if self.field.user_grid[row, column] == 0:
                self.field.user_grid[row, column] = 1
                self.rect_grid[row][column].color = arcade.color.GREEN
                self._create_opened_cell(row, column)
                cell_content = self.field.content_grid[row, column]
                if cell_content != 0:
                    self._create_text_cell(row, column, cell_content)
                else:
                    self.field.auto_open(row, column)
                    self._update_opened_cells()

            elif self.field.user_grid[row, column] == 1:
                self.field.user_grid[row, column] = 0
                self.rect_grid[row][column].color = arcade.color.DARK_GRAY
                self._remove_opened_cell(row, column)
                self._remove_text_cell(row, column)
        if self.pressed_cell is not None:
            self.pressed_cell = None
            self.pressed_shape_list = None

    def on_right_mouse_release(self, column, row):
        if row < ROW_COUNT and column < COLUMN_COUNT:
            # Flip the location between 1 and 0.
            if self.field.user_grid[row, column] == 0:
                self.field.user_grid[row, column] = 2

                flag_sprite = FlagSSprite("red")
                flag_sprite.center_x = WIDTH * column + WIDTH // 2
                flag_sprite.center_y = HEIGHT * row + HEIGHT // 2
                flag_sprite.width = WIDTH
                flag_sprite.height = HEIGHT
                self.flag_grid[row, column] = flag_sprite
                self.user_sprite_list.append(flag_sprite)
            elif self.field.user_grid[row, column] == 2:
                self.field.user_grid[row, column] = 0
                self.rect_grid[row][column].color = arcade.color.DARK_GRAY

                flag_sprite = self.flag_grid[row, column]
                self.flag_grid[row, column] = None
                self.user_sprite_list.remove(flag_sprite)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.on_left_mouse_release(column, row)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.on_right_mouse_release(column, row)

class GameView(arcade.View):

    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

        self.field = MinesweeperField(ROW_COUNT, COLUMN_COUNT, 10)

        self.top_section = TopSection(0, SCREEN_HEIGHT - TOP_SECTION_HEIGHT, SCREEN_WIDTH, TOP_SECTION_HEIGHT, self.field)
        self.field_section = FieldSection(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - TOP_SECTION_HEIGHT, self.field)
        self.section_manager.add_section(self.top_section)
        self.section_manager.add_section(self.field_section)

    def setup(self):
        self.top_section.setup()
        self.field_section.setup()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Set up the application.
        """
        super().__init__(width, height)
        self.game_view = GameView(self)

    def setup(self):
        self.game_view.setup()
        self.show_view(self.game_view)


def main():
    arcade.enable_timings()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
