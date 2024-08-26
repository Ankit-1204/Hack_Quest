import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import joblib
import numpy as np

import re
import csv
import os.path

sentiment_pipe = joblib.load('Sentiment_pipe.joblib')

sentiment_df = pd.read_csv('sentiment_data.csv')

def predict_sentiment(input_text):
    
    prediction=int(sentiment_pipe(input_text)[0]['label'][0])
    if prediction in [1, 2]:
        return 1
    elif prediction in [3, 4]:
        return 2
    elif prediction == 5:
        return 3
    else:
        return "Unknown"


def update_csv(product_name, prediction):
    filename = 'sentiment_data.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product', '1', '2', '3'])

    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        found = False
        for row in rows:
            if row['Product'] == product_name:
                row[str(prediction)] = int(row[str(prediction)]) + 1
                found = True
                break
        if not found:
            new_row = {'Product': product_name, '1': 0, '2': 0, '3': 0}
            new_row[str(prediction)] = 1
            rows.append(new_row)

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Product', '1', '2', '3'])
        writer.writeheader()
        writer.writerows(rows)


def plot_doughnut_pie_chart(product_name):
    product_row = sentiment_df[sentiment_df['Product'] == product_name]
    if product_row.empty:
        st.warning(f"No sentiment data available for {product_name}")
        return

    product_data = product_row.iloc[0]
    counts = [product_data['1'], product_data['2'], product_data['3']]
    total_reviews = sum(counts)
    percentages = [count / total_reviews * 100 for count in counts]



    fig, ax = plt.subplots(figsize=(1,1))
    ax.pie(percentages, labels=['Negative', 'Neutral', 'Positive'], autopct='%1.1f%%', startangle=90, colors=['red', 'green', 'blue'],wedgeprops={'width': 0.6, 'edgecolor': 'black'})
    centre_circle = plt.Circle((0,0),0.94,fc='black')
    fig.patch.set_facecolor('black') 
    fig.gca().add_artist(centre_circle)
    plt.title('Sentiment Distribution',color='white', fontsize=6)
    plt.axis('equal') 
         
    for text in ax.texts:
        text.set_color('white')
        text.set_fontsize(6)
    st.pyplot(fig,width=200) 
    


products = {
    'Fire TV Stick': { "image": "images/Fire Stick.jpg"},
    'Speaker Echo 2': { "image": "images/Speaker Echo 2.jpg"},
    'Walnut Finish Echo': {"image":"images/Walnut finish echo.jpg"},
    'White echo dot': {"image": "images/white echo dot.jpg"},
    'White Show': {"image": "images/white show.jpg"},
    'Oak Finish Echo': {"image": "images/oak finish echo dot.jpg"},
    'Black Plus Echo': {"image": "images/black plus echo.jpg"},
}
products_df = pd.read_csv('products.csv')


def main():
    st.title("Alexa Product Reviews")
    for index, row in products_df.iterrows():
        product_name = row['Product']
        product_image_path = row['Image_Path']

        st.write(f"## {product_name}")
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.write("")
            
        with col2:
            st.image(f"{product_image_path}", width=150)
            
         
            
        with col3:
            fig = plot_doughnut_pie_chart(product_name)
            
            
            
        review = st.text_area(f"Leave a Review for {product_name}")
        submit_button = st.button(f"Submit Review for {product_name}")
        if submit_button and review:
    
            sentiment = predict_sentiment(review)
            if sentiment == 1:
                st.image('images/negative.PNG', caption='Negative Sentiment', width=100)
            elif sentiment == 2:
                st.image('images/neutral.PNG', caption='Neutral Sentiment', width=100)
            elif sentiment == 3:
                st.image('images/positive.PNG', caption='Positive Sentiment', width=100)
            update_csv(product_name, sentiment)

if __name__ == '__main__':
    main()

