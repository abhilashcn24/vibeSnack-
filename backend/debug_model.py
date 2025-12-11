
import model_utils
import numpy as np
import traceback

try:
    print("Loading model...")
    model = model_utils.load_model()
    if not model:
        print("Failed to load model")
        exit(1)
    
    print("Model loaded.")
    
    user_input = {
        'hour': 10,
        'mood': 'happy',
        'hunger': 3,
        'diet': 'veg',
        'context': 'working'
    }
    
    print("Preparing input...")
    X = model_utils.prepare_input(user_input)
    print(f"Input shape: {X.shape}")
    print(f"Input content: {X}")
    
    print("Predicting...")
    probs = model.predict_proba(X)
    print(f"Probabilities: {probs}")

except Exception:
    traceback.print_exc()
