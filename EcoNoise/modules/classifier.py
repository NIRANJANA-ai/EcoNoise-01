import numpy as np
import tensorflow as tf
from python_speech_features import mfcc

def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    print(f"[classifier] Loaded TFLite model from {model_path}")
    return interpreter

def classify_audio(interpreter, samples, sr):
    # Extract MFCC features
    features = mfcc(samples, samplerate=sr, numcep=13)
    features = features.flatten()

    # Get input tensor details
    input_details = interpreter.get_input_details()
    input_shape = input_details[0]['shape']

    needed = input_shape[1]
    features = features[:needed] if len(features) >= needed else np.pad(features, (0, needed - len(features)))

    features = np.array(features, dtype=np.float32).reshape(1, needed)

    interpreter.set_tensor(input_details[0]['index'], features)
    interpreter.invoke()

    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    class_index = np.argmax(output_data)
    confidence = float(output_data[class_index])

    # Example labels — replace with your model labels
    LABELS = ["silence", "traffic", "horn", "animal", "bird"]
    predicted_label = LABELS[class_index]

    return predicted_label, confidence


