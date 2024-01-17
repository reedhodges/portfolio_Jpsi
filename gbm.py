from skmultilearn.problem_transform import LabelPowerset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb

from data_processing import process_data

filepath = 'cs_data/cross_sections.csv'
processed_data = process_data(filepath)

ldmes = ['oct3s1', 'oct1s0', 'oct3p0', 'sing3s1']
pols = ['U', 'L']
types = ['grid', 'dom']
all_target_variables = []
for ldme in ldmes:
    for pol in pols:
        for type in types:
            all_target_variables.append(ldme + '_' + pol + '_' + type)
all_target_variables.append('total')
all_target_variables.append('total_U')
all_target_variables.append('total_L')

X = processed_data.drop(all_target_variables, axis=1)
current_target_columns = [ldme + '_U_dom' for ldme in ldmes]
Y = processed_data[current_target_columns]

lp = LabelPowerset()
Y_transformed = lp.transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y_transformed, test_size=0.2, random_state=42)

model = xgb.XGBClassifier()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Accuracy: {accuracy}")