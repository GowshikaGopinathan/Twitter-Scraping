import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
import pymongo
import openpyxl 
from PIL import Image
import certifi
ca = certifi.where()
import io

# Function to scrape tweets
def scrape_tweets(search_query, limit):
    # Create a list to hold the tweets
    tweets_list = []

    # Iterate through the search results and add them to the list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        if i >= limit:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content,
                     tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source,
                      tweet.likeCount])

    # Create a Pandas DataFrame from the list of tweets
    tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'ID', 'URL','Content',
                                                   'Username','Replycount','Retweetcount','Language','Source',
                                                   'Likecount',])

    return tweets_df

# Function to connect to MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb url", tlsCAFile=ca)
    db = client["tweets"]
    collection = db["twitter_data"]
    return collection

# Function to store tweets in MongoDB
def store_tweets_in_mongodb(tweets_df, collection):
    # Convert the Pandas DataFrame to a list of dictionaries
    tweets_dict = tweets_df.to_dict('records')

    # Insert the tweets into MongoDB
    result = collection.insert_many(tweets_dict)

    return result.inserted_ids

# Create the Streamlit app
st.title('Twitter Scraper')
st.write('Enter a search query and the number of tweets to scrape.')
image = Image.open('Twitter.png')
st.image(image,caption="Twitter Scraping")
st.subheader('''Twitter Data''')

# Get the search query and number of tweets from the user
search_query = st.text_input('Search Query')
limit= st.number_input('Number of Tweets', min_value=1, max_value=1000)

# Scrape the tweets and display them in a table
if st.button('Submit'):
    # Call the scrape_tweets function and display the results
    tweets_df = scrape_tweets(search_query, limit)
    st.write(tweets_df)
 # Connect to MongoDB
    collection = connect_to_mongodb()
# Store the tweets in MongoDB
    result = store_tweets_in_mongodb(tweets_df, collection)
    st.write(f"{len(result)} tweets were successfully stored in MongoDB.")
    st.download_button("Download CSV", tweets_df.to_csv(index=False), "tweets.csv", "text/csv")
    st.download_button("Download JSON", tweets_df.to_json(indent=4), "tweets.json", "application/json")
# Convert the datetime column to timezone-unaware
    tweets_df["Date"] = tweets_df["Date"].dt.tz_localize(None)

    excel_file = io.BytesIO()
    tweets_df.to_excel(excel_file, index=False)
    st.download_button(label="Download Excel", data=excel_file.getvalue(), file_name="tweets.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



