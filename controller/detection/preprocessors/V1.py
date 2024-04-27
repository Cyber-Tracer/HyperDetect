from preprocessors.preprocessor import Preprocessor
import pandas as pd

class V1(Preprocessor):
    def list_to_str(self, lst: list):
        return ' '.join(lst)

    def group_by_pid_and_timestamp(self, df, floor='10s'):
        """
            Group df by pid and timestamp, aggregating syscalls in a list

            Parameters
                df: pd.DataFrame
                floor: str, e.g. '10s', '1min', '5s' etc.

            Returns
                df(pid, timestamp, syscall, malicious)
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df['timestamp'] = df['timestamp'].dt.floor(floor)
        df = df.drop(columns=['pname', 'tid', 'rcx', 'rdx', 'r8', 'r9'])
        grouped_df = df.groupby(['pid', 'timestamp']).agg({'syscall':list, 'malicious': 'first'})
        return grouped_df

    def preprocess(self, df):
        df = self.group_by_pid_and_timestamp(df)
        df['syscall'] = df['syscall'].apply(self.list_to_str)
        return df