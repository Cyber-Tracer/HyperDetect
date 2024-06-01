from pyod.models.iforest import IForest
from sklearn.metrics import f1_score
from log_reader import read_all_logs
from preprocessors.preprocessor import Preprocessor
from train_models import train_test_split_df
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Read and preprocess logs
df = read_all_logs(version=1)
preprocessor = Preprocessor.get(version=1)
df = preprocessor.preprocess(df)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split_df(df)
X_train = X_train[y_train == 0]
y_train = y_train[y_train == 0]

# Define the parameters to be tuned

ngram_range = range(1, 6)
vectorizers = [CountVectorizer, TfidfVectorizer]


# Define the parameters to be tuned
param_grid = {
    'ngram': ngram_range,
    'vectorizer': vectorizers,
    'n_estimators': [50, 100, 200],
    'max_samples': ['auto', 0.5, 1.0],
    'max_features': [0.5, 0.75, 1.0],
}

# Get all parameter names and their corresponding values
keys, values = zip(*param_grid.items())
param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

print(f"Total number of parameter combinations: {len(param_combinations)}")

best_params = None
best_vectorizer = None
best_ngram = 0
best_f1 = 0

def vectorize(X_train, X_test, vectorizer):
    X_train = vectorizer.fit_transform(X_train).toarray()
    X_test = vectorizer.transform(X_test).toarray()
    return X_train, X_test

def train_and_evaluate(params):
    vectorizer = params.pop('vectorizer')
    ngram = params.pop('ngram')
    vectorizer = vectorizer(ngram_range=(ngram, ngram), token_pattern=r'\b\w+\b')
    X_train_vectorized, X_test_vectorized = vectorize(X_train, X_test, vectorizer)
    model = IForest(contamination=0.044, random_state=42, **params)
    model.fit(X_train_vectorized)
    y_test_pred = model.predict(X_test_vectorized)
    f1 = f1_score(y_test, y_test_pred)
    return f1, params, vectorizer.ngram_range[0], vectorizer.__class__.__name__

def update_best_params(results):
    global best_f1, best_params, best_ngram, best_vectorizer
    f1, params, ngram, vectorizer = results
    print(f"Scaler: {vectorizer}, Ngram: {ngram}, Parameters: {params}, F1 Score: {f1}")
    if f1 > best_f1:
        best_f1 = f1
        best_params = params
        best_ngram = ngram
        best_vectorizer = vectorizer
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
print(f"Best Ngram found: {best_ngram}")
print(f"Best Scaler found: {best_vectorizer}")