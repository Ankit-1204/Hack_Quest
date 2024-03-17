import joblib

sentiment_pipe = joblib.load('Sentiment_pipe.joblib')

print(int(sentiment_pipe("Absoulutely awesome")[0]['label'][0]))