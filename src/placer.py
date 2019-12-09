from terrain import Terrain


class Placer:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not Placer.instance:
            Placer.instance = object.__new__(cls)
        return Placer.instance

    def __init__(self, terrain: Terrain):
        self.terrain_set = terrain.terrain_set.copy()



# p = Placer('p')
# print(p.terrain, id(p))
# q = Placer('q')
# print(p.terrain, id(q))
