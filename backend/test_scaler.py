import numpy as np
from sklearn.preprocessing import StandardScaler

try:
    X = np.array([[1, 'happy', 5, 'veg', 'gaming']], dtype=object)
    scaler = StandardScaler()
    # Mocking what ColumnTransformer does on the subset
    # It would pass X[:, [2]]
    col_idx = [2]
    X_subset = X[:, col_idx]
    print(f"Subset type: {X_subset.dtype}")
    print(f"Subset content: {X_subset}")
    
    # StandardScaler usually tries to convert to float.
    # If the array is object type, it might work if the content is numeric, but let's verify.
    scaler.fit(X_subset)
    print("Fit success")
    transform = scaler.transform(X_subset)
    print("Transform success")
    print(transform)
except Exception as e:
    print(f"Error: {e}")
