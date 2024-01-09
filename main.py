# main.py

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image


def perform_object_detection(image_path):
    processor = DetrImageProcessor.from_pretrained(
        "./", revision="no_timm", local_files_only=True
    )
    model = DetrForObjectDetection.from_pretrained(
        "./", revision="no_timm", local_files_only=True
    )

    image = Image.open(image_path)

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.9
    )[0]

    detected_objects = []

    for score, label, box in zip(
        results["scores"], results["labels"], results["boxes"]
    ):
        box = [round(i, 2) for i in box.tolist()]
        detected_objects.append(
            {
                "label": model.config.id2label[label.item()],
                "confidence": round(score.item(), 3),
                "bounding_box": box,
            }
        )

    return detected_objects


if __name__ == "__main__":
    detected_objects = perform_object_detection("shutterstock_2164898457.jpg")
    print(detected_objects)
