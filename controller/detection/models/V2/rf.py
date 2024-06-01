from ..model import Model
from sklearn.ensemble import RandomForestClassifier

class RF(Model):
    instance = None

    def fit_vectorized(self, X_train, y_train):
        self.instance = RandomForestClassifier()
        self.instance.fit(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.transform(X_test)
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'RF'

    def get_model_type(self):
        return 'Classification'
