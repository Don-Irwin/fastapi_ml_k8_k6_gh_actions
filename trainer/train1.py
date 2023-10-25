from operator import mod
from os import getcwd
from os.path import exists, join

import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVR

# Metadata
data = fetch_california_housing()
features = data.feature_names


X = data.data
y = data.target
print(f"features: {features}")

# return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")
# curl ${CURL_URI}
# echo ""
# echo "the return code is : ${return_code}"
# echo ""

with open('curl_commands.txt','w') as f:
    for i in range(25):
        s="return_code=$(curl -o /dev/null -s -w \"%{{http_code}}\\n\" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{{\"MedInc\":{},\"HouseAge\":{},\"AveRooms\":{},\"AveBedrms\":{},\"Population\":{},\"AveOccup\":{},\"Latitude\":{},\"Longitude\":{} }}')\n".format(X[i][0],X[i][1],X[i][2],X[i][3],X[i][4],X[i][5],X[i][6],X[i][7])
        f.write(s)
        print(s)
        s="echo \"the return code is : ${return_code}\"\n"
        f.write(s)
        print(s)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

n_samples, n_features = X.shape

print(type(X_test))

my_test_dealio = X[0]
my_value_dealio = y[0]
print("*"*30)
print(my_test_dealio)
print(my_value_dealio)
print("*"*30)



# # Model Pipeline
# processing_pipeline = make_pipeline(SimpleImputer(), RobustScaler(), SVR())

# params = {
#     "simpleimputer__strategy": ["mean", "median"],
#     "robustscaler__quantile_range": [(25.0, 75.0), (30.0, 70.0)],
#     "svr__C": [0.1, 1.0],
#     "svr__gamma": ["auto", 0.1],
# }

# grid = GridSearchCV(processing_pipeline, param_grid=params, n_jobs=-1, cv=5, verbose=3)

model_filename = "model_pipeline.pkl"
model_path = join(getcwd(), model_filename)
# print("About to write the trained file to the following location:")
# print(model_path)
# if not exists(model_path):
#     grid.fit(X_train, y_train)

#     print(f"Train R^2 Score : {grid.best_estimator_.score(X_train, y_train):.3f}")
#     print(f"Test R^2 Score : {grid.best_estimator_.score(X_test, y_test):.3f}")
#     print(f"Best R^2 Score Through Grid Search : {grid.best_score_:.3f}")
#     print(f"Best Parameters : {grid.best_params_}")

#     joblib.dump(grid.best_estimator_, model_path)
# else:
#     print("Model has already been trained, no need to rerun")

loaded_model = joblib.load(model_path)
print("*"*30)
print("MY PREDICTION FROM LOADED MODEL")
print("*"*30)
print(loaded_model.predict([my_test_dealio]))
print("*"*30)