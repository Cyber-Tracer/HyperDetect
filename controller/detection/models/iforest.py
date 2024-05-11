from models.model import Model
from pyod.models.iforest import IForest as PyodIForest
from sklearn.metrics import accuracy_score

class IForest(Model):
    instance = None
    contamination = 0.1


    def fit(self, X_train, y_train=None):
        X_train = self.scaler.fit_transform(X_train).toarray()
        self.instance = PyodIForest(random_state=42, contamination=self.contamination)
        self.instance.fit(X_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.scaler.transform(X_test).toarray()
        return self.instance.predict(X_test)

    def get_score(self, X_test, y_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.scaler.transform(X_test).toarray()
        y_pred = self.instance.predict(X_test)
        return accuracy_score(y_true=y_test, y_pred=y_pred)
