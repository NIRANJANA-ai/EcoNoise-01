def compute_harm_rate(sound_class):
    harm_values = {
        "silence": 0,
        "traffic": 80,
        "horn": 95,
        "animal": 10,
        "bird": 5
    }
    return harm_values.get(sound_class, 50)
