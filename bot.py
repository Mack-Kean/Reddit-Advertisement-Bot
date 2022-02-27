import praw
from praw.models import InlineGif, InlineImage, InlineVideo
import feedparser
import json

CLIENT_ID = 'pm25UeetuPduMhmHDgfocQ'
SECRET_KEY = '-kHk4dAxWCAkfrbpM1Mz8EZ1qlZRBw'

#open json confif file
f = open('config.json')
data = json.load(f)

reddit = praw.Reddit(
    client_id=data['client_id'],
    client_secret=data['client_secret_key'],
    user_agent=data['user_agent'],
    username=data['username'],
    password=data['password']
)

reddit.validate_on_submit = True

RSSfeed = feedparser.parse('https://anchor.fm/s/82415e74/podcast/rss')
newestEpisode = RSSfeed.entries[0] #this will always be the most recent entry in the feed

# the next 4 lines take away the html tags (will eventually be changed to anything between <>)
neatSummaryText = newestEpisode.summary
neatSummaryText = neatSummaryText.replace('<p>', '')
neatSummaryText = neatSummaryText.replace('</p>', '')
neatSummaryText = neatSummaryText.replace('<br />', '')

#put together the contents of the post
image = InlineImage('LOGO-04new.jpg', '')
selftext =  '{image1}' \
+ neatSummaryText \
+ '\n\n# Find us here: \n\n' \
+ '### **Anchor.fm:** https://anchor.fm/manswithopinions/episodes/Mans-With-Opinions-V2-3-e1e11lj \n\n' \
+ '### **Spotify:** https://open.spotify.com/show/2QttwoLNUprOBZaazsJJ7U \n\n' \
+ '### **Google Podcasts:** https://podcasts.google.com/feed/aHR0cHM6Ly9hbmNob3IuZm0vcy84MjQxNWU3NC9wb2RjYXN0L3Jzcw \n\n' \
+ '### **Apple Podcasts:** https://podcasts.apple.com/us/podcast/mans-with-opinions/id1608806064 \n\n' \
+ '### **Youtube:** https://www.youtube.com/watch?v=MB0f4uR-yZ4&t=16s \n\n'

media = {"image1": image}

#this is where the magic happens
for sub in data['subreddits']:
    reddit.subreddit('test').submit(newestEpisode.title, selftext=selftext, inline_media=media)
