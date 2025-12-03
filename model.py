"""Braak staging assessment module.

Author: Kelsan Giamporcaro
Version: 12/3/2025
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras.layers as layers
import tensorflow.keras.models as models
import scanpy as sc
import shap

# Load data
early = sc.read_h5ad("./AD00101.h5ad")
late = sc.read_h5ad("./AD00102.h5ad")

# Set stage labels (binary classification)
early.obs["stage"] = 0
late.obs["stage"] = 1

adata = early.concatenate(late, join="inner")

# Normalize data
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

# Genes of interest (mainly focused on PHGDH)
# Also checks genes that are only in one dataset
genes = ["PHGDH", "PSAT1", "PCYT2", "MBOAT1", "PLA2G4A", "PLA2G6", "PTDSS1"]
missing = [g for g in genes if g not in adata.var_names]
print("Missing genes:", missing)

# Set data for PHGDH model
X = adata[:, genes].X.toarray()
X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
y = adata.obs["stage"].to_numpy()

# Set data for non PHGDH model
genes_no_phgdh = [g for g in genes if g != "PHGDH"]
X_no_phgdh = adata[:, genes_no_phgdh].X.toarray()
X_no_phgdh = np.nan_to_num(X_no_phgdh, nan=0.0, posinf=0.0, neginf=0.0)
y = adata.obs["stage"].to_numpy()

# Binary classification model with PHGDH
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(len(genes),)),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(2, activation='softmax')
]
)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
)

accuracy_phgdh = model.fit(X, y, epochs=50, batch_size=8, validation_split=0.2)

# Binary classification model without PHGDH
model_no_phgdh = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(len(genes_no_phgdh),)),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(2, activation='softmax')
])
model_no_phgdh.compile(optimizer='adam',
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])

accuracy_no_phgdh = model_no_phgdh.fit(X_no_phgdh, y, epochs=50, batch_size=8, validation_split=0.2)

# SHAP explainer for PHGDH model
explainer_phgdh = shap.KernelExplainer(model.predict, X[:100])  # use a small background sample
shap_values_PHGDH = explainer_phgdh.shap_values(X)

# SHAP explainer for no-PHGDH model
explainer_no_phgdh = shap.KernelExplainer(model_no_phgdh.predict, X_no_phgdh[:100])
shap_values_no_PHGDH = explainer_no_phgdh.shap_values(X_no_phgdh)

# Visualize with PHGDH
shap.summary_plot(shap_values_PHGDH, feature_names=genes)
plt.title("SHAP summary (PHGDH)")
plt.show()

shap.dependence_plot("PHGDH", shap_values_PHGDH.values, X, feature_names=genes)
plt.title("SHAP dependence (PHGDH)")
plt.show()

# Visualize without PHGDH
shap.summary_plot(shap_values_no_PHGDH, feature_names=genes_no_phgdh)
plt.title("SHAP summary (No PHGDH)")
plt.show()

shap.dependence_plot("PSAT1", shap_values_no_PHGDH.values, X_no_phgdh, feature_names=genes_no_phgdh)
plt.title("SHAP dependence (No PHGDH)")
plt.show()

# Model accuracy
hist_no = accuracy_no_phgdh.history
hist_ph = accuracy_phgdh.history

plt.plot(hist_no['accuracy'], label='Train (No PHGDH)')
plt.plot(hist_no['val_accuracy'], label='Val (No PHGDH)')
plt.plot(hist_ph['accuracy'], label='Train (PHGDH)')
plt.plot(hist_ph['val_accuracy'], label='Val (PHGDH)')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Losses
plt.plot(hist_no['loss'], label='Train Loss (No PHGDH)')
plt.plot(hist_no['val_loss'], label='Val Loss (No PHGDH)')
plt.plot(hist_ph['loss'], label='Train Loss (PHGDH)')
plt.plot(hist_ph['val_loss'], label='Val Loss (PHGDH)')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()