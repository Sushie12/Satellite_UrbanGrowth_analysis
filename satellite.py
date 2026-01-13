# ===============================
# IMPORTS
# ===============================
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

np.seterr(divide='ignore', invalid='ignore')

# ===============================
# YEARS
# ===============================
years = range(2014, 2025)

# ===============================
# INDEX FUNCTION
# ===============================
def compute_indices(b3, b4, b5, b6, b7):
    ndvi = (b5 - b4) / (b5 + b4 + 1e-10)
    ndbi = (b6 - b5) / (b6 + b5 + 1e-10)
    mndwi = (b3 - b6) / (b3 + b6 + 1e-10)
    baei = (b6 + b7) / (b5 + 1e-10)
    return ndvi, ndbi, mndwi, baei

# ===============================
# DATA CONTAINERS
# ===============================
X_all = []
y_all = []

# ===============================
# LOOP THROUGH YEARS
# ===============================
for year in years:

    # --- Load bands ---
    with rasterio.open(f"satellite_images/Landsat8_Godavari_{year}_8SR_B3.tif") as src:
        b3 = src.read(1).astype("float32")

    with rasterio.open(f"satellite_images/Landsat8_Godavari_{year}_8SR_B4.tif") as src:
        b4 = src.read(1).astype("float32")

    with rasterio.open(f"satellite_images/Landsat8_Godavari_{year}_8SR_B5.tif") as src:
        b5 = src.read(1).astype("float32")

    with rasterio.open(f"satellite_images/Landsat8_Godavari_{year}_8SR_B6.tif") as src:
        b6 = src.read(1).astype("float32")

    with rasterio.open(f"satellite_images/Landsat8_Godavari_{year}_8SR_B7.tif") as src:
        b7 = src.read(1).astype("float32")

    # --- Compute indices ---
    ndvi, ndbi, mndwi, baei = compute_indices(b3, b4, b5, b6, b7)

    # ===============================
    # CREATE LABELS FROM NDBI
    # ===============================
    # Urban if NDBI > adaptive threshold
    threshold = np.percentile(ndbi, 65)
    labels = (ndbi > threshold).astype(int)

    # ===============================
    # FEATURES
    # ===============================
    features = np.stack([
        ndvi.flatten(),
        ndbi.flatten(),
        mndwi.flatten(),
        baei.flatten()
    ], axis=1)

    X_all.append(features)
    y_all.append(labels.flatten())

# ===============================
# FINAL DATASET
# ===============================
X = np.vstack(X_all)
y = np.hstack(y_all)

# Remove invalid pixels
mask = np.isfinite(X).all(axis=1)
X = X[mask]
y = y[mask]

# ===============================
# TRAIN / TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# ===============================
# RANDOM FOREST MODEL
# ===============================
model = RandomForestClassifier(
    n_estimators=120,
    max_depth=12,
    min_samples_leaf=10,
    random_state=42
)

model.fit(X_train, y_train)

# ===============================
# PREDICTION
# ===============================
y_pred = model.predict(X_test)

# ===============================
# EVALUATION METRICS
# ===============================
accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall    = recall_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)

print("\n===== MODEL EVALUATION =====")
print(f"Accuracy  : {accuracy*100:.2f}%")
print(f"Precision : {precision*100:.2f}%")
print(f"Recall    : {recall*100:.2f}%")
print(f"F1-score  : {f1*100:.2f}%")