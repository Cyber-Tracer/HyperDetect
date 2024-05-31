from ..model import Model
from pyod.models.iforest import IForest as PyodIForest

class IForest(Model):
    instance = None
    contamination = 0.044


    def fit(self, X_train, y_train=None):
        X_train = X_train[y_train == 0] # Only fit on normal data
        X_train = self.scaler.fit_transform(X_train).toarray()
        self.instance = PyodIForest(random_state=42, contamination=self.contamination, n_estimators=200, max_samples=1.0, max_features=1.0)
        self.instance.fit(X_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.scaler.transform(X_test).toarray()
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'IForest'

    def get_model_type(self):
        return 'Anomaly Detection'
