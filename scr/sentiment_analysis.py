from googletrans import Translator
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import plotly.io as pio
from translate import Translator
from google.cloud import translate_v2 as translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib.patches import Patch
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import emoji
from collections import Counter
from wha import df
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.special import softmax


def emoji_analysis(df):
    unique_names = df['Name'].unique()
    for name in unique_names:
        roberta = "cardiffnlp/twitter-roberta-base-sentiment"
        model = AutoModelForSequenceClassification.from_pretrained(roberta)
        tokenizer = AutoTokenizer.from_pretrained(roberta)
        labels = ['Negative', 'Neutral', 'Positive']
        emoji_list = []
        emoji_count_dict = {}
        for message, message_name in zip(df['Message'], df['Name']):
            if message_name == name:
                emoji_list.extend([d['emoji']
                                  for d in emoji.emoji_list(message)])
                emoji_count = Counter(
                    [emoji for emojis in emoji_list for emoji in emojis])
                top_10_emoji = dict(emoji_count.most_common(10))
                emoji_count_dict[name] = top_10_emoji
        emoji_sentiment_dict = {}
        for e in set(emoji_list):
            sentiment_score = tokenizer(e, return_tensors='pt')
            output = model(**sentiment_score)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            emoji_sentiment_dict[e] = {labels[i]: scores[i]
                                       for i in range(len(scores))}

        # Get data for plotting
        data = []
        for e, scores in emoji_sentiment_dict.items():
            data.append({
                'Emoji': e,
                'Negative': scores.get('Negative', 0),
                'Neutral': scores.get('Neutral', 0),
                'Positive': scores.get('Positive', 0)
            })
        data = pd.DataFrame(data)
        total = data[['Negative', 'Neutral', 'Positive']].sum().round(2)
        # Sort data by Positive column
        data1 = data.sort_values(by='Positive', ascending=False).head(10)[::-1]

        # Plot the data
        fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3])

        # First plot
        fig.add_trace(go.Bar(
            x=data1['Negative'], y=data1['Emoji'], name='Negative', orientation='h', marker_color='red',
            showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(
            x=data1['Neutral'], y=data1['Emoji'], name='Neutral', orientation='h', marker_color='yellow',
            showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(
            x=data1['Positive'], y=data1['Emoji'], name='Positive', orientation='h', marker_color='green',
            showlegend=False), row=1, col=1)

        # Second plot
        fig.add_trace(go.Bar(
            y=['Total'], x=[total['Negative']], name='Negative', orientation='h', marker_color='red',
            text=[total['Negative']], textposition='inside'), row=1, col=2)
        fig.add_trace(go.Bar(
            y=['Total'], x=[total['Neutral']], name='Neutral', orientation='h', marker_color='yellow',
            text=[total['Neutral']], textposition='inside'), row=1, col=2)
        fig.add_trace(go.Bar(
            y=['Total'], x=[total['Positive']], name='Positive', orientation='h', marker_color='green',
            text=[total['Positive']], textposition='inside'), row=1, col=2)

        fig.update_xaxes(title_text='Sentiment Score', row=1,
                         col=1, title_font=dict(size=20), tickfont=dict(size=16))

        fig.update_yaxes(title_text='Emoji', row=1, col=1,
                         title_font=dict(size=20), tickfont=dict(size=16))
        fig.update_xaxes(title_text='Sentiment Score', row=1, col=2,
                         title_font=dict(size=20), tickfont=dict(size=16))
        fig.update_layout(title_text=f"Sentiment analysis for {name}", height=600, width=900, title_font=dict(
            size=24), font=dict(size=16))

        fig.update_layout(
            title_text=f"Sentiment analysis for {name}", height=600, width=900)

        fig.write_image(f"../images/{name}-sent_analysis_emoji.jpg")


df1 = df[['Name', 'Message']]
# emoji_analysis(df1)
