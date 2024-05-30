from pyod.models.lof import LOF
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from log_reader import read_all_logs
from preprocessors.preprocessor import Preprocessor
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Read and preprocess logs
df = read_all_logs(version=1)
preprocessor = Preprocessor.get(version=1)
df = preprocessor.preprocess(df)

# Vectorize data
vectorizer = CountVectorizer(ngram_range=(3, 3))
X = vectorizer.fit_transform(df['syscall']).toarray()
y = df['malicious']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_test = np.concatenate((X_test, X_train[y_train == 1]))
y_test = np.concatenate((y_test, y_train[y_train == 1]))
X_train = X_train[y_train == 0]
y_train = y_train[y_train == 0]

# Define the parameters to be tuned
param_grid = {
    'n_neighbors': [10, 20, 50],
    'algorithm': ['auto', 'ball_tree', 'kd_tree'],
    'metric': ['euclidean', 'manhattan', 'minkowski'],
}

# Get all parameter names and their corresponding values
keys, values = zip(*param_grid.items())
param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

print(f"Total number of parameter combinations: {len(param_combinations)}")

best_params = None
best_f1 = 0

def train_and_evaluate(params):
    model = LOF(novelty=True, contamination=0.044, **params)
    model.fit(X_train)
    y_test_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_test_pred)
    return f1, params

def update_best_params(results):
    global best_f1, best_params
    f1, params = results
    print(f"Parameters: {params}, F1 Score: {f1}")
    if f1 > best_f1:
        best_f1 = f1
        best_params = params
print("Starting grid search...")
start = time.time()

with ThreadPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(train_and_evaluate, params) for params in param_combinations]
    for future in as_completed(futures):
        try:
            result = future.result(timeout=120)
            update_best_params(result)
        except TimeoutError:
            print("Timeout error occurred")

print(f"Grid search completed in {time.time() - start} seconds")
print(f"Best parameters found: {best_params}")
print(f"Best F1 Score found: {best_f1}")