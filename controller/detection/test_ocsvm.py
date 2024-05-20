from log_reader import read_logs_from_dir
from preprocessors.preprocessor import Preprocessor
from models.ocsvm import OCSVM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import time


df = read_logs_from_dir('../logs/V2/')
df = Preprocessor.get(version=2).preprocess(df)
ocsvm = OCSVM(TfidfVectorizer(ngram_range=(7, 7)), "ocsvm", "TF-IDF", (7, 7))
X_Train, X_Test, y_train, y_test = train_test_split(df['syscall'], df['malicious'], test_size=0.2, random_state=42)
print("Start training...")
start = time.time()
ocsvm.fit(X_Train)
print("Training time: ", time.time() - start, " seconds")

print("Start testing...")
start = time.time()
score = ocsvm.get_score(X_Test, y_test)
print("Testing time: ", time.time() - start, " seconds")

print("Score: ", score)