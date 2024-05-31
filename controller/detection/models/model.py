from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, scaler):
        self.scaler = scaler

    @abstractmethod
    def fit(self, X_train, y_train=None):
        """
        Train model

        Returns
            model
        """
        pass

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
    
    def get_scaler_type(self):
        return self.scaler.__class__.__name__
    
    def get_ngram_range(self):
        return self.scaler.ngram_range
    
    def __str__(self) -> str:
        return f"{self.get_model_name()}_{self.get_scaler_type()}_{self.get_ngram_range()[0]}_{self.get_ngram_range()[1]}"
