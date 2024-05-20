from abc import ABC, abstractmethod

class Preprocessor(ABC):
    @staticmethod
    def get(version):
        """
        Get preprocessor based on version

        Returns
            Preprocessor
        """
        match version:
            case 1 | 2:
                from .V1 import V1
                return V1()
            case _:
                raise ValueError(f'Version {version} not supported')

    @abstractmethod
    def preprocess(self, df):
        """
        Preprocess data

        Returns
            df
        """
        pass