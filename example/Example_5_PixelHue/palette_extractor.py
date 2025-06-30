import numpy as np
from sklearn.cluster import KMeans


def extract(img, n=9):
    img = img.convert("RGB").resize((150, 150))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n, random_state=42, n_init=10).fit(pixels)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    # Count frequency of each cluster
    counts = np.bincount(labels)
    # Sort centers by frequency (descending)
    sorted_idx = np.argsort(-counts)
    centers = centers[sorted_idx]
    palette = [f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper() for r, g, b in centers]
    return palette