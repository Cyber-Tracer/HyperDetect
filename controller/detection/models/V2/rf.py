from ..model import Model
from sklearn.ensemble import RandomForestClassifier

class RF(Model):

    def fit_vectorized(self, X_train, y_train):
        self.instance = RandomForestClassifier(criterion = 'log_loss', max_features='log2')
        self.instance.fit(X_train, y_train)
    
    def get_model_name(self):
        return 'RF'

    def get_model_type(self):
        return 'Classification'
