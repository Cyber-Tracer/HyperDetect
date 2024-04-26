from models.model import Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

class NB(Model):
    instance = None

    def train_test_split(self, df):
        malicious_sample = df.loc[df['malicious'] == 1]
        benign_sample = df.loc[df['malicious'] == 0].sample(n=malicious_sample.shape[0], random_state=42)
        classifier_sample = pd.concat([malicious_sample, benign_sample])

        return train_test_split(classifier_sample['syscall'], classifier_sample['malicious'], test_size=0.2, random_state=42)

    def fit(self, X_train, y_train=None):
        if y_train is None:
            raise ValueError("y_train is required for naive bayes model.")
        X_train = self.scaler.fit_transform(X_train)
        self.instance = MultinomialNB()
        self.instance.fit(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.scaler.transform(X_test)
        return self.instance.predict(X_test)

    def get_score(self, X_test, y_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.scaler.transform(X_test)
        return self.instance.score(X_test, y_test)
