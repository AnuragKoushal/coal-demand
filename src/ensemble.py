
def weighted_ensemble(prophet_pred, lstm_pred, w1=0.6, w2=0.4):
    return (w1 * prophet_pred) + (w2 * lstm_pred)
