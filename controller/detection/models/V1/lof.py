from ..model import Model
from pyod.models.lof import LOF as PyodLocalOutlierFactor

class LOF(Model):
    instance = None
    contamination = 0.044


    def fit(self, X_train, y_train=None):
        X_train = X_train[y_train == 0] # Only fit on normal data
        X_train = self.vectorizer.fit_transform(X_train).toarray()
        self.instance = PyodLocalOutlierFactor(contamination=self.contamination, novelty=True, n_neighbors=10, algorithm='auto', metric='euclidean')
        self.instance.fit(X_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.vectorizer.transform(X_test).toarray()
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'LOF'

    def get_model_type(self):
        return 'Anomaly Detection'
