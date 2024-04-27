import argparse
from log_reader import read_all_logs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessors.preprocessor import Preprocessor
from models.nb import NB
from models.iforest import IForest
import pickle
import os
import pandas as pd

def train_model(model, df):
    X_train, X_test, y_train, y_test =  model.train_test_split(df)
    model.fit(X_train, y_train)
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
    ngrams = range(1, 8)
    models = []
    for ngram in ngrams:
        m1 = NB(CountVectorizer(ngram_range=(ngram, ngram)), 'NB', 'Frequency', (ngram, ngram))
        m2 = IForest(CountVectorizer(ngram_range=(ngram, ngram)), 'IForest', 'Frequency', (ngram, ngram))
        m3 = NB(TfidfVectorizer(ngram_range=(ngram, ngram)), 'NB', 'TFID', (ngram, ngram))
        m4 = IForest(TfidfVectorizer(ngram_range=(ngram, ngram)), 'IForest', 'TFID', (ngram, ngram))
        models.extend((m1, m2, m3, m4))
    m1 = NB(CountVectorizer(ngram_range=(1, 8)), 'NB', 'Frequency', (1, 7))
    m2 = IForest(CountVectorizer(ngram_range=(1, 8)), 'IForest', 'Frequency', (1, 7))
    m3 = NB(TfidfVectorizer(ngram_range=(1, 8)), 'NB', 'TFID', (1, 7))
    m4 = IForest(TfidfVectorizer(ngram_range=(1, 8)), 'IForest', 'TFID', (1, 7))
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


def main(version, output_dir):
    df = read_all_logs(version)
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
    parser.add_argument('--version', type=int, default=1, help='Version of the detector system')
    parser.add_argument('--output_dir', type=str, default=os.path.join(os.getcwd() ,'./models/trained'), help='Output directory to save the models')
    opt = parser.parse_args()
    if not os.path.exists(opt.output_dir):
        raise FileNotFoundError(f"Output directory {opt.output_dir} not found")
    main(opt.version, opt.output_dir)