from preprocessors.preprocessor import Preprocessor
import pandas as pd

class V1(Preprocessor):
    def list_to_str(self, lst: list):
        return ' '.join(lst)

    def group_by_pid_and_ten_seconds(self, df):
        """
            Group df by pid and 10 seconds, aggregating syscalls in a list

            Returns
                df(pid, timestamp, syscall, malicious)
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df['timestamp'] = df['timestamp'].dt.floor('10s')
        df = df.drop(columns=['pname', 'tid', 'rcx', 'rdx', 'r8', 'r9'])
        grouped_df = df.groupby(['pid', 'timestamp']).agg({'syscall':list, 'malicious': 'first'})
        return grouped_df

    def preprocess(self, df):
        df = self.group_by_pid_and_ten_seconds(df)
        df['syscall'] = df['syscall'].apply(self.list_to_str)
        return df