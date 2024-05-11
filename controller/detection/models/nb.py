from models.model import Model
from sklearn.naive_bayes import MultinomialNB

class NB(Model):
    instance = None

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
