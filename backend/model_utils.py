import joblib
import numpy as np
import os
import json
from sklearn.base import BaseEstimator, TransformerMixin

# Define TimeCategoryEncoder class (Must match the one used during training)
def get_time_category(hour):
    if 7 <= hour <= 11: return "morning"
    if 12 <= hour <= 16: return "afternoon"
    if 17 <= hour <= 20: return "evening"
    return "night"

# IMPORTANT: This class name and structure must match exactly what was defined in train_model.py
class TimeCategoryEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        # Expecting numpy array, hour is col 0
        if hasattr(X, 'values'):
             hours = X.iloc[:, 0]
        else:
             hours = X[:, 0]
        cats = [get_time_category(h) for h in hours]
        return np.array(cats).reshape(-1, 1)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "snack_model.joblib")



def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    else:
        print(f"Model not found at {MODEL_PATH}")
        return None

def prepare_input(user_input):
    # Order: hour, mood, hunger, diet, context
    return np.array([[
        user_input['hour'],
        user_input['mood'],
        user_input['hunger'],
        user_input['diet'],
        user_input['context']
    ]], dtype=object)

def predict_snack(model, user_input, snack_catalog, user_history, top_k=3):
    """
    Returns top_k snack IDs and their probabilities.
    snack_catalog: list of snack dicts
    user_history: dict of snack_id -> count
    """
    df = prepare_input(user_input)
    
    # Get probabilities
    probs = model.predict_proba(df)[0]
    classes = model.classes_
    
    # Create a dict of snack_id -> prob
    prob_dict = {cls: prob for cls, prob in zip(classes, probs)}
    
    # Boost from history
    total_history = sum(user_history.values())
    if total_history > 0:
        for sid, count in user_history.items():
            sid = int(sid)
            if sid in prob_dict:
                # Small boost: 1% per accept, capped at 10%
                boost = min(0.1, (count / total_history) * 0.2) 
                prob_dict[sid] += boost
    
    # Sort
    sorted_snacks = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
    
    top_k_snacks = []
    
    # Filter by diet
    user_diet = user_input.get('diet')
    
    # Helper to find snack by ID
    def get_snack(sid):
        for s in snack_catalog:
            if s['id'] == sid:
                return s
        return None

    for sid, prob in sorted_snacks:
        sid = int(sid) # Convert numpy int64 to native int
        snack = get_snack(sid)
        if snack:
            # Strict filtering
            if user_diet == "veg" and "non-veg" in snack['tags']:
                continue
            if user_diet == "non-veg" and "veg" in snack['tags']:
                continue
                
            top_k_snacks.append({
                "id": sid,
                "name": snack['name'],
                "prob": float(prob),
                "tags": snack['tags'],
                "snack_details": snack # Include full details for explanation
            })
            
        if len(top_k_snacks) >= top_k:
            break
            
    return top_k_snacks

def format_personalized_message(user_input, snack_name):
    hour = user_input.get('hour')
    mood = user_input.get('mood')
    hunger = user_input.get('hunger')
    context = user_input.get('context')
    
    time_str = f"{hour}:00"
    msg = f"It's around {time_str} and you're feeling {mood}. "
    
    if hunger >= 4:
        msg += "You're pretty hungry! "
    elif hunger <= 2:
        msg += "Just looking for a light nibble? "
        
    if context and context != "none":
        msg += f"Since you're {context}, "
    
    msg += f"I recommend **{snack_name}**."
    return msg

def generate_explanation(user_input, snack):
    reasons = []
    tags = snack.get('tags', [])
    is_heavy = snack.get('heavy', False)
    name = snack.get('name', '')
    price = snack.get('price', 'medium')
    
    hour = user_input.get('hour')
    hunger = user_input.get('hunger')
    context = user_input.get('context')
    mood = user_input.get('mood')

    # Logic copied from original...
    if "Yogurt" in name: reasons.append("Creamy and protein-packed.")
    elif "Banana" in name or "Fruit" in name: reasons.append("Nature's own fast food.")
    elif "Chocolate" in name: reasons.append("A classic mood booster.")
    elif "Coffee" in name: reasons.append("For that caffeine kick.")

    if hunger >= 4:
        if is_heavy: reasons.append("Since you're very hungry, this substantial snack will fill you up.")
        elif "healthy" in tags: reasons.append("A high-volume, healthy option to satisfy your hunger.")
        else: reasons.append("A nice portion to help curb that major hunger.")
    elif hunger <= 2:
        if not is_heavy: reasons.append("It's light and won't ruin your appetite.")
        elif "sweet" in tags: reasons.append("A small sweet treat just for the taste.")
        else: reasons.append("A bit indulgent, but perfect if you want just one satisfying bite.")

    if context == "gaming":
        if "healthy" in tags: reasons.append("Fresh and clean - keeps your hands grease-free for gaming.")
        elif "quick" in tags and not is_heavy: reasons.append("Easy to pop in your mouth between rounds.")
        elif is_heavy: reasons.append("Hearty fuel for a long gaming session.")
        else: reasons.append("Good for a break between matches.")
    elif context == "studying":
        if "healthy" in tags: reasons.append("Brain food to keep you focused without the crash.")
        elif "sweet" in tags: reasons.append("A little sugar rush to keep you going.")
        elif "savory" in tags: reasons.append("A savory distraction to reward your hard work.")
    elif context == "gym":
        if "healthy" in tags: reasons.append("Great for fueling up or recovering.")
        elif is_heavy: reasons.append("Good for bulking up!")
        else: reasons.append("You earned a treat!")
    elif context == "chilling":
        if "savory" in tags: reasons.append("Perfect savory companion for relaxing.")
        elif "sweet" in tags: reasons.append("Sweet comfort food for downtime.")
        elif "healthy" in tags: reasons.append("A refreshing snack to chill with.")

    if 7 <= hour <= 10:
        if "healthy" in tags: reasons.append("A healthy start to your morning.")
        elif "sweet" in tags: reasons.append("A sweet breakfast treat.")
        else: reasons.append("A tasty morning bite.")
    elif 14 <= hour <= 16:
        if "healthy" in tags: reasons.append("A refreshing afternoon pick-me-up.")
        elif "sweet" in tags: reasons.append("Perfect for that afternoon sugar craving.")
        elif "savory" in tags: reasons.append("A savory kick to wake you up.")
        else: reasons.append("Beats the afternoon slump.")
    elif 20 <= hour <= 23:
        if is_heavy: reasons.append("A hearty late-night meal.")
        elif "healthy" in tags: reasons.append("Light enough to not disrupt your sleep.")
        else: reasons.append("A light late-night munch.")

    if price == "low" and not reasons: reasons.append("Great value for a quick bite.")
    elif price == "high" and mood == "sad": reasons.append("Treat yourself, you deserve it.")

    if not reasons:
        if "spicy" in tags: reasons.append("Spices things up a bit!")
        elif "sweet" in tags: reasons.append("Satisfies your sweet tooth.")
        elif "healthy" in tags: reasons.append("A guilt-free choice.")
        else: reasons.append("Matches your current vibe perfectly.")
            
    return " ".join(reasons)
