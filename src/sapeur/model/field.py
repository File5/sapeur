from sapeur.utils.array import GridList


class MinesweeperField:
    def __init__(self, width, height, mine_count):
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.content_grid = GridList(width, height, 0)
        self.user_grid = GridList(width, height, 0)
        self.game_ended = False

        self.generate_mines()

    def generate_mines(self):
        import random
        for _ in range(self.mine_count):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.content_grid[x, y] != -1:
                    self.content_grid[x, y] = -1
                    break
        for y in range(self.height):
            for x in range(self.width):
                if self.content_grid[x, y] == -1:
                    continue
                for y2 in range(max(y - 1, 0), min(y + 2, self.height)):
                    for x2 in range(max(x - 1, 0), min(x + 2, self.width)):
                        if self.content_grid[x2, y2] == -1:
                            self.content_grid[x, y] += 1

    def auto_open(self, x, y):
        if self.user_grid[x, y] != 1 or self.content_grid[x, y] != 0:
            return
        to_open = [(x, y)]
        while to_open:
            x, y = to_open.pop()
            self.user_grid[x, y] = 1
            if self.content_grid[x, y] == 0:
                for y2 in range(max(y - 1, 0), min(y + 2, self.height)):
                    for x2 in range(max(x - 1, 0), min(x + 2, self.width)):
                        if self.user_grid[x2, y2] == 0:
                            to_open.append((x2, y2))

    @property
    def flag_count(self):
        return sum(1 for x in self.user_grid if x == 2)
