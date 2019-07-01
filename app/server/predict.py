import sys
from joblib import dump, load

clf = load('model.joblib')
print(clf.predict([sys.argv[1]]))