from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, scaler, model_type: str, scaler_type: str, ngram_range: tuple):
        self.scaler = scaler
        self.model_type = model_type
        self.scaler_type = scaler_type
        self.ngram_range = ngram_range

    @abstractmethod
    def train_test_split(self, df):
        """
        Split data into train and test set

        Returns
            train, test
        """
        pass

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
    def get_score(self, X_test, y_test):
        """
        Get score

        Returns
            score in range [0, 1]
        """
        pass

    def get_model_type(self):
        return self.model_type
    
    def get_scaler_type(self):
        return self.scaler_type
    
    def get_ngram_range(self):
        return self.ngram_range
    
    def __str__(self) -> str:
        return f"{self.model_type}_{self.scaler_type}_{self.ngram_range[0]}_{self.ngram_range[1]}"
