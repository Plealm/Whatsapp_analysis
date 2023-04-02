# Whatsapp_analysis

This project involved conducting a unique conversation with an individual (referred to as 'Unknow'). Through the use of algorithms created in Python, we were able to perform tasks such as data cleaning, organization, visualization, and sentiment analysis using NLP methods (specifically Roberta) for emojis.

## Message distribution by time
The first graph demonstrates the number of daily messages over the recorded period, separated by season.

<img src="https://user-images.githubusercontent.com/84750731/229315497-51574c3b-c4d2-46ee-a7bf-d44b4010eb55.jpg" width="700" height="400" />

The second image is a horizontal bar plot displaying the quantity of messages per day of the week and the corresponding contribution from each season.

<img src="https://user-images.githubusercontent.com/84750731/229315496-520579f7-7869-43f2-b66b-297aa495f0fb.jpg" width="700" height="400" />

To conclude the visualization of message quantity, we observe the message frequency per hour, per day of the week, and the respective contribution from each season of the year.

![Mes_Hour_Season](https://user-images.githubusercontent.com/84750731/229315492-ccb55f20-bbf1-4ac7-97c9-e54e4f5d06a5.png)

## Insights about the conversation

Some of the insights discovered through the analysis are presented below: 

Starting with the 10 most frequently used words (in Spanish) for each user

<p float="left">
  <img src="https://user-images.githubusercontent.com/84750731/229315490-76f6e3b7-c96d-4af5-be3d-bb800b8c8f7b.jpg" width="500" height="400" />
  <img src="https://user-images.githubusercontent.com/84750731/229315491-677e3226-bb5a-4021-a8fa-69e511ffc074.jpg" width="500" height="400" />
</p>

Followed by the top 10 emojis used by each person

<p float="left">
  <img src="https://user-images.githubusercontent.com/84750731/229315493-4a2ddaed-1193-42dc-8d3c-c10d0bd7192b.jpg" width="500" height="400" />
  <img src="https://user-images.githubusercontent.com/84750731/229315495-c2d21989-feeb-46f3-ba95-313cdcbad399.jpg" width="500" height="400" />
</p>

and identifying the person with the best vocabulary, determined by the number of unique words written in the chat.

 <img src="https://user-images.githubusercontent.com/84750731/229315489-19cf6a73-9df4-48c5-92bf-945370ca9110.jpg" width="600" height="400" />

## Sentiment Analysis

Finally, an algorithm was developed to analyze the emotions demonstrated by emojis using the [Roberta](https://huggingface.co/docs/transformers/model_doc/roberta) model. This model classifies the probability that the respective emoji expresses a negative, neutral, or positive sentiment into three categories, with their sum equaling one. However, it has been observed that this model encounters difficulties in providing accurate results for newer emojis.

<p float="left">
  <img src="https://user-images.githubusercontent.com/84750731/229315486-e83e9f20-3ba3-4db9-a81d-e5d1fdae4ff3.jpg" width="500" height="400" />
  <img src="https://user-images.githubusercontent.com/84750731/229315488-7a3f6824-a118-49d5-8058-aa83e7c687f6.jpg" width="500" height="400" />
</p>



