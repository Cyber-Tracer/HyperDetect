import argparse
from log_reader import read_all_logs
from sklearn.feature_extraction.text import CountVectorizer
from preprocessors.preprocessor import Preprocessor
from models.nb import NB
from models.iforest import IForest
import pickle
import os

def train_model(model, df):
    X_train, X_test, y_train, y_test =  model.train_test_split(df)
    model.fit(X_train, y_train)
    score = model.get_score(X_test, y_test)
    print(f"{model} Score: {score}")

def save_model(model, version, output_dir):
    file = os.path.join(output_dir, f'v{version}_{model.get_model_type()}_{model.get_scaler_type()}.pkl')
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
        m1 = NB(CountVectorizer(ngram_range=(ngram, ngram)), 'NB', f'{ngram}-gram')
        m2 = IForest(CountVectorizer(ngram_range=(ngram, ngram)), 'IForest', f'{ngram}-gram')
        models.extend((m1, m2))
    return models

def main(version, output_dir):
    df = read_all_logs(version)
    preprocessor = Preprocessor.get(version)
    df = preprocessor.preprocess(df)

    output_dir = os.path.join(output_dir, f'v{version}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    models = get_v1_models()
    for model in models:
        train_model(model, df)
        save_model(model, version, output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, default=1, help='Version of the detector system')
    parser.add_argument('--output_dir', type=str, default=os.path.join(os.getcwd() ,'./models/trained'), help='Output directory to save the models')
    opt = parser.parse_args()
    if not os.path.exists(opt.output_dir):
        raise FileNotFoundError(f"Output directory {opt.output_dir} not found")
    main(opt.version, opt.output_dir)