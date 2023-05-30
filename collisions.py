import particle

class collision_grid:

    def __init__(self, width: int, height: int, blocksize: int):
        self.blocksize = blocksize
        self.blockwidth = (width // blocksize) + 1
        self.blockheight = (height // blocksize) + 1
        self.size = self.blockheight * self.blockwidth
        self.hashmap = self._create_map()
        
    def _create_map(self):
        return [[] for _ in range(self.size)]
    
    def _get_index(self, x: int, y: int):
        return x * self.blockwidth + y
    
    def add_particle(self, p: particle):
        for i in range(self.blockwidth):
            left_wall = i * self.blocksize
            for j in range(self.blockheight):
                bottom_wall = j * self.blocksize
                if p.x >= left_wall and p.x <= left_wall + self.blocksize and p.y >= bottom_wall and p.y <= bottom_wall + self.blocksize:
                    self.hashmap[self._get_index(i, j)].append(p)
                    p.occupied_blocks.append(self._get_index(i, j))
                    
    def reset_map(self):
        self.hashmap = self._create_map()
    
                