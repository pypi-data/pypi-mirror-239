from rataGUI.plugins.base_plugin import BasePlugin
from rataGUI.utils import slugify

import os
import csv
import cv2
# import json
import numpy as np
import tensorflow as tf
from datetime import datetime

import logging
logger = logging.getLogger(__name__)


class DLCInference(BasePlugin):
    """
    Plugin that inferences on frames using trained DLC model to predict animal pose and write keypoints as metadata
    """

    DEFAULT_CONFIG = {
        "Model directory": "",
        "Save file (.csv)": "data",
        # "Model type": ["Default"], # "TensorRT", "TFLite"
        "Inference FPS": ["Match Camera", "Every Interval"],
        "Scale factor": 1.0,
        "Fixed Interval": 0, 
        "Score Threshold": 0.5,
        "Batch Processing": {"Disabled": False, "Enabled": True}, # TODO
        "Draw on frame": {"Disabled": False, "Enabled": True},
        "Write to file": {"Disabled": False, "Enabled": True},
        "Publish to socket": {"Disabled": False, "Enabled": True},
    }

    def __init__(self, cam_widget, config, queue_size=0):
        super().__init__(cam_widget, config, queue_size)
        self.model_dir = os.path.normpath(os.path.abspath(config.get("Model directory")))

        try:
            self.model = load_frozen_model(self.model_dir)
            self.model_input = self.model.inputs[0]

            # Warm start to load cuDNN
            input_shape = self.model_input.shape.as_list()
            self.batch_size = 1
            self.input_height = input_shape[1]  # None
            self.input_width = input_shape[2]   # None
            self.num_channels = input_shape[3]  # 3 (no grayscale)

            dummy_frame = tf.zeros(shape=(self.batch_size, 1, 1, self.num_channels), dtype=self.model_input.dtype) # Arbitrary size
            self.model(tf.constant(dummy_frame))
        except Exception as err:
            logger.exception(err)
            logger.debug("Unable to load model ... auto-disabling DLC Inference plugin")
            self.active = False

        self.interval = 0
        self.poses = []
        
        self.save_file = None
        self.csv_writer = None
        if config.get("Write to file"):
            file_name = slugify(config.get("Save file (.csv)"))
            if len(file_name) == 0: # Use default file name
                file_name = slugify(cam_widget.camera.getDisplayName()) + "_DLCInference_" + datetime.now().strftime('%H-%M-%S') + ".csv"
            elif not file_name.endswith('.csv'):
                file_name += '.csv'

            self.file_path = os.path.join(cam_widget.save_dir, file_name)
            self.save_file = open(file_name, 'w')
            self.csv_writer = csv.writer(self.save_file)

        self.socket_trigger = None
        if config.get("Publish to socket"):
            triggers = []
            for trigger in cam_widget.triggers:
                if type(trigger).__name__ == "UDPSocket":
                    triggers.append(trigger)
            if len(triggers) > 1:
                pass
            elif len(triggers) == 1:
                self.socket_trigger = triggers[0]
            else:
                logger.error("Unable to find enabled socket trigger")


    def process(self, frame, metadata):

        self.interval -= 1
        if self.interval <= 0:
            scale = self.config.get("Scale factor")
            if scale != 1.0:
                img_h, img_w, num_ch = frame.shape
                image = cv2.resize(frame, (int(img_w * scale), int(img_h * scale))) # resize uses reverse order
                image = np.expand_dims(image, axis=0)
            else:
                image = np.expand_dims(frame, axis=0)

            prediction = self.model(tf.constant(image, dtype=self.model_input.dtype))  # outputs list of tensors
            
            # new list of lists (instances) of tuples (points) with format ((h,w), score)
            self.poses = []
            
            for instance in prediction:
                pose = []
                for point in instance.numpy():
                    if scale != 1.0:
                        resized = (point[0] / scale, point[1] / scale)
                        pose.append((resized, point[2]))
                    else:
                        pose.append( ((point[0], point[1]), point[2]) )

                self.poses.append(pose)

            fps_mode = self.config.get("Inference FPS")            
            if fps_mode == "Match Camera":
                self.interval = self.in_queue.qsize()
                self.blocking = True
            else:
                self.interval = self.config.get("Fixed Interval")
                self.blocking = False

        if self.config.get("Draw on frame"):
            threshold = self.config.get("Score Threshold")
            for num, pose in enumerate(self.poses):
                color = [0,0,0]
                color[num % 3] = 255

                for point, score in pose:
                    h_pos, w_pos = point
                    if not(np.isnan(h_pos) or np.isnan(w_pos)) and score >= threshold:
                        frame = cv2.circle(frame, (round(w_pos), round(h_pos)), 5, color, -1)

        if self.csv_writer is not None:
            self.csv_writer.writerow(self.poses)

        if self.socket_trigger is not None:
            self.socket_trigger.execute(str(self.poses))

        metadata["DLC Poses"] = self.poses

        return frame, metadata

    def close(self):
        logger.info("DLC Inference closed")
        self.active = False

        if self.save_file is not None:
            self.save_file.close()


def load_frozen_model(model_dir):
    # Load frozen graph using TensorFlow 1.x functions
    model_file = [file for file in os.listdir(model_dir) if file.endswith('.pb')]
    if len(model_file) > 1:
        raise IOError("Multiple model files found. Model folder should only contain one .pb file")
    elif len(model_file) == 0:
        raise IOError("Could not fild frozen model (.pb) file in specified folder")
    else:
        model_file = model_file[0]

    model_path = os.path.join(model_dir, model_file)
    with tf.io.gfile.GFile(model_path, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    def _imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
    import_graph = wrapped_import.graph

    graph_ops = import_graph.get_operations()

    inputs = [graph_ops[0].name + ":0"]
    if "concat_1" in graph_ops[-1].name:
        outputs = [graph_ops[-1].name + ":0"]
    else:
        outputs = [graph_ops[-1].name + ":0", graph_ops[-2].name + ":0"]

    model = wrapped_import.prune(
        tf.nest.map_structure(import_graph.as_graph_element, inputs),
        tf.nest.map_structure(import_graph.as_graph_element, outputs)
    )

    return model