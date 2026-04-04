from pathlib import Path

import tensorflow as tf


def convert_savedmodel_to_int8_tflite(saved_model_dir, tflite_path):
    saved_model_dir = Path(saved_model_dir)
    tflite_path = Path(tflite_path)
    tflite_path.parent.mkdir(parents=True, exist_ok=True)

    converter = tf.lite.TFLiteConverter.from_saved_model(str(saved_model_dir))
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    tflite_model = converter.convert()

    tflite_path.write_bytes(tflite_model)
    return tflite_path, len(tflite_model) / 1e6
