from ..model import Model
from sklearn.neighbors import LocalOutlierFactor

class LOF(Model):
    contamination = 0.093

    def fit_vectorized(self, X_train, y_train=None):
        self.instance = LocalOutlierFactor(contamination=self.contamination, novelty=True, n_neighbors=10, algorithm='auto', metric='manhattan')
        self.instance.fit(X_train)

    def fit(self, X_train, y_train=None):
        X_train = X_train[y_train == 0] # Only fit on normal data
        y_train = y_train[y_train == 0]
        super().fit(X_train, y_train)

    def pred_to_binary(self, pred):
        pred[pred == 1] = 0
        pred[pred == -1] = 1
        return pred

    def predict(self, X_test):
        pred = super().predict(X_test)
        return self.pred_to_binary(pred)
    
    def get_model_name(self):
        return 'LOF'

    def get_model_type(self):
        return 'Anomaly Detection'
