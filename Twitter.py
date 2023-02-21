

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
    client = pymongo.MongoClient("mongodb+srv://Gowshika:12345@cluster0.dkj1do3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
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
    # st.download_button("Download Excel",tweets_df.to_excel("tweets.xlsx",index=False), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

#     # st.header("Download tweets")
#     # format = st.selectbox("Select a format", [ "JSON","CSV", "Excel"])
#     # download_tweets(tweets_df, format)



# if st.button("Download"):
#     format = st.selectbox("Select a format", ["CSV", "Excel", "JSON"])
#     if format:
#         if format == "CSV":
#             # download the tweets as a CSV file
#             csv = tweets_df.to_csv(index=False)
#             st.download_button(label="Download CSV", data=csv, file_name="tweets.csv", mime="text/csv")
#         elif format == "Excel":
#             # download the tweets as an Excel file
#             excel = tweets_df.to_excel(index=False, sheet_name="Tweets")
#             st.download_button(label="Download Excel", data=excel, file_name="tweets.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#         elif format == "JSON":
#             # download the tweets as a JSON file
#             json = tweets_df.to_json(orient="records")
#             st.download_button(label="Download JSON", data=json, file_name="tweets.json", mime="application/json")
#     else:
#         st.error("Please select a format to download the tweets.")
#




#
#
#
#
#
#
#
# # # Create a dropdown menu to download the tweets in different formats
# if tweets_df in locals():
#     st.header("Download tweets")
#     format = st.sidebar.selectbox("Select a format", [ "JSON","CSV", "Excel", "JSON"])
#     download_tweets(tweets_df, format)


# if st.button("Submit"):
#     # Call the scrape_tweets function and display the results
#     tweets_df = scrape_tweets(search_query, limit)
#     st.write(tweets_df)
#
#     # Connect to MongoDB
#     collection = connect_to_mongodb()
#
#     # Store the tweets in MongoDB
#     result = store_tweets_in_mongodb(tweets_df, collection)
#     st.write(f"{len(result)} tweets were successfully stored in MongoDB.")
#
#     # Download the tweets in different formats
#     st.header("Download tweets")
#     format = st.selectbox("Select a format", [" ","CSV", "Excel", "JSON"])
#     if format:
#        download_tweets(tweets_df, format)

# --------------------------------------------------------------------------------------------


# # Create a sidebar with input fields for the query and limit
# st.sidebar.header("Search parameters")
# query = st.sidebar.text_input("Enter a Twitter search query")
# limit = st.sidebar.number_input("Enter the maximum number of tweets to scrape", value=100, step=5)
#
#
# if st.sidebar.button("Submit"):
#     # Call the scrape_tweets function and display the results
#     tweets_df = scrape_tweets(query, limit)
#     st.write(tweets_df)
#
#     # Connect to MongoDB
#     collection = connect_to_mongodb()
#
#     # Store the tweets in MongoDB
#     result = store_tweets_in_mongodb(tweets_df, collection)
#     st.write(f"{len(result)} tweets were successfully stored in MongoDB.")
#
# # Create a dropdown menu to download the tweets in different formats
# # if tweets_df is not None:
#     st.sidebar.header("Download tweets")
#     format = st.sidebar.selectbox("Select a format", [ "JSON","CSV", "Excel", "JSON"])
#     download_tweets(tweets_df, format)


# # Function to download tweets in different formats
# def download_tweets(tweets_df, format):
#     if format == "CSV":
#         st.download_button("Download CSV", tweets_df.to_csv(index=False), "tweets.csv", "text/csv")
#     elif format == "Excel":
#         st.download_button("Download Excel", tweets_df.to_excel(index=False), "tweets.xlsx",
#                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     elif format == "JSON":
#         st.download_button("Download JSON", tweets_df.to_json(indent=4), "tweets.json", "application/json")

