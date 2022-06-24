import time
from enum import Enum

from object_detection.utils import visualization_utils as vis_util
from decouple import config
from PIL import Image

OUTSIDE_BOUNDING_BOX = ((0.25, 0), (1, 1))
IMAGE_SIZE = (config("IMAGE_WIDTH", cast=int), config("IMAGE_HEIGHT", cast=int))

TRACKED_OBJECTS = ['Pippa', 'Pablo', 'Chipper']


class State(Enum):
    INSIDE = 1
    OUTSIDE = 2
    CUISINE = 3
    UNKNOWN = 4


def preview_bounding_box(image=Image.open("../test_image.jpg")):
    (x_min, y_min), (x_max, y_max) = OUTSIDE_BOUNDING_BOX
    vis_util.draw_bounding_box_on_image(image, y_min, x_min, y_max, x_max, color='red', thickness=4)
    image.show()


def update(detections):
    print(detections)


class ObjectsTracker:
    def __init__(self):
        self.objects = {name: ObjectTracker(name) for name in TRACKED_OBJECTS}

    def update(self, detected_objects, detected_objects_positions) -> None:
        for object, (ymin, xmin, ymax, xmax) in zip(detected_objects, detected_objects_positions):
            object_pos_point = (xmin + xmax) / 2, (ymin + ymax) / 2
            self.objects[object].update(object_pos_point)

    def __str__(self):
        return '\n'.join(f'{name} is {self.objects[name].get_state()}' for name in self.objects)


class ObjectTracker:
    def __init__(self, object_name):
        self.object = object_name
        self._state = State.UNKNOWN
        self._last_seen_coordinates = None
        self._last_seen_time = None

    def update_state(self, coordinates) -> None:
        _last_seen_time = time.time()
        _last_seen_coordinates = coordinates
        if OUTSIDE_BOUNDING_BOX[0][0] < coordinates[0] < OUTSIDE_BOUNDING_BOX[1][0] and \
                OUTSIDE_BOUNDING_BOX[0][1] < coordinates[1] < OUTSIDE_BOUNDING_BOX[1][1]:
            self._state = State.INSIDE
        else:
            self._state = State.OUTSIDE

    def get_state(self) -> str:
        if time.time() - self._last_seen_time < 5:
            # they were seen less than 5 seconds ago
            return 'in ' + State.CUISINE.name
        else:
            return self._state.name
