import argparse
from log_reader import read_all_logs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
from preprocessors.preprocessor import Preprocessor
from models.model import Model
import pickle
import os
import pandas as pd
import time
import concurrent.futures as cf

def train_test_split_df(df):
    return train_test_split(df['syscall'], df['malicious'], test_size=0.2, random_state=42)

def save_model(model, version, output_dir):
    file = os.path.join(output_dir, f'v{version}_{str(model)}.pkl')
    with open(file, 'wb') as f:
        pickle.dump(model, f)

def load_model(file):
    with open(file, 'rb') as f:
        model = pickle.load(f)
    return model

def get_instantiated_models(version):
    ngrams = range(1, 6)
    vectorizers = [CountVectorizer, TfidfVectorizer]
    models = Model.get_model_classes(version=version)
    instantiated_models = []
    token_pattern = r'\b\w+\b'
    for vectorizer in vectorizers:
        for ngram in ngrams:
            for model in models:
                instantiated_models.append(model(vectorizer(ngram_range=(ngram, ngram), token_pattern=token_pattern)))
    return instantiated_models

def to_model_properties(model):
    return {
        'Model': model.get_model_name(),
        'Model_Type': model.get_model_type(),
        'Vectorizer': model.get_vectorizer_type(),
        'Min Ngram': model.get_ngram_range()[0],
        'Max Ngram': model.get_ngram_range()[1]
    }

def load_scores_from_dir(output_dir):
    file = os.path.join(output_dir, 'test_scores.csv')
    if not os.path.exists(file):
        return None
    df = pd.read_csv(file)
    return df


def load_scores(version, output_dir):
    score_dir = os.path.join(output_dir, f'V{version}')
    return load_scores_from_dir(score_dir)
    
def train_eval_model(model, X_train, X_test, y_train, y_test):
    start = time.time()
    model.fit(X_train, y_train)
    duration = time.time() - start
    y_pred = model.predict(X_test)
    score = accuracy_score(y_pred, y_test)
    f1 = f1_score(y_pred, y_test)
    recall = recall_score(y_pred, y_test)
    precision = precision_score(y_pred, y_test)
    print(f"Model: {model} - F1 Score: {f1}")
    return model, {"Score": score, "Duration": duration, "F1": f1, "Recall": recall, "Precision": precision}


def main(version, log_dir, output_dir):
    print(log_dir)
    df = read_all_logs(version, logs_dir=log_dir)
    preprocessor = Preprocessor.get(version)
    df = preprocessor.preprocess(df)

    output_dir = os.path.join(output_dir, f'v{version}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    X_train, X_test, y_train, y_test = train_test_split_df(df)
    scores = []
    models = get_instantiated_models(version)

    with cf.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(train_eval_model, model, X_train, X_test, y_train, y_test) for model in models]
        for future in cf.as_completed(futures):
            model, model_scores = future.result()
            row = model_scores | to_model_properties(model)
            scores.append(row)
            save_model(model, version, output_dir)
        
        cf.wait(futures)
    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.sort_values(by='F1', ascending=False)
    scores_df.to_csv(os.path.join(output_dir, 'test_scores.csv'), index=False)
    print("Top 3 models: ")
    print(scores_df.head(3))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument('--version', type=int, default=1, help='Version of the detector system')
    parser.add_argument('--log_dir', type=str, default=os.path.join(file_dir ,'../logs'), help='Directory where the logs are stored, default is ../logs')
    parser.add_argument('--output_dir', type=str, default=os.path.join(file_dir ,'./models/trained'), help='Output directory to save the models, default is ./models/trained')
    opt = parser.parse_args()
    if not os.path.exists(opt.output_dir):
        raise FileNotFoundError(f"Output directory {opt.output_dir} not found")
    if not os.path.exists(opt.log_dir):
        raise FileNotFoundError(f"Log directory {opt.log_dir} not found")
    main(opt.version, opt.log_dir, opt.output_dir)