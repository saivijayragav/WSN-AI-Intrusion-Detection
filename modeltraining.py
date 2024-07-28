# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from tabulate import tabulate
import joblib

# Load your dataset (replace 'your_dataset.csv' with the actual path)
train = pd.read_csv('E:/WSN-DS.csv',sep=r'\s*,\s*',header=0, encoding='ascii', engine='python')

features = ["ADV_S", "ADV_R", "Rank", "send_code", "id", "who CH"]
for i in features:
    train.pop(i)
# Assuming 'class' is the target variable, modify accordingly
X_train = train.drop(['Attack type'], axis=1)
Y_train = train['Attack type']
print(Y_train)
# Split the data
x_train, x_test, y_train, y_test = train_test_split(X_train, Y_train, train_size=0.70, random_state=2)

# Train the KNN model
knn_model = KNeighborsClassifier(n_neighbors=1)  # You can adjust the number of neighbors as needed
knn_model.fit(x_train, y_train)

# Save the trained KNN model
joblib.dump(knn_model, 'knn_model2.joblib')
# Train the Decision Tree model
dt_model = DecisionTreeClassifier(max_depth=4, criterion="entropy")
dt_model.fit(x_train, y_train)

# Save the trained Decision Tree model
joblib.dump(dt_model, 'decision_tree_model.joblib')

# Predictions on the training set
train_predictions = dt_model.predict(x_train)
train_predictions1 = knn_model.predict(x_train)
# Print training metrics
print("Training Accuracy:", accuracy_score(y_train, train_predictions), " ", accuracy_score(y_train, train_predictions1))
print("Training Classification Report:")
print(classification_report(y_train, train_predictions), " ", classification_report(y_train, train_predictions1))

# Predictions on the testing set
test_predictions = dt_model.predict(x_test)
test_predictions1 = knn_model.predict(x_test)
# Print testing metrics
print("\nTesting Accuracy:", accuracy_score(y_test, test_predictions), " ", accuracy_score(y_test, test_predictions1))
print("Testing Classification Report:")
print(classification_report(y_test, test_predictions)," ", classification_report(y_test, test_predictions1))
