from ..model import Model
from sklearn.naive_bayes import MultinomialNB

class NB(Model):

    def fit_vectorized(self, X_train, y_train=None):
        self.instance = MultinomialNB()
        self.instance.fit(X_train, y_train)
    
    def get_model_name(self):
        return 'NB'

    def get_model_type(self):
        return 'Classification'
