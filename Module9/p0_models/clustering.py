# Simple unsupervised learning workflow (clustering)
# Dataset: Chronic Kidney Disease patient data
# Task: Discover natural patient groupings based on health indicators
# To install dependencies (in your environment/terminal):
#   pip install scikit-learn matplotlib pandas

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------

"""
This dataset contains health information for 1,659 patients with various
biomarkers and health metrics related to kidney disease.

For clustering, we'll focus on continuous clinical measurements:
- Vital signs (blood pressure)
- Lab values (blood sugar, kidney function markers, cholesterol)
- Physical metrics (BMI)

We want to discover natural groupings of patients based on their
health profiles, which could help with:
- Risk stratification
- Targeted interventions
- Treatment planning
"""

# Load the dataset
df = pd.read_csv('Module9/p0_models/datasets/Chronic_Kidney_Dsease_data.csv')

print("Step 1: Load data")
print("  Dataset shape:", df.shape)
print("  Number of patients:", len(df))
print("  Total columns:", len(df.columns))

# Select continuous features for clustering (clinical measurements)
# Avoiding binary/categorical variables for cleaner clustering
feature_columns = [
    'Age',
    'BMI',
    'SystolicBP',
    'DiastolicBP',
    'FastingBloodSugar',
    'HbA1c',
    'SerumCreatinine',
    'BUNLevels',
    'GFR',
    'ProteinInUrine',
    'CholesterolTotal',
    'CholesterolLDL',
    'CholesterolHDL',
    'HemoglobinLevels',
]

print(f"\n  Selected {len(feature_columns)} features for clustering:")
for col in feature_columns:
    print(f"    - {col}")

# Extract features
X = df[feature_columns].values

print("\n  Feature matrix shape:", X.shape)
print("\n  Feature statistics:")
print(df[feature_columns].describe().round(1).to_string())


# -------------------------------------------------
# 2. Preprocess the data (scaling)
# -------------------------------------------------
#
# WHY SCALE?
#   - Clustering algorithms like K-Means use distance metrics (Euclidean distance).
#   - Features with larger scales dominate the distance calculation.
#   - StandardScaler transforms features to have mean=0 and std=1.
#   - This ensures all features contribute equally to the clustering.
#
# EXAMPLE:
#   - Cholesterol ranges 150-300, while HbA1c ranges 4-10.
#   - Without scaling, cholesterol would dominate distance calculations.
#   - After scaling, both have similar ranges and equal influence.

print("\n" + "="*50)
print("Step 2: Preprocess data (standardization)")
print("="*50)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)



# -------------------------------------------------
# 3. K-Means clustering
# -------------------------------------------------
#
# K-MEANS ALGORITHM:
#   1. Initialize k cluster centroids randomly
#   2. Assign each point to the nearest centroid
#   3. Update centroids as the mean of assigned points
#   4. Repeat steps 2-3 until convergence
#
# KEY HYPERPARAMETERS:
#   - n_clusters: number of clusters to form
#   - init: method for initialization ('k-means++' is smart initialization)
#   - n_init: number of times to run with different initializations
#   - max_iter: maximum iterations for a single run





#### setting up the model with hyperparameters
kmeans_model = KMeans(
    n_clusters=3,       # number of clusters to form
    init='k-means++',   # smart initialization to speed up convergence
    n_init=10,          # run 10 times with different centroid seeds
    max_iter=300,       # maximum iterations for single run
    random_state=42,    # for reproducibility
)


######### TRAINING (FITTING) ########
### This is where the model learns cluster structure from the data

print("\n  Fitting K-Means model...")
kmeans_model.fit(X_scaled)  ## this is where the model learns the cluster structure

# Get cluster assignments and model info
cluster_labels = kmeans_model.labels_
centroids = kmeans_model.cluster_centers_
inertia = kmeans_model.inertia_  # sum of squared distances to nearest centroid

print(f"\n  Model trained successfully!")
print(f"  Inertia (within-cluster sum of squares): {inertia:.3f}")
print("  Cluster sizes:", dict(zip(*np.unique(cluster_labels, return_counts=True))))


######## EVALUATION ########

print("\n" + "="*50)
print("Step 4: Evaluate clustering quality")
print("="*50)

# Silhouette score: measures how similar samples are to their own cluster vs other clusters
# Range: -1 to 1, higher is better
silhouette = silhouette_score(X_scaled, cluster_labels)

print(f"\n  Silhouette Score: {silhouette:.3f}")
print("\n  Interpretation:")
print("    - Close to 1: samples are well matched to their own cluster")
print("    - Close to 0: samples are on the boundary between clusters")
print("    - Negative: samples might be assigned to the wrong cluster")


# -------------------------------------------------
# 4. Find optimal number of clusters (Elbow Method)
# -------------------------------------------------

inertias = []
silhouettes = []
k_range = range(2, 8)

for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, km.labels_))

print("\n  Results:")
print("  k  | Inertia    | Silhouette")
print("  ---|------------|----------")
for k, inertia, sil in zip(k_range, inertias, silhouettes):
    print(f"  {k}  | {inertia:>10.1f} | {sil:.3f}")


# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Number of Clusters (k)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method - Finding Optimal k')
ax1.grid(True, alpha=0.3)

ax2.plot(k_range, silhouettes, 'ro-', linewidth=2, markersize=8)
ax2.set_xlabel('Number of Clusters (k)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score vs Number of Clusters')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# -------------------------------------------------
# 5. Analyze cluster characteristics
# -------------------------------------------------

print("\n" + "="*50)
print("Step 6: Analyze cluster characteristics")
print("="*50)

# Add cluster labels to dataframe
df['Cluster'] = cluster_labels

# Calculate cluster means for each feature
cluster_summary = df.groupby('Cluster')[feature_columns].mean().round(1)
cluster_counts = df.groupby('Cluster').size()

print("\n  Cluster centroids (average feature values):")
print(cluster_summary.T.to_string())  # Transpose for better readability

print("\n  Patients per cluster:")
for cluster, count in cluster_counts.items():
    print(f"    Cluster {cluster}: {count} patients ({count/len(df)*100:.1f}%)")


# -------------------------------------------------
# 6. Visualize clusters
# -------------------------------------------------

print("\n" + "="*50)
print("Step 7: Visualize clusters")
print("="*50)

# Use PCA to reduce to 2D for visualization
from sklearn.decomposition import PCA

pca = PCA(n_components=2) 
X_pca = pca.fit_transform(X_scaled)

# Plot clusters
fig, ax = plt.subplots(figsize=(10, 8))

scatter = ax.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=cluster_labels,
    cmap='viridis',
    alpha=0.6,
    s=50
)

# Plot centroids
centroids_pca = pca.transform(centroids)
ax.scatter(
    centroids_pca[:, 0],
    centroids_pca[:, 1],
    c='red',
    marker='X',
    s=300,
    edgecolors='black',
    linewidths=2,
    label='Centroids'
)

ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
ax.set_title('Chronic Kidney Disease Patient Clusters (K-Means)')
ax.legend(*scatter.legend_elements(), title="Cluster")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# -------------------------------------------------
# 7. View sample results
# -------------------------------------------------

print("\n" + "="*50)
print("Step 8: Sample patient assignments")
print("="*50)

# Show first 15 patients with key features and their cluster assignments
display_cols = ['PatientID', 'Age', 'BMI', 'GFR', 'SerumCreatinine', 'CholesterolTotal', 'Cluster']
### sort by cluster for better readability
df = df.sort_values(by='Cluster').reset_index(drop=True)
print("\n  First 15 patients and their cluster assignments:")
print(df[display_cols].head(15).to_string())

### create a means table for each cluster
print("\n  Cluster means for key features:")
key_features = ['Age', 'BMI', 'GFR', 'SerumCreatinine', 'CholesterolTotal']
cluster_means = df.groupby('Cluster')[key_features].mean().round(1)
print(cluster_means.to_string())

# -------------------------------------------------

