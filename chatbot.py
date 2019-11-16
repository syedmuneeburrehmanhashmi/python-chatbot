#Import the random module
import re
import time
import requests
import random
import urllib.request
from bs4 import BeautifulSoup


def weatherFunc(city):
    url="https://www.timeanddate.com/weather/pakistan/{0}"
    url = url.format(city)
    
    data= requests.get(url)
    
    soup = BeautifulSoup(data.text, "html.parser")
    
    data = soup.find('div', {"id":"qlook"})
    degree = data.find('div', {"class":"h2"})
    forecast = data.find('p')
    
    return degree.contents[0], forecast.contents[0]
    

# Define variables
name = "Ava"
curCity = "Karachi"
weather = weatherFunc(curCity)
color = "Blue"

bot_template = "AVA : {0}"
user_template = "USER : {0}"

# Define a dictionary containing a list of responses for each message
responses = {
  "what's your name?": [
      "My name is {0}".format(name),
      "They call me {0}".format(name),
      "I go by {0}".format(name)
   ],
  "what's your favourite color?" : [
      "my favourite color is {0}".format(color)
    ],
  "what's today's weather?" : [
      "the weather is {0} in {1}.".format(weather[1], curCity),
      "it's {0} today, in {1}".format(weather[1], curCity)
    ],
  "default": ["default message"],
  "questions": [
	"you tell me!",
	"Can't catch up on that!",
	"Hello?? Couldn't get that.."
   ],
  "statements": [
	"Oh! That's intersting to hear!",
	"Oh WoW!",
	"WeW!!",
	"I like that!"]
}

# Use random.choice() to choose a matching response
def respond(message):
    if message in responses:
        bot_message = random.choice(responses[message])
        #Check for a question mark
    elif bool(re.search("what\'s the meaning of ", message)) == True:
        search = re.search("what\'s the meaning of ", message)
        start = search.end()
        search1 = re.search("\?", message)
        end = search1.start()
        word = message[start:end]
        bot_message = wordFunc(word)
    elif bool(re.search("what\'s the weather today in ", message)) == True:
        search = re.search("what\'s the weather today in ", message)
        start = search.end()
        search1 = re.search("\?", message)
        end = search1.start()
        city = message[start:end]
        weather = weatherFunc(city)
        bot_message = "The weather today is {0} and {1} in ".format(weather[0],
                                            weather[1][:-1]) + city +'.'
    elif message.endswith('?')==True:
        # Return a random question
        bot_message = random.choice(responses["questions"])
    else:
        #Return a random statement
        bot_message = random.choice(responses["statements"])
    return bot_message


# Define a function that sends a message to the bot: send_message
def send_message(message):
    # Get the bot's response to the message
    response = respond(message)
    # Print the bot template including the bot's response.
    time.sleep(1)
    print(bot_template.format(response))

def wordFunc(word):
    url="https://www.dictionary.com/browse/"
    url= url+word
    
    data= urllib.request.urlopen(url).read()
    data1= data.decode("utf-8")
    
    search1= re.search('meta name="description" content="', data1)
    search2= re.search("See", data1)
    
    start = search1.end()
    end = search2.end()
    end = end-4
    
    meaning= data1[start:end]
    return meaning
    

while True:
    send_message(input("USER: "))
