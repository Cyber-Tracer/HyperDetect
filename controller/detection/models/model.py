from abc import ABC, abstractmethod
from scipy.sparse import csr_matrix

class Model(ABC):
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    @staticmethod
    def get_model_classes(version):
        match version:
            case 1:
                from .V1.iforest import IForest
                from .V1.lof import LOF
                from .V1.nb import NB
                from .V1.rf import RF
                return [IForest, LOF, NB, RF]
            case 2:
                from .V2.iforest import IForest
                from .V2.lof import LOF
                from .V2.nb import NB
                from .V2.rf import RF
                return [IForest, LOF, NB, RF]
            case _:
                raise ValueError("Invalid version")

    def set_vectorizer(self, vectorizer):
        self.vectorizer = vectorizer

    @abstractmethod
    def fit_vectorized(self, X_train, y_train):
        pass

    def transform(self, X):
        return csr_matrix(self.vectorizer.transform(X))

    def fit(self, X_train, y_train):
        """
        Train model

        Returns
            model
        """
        self.vectorizer.fit(X_train)
        X_train = self.transform(X_train)
        self.fit_vectorized(X_train, y_train)

    @abstractmethod
    def predict(self, X_test):
        """
        Predict

        Returns
            prediction
        """
        pass

    @abstractmethod
    def get_model_name(self):
        pass

    @abstractmethod
    def get_model_type(self):
        pass
    
    def get_vectorizer_type(self):
        return self.vectorizer.__class__.__name__
    
    def get_ngram_range(self):
        return self.vectorizer.ngram_range
    
    def __str__(self) -> str:
        return f"{self.get_model_name()}_{self.get_vectorizer_type()}_{self.get_ngram_range()[0]}_{self.get_ngram_range()[1]}"
