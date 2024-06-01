from ..model import Model
from pyod.models.lof import LOF as PyodLocalOutlierFactor

class LOF(Model):
    instance = None
    contamination = 0.044

    def transform(self, X):
        return self.vectorizer.transform(X).toarray()
    
    def fit_vectorized(self, X_train, y_train):
        self.instance = PyodLocalOutlierFactor(contamination=self.contamination, novelty=True, n_neighbors=10, algorithm='auto', metric='euclidean')
        self.instance.fit(X_train)

    def fit(self, X_train, y_train):
        X_train = X_train[y_train == 0] # Only fit on normal data
        self.vectorizer.fit(X_train)
        X_train = self.transform(X_train)
        self.fit_vectorized(X_train, y_train)

    def predict(self, X_test):
        if self.instance is None:
            raise ValueError("Model is not fitted.")
        X_test = self.transform(X_test)
        return self.instance.predict(X_test)
    
    def get_model_name(self):
        return 'LOF'

    def get_model_type(self):
        return 'Anomaly Detection'
