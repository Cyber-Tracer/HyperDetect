import argparse
from pyod.models.iforest import IForest as PyodIForest
from pyod.models.lof import LOF as PyodLOF
from sklearn.ensemble import IsolationForest as SklearnIForest
from sklearn.neighbors import LocalOutlierFactor as SklearnLOF
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from models.model import Model
from sklearn.metrics import f1_score
from log_reader import read_all_logs
from preprocessors.preprocessor import Preprocessor
from train_models import train_test_split_df
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--version", type=int, help="Version number", default=1)
parser.add_argument("--model", type=str, help="Model to use", choices=['IForest', 'LOF', 'NB', 'RF'])
args = parser.parse_args()

# Get the version number from command line arguments
version = args.version
model_name = args.model
model_wrapper = next((cls for cls in Model.get_model_classes(version=version) if cls.__name__ == model_name), None) 

if model_wrapper is None:
    raise ValueError(f"Model {model_name} not found for version {version}")

# Read and preprocess logs
df = read_all_logs(version=version)
preprocessor = Preprocessor.get(version=version)
df = preprocessor.preprocess(df)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split_df(df)

# Define the parameters to be tuned

ngram_range = range(1, 6)
vectorizers = [CountVectorizer, TfidfVectorizer]

version_param_grid = {
    1: {
        'IForest': (
            PyodIForest,
            {
                'contamination': [0.044], # Fixed
                'random_state' : [42], # Fixed
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'n_estimators': [50, 100, 200],
                'max_samples': ['auto', 0.5, 1.0],
                'max_features': [0.5, 0.75, 1.0],
            },
            False
        ),
        'LOF': (
            PyodLOF,
            {
                'contamination': [0.044], # Fixed
                'random_state' : [42], # Fixed
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'n_neighbors': [10, 20, 50],
                'algorithm': ['auto', 'ball_tree', 'kd_tree'],
                'metric': ['euclidean', 'manhattan', 'minkowski'],
            },
            False
        )
    },
    2: {
        'IForest': (
            SklearnIForest,
            {
                'contamination': [0.093], # Fixed
                'random_state' : [42], # Fixed 
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'n_estimators': [50, 100, 200],
                'max_samples': ['auto', 0.5, 1.0],
                'max_features': [0.5, 0.75, 1.0],
            },
            False
        ),
        'LOF': (
            SklearnLOF,
            {
                'contamination': [0.093], # Fixed
                'novelty' : [True], # Fixed  
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'n_neighbors': [10, 20, 50],
                'metric': ['euclidean', 'manhattan', 'minkowski'],
            },
            False
        ),
        'NB': (
            MultinomialNB,
            {
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'alpha': [0.2, 1.0, 2.0],
            },
            True
        ),
        'RF': (
            RandomForestClassifier,
            {
                'ngram': ngram_range,
                'vectorizer': vectorizers,
                'n_estimators': [50, 100, 200],
                'criterion': ['gini', 'entropy', 'log_loss'],
                'max_features': ['log2', 'sqrt', None],
            },
            True
        )
    }
}

# Define the parameters to be tuned
model_class = version_param_grid[version][model_name][0]
param_grid = version_param_grid[version][model_name][1]
is_classifier = version_param_grid[version][model_name][2]

if not is_classifier:
    X_train = X_train[y_train == 0]
    y_train = y_train[y_train == 0]

# Get all parameter names and their corresponding values
keys, values = zip(*param_grid.items())
param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

print(f"Start gridsearch for {model_name}, version {version}. Grid: ", param_grid)

print(f"Total number of parameter combinations: {len(param_combinations)}")

best_params = None
best_vectorizer = None
best_ngram = 0
best_f1 = 0

def train_and_evaluate(params):
    vectorizer = params.pop('vectorizer')
    ngram = params.pop('ngram')
    vectorizer = vectorizer(ngram_range=(ngram, ngram), token_pattern=r'\b\w+\b')
    instance = model_class(**params)
    vectorizer.fit(X_train)
    model = model_wrapper(vectorizer)
    X_train_vectorized = model.transform(X_train)
    if is_classifier:
        instance.fit(X_train_vectorized, y_train)
    else:
        instance.fit(X_train_vectorized)
    model.instance = instance
    y_test_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_test_pred)
    return f1, params, ngram, vectorizer.__class__.__name__

def update_best_params(results):
    global best_f1, best_params, best_ngram, best_vectorizer
    f1, params, ngram, vectorizer = results
    print(f"Vectorizer: {vectorizer}, Ngram: {ngram}, Parameters: {params}, F1 Score: {f1}")
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
print(f"Best Vectorizer found: {best_vectorizer}")