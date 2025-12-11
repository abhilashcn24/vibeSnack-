import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import joblib
import model_utils # Import our utils

# Load Data
def load_data():
    try:
        return pd.read_csv("snack_data.csv")
    except FileNotFoundError:
        print("Data not found. Generating new data...")
        import data_generator
        data_generator.generate_data()
        return pd.read_csv("snack_data.csv")



def train():
    print("Loading data...")
    df = load_data()
    
    # Features and Target
    # Order: hour(0), mood(1), hunger(2), diet(3), context(4)
    X = df[['hour', 'mood', 'hunger', 'diet', 'context']].values
    y = df['snack_id'].values
    
    # Preprocessing
    
    # Define Transformers
    
    # 1. Time Transformer (Custom)
    time_transformer = Pipeline(steps=[
        ('binner', model_utils.TimeCategoryEncoder()),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # mood(1), diet(3), context(4)
    categorical_features = [1, 3, 4] 
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('time', time_transformer, [0]), # hour is col 0
            ('cat', categorical_transformer, categorical_features),
            ('num', StandardScaler(), [2]) # hunger is col 2
        ])
    
    # Model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', clf)])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    # Top-3 Accuracy
    probs = pipeline.predict_proba(X_test)
    top3_acc = 0
    for i in range(len(y_test)):
        top3_idxs = np.argsort(probs[i])[-3:]
        classes = pipeline.classes_
        top3_classes = classes[top3_idxs]
        if y_test[i] in top3_classes:
            top3_acc += 1
    print(f"Top-3 Accuracy: {top3_acc / len(y_test):.4f}")
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save
    # Save to current directory (backend/)
    joblib.dump(pipeline, "snack_model.joblib")
    print("Model saved to snack_model.joblib")

if __name__ == "__main__":
    train()
