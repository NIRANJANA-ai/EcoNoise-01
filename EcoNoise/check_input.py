import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path="models/sound_classifier.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
print("INPUT SHAPE:", input_details[0]['shape'])
print("INPUT TYPE:", input_details[0]['dtype'])
