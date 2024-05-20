from models.model import Model
from pyod.models.ocsvm import OCSVM as PyodOCSVM
from sklearn.metrics import accuracy_score

class OCSVM(Model):
    instance = None
    contamination = 0.05


    def fit(self, X_train, y_train=None):
        X_train = self.scaler.fit_transform(X_train).toarray()
        self.instance = PyodOCSVM(cache_size=200, gamma='scale', kernel='rbf',nu=0.05,  shrinking=True, tol=0.001,verbose=False)
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
