from ..model import Model
from sklearn.naive_bayes import MultinomialNB

class NB(Model):
    instance = None

    def fit_vectorized(self, X_train, y_train=None):
        self.instance = MultinomialNB()
        self.instance.fit(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.transform(X_test)
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'NB'

    def get_model_type(self):
        return 'Classification'
