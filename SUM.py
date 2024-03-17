import pickle

with open("summarizer_pipeline2 (1).pkl", "rb") as f:
    summarizer = pickle.load(f)

text = "John: doing anything special?\r\nAlex: watching 'Millionaires' on tvn\r\nSam: me too! He has a chance to win a million!\r\nJohn: ok, fingers crossed then! :)"
summary = "Alex and Sam are watching Millionaires."
generated_summary = summarizer(text)

print(generated_summary)[0]["summary_text"]
