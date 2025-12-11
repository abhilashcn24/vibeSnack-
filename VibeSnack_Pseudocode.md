### **5.1 Pseudocode**

#### **IMPLEMENTATION**

```python
def predict_snack(model, user_input, snack_catalog, user_history, top_k=5) -> List[Dict]
    """
    - Prepares input dataframe from user context
    - Generates base probability predictions using Random Forest
    - Applies history boost (max 10% based on previous selections)
    - Filters strictly by diet preference (Veg/Non-Veg)
    - Returns top-K recommendations with details
    """
    # 1. Get Probabilities
    probs = model.predict_proba(user_input)
    
    # 2. Apply History Boost
    for snack_id, count in user_history:
        boost = min(0.1, (count / total_history) * 0.2)
        probs[snack_id] += boost

    # 3. Filter & Sort
    candidates = []
    for snack in sorted_by_prob:
        if matches_diet(snack, user_input.diet):
            candidates.append(snack)
            
    return candidates[:top_k]

def generate_explanation(user_input, snack) -> str
    """
    - Name-based reasoning (Yogurt → "Creamy and protein-packed")
    - Hunger matching (High hunger + Heavy → "Substantial and filling")
    - Context combinations (Gaming + Healthy → "Keeps hands clean")
    - Time-based logic (Morning + Healthy → "Healthy start")
    - Fallback to tag-based explanations
    """
    reasons = []
    if "Yogurt" in snack.name: reasons.append("Creamy and protein-packed.")
    if user_input.hunger >= 4 and snack.is_heavy: reasons.append("Substantial and filling.")
    if user_input.context == "gaming" and "healthy" in snack.tags: reasons.append("Keeps hands clean.")
    
    return " ".join(reasons)

# Scikit-learn Pipeline Structure
sklearn.pipeline.Pipeline([
    ('preprocessor', ColumnTransformer([
        ('time', Pipeline([
            ('binner', TimeCategoryEncoder()),  # Custom Transformer
            ('encoder', OneHotEncoder())
        ]), ['hour']),
        ('cat', OneHotEncoder(), ['mood', 'diet', 'context']),
        ('num', StandardScaler(), ['hunger'])
    ])),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

def submit_feedback(feedback: Feedback) -> Dict
    """
    - Receives snack selection from frontend
    - Updates global history counter in MongoDB
    - Uses atomic $inc operation for concurrency safety
    """
    db.history.update_one(
        {"_id": "global_history"},
        {"$inc": {f"counts.{feedback.snack_id}": 1}},
        upsert=True
    )
```
