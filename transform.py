import vector_geom as vg
import math

class SimilarityTransform:

    def __init__(self, theta, scale):
        self.theta = theta  # in radians
        self.scale = scale

    def __call__(self, point: vg.Point) -> vg.Point:
        return vg.Point(self.scale * (math.cos(self.theta) * point.x - math.sin(self.theta) * point.y),
                        self.scale * (math.sin(self.theta) * point.x + math.cos(self.theta) * point.y))

    def inverse(self, point: vg.Point) -> vg.Point:
        return vg.Point((math.cos(self.theta) * point.x + math.sin(self.theta) * point.y) / self.scale,
                        (-math.sin(self.theta) * point.x + math.cos(self.theta) * point.y) / self.scale)


transform_identity = SimilarityTransform(theta=0, scale=1)
