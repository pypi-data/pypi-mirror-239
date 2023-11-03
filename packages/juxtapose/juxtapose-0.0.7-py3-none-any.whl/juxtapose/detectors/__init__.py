from .groundingdino import GroundingDino
from .rtmdet import RTMDet
from .yolov8 import YOLOv8

DET_MAP = {"rtmdet": RTMDet, "groundingdino": GroundingDino, "yolov8": YOLOv8}


def get_detector(model: str = "rtmdet-l", *args, **kwargs):
    if model.startswith("groundingdino"):
        return DET_MAP["groundingdino"]("", *args, **kwargs)

    type, size = model.split("-")

    return DET_MAP[type](size, *args, **kwargs)
