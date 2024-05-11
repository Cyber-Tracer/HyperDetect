import argparse
from log_reader import read_all_logs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from preprocessors.preprocessor import Preprocessor
from models.nb import NB
from models.iforest import IForest
import pickle
import os
import pandas as pd

def balance_eval_set(X_test, y_test):
    malicious = X_test[y_test == 1]
    benign = X_test[y_test == 0]
    n = min(len(malicious), len(benign))
    X_test = pd.concat([malicious.head(n), benign.head(n)])
    y_test = pd.concat([y_test[malicious.head(n).index], y_test[benign.head(n).index]])
    return X_test, y_test

def train_model(model, df):
    X_train, X_test, y_train, y_test = train_test_split(df['syscall'], df['malicious'], test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    X_test, y_test = balance_eval_set(X_test, y_test)
    score = model.get_score(X_test, y_test)
    return (model, score)

def save_model(model, version, output_dir):
    file = os.path.join(output_dir, f'v{version}_{str(model)}.pkl')
    with open(file, 'wb') as f:
        pickle.dump(model, f)

def load_model(file):
    with open(file, 'rb') as f:
        model = pickle.load(f)
    return model

def get_v1_models():
    ngrams = range(1, 10)
    models = []
    for ngram in ngrams:
        m1 = NB(CountVectorizer(ngram_range=(ngram, ngram)), 'NB', 'Frequency', (ngram, ngram))
        m2 = IForest(CountVectorizer(ngram_range=(ngram, ngram)), 'IForest', 'Frequency', (ngram, ngram))
        m3 = NB(TfidfVectorizer(ngram_range=(ngram, ngram)), 'NB', 'TFID', (ngram, ngram))
        m4 = IForest(TfidfVectorizer(ngram_range=(ngram, ngram)), 'IForest', 'TFID', (ngram, ngram))
        models.extend((m1, m2, m3, m4))
    min_max = (ngrams[0], ngrams[-1])
    m1 = NB(CountVectorizer(ngram_range=min_max), 'NB', 'Frequency', min_max)
    m2 = IForest(CountVectorizer(ngram_range=min_max), 'IForest', 'Frequency', min_max)
    m3 = NB(TfidfVectorizer(ngram_range=min_max), 'NB', 'TFID', min_max)
    m4 = IForest(TfidfVectorizer(ngram_range=min_max), 'IForest', 'TFID', min_max)
    models.extend((m1, m2, m3, m4))
    return models

def to_scores_df(models, scores):
    data = []
    for model, score in zip(models, scores):
        data.append([model.get_model_type(), model.get_scaler_type(), model.get_ngram_range()[0], model.get_ngram_range()[1], score])
    df = pd.DataFrame(data, columns=['Model', 'Scaler', 'Min Ngram', 'Max Ngram', 'Score'])
    df = df.sort_values(by='Score', ascending=False)
    return df

def load_scores(version, output_dir):
    file = os.path.join(output_dir, f'V{version}', 'test_scores.csv')
    if not os.path.exists(file):
        return None
    df = pd.read_csv(file)
    return df


def main(version, log_dir, output_dir):
    print(log_dir)
    df = read_all_logs(version, logs_dir=log_dir)
    preprocessor = Preprocessor.get(version)
    df = preprocessor.preprocess(df)

    output_dir = os.path.join(output_dir, f'v{version}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    models = get_v1_models()
    scores = []
    for model in models:
        model, score = train_model(model, df)
        print(f"Model: {model} - Score: {score}")
        scores.append(score)
        save_model(model, version, output_dir)
    df = to_scores_df(models, scores)
    df.to_csv(os.path.join(output_dir, 'test_scores.csv'), index=False)
    print("Top 3 models: ")
    print(df.head(3))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument('--version', type=int, default=1, help='Version of the detector system')
    parser.add_argument('--log_dir', type=str, default=os.path.join(file_dir ,'../logs'), help='Directory where the logs are stored')
    parser.add_argument('--output_dir', type=str, default=os.path.join(file_dir ,'./models/trained'), help='Output directory to save the models')
    opt = parser.parse_args()
    if not os.path.exists(opt.output_dir):
        raise FileNotFoundError(f"Output directory {opt.output_dir} not found")
    if not os.path.exists(opt.log_dir):
        raise FileNotFoundError(f"Log directory {opt.log_dir} not found")
    main(opt.version, opt.log_dir, opt.output_dir)