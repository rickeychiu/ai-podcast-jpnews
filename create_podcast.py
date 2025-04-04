from dotenv import load_dotenv
import os 
from openai import OpenAI
import json
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import feedparser

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

newsFeed = "https://www.nippon.com/en/feed/"

print("## Processing RSS Feed ##")

feed = feedparser.parse(newsFeed)
stories = ""
storiesLimit = 10

for item in feed.entries[:storiesLimit]:
    stories = stories + " New Story: " + item.title + ". " + item.description

print("## Processing ChatGPT ##")

chatOutput = client.chat.completions.create(model = "gpt-3.5-turbo",
messages = [{
    "role": "user",
    "content": "Please rewrite the following news headlines and summaries in a discussion way, then add some context on each of them. Make sure to say it as though someone is talking about them one by one on a one-off podcast in a non-judgmental way and with no follow-on discussion, although there should be a final closing greeting. Please add more content or context when possible to make each talking article a few sentences long: " + stories
}])

chatContent = chatOutput.choices[0].message.content

print(chatContent)

print("## Processing Audio ##")

voiceID = "UgBBYS2sOqTuMpoF3BR0"

audioOutput = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/" + voiceID, 
    data = json.dumps({
        "text": chatContent,
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0
        }
    }),
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key,
        "accept": "audio/mpeg"
    }
)

if audioOutput.status_code == 200:
    # it has worked, do something
    with open("nipponpodcast.mp3", "wb") as output_file:
        output_file.write(audioOutput.content)
else:
    print(audioOutput.text)

print("## Processing complete! ##")