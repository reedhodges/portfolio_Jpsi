import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# import /cs_data/percent_contributions.csv
df = pd.read_csv('cs_data/percent_contributions.csv')

# split into input and output variables
X = df[['x', 'z', 'Q', 'PT']]
y = df[['percent_O3S1SING']]

# split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# scale the features: subtract the mean, scale to unit variance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# use a random sample of the data for faster computation.
# first argument tells it to pick from all the rows, 
# second argument tells it to pick 10000 rows, 
# third argument tells it to pick without replacement
sample_indices = np.random.choice(X_train_scaled.shape[0], 10000, replace=False)
X_train_sample = X_train_scaled[sample_indices]

dbscan = DBSCAN(eps=0.3, min_samples=10)
labels = dbscan.fit_predict(X_train_sample)

plt.scatter(X_train_sample[:, 0], X_train_sample[:, 1], c=labels, cmap='viridis', edgecolor='k', s=50)
plt.xlabel('Feature x')
plt.ylabel('Feature z')
plt.title('DBSCAN Clustering')
plt.colorbar().set_label('Cluster Label')
plt.show()

# need to learn more about interpreting these results and the correct choice of parameters