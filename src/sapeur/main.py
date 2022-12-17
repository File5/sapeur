"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.
"""
import arcade

from sapeur.graphics.cells import create_cells_triangles

# Set how many rows and columns we will have
ROW_COUNT = 10
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = WIDTH

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 0
IMARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Set up the application.
        """
        super().__init__(width, height)
        self.grid = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
        self.rect_grid = [[None for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(arcade.create_triangles_filled_with_colors(
            *create_cells_triangles(ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, color=arcade.color.GRAY)
        ))
        self.shape_list.append(arcade.create_triangles_filled_with_colors(
            *create_cells_triangles(ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, upper=True, color=arcade.color.WHITE)
        ))
        self.sprite_list = arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.DARK_GRAY

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                rect = arcade.SpriteSolidColor(WIDTH - IMARGIN * 2, HEIGHT - IMARGIN * 2, arcade.color.WHITE)
                rect.center_x = x
                rect.center_y = y
                rect.color = color
                self.rect_grid[row][column] = rect
                self.sprite_list.append(rect)


    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()
        # This command has to happen before we start drawing
        arcade.start_render()
        # Draw the grid
        self.shape_list.draw()
        self.sprite_list.draw()
        arcade.draw_text(f"FPS: {arcade.get_fps():.2f}", 10, 20, arcade.color.RED, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the location between 1 and 0.
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
                self.rect_grid[row][column].color = arcade.color.GREEN
            else:
                self.grid[row][column] = 0
                self.rect_grid[row][column].color = arcade.color.DARK_GRAY


def main():
    arcade.enable_timings()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
