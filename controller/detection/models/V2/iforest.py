from ..model import Model
from sklearn.ensemble import IsolationForest

class IForest(Model):
    instance = None
    contamination = 0.093

    def fit_vectorized(self, X_train, y_train=None):
        self.instance = IsolationForest(random_state=42, contamination=self.contamination, n_estimators=200, max_samples=1.0, max_features=1.0)
        self.instance.fit(X_train)

    def fit(self, X_train, y_train=None):
        X_train = X_train[y_train == 0] # Only fit on normal data
        y_train = y_train[y_train == 0]
        super().fit(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.transform(X_test)
        pred = self.instance.predict(X_test)
        pred[pred == 1] = 0
        pred[pred == -1] = 1
        return pred
    
    def get_model_name(self):
        return 'IForest'

    def get_model_type(self):
        return 'Anomaly Detection'
