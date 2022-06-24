from os import path

import cv2
import numpy as np
import tensorflow as tf
from decouple import config
from telegram_notifier import TelegramNotifier
from object_tracking import ObjectsTracker
from object_detection.utils import visualization_utils as vis_util

MODEL_PATH = "../poulenet/saved_model"
LABEL_MAP = [
    "Pippa",
    "Pablo",
    "Chipper",
    "Thomas",
    "Sandrine",
    "Arnaud",
]

TELEGRAM_SHOW_BOXES = config("TELEGRAM_SHOW_BOXES", cast=bool)


def draw_boxes(image, detections, category_index, min_confidence):
    return vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        detections["detection_boxes"],
        detections["detection_classes"],
        detections["detection_scores"],
        category_index,
        use_normalized_coordinates=True,
        min_score_thresh=min_confidence,
    )


class PouleNet:
    def __init__(self):
        self.objects_tracker = (
            ObjectsTracker.load()
            if path.exists("objects_tracker.pkl")
            else ObjectsTracker()
        )
        self.model = tf.saved_model.load(MODEL_PATH)
        self.category_index = {
            i + 1: {"id": i + 1, "name": LABEL_MAP[i]} for i in range(len(LABEL_MAP))
        }
        self.telegram_notifier = TelegramNotifier(objects_tracker=self.objects_tracker)
        self.min_confidence = config("MIN_CONFIDENCE", cast=float)

    def process(self, image):
        detections = self._predict(image)
        image_with_boxes = draw_boxes(
            image.copy(), detections, self.category_index, self.min_confidence
        )
        self._on_object_detected(image, image_with_boxes, detections)
        return image_with_boxes

    def _predict(self, image):
        image = tf.expand_dims(image, 0)
        detections = self.model(image)
        num_detections = int(detections.pop("num_detections"))
        detections = {
            key: value[0, :num_detections].numpy() for key, value in detections.items()
        }
        detections["num_detections"] = num_detections
        detections["detection_classes"] = detections["detection_classes"].astype(
            np.int64
        )
        return detections

    def _on_object_detected(self, image, image_with_boxes, detections):
        detected_objects = [
            LABEL_MAP[i - 1]
            for i in detections["detection_classes"][
                detections["detection_scores"] > self.min_confidence
                ]
        ]
        detected_objects_positions = [
            i
            for i in detections["detection_boxes"][
                detections["detection_scores"] > self.min_confidence
                ]
        ]

        self.objects_tracker.update(detected_objects, detected_objects_positions)
        self.telegram_notifier.update()

        if len(detected_objects) <= 0:
            return

        self.telegram_notifier.notify(image_with_boxes if TELEGRAM_SHOW_BOXES else image, detected_objects)


# if __name__ == "__main__":
#     poule_net = PouleNet()
#     image = cv2.imread("../test_image.jpg")
#     image_with_boxes = poule_net.process(image)
#     image_with_boxes.show()
