import particle

class SpatialHashMap:
    
    def __init__(self, grid_dimensions: list, cell_size: int) -> None:
        self.width = 0
        self.height = 0
        self.left = grid_dimensions[0]
        self.bottom = grid_dimensions[2]
        self.cell_size = cell_size
        self.map = None
        self.list = []
        self._initialize_map(grid_dimensions)
    
    def _initialize_map(self, grid_dimensions: list):
        self.width = ((grid_dimensions[1] - grid_dimensions[0]) // self.cell_size) + 1
        self.height = ((grid_dimensions[3] - grid_dimensions[2]) // self.cell_size) + 1
        self.cell_size = self.cell_size
        cell_num = self.width * self.height
        self.map = [[] for _ in range(cell_num)]
        
    def _hash(self, coords: tuple):
        x = coords[0] - self.left
        y = coords[1] - self.bottom
        i = (x // self.cell_size)
        j = (y // self.cell_size)
        
        if x < 0: i = 0
        elif x > self.width * self.cell_size: i = self.width - 1
        if y < 0: j = 0
        elif y > self.height * self.cell_size: j = self.height - 1
        
        return int(j * self.width + i)
    
    def insert(self, coords: tuple, item):
        self.map[self._hash(coords)].append(item)
        self.list.append(item)
        
    def remove(self, coords: tuple, item):
        self.map[self._hash(coords)].remove(item)
        self.list.remove(item)
        
    def get_collisions(self):
        collisions = []

        for i, bucket in enumerate(self.map):
            for a in range(len(bucket)):
                if bucket[a].collisionless: continue

                # This bucket
                for b in range(a+1, len(bucket)):
                    if bucket[b].collisionless: continue
                    if bucket[a].collides_with(bucket[b]):
                        collisions.append((bucket, a, bucket, b))

                buckets_to_check = []
                # (x+1, y) bucket
                if (i % self.width) + 1 < self.width:
                    buckets_to_check.append(self.map[i + 1])

                    # (x+1, y-1) bucket
                    if i - self.width >= 0:
                        buckets_to_check.append(self.map[i - self.width + 1])

                # (x, y-1) bucket
                if i -self.width >= 0:
                    buckets_to_check.append(self.map[i - self.width])

                    # (x-1, y-1) bucket
                    if i % self.width >= 1:
                        buckets_to_check.append(self.map[i - self.width - 1])

                for neighbour in buckets_to_check:
                    for b in range(len(neighbour)):
                        if neighbour[b].collisionless: continue
                        if bucket[a].collides_with(neighbour[b]):
                            collisions.append((bucket, a, neighbour, b))

        return collisions
    
    def update_positions(self, box: list, delta: int):
        cols = self.get_collisions()
        for bucket1, a, bucket2, b in cols:
            particle.collide(bucket1[a], bucket2[b])
        
        items = []
        for bucket in self.map:
            while len(bucket) > 0:
                items.append(bucket.pop())
        for item in items:
            item.update_position(box, delta)
            self.map[self._hash((item.x, item.y))].append(item)