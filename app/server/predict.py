import sys
from joblib import dump, load

clf = load('model.joblib')
probs = clf.predict_proba([sys.argv[1]])[0]
print("[" + str(probs[0]) + ", " + str(probs[1]) + "]")
