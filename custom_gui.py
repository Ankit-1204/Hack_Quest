import streamlit as st

from ddd import cust
from keras.models import load_model

model = load_model('model_filename.h5')

def analyze_sentiment(text):
    vad=cust(text)
    sentiment = model.predict(vad)

    if sentiment == 1:
        st.image('images/negative.PNG', caption='Negative Sentiment', width=100)
    elif sentiment == 2:
        st.image('images/neutral.PNG', caption='Neutral Sentiment', width=100)
    elif sentiment == 3:
        st.image('images/positive.PNG', caption='Positive Sentiment', width=100)
def main():
    st.title("Sentiment Analysis")

    # Input text box
    user_input = st.text_input("Enter your text here:")

    # Submit button
    if st.button("Submit"):
        if user_input.strip() != "":
            # Sentiment analysis
            prediction = analyze_sentiment(user_input)
            st.write("Prediction:", prediction)
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
