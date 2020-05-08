import sys
import pytz
import praw
import time
import requests
import webbrowser
from pypresence import Presence

def drp():
    print("Connecting to Discord for Rich Presence...\n")

    try:
      client_id = "694286426338099250"
      RPC = Presence(client_id)
      RPC.connect()
      RPC.update(state="Setting up RPAN stream...", large_image="icon", large_text="Made by u/IOnlyPlayAsDrif", start=int(time.time()))
    except:
      print("Failed to connect to Discord, restart the program or try again later to get Rich Presence!")

def discordinit():
    while True:
        try:
            drpask = input("Would you like to enable Discord Rich Presence?\nIf you say yes, your stream link and title will be put in your Discord status for everyone that looks at it to see!\n")
            drpasklower = drpask.lower()
            if drpasklower == "yes":
                print("")
                drp()
            else:
                if drpasklower == "no":
                    print("")
                    break
                print("")
                print("Please input a valid answer.\n")
                continue
        except:
            print("")
            print("Please input a valid answer.\n")

def info():
    print("Welcome to Snookey2 v3.1 made by u/Spikeedoo and modified by u/IOnlyPlayAsDrif!\n")
    print("Snookey2 is now a downloadable Python Module thanks to mingo to make streaming on RPAN more easier!")
    print("There is also a new video tutorial if you need help using Snookey2 v3.0! Just type 'tutorial' into the prompt!")
    print("Remember to follow the Reddit TOS and Broadcasting Guidelines here: https://www.redditinc.com/policies/broadcasting-content-policy\n")
    print("The app icon is the official logo to RPAN so credit to Reddit for the logo.\n")
    print("Join the RPAN Discord Server if you need help with Snookey2, or just want to chat with other streamers/viewers!\nhttps://discord.gg/NDfcVkP\n")

def sublist():
    print("")
    print("Here's the list of subreddits for you:")
    print("PAN - The OG subreddit for all livestreams on Wednesday's from Midnight to 5PM PST!")
    url = "https://pastebin.com/raw/rgsZYPkC"
    r = requests.get(url)
    content = r.text
    Dict = eval(content)
    for key,val in Dict.items():
        print("")
        print(key + " - " + val)
    print("The list and database get updated whenever they add new subreddits and I have the time to add them.")

def tutorial():
    webbrowser.open("https://www.youtube.com/watch?v=Oi54fiFOoCI&t=2s", new=0)

def discord():
    webbrowser.open("https://discord.gg/NDfcVkP", new=0)

def chat(subreddit, streamid):
    reddit = praw.Reddit(client_id='yk_0akSBTjExEA',
                     client_secret='DsBcBc6uTez8nHj3_DSf9FET-yY',
                     user_agent='RPAN Plays Pokemon Classic v1')

    subreddit = reddit.subreddit(subreddit)

    print("Connecting to stream chat...")
    print("Note: Emojis may not render properly, and that's something I can't fix.")
    print("If no chat messages pop up in here, and there's chat messages being sent that means you made a mistake in the command. Please try again.")

    for comment in subreddit.stream.comments(skip_existing=True, pause_after=0):
        if comment is None:
            continue
        if comment.parent() == streamid:
            try:
                print(30*"_")
                print(comment.author)
                print(comment.body)
            except:
                pass

def init(subreddit, title):
    print("Subreddit selected is " + subreddit + ".")
    print("The title of the stream will be " + title + ".\n")
    # 'Reddit for Android' Client ID

    client_id = "ohXpoqrZYub1kg"
    response_type = "token"
    scope = "*"
    callback = "http://localhost:65010/callback"
    state = "SNOOKEY"
    request_url = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s" % (client_id, response_type, callback, scope, state)

    #Open browser to get access token
    webbrowser.open(request_url, new=0)

    #Get user input
    print("The access code can be found after you click Accept and in the URL after it's done loading after the part that says access_token, but DON'T include the = or &.\n")
    while True:
      try:
        user_token = input("Please enter your access token:\nType tutorial for a video tutorial on how to use Snookey!\nType reopen in the field to reopen the webpage if you closed it/didn't load up.\nType discord in the prompt to join the Unoffical RPAN Server for chatting with other streamers and Snookey2 support/bug reports/suggestions!\n")
        options = user_token.lower()
        if options == "tutorial":
          print("")
          webbrowser.open("https://www.youtube.com/watch?v=Oi54fiFOoCI&t=2s", new=0)
          continue
        elif options == "reopen":
          print("")
          webbrowser.open(request_url, new=0)
          continue
        elif options == "discord":
            print("")
            webbrowser.open("https://discord.gg/NDfcVkP", new=0)
            continue
        elif len(user_token) < 40:
          if len(user_token) < 36:
            print("")
            ays = input("This access token is in a different format, or you copy and pasted it wrong.\nAre you sure this is correct? Type yes or no to answer:\n")
            if ays.lower() == "yes":
              print("")
              break
            if ays.lower() == "no":
              print("")
              continue
            else:
              print("")
              print("Invalid response inputted. Please try again.")
              print("")
              continue
          else:
            break
        elif user_token[0:8].isdigit() is False:
          if user_token[0:12].isdigit() is False:
            print("")
            ays = input("This access token is in a different format, or you copy and pasted it wrong.\nAre you sure this is correct? Type yes or no to answer:\n")
            if ays.lower() == "yes":
              break
            if ays.lower() == "no":
              print("")
              continue
            else:
              print("")
              print("Invalid response inputted. Please try again.")
              print("")
              continue
          else:
            break
      except:
        print("Unexpected error occured, closing program in 10 seconds...")
        time.sleep(10)
        sys.exit()
      else:
        break
      
    full_token = "Bearer " + user_token

    print("")
    subset = subreddit.lower()
        
    if subset == "thegamerlounge":
        while True:
            try:
                print("")
                assure = input("This program is not meant to be used to just do random gaming streams, please use this program for things that are worth the limited spots.\nDO NOT do a boring regular gaming stream.\nIf you're going to do a gaming stream, make sure it has something interesting and fun to it.\nIf you want to do just a normal gaming stream and there's already a bunch of other people doing a normal gaming stream on RPAN, please wait until they're done so RPAN isn't flooded with gaming streams.\n\nType yes if you read the whole thing and understand.\n")
                assset = assure.lower()
                if assset == "yes":
                    break
              
            except:
              print("Please type yes or no into the prompt.")
              continue
            else:
              if assset == "no":
                sys.exit()
              print("Please type yes or no into the prompt.")
              continue

    url = "https://pastebin.com/raw/6D92xhca"
    r = requests.get(url)
    content = r.text
    while True:
        if subset not in str([content]):
            print("")
            subnotfound = input("The subreddit you just typed in couldn't be found in this script's database.\nType yes to move on with " + subreddit + " or type no if you made a mistake.\n")
            snf = subnotfound.lower()
            if snf == "yes":
                print("")
                break
            if snf == "no":
                print("")
                continue
            else:
                print("")
                print("Invalid response. Please try again.")
                continue
          
        else:
            if subset == "pan":
                print("")
                print("RPAN is available on Wednesdays from 1AM-5PM PST (times might change).\nPlease keep this in mind.\n")
                break
            else:
                print("")
                break

    broadcast_endpoint = "https://strapi.reddit.com/r/%s/broadcasts?title=%s" % (subreddit, title)

    payload = {}
    headers = {
      'User-Agent': 'Project SnooKey/0.1',
      'Authorization': full_token
    }

    count = 0

    # Request broadcast slot
    print("Going to start attempting to start up a stream right now...\n")
    while True:
      token_req = requests.request("POST", url=broadcast_endpoint, headers=headers, data=payload)

      if token_req.status_code == 200:
        # Success!  Stream prepped
        response = token_req.json()
        try:
          RPC.update(state="Streaming " + title + " on r/" + subset + "!", details=response["data"]["post"]["outboundLink"]["url"], large_image="icon", large_text="Made by u/IOnlyPlayAsDrif")
        except:
          pass
        print("")
        print("Server Link: rtmp://ingest.redd.it/inbound/")
        print("Your Stream Key: " + response["data"]["streamer_key"])
        print("DON'T share your Stream Key with anyone.")
        print("You can put these into your OBS Settings by going to the Stream section of the settings and switching Service to Custom...")
        print("YOU ARE LIVE: " + response["data"]["post"]["outboundLink"]["url"])
        print("\nThis program will close in about an hour.\n")
        time.sleep(180)
        try:
            RPC.update(state="Streaming on r/" + subset + " on RPAN!", details=response["data"]["post"]["outboundLink"]["url"], large_image="icon", large_text="Made by u/IOnlyPlayAsDrif", start=int(time.time()))
        except:
            pass
        time.sleep(3600)
        sys.exit()

      
      else:
        # Failed
        if count == 0:
          try:
            RPC.update(state="Trying to stream on RPAN...", details="Attempting to stream to r/" + subset + "...", start=int(time.time()), large_image="icon", large_text="Made by u/IOnlyPlayAsDrif")
            count += 1
          except:
            pass
        print("")
        print("Stream failed to connect! Trying again in 2 seconds...")
        try:
          print("Error message: " + token_req.json()["status"])
          time.sleep(2)
        except:
          print("Error message: Invalid subreddit/access code/broadcast title.\nPlease restart the program and try again.\nThis program will automatically close in 10 seconds.")
          time.sleep(10)
          sys.exit()

    # Fix to prevent windows .exe from closing on completion
    #print("")
    #aainput("Press enter to exit...")

def check_args():
 
    if len(sys.argv) <= 1:
        info()
        #show something here when the user gives no arguments
        return
        
    arg_names = ['filename', 'command', 'var1', 'var2']
    args = dict(zip(arg_names, sys.argv))
    
    if args['command'] == 'stream':
        if 'var2' not in args.keys():
            print('Error. Proper command format: snookey stream subreddit title')
            return
        subreddit = args['var1']
        title = args['var2']
        #check if subreddit exists here or on top of init
        discordinit()
        init(subreddit, title)
        return
    if args['command'] == 'chat':
        if 'var2' not in args.keys():
            print('Error. Proper command format: snookey chat subreddit streamid')
            return
        subreddit = args['var1']
        streamid = args['var2']
        chat(subreddit, streamid)
        return
    if args['command'] == 'commands':
        print("The Snookey2 Help Center")
        print("Join the Discord for any support problems! https://discord.gg/efS4KJM")
        print("")
        print("List of currently available commands:")
        print("(include the quotation marks in the command if specified)")
        print("snookey info")
        print("snookey commands")
        print('snookey chat subreddit streamid')
        print('snookey stream subreddit "title"')
        print("")
        print("The Stream ID is the 6 characters after the last / in the URL.")
        return
    if args['command'] == 'info':
        info()
        return

def main():
    check_args()
