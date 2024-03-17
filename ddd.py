import nltk
nltk.download('vader_lexicon')
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm  # Use the standard tqdm import for non-notebook environments

def cust(input_text):
# Initialize SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Creating a DataFrame
    data = {'id': [0], 'verified_reviews': [input_text]}
    dxf = pd.DataFrame(data)

    # Initialize an empty dictionary to store results
    ress = {}

    # Use tqdm directly with iterrows for a DataFrame
    for i, row in tqdm(dxf.iterrows(), total=dxf.shape[0]):
        text = str(row['verified_reviews'])  # Convert to string explicitly
        myid = row['id']
        ress[myid] = sia.polarity_scores(text)  # Store polarity scores in the dictionary

    # Convert the results dictionary to a DataFrame
    vad = pd.DataFrame.from_dict(ress, orient='index').reset_index().rename(columns={'index': 'id'})
    vad = vad.merge(dxf, how='left', on='id').drop(['id', 'verified_reviews'], axis=1)

    return vad

