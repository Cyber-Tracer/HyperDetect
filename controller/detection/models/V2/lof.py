from ..model import Model
from sklearn.neighbors import LocalOutlierFactor

class LOF(Model):
    instance = None
    contamination = 0.093

    def fit_vectorized(self, X_train, y_train=None):
        self.instance = LocalOutlierFactor(contamination=self.contamination, novelty=True, n_neighbors=10, algorithm='auto', metric='euclidean')
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
        return 'LOF'

    def get_model_type(self):
        return 'Anomaly Detection'
