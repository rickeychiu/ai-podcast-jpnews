from dotenv import load_dotenv
import os 
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import feedparser

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

newsFeed = "https://www.japantimes.co.jp/feed/"

print("## Processing RSS Feed ##")

feed = feedparser.parse(newsFeed)
stories = ""
storiesLimit = 10

for item in feed.entries[:storiesLimit]:
    stories = stories + " New Story: " + item.title + ". " + item.description

print("## Processing ChatGPT")

chatOutput = client.chat.completions.create(model = "gpt-3.5-turbo",
messages = [{
    "role": "user",
    "content": "Please rewrite the following news headlines and summaries in a discussion way, as though someone is talking about them one by one on a one-off podcast in a non-judgmental way and with no follow-on discussion, although there should be a final closing greeting: " + stories
}])

chatContent = chatOutput.choices[0].message.content

print(chatContent)