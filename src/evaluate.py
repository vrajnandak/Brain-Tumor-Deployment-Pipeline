from sklearn.metrics import classification_report
import numpy as np

def evaluate(model, X_test, y_test):
    preds = np.argmax(model.predict(X_test), axis=1)
    print(classification_report(y_test, preds))
