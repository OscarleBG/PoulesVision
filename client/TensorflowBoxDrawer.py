import numpy as np
import tensorflow as tf
from object_detection.utils import visualization_utils as vis_util

MODEL_PATH = '../poulenet/saved_model'
LABEL_MAP = [
    'Pippa',
    'Pablo',
    'Chipper',
    'Thomas',
    'Sandrine',
    'Arnaud',
]
MIN_CONFIDENCE = 0.8

class BoxDrawer:
    def __init__(self):
        self.model = tf.saved_model.load(MODEL_PATH)
        self.category_index = {i + 1: {'id': i + 1, 'name': LABEL_MAP[i]} for i in range(len(LABEL_MAP))}

    def draw_boxes(self, image):
        detections = self._predict(image)
        image = self._draw_boxes(image, detections)
        return image

    def _predict(self, image):
        image = tf.expand_dims(image, 0)
        detections = self.model(image)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        return detections

    def _draw_boxes(self, image, detections):
        return vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            self.category_index,
            use_normalized_coordinates=True,
            min_score_thresh=MIN_CONFIDENCE)
