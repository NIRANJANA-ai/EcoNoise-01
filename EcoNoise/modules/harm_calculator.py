# Example harm rate mapping
HARM_RATES = {
    0: 10,  # Urban Noise
    1: 5,   # Birdsong
    2: 8    # Other wildlife
}

def calculate_harm(predicted_class):
    return HARM_RATES.get(predicted_class, 0)
