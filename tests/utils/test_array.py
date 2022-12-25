from sapeur.utils.array import GridList


def test_grid_list_create():
    width = 4
    height = 3
    expected = [[None for col in range(width)] for row in range(height)]
    grid = GridList(width, height, default=None)
    assert grid == expected


def test_grid_list_iter():
    width = 4
    height = 3
    expected = [[(row, col) for col in range(width)] for row in range(height)]
    grid = GridList(width, height, default=None)
    for row in range(height):
        for col in range(width):
            grid[row][col] = (row, col)
    assert grid == expected

    from itertools import chain
    expected_iter = chain(*expected)
    assert list(expected_iter) == list(grid)

def test_grid_list_len():
    width = 4
    height = 3
    grid = GridList(width, height, default=None)
    assert len(grid) == width * height

def test_grid_list_getitem():
    width = 4
    height = 3
    grid = GridList(width, height, default=None)
    for row in range(height):
        for col in range(width):
            grid[row][col] = (row, col)
    for row in range(height):
        assert grid[row] == [(row, col) for col in range(width)]
    for row in range(height):
        for col in range(width):
            assert grid[row, col] == (row, col)
