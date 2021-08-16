

import numpy as np
import tensorflow as tf
from cv2 import resize
from utils import visualization_utils
import gradio as gr

MODEL_FILE = "../models/model_efficientdet.tflite"

LABELS = ['person',
          'bicycle',
          'car',
          'motorcycle',
          'airplane',
          'bus',
          'train',
          'truck',
          'boat',
          'traffic light',
          'fire hydrant',
          'street sign',
          'stop sign',
          'parking meter',
          'bench',
          'bird',
          'cat',
          'dog',
          'horse',
          'sheep',
          'cow',
          'elephant',
          'bear',
          'zebra',
          'giraffe',
          'hat',
          'backpack',
          'umbrella',
          'shoe',
          'eye glasses',
          'handbag',
          'tie',
          'suitcase',
          'frisbee',
          'skis',
          'snowboard',
          'sports ball',
          'kite',
          'baseball bat',
          'baseball glove',
          'skateboard',
          'surfboard',
          'tennis racket',
          'bottle',
          'plate',
          'wine glass',
          'cup',
          'fork',
          'knife',
          'spoon',
          'bowl',
          'banana',
          'apple',
          'sandwich',
          'orange',
          'broccoli',
          'carrot',
          'hot dog',
          'pizza',
          'donut',
          'cake',
          'chair',
          'couch',
          'potted plant',
          'bed',
          'mirror',
          'dining table',
          'window',
          'desk',
          'toilet',
          'door',
          'tv',
          'laptop',
          'mouse',
          'remote',
          'keyboard',
          'cell phone',
          'microwave',
          'oven',
          'toaster',
          'sink',
          'refrigerator',
          'blender',
          'book',
          'clock',
          'vase',
          'scissors',
          'teddy bear',
          'hair drier',
          'toothbrush',
          'hair brush']

category_index = {i: {"id": i, "name": LABELS[i]} for i in range(len(LABELS))}

# Read the model
interpreter: tf.lite.Interpreter = tf.lite.Interpreter(MODEL_FILE)
interpreter.allocate_tensors()

# Getting the input and output tensors
input_details: list = interpreter.get_input_details()
output_details: list = interpreter.get_output_details()


def process_image(image: np.array, threshold: float, max_boxes: float):
    original_image: np.array = np.copy(image)
    image = resize(image, dsize=(448, 448))
    image = np.expand_dims(image, axis=0)

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    boxes: np.array = interpreter.get_tensor(output_details[0]['index'])
    classes: np.array = interpreter.get_tensor(output_details[1]['index'])
    scores: np.array = interpreter.get_tensor(output_details[2]['index'])

    image = visualization_utils.visualize_boxes_and_labels_on_image_array(
        original_image,
        boxes[0],
        classes[0].astype(np.uint32),
        scores[0],
        category_index,
        use_normalized_coordinates=True,
        min_score_thresh=threshold,
        max_boxes_to_draw=int(max_boxes) + 1
    )

    return image


if __name__ == "__main__":
    input_image = gr.inputs.Image(shape=None, source="upload", label="Image")
    input_threshold = gr.inputs.Slider(minimum=0, maximum=1, default=0.3, label="Threshold")
    input_max_boxes = gr.inputs.Slider(minimum=1, maximum=20, default=10, step=1, label="Max number of boxes")
    output = gr.outputs.Image(type="numpy", labeled_segments=False, label="Segmented image")
    interface = gr.Interface(fn=process_image, inputs=[input_image, input_threshold, input_max_boxes], outputs=output)
    interface.launch(inbrowser=True)
