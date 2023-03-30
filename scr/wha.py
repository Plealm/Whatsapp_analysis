import string
from matplotlib.patches import Patch
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import emoji
from collections import Counter


def w_df(path):
    """
    Converts a WhatsApp chat log file to a pandas DataFrame.

    Args:
        path (str): The file path of the WhatsApp chat log.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the chat log data.
    """

    # Read in the WhatsApp text file as a pandas DataFrame
    df = pd.read_csv(path, header=None, names=[
                     'DateTime', 'Message'], sep=' - ', engine='python')

    # Convert the Date/Time string to datetime format
    df['DateTime'] = pd.to_datetime(
        df['DateTime'], format='%m/%d/%y, %H:%M', errors='coerce')

    # Drop any rows with invalid dates/times
    df = df.dropna()

    # Split the Message column into the Name and Message columns
    df[['Name', 'Message']] = df['Message'].str.split(': ', n=1, expand=True)

    # Replace any missing values in the Message column with an empty string
    df['Message'] = df['Message'].fillna('')

    # Filter out rows containing '<Media omitted>' in the Message column
    df = df[~df['Message'].str.contains('<Media omitted>')]

    df['DayOfWeek'] = df['DateTime'].dt.dayofweek

    df['Season'] = pd.cut(df['DateTime'].dt.month, bins=[0, 2, 5, 8, 11, 12], labels=[
                          'Winter', 'Spring', 'Summer', 'Fall', 'Winter'], ordered=False)

    df['HourOfDay'] = df['DateTime'].dt.hour

    df = df.iloc[1:, :]
    # Reset the index of the DataFrame
    df = df.reset_index(drop=True)

    # Return the DataFrame
    return df


def daily_messages(df, colors=None):
    """
    Given a pandas DataFrame with columns 'DateTime' and 'Message', plots the daily amount of messages in the chat history
    using different colors for each season.

    Parameters:
        - df (pandas DataFrame): The DataFrame with the WhatsApp chat history.
        - colors (dict, optional): A dictionary of colors to use for each season. If None, default colors will be used.

    """

    # Group by date and season to get the daily message counts for each season
    daily_counts = df.groupby([df['DateTime'].dt.date, 'Season']).count()[
        'Message'].unstack()

    # Define a default color palette for each season
    default_colors = {'Winter': 'tab:blue', 'Spring': 'tab:green',
                      'Summer': 'tab:orange', 'Fall': 'tab:red'}

    # Update the default color palette with the user-specified colors
    colors = {**default_colors, **(colors or {})}

    # Plot the daily message counts for each season using a stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_counts.plot(kind='bar', stacked=True, ax=ax, color=colors)
    ax.set_title('Daily Message Counts by Season')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Messages')

    # Format the x-axis tick labels
    month_year_list = [date.strftime('%B %Y') for date in daily_counts.index]
    ax.set_xticks(range(len(month_year_list)))
    ax.set_xticklabels(month_year_list, rotation=0)
    xticklabels = ax.get_xticklabels()
    for i, label in enumerate(xticklabels):
        if i % 45 != 0:
            label.set_visible(False)
    plt.savefig("../images/daily.jpg")
    plt.show()


def weekly_messages(df, colors=None):
    """
    Plot the weekly message counts for each season using a stacked bar chart.

    Args:
    - df: A pandas DataFrame with a 'DateTime' column and a 'Message' column.
    - colors: A dictionary of colors to use for each season. If not provided, the default colors will be used.

    Returns: None
    """

    # Group by day of the week and season to get the message counts for each season
    dayofweek_counts = df.groupby(['DayOfWeek', 'Season']).count()[
        'Message'].unstack()

    # Define the default colors for each season
    default_colors = {'Winter': 'tab:blue', 'Spring': 'tab:green',
                      'Summer': 'tab:orange', 'Fall': 'tab:red'}

    # Merge the default colors with any user-provided colors
    colors = {**default_colors, **(colors or {})}

    # Plot the daily message counts for each season using a stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    dayofweek_counts.plot(kind='barh', stacked=True,
                          ax=ax, color=colors, width=0.75)

    # Set the title and axis labels
    ax.set_title('Message Counts by Day of the Week and Season')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Messages')

    # Format the x-axis tick labels
    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_yticks(range(len(days)))
    ax.set_yticklabels(days, rotation=0)

    # Show the plot
    plt.show()


def plot_emojis(df):
    # Group the DataFrame by name and count the frequency of each emoji
    emoji_count_dict = {}
    for name, group in df.groupby('Name'):
        emoji_list = group['Message'].apply(
            lambda x: [d['emoji'] for d in emoji.emoji_list(x)])
        emoji_count = Counter(
            [emoji for emojis in emoji_list for emoji in emojis])
        top_10_emoji = dict(emoji_count.most_common(10))
        emoji_count_dict[name] = top_10_emoji

    # Define colors for each bar in the plot
    colors = ['rgb(255, 102, 102)', 'rgb(102, 178, 255)', 'rgb(102, 255, 178)',
              'rgb(255, 178, 102)', 'rgb(178, 102, 255)', 'rgb(178, 255, 102)',
              'rgb(255, 255, 102)', 'rgb(255, 102, 255)', 'rgb(102, 255, 255)',
              'rgb(255, 178, 255)']

    # Create a separate plot for each name in the DataFrame
    for i, (name, emoji_count) in enumerate(emoji_count_dict.items()):
        fig = go.Figure(data=[go.Bar(x=list(emoji_count.keys()),
                                     y=list(emoji_count.values()),
                                     marker=dict(color=colors))])
        fig.update_layout(title=f'Top 10 Most Used Emojis - {name}',
                          xaxis_title='Emoji',
                          yaxis_title='Frequency')
        fig.update_xaxes(visible=False)

        # Update marker to add emoji over the bar and increase size
        for j in range(len(fig.data[0].x)):
            emoji_char = fig.data[0].x[j]
            fig.add_annotation(x=emoji_char,
                               # adjust height of annotation
                               y=fig.data[0].y[j]+10,
                               text=emoji_char,
                               font=dict(size=20),  # increase size of emoji
                               showarrow=False,
                               yanchor='bottom')
        fig.write_image(f"../images/{name}-count_emoji.jpg")
        fig.show()


def plot_messages(df):
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = {'Winter': 'tab:blue', 'Spring': 'tab:green',
              'Summer': 'tab:orange', 'Fall': 'tab:red'}

    fig, axs = plt.subplots(1, 7, figsize=(16, 6), sharey=True)

    for i, day in enumerate(weekdays):
        df_day = df[df['DayOfWeek'] == i]
        grouped = df_day.groupby(['HourOfDay', 'Season'])[
            'Message'].count().unstack()
        ax = grouped.plot(kind='bar', stacked=True, ax=axs[i], color=[
                          colors[c] for c in grouped.columns], legend=None)
        ax.set_xticks([0, 5, 12, 20])
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Message Count')
        ax.set_title(day)

    # Crear leyenda
    handles = [Patch(facecolor=colors[c], label=c) for c in colors]
    fig.legend(handles=handles, ncol=4)

    plt.suptitle(
        '  ', fontsize=16)
    plt.tight_layout()
    plt.savefig('../images/Mes_Hour_Season.png')
    plt.show()


def plot_top_words(df):
    # Define a color map with a unique color for each name
    cmap = plt.get_cmap('tab10')
    colors = {name: cmap(i) for i, name in enumerate(df['Name'].unique())}

    stop_words_es = [
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por',
        'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero',
        'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando',
        'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien',
        'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra',
        'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos',
        'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos',
        'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas',
        'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas',
        'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo',
        'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra',
        'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos',
        'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés',
        'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos',
        'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais',
        'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve',
        'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera',
        'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese',
        'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado',
        'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis',
        'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá',
        'habremos', "es", "sea", "fue", "pues", "si", "meno", "cómo", "bien",
        "solo", "igual", "bueno", "así", "mejor", "ahí", "bien", "cosas", "sé", "vez", "tan", "vas"]

    for name in df['Name'].unique():
        # Filter DataFrame by name
        df_name = df[df['Name'] == name]

        # Join all messages into one string
        messages = ' '.join(df_name['Message'].tolist())

        # Remove emojis
        messages = emoji.replace_emoji(messages, replace='')

        # Remove punctuation symbols
        messages = messages.translate(
            str.maketrans('', '', string.punctuation))

        # Split string into words and count frequency
        word_counts = Counter(word.lower() for word in messages.split() if not word.lower().startswith(
            'jaj') and not word.lower().startswith('jej') and word.lower() not in stop_words_es
            and not word.isdigit() and len(word) >= 4)

        # Get top 10 words and their counts
        top_words = word_counts.most_common(10)
        top_words.reverse()
        words = [word[0] for word in top_words]
        counts = [word[1] for word in top_words]

        # Create line plot
        fig, ax = plt.subplots(figsize=(8, 6))
        for i in range(len(words)):
            # Use a unique color for each name
            color = colors[name]

            # Plot dot and hline with the same color
            ax.plot(counts[i], words[i], 'o', markersize=8, color=color)
            ax.hlines(words[i], 0, counts[i], linewidth=1, color=color)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Words')
        ax.set_title(f'Top 10 words used by {name}')
        plt.savefig(f"../images/{name}-word_count.jpg")
        plt.show()


def plot_lexicon(df):
    # Create a dictionary to store the number of unique words for each name
    unique_words = {}

    # Loop through each unique name and count the number of unique words
    for name in df['Name'].unique():
        # Filter DataFrame by name
        df_name = df[df['Name'] == name]

        # Join all messages into one string
        messages = ' '.join(df_name['Message'].tolist())

        # Split string into words and count unique words
        unique_words[name] = len(set(word.lower()
                                 for word in messages.split()))

    # Sort dictionary by value in descending order
    sorted_unique_words = dict(
        sorted(unique_words.items(), key=lambda item: item[1], reverse=True))

    # Create bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(list(sorted_unique_words.keys()), list(
        sorted_unique_words.values()), color=plt.cm.tab20(range(len(sorted_unique_words))))
    ax.set_xlabel('Number of Unique Words')
    ax.set_ylabel('Name')
    ax.set_title('Number of Unique Words per Name')
    plt.savefig(f"../images/lexicon.jpg")
    plt.show()


df = w_df('../data/WhatsApp.txt')
# plot_messages(df)
# daily_messages(df)
# weekly_messages(df)
# plot_emojis(df)
# plot_lexicon(df)
plot_top_words(df)
