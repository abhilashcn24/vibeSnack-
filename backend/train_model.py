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

# Define TimeCategoryEncoder locally to ensure it can be pickled and unpickled correctly
# without relying on external module structure during unpickling if the path changes.
class TimeCategoryEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        hours = X.iloc[:, 0] if isinstance(X, pd.DataFrame) else X[:, 0]
        cats = [model_utils.get_time_category(h) for h in hours]
        return pd.DataFrame(cats, columns=['time_of_day_category'])

def train():
    print("Loading data...")
    df = load_data()
    
    # Features and Target
    X = df[['hour', 'mood', 'hunger', 'diet', 'context']]
    y = df['snack_id']
    
    # Preprocessing
    # We need to handle:
    # - hour: Numerical, but maybe cyclical or categorical? Let's bin it.
    # - mood: Categorical
    # - hunger: Numerical
    # - diet: Categorical
    # - context: Categorical
    
    # Define Transformers
    
    # 1. Time Transformer (Custom)
    # We'll use the one from model_utils to ensure consistency, 
    # BUT for the pipeline to pickle correctly, the class needs to be available.
    # Since we import model_utils, it should be fine if we use model_utils.TimeCategoryEncoder
    
    time_transformer = Pipeline(steps=[
        ('binner', TimeCategoryEncoder()),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    categorical_features = ['mood', 'diet', 'context']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('time', time_transformer, ['hour']),
            ('cat', categorical_transformer, categorical_features),
            ('num', StandardScaler(), ['hunger'])
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
        if y_test.iloc[i] in top3_classes:
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
