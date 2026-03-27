# app/utils.py

import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def normalize_score(raw_score):
    return 1 / (1 + np.exp(-raw_score))


def get_score_label(score):
    if score < 0.4:
        return "Weak match"
    elif score < 0.7:
        return "Good match"
    elif score < 0.9:
        return "Strong match"
    else:
        return "Very strong match 🔥"