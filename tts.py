from quart import Quart, render_template, request
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
from pathlib import Path
import warnings
import string
warnings.filterwarnings("ignore", category =DeprecationWarning)
from playsound import playsound

# Initialize OpenAI client
from openai import OpenAI
client = OpenAI()
import requests
from pynytimes import NYTAPI
import json
import pprint
import datetime
import _strptime


nyt = NYTAPI("fmfYUaDCYD6c1ND4mp9W1G2SZNAzESJF", parse_dates=True)

def strip_punctuation_from_list(text_list):

    punctuation_set = set(string.punctuation)
    stripped_list = [''.join(char for char in text if char not in punctuation_set) for text in text_list]
    return stripped_list

articles = nyt.top_stories()
#print(articles)
article_list = []
n = 10
articles = articles[:n]
for item in articles:
    article_list.append(item['title'])
    cleaned_list = strip_punctuation_from_list(article_list)
    json_string = json.dumps(cleaned_list)

   # print(json_string)
speech_file_path = Path(__file__).parent / "speech.mp3"
#print(speech_file_path)
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input=json_string
)
response.stream_to_file(speech_file_path)
playsound('speech.mp3')
