from ..model import Model
from sklearn.ensemble import RandomForestClassifier

class RF(Model):
    instance = None

    def fit(self, X_train, y_train=None):
        if y_train is None:
            raise ValueError("y_train is required for naive bayes model.")
        X_train = self.vectorizer.fit_transform(X_train).toarray()
        self.instance = RandomForestClassifier()
        self.instance.fit(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.vectorizer.transform(X_test).toarray()
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'RF'

    def get_model_type(self):
        return 'Classification'
