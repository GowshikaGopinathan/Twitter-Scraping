# Twitter-Scraping
Scrape the twitter data and store that in the database and allow the user to download the data with multiple data formats.


streamlit is the library used to create the web app.
pandas is used to handle the data in a tabular format.
snscrape is used to scrape data from Twitter.
pymongo is used to connect and interact with the MongoDB database.
openpyxl is used to write data to Excel.
PIL is used to work with images.
certifi is used to get the location of the SSL certificates.
io is used to handle input/output.

**scrape_tweets** is a function that scrapes tweets based on the **search query and limit.**
It first creates an empty list to hold the tweets.
Then, it iterates through the search results and adds the tweets to the list.
Once all the tweets have been added or the limit has been reached, it creates a Pandas DataFrame from the list of tweets and returns it.

**connect_to_mongodb** is a function that connects to the MongoDB database and returns the collection.

**store_tweets_in_mongodb** is a function that stores the tweets in the MongoDB collection.
It first converts the Pandas DataFrame to a list of dictionaries.
Then, it inserts the tweets into the collection and returns the inserted ids.

--------------------------------------------------------------------------------

st.title('Twitter Scraper')

st.write('Enter a search query and the number of tweets to scrape.')

image = Image.open('Twitter.png')

st.image(image,caption="Twitter Scraping")

st.subheader('''Twitter Data''')

This section creates the **Streamlit app** and displays the title, description, and an image.

--------------------------------------------------------------------------------------------------------------

search_query = st.text_input('Search Query')

limit= st.number_input('Number of Tweets', min_value=1, max_value=1000)


These two lines get the search query and number of tweets from the user using Stream
