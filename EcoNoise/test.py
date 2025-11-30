from modules import recorder, classifier

# Record 5 seconds audio
audio_file = recorder.record_sound(duration=5, filename="test.wav")

# Load model
interpreter = classifier.load_model(model_path="models/sound_classifier.tflite")

# Classify recorded audio
predicted_class, confidence = classifier.classify_audio(interpreter, audio_file)
print(f"Predicted class: {predicted_class}, Confidence: {confidence:.2f}")
