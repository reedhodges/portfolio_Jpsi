from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from data_processing import process_data

filepath = 'cs_data/cross_sections.csv'
processed_data = process_data(filepath)

target_variables_to_drop = ['oct3s1_U_grid', 'oct3s1_L_grid', 'oct1s0_U_grid', 'oct1s0_L_grid', 'oct3p0_U_grid', 'oct3p0_L_grid', 'sing3s1_U_grid', 'sing3s1_L_grid', 'total_U', 'total_L', 'total']
target_variable = 'total'

X = processed_data.drop(target_variables_to_drop, axis=1)
y = processed_data[target_variable]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean squared error: {mse}")
print(f"R2 score: {r2}")

print('Model coefficients:', model.coef_)