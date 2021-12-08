import numpy as np

from dataclasses import dataclass, field


@dataclass
class BBoxData:
    img: np.ndarray
    img_name: str
    coco_coords: np.ndarray(shape=(), dtype=float)
    voc_coords: np.ndarray(shape=(), dtype=int) = field(init=False, repr=False)
    class_counts: np.zeros(shape=(), dtype=int) = field(init=False, repr=False)

    def __post_init__(self):
        self.set_voc_coords()
        self.class_counts = self.set_class_counts()

    def __repr__(self):
        return f"---> {self.img_name}\n {self.coco_coords}\n"

    def set_voc_coords(self):
        self.voc_coords = [self.convert_coco_to_voc(ele) for ele in self.coco_coords]

    def set_class_counts(self):
        x = np.zeros(shape=(4,), dtype=int)
        for ele in self.coco_coords:
            x[int(ele[0])] += 1

        return x
    
    def convert_coco_to_voc(self, coords):
        size = self.img.shape
        x2 = int(((2 * size[1] * float(coords[1])) + (size[1] * float(coords[3]))) / 2)
        x1 = int(((2 * size[1] * float(coords[1])) - (size[1] * float(coords[3]))) / 2)
        y2 = int(((2 * size[0] * float(coords[2])) + (size[0] * float(coords[4]))) / 2)
        y1 = int(((2 * size[0] * float(coords[2])) - (size[0] * float(coords[4]))) / 2)

        return np.array([coords[0], x1, y1, x2, y2], dtype=int)





