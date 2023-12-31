import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# MAYBE USE PREPROCESSING TO SCALE THE VARIABLES INSTEAD OF IN PANDAS

# import /cs_data/percent_contributions.csv
df = pd.read_csv('cs_data/percent_contributions.csv')

# split into input and output variables
X = df[['x', 'z', 'Q', 'PT']]
y = df[['percent_O3S1SING']]

# split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# scale the features: subtract the mean, scale to unit variance
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# initialize the regressor with desired parameters
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

# fit the model
rf.fit(X_train, y_train.values.ravel())

# make predictions
y_train_pred = rf.predict(X_train)
y_test_pred = rf.predict(X_test)

# calculate mean squared error
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)

# print results
print(f"Training MSE: {train_mse}")
print(f"Test MSE: {test_mse}")

# get feature importances
importances = rf.feature_importances_
features = X.columns
for feature, importance in zip(features, importances):
    print(f"Importance of {feature}: {importance}")