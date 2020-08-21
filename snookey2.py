import sys
import praw
import time
import random
import requests
import webbrowser
from pypresence import Presence
from http.server import HTTPServer, BaseHTTPRequestHandler

# Constants and Globals
SNOOKEY_VERSION = "3.2"
CHAT_VIEWER_VERSION = "1.0"

# URLs
DONATE_URL = "https://ko-fi.com/snookey2"
SUBLIST_URL = "https://raw.githubusercontent.com/IOnlyPlayAsDrift/Snookey2/master/subreddit-list"
DISCORD_URL = "https://discord.gg/NDfcVkP"
AUTH_URL = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s"
TOKEN_CALLBACK_URL = "http://localhost:65010/callback"

# Discord Rich Presence
DISCORD_CLIENT_ID = "694286426338099250"
rpc = Presence(DISCORD_CLIENT_ID)
rpc_enabled = False

# Chat
CHAT_CLIENT_ID = "yk_0akSBTjExEA"
CHAT_CLIENT_SECRET = "DsBcBc6uTez8nHj3_DSf9FET-yY"
CHAT_USER_AGENT = "Snookey Chat Viewer v{}".format(CHAT_VIEWER_VERSION)

# Getting Stream Key
CLIENT_ID = "ohXpoqrZYub1kg"
RESPONSE_TYPE = "token"
SCOPE = "*"
STATE = "SNOOKEY"
auth_url = AUTH_URL % (CLIENT_ID, RESPONSE_TYPE, TOKEN_CALLBACK_URL, SCOPE, STATE)
auth_token = None  # Not currently used outside of getting stream url, but may be useful to store global ref for future

sublist_dict = None
available_subs = None


def load_sublist():
    # Loads RPAN supported subreddits and their descriptions
    global sublist_dict, available_subs
    try:
        r = requests.get(SUBLIST_URL)
        sublist_dict = eval(r.text)
        available_subs = list(sublist_dict.keys())
    except BaseException as error:
        print("Unexpected error occured: {}".format(error))
        print("Failed to fetch available subreddits. Either list format has changed, or it is currently inaccessible")
        sys.exit(3)


def donate_info():
    # Prints donate info on 1/5 (20%) chance. Prior code executed on a 3/15 chance, which reduces to the same odds.
    if random.random() <= 0.20:
        print(69 * "-")
        print("Like using Snookey2? Donate to the creator to support him!")
        print("Snookey2 was mainly developed by one person in his free time!")
        print('Type "snookey donate" into your command prompt program or copy and paste this link into a web browser: ' + DONATE_URL)
        print("Donating gets you a Donator role in the Discord, Beta Testing for Snookey2 and future projects, a custom thank you message from me, and the removal of this random message.")
        print("Thank you for Snookey2, and sorry to bother you. Have fun streaming!")
        print(69 * "-")


def donate():
    # Opens donation page
    webbrowser.open(DONATE_URL, new=0)
    print("Thank you so much if you end up donating to me :D\n")


def discord_init():
    # Initializes DRP connection
    global rpc, rpc_enabled
    try:
        rpc.connect()
        rpc_enabled = True
    except:
        print("Failed to connect to Discord, restart the program or try again later to get Rich Presence!")
        rpc_enabled = False


def drp(state, large_image="icon", large_text="Made by u/IOnlyPlayAsDrif", start=None, **kwargs):
    # Updates DRP message being displayed
    global rpc, rpc_enabled
    if not rpc_enabled:
        print("Discord Rich Presence has been called before being initialized!")
        return
    try:
        rpc.update(state=state, large_image=large_image, large_text=large_text, start=start, **kwargs)
    except BaseException as error:
        print("Unexpected error occured: {}".format(error))
        print("Unable to update Discord Rich Presence")


def info():
    # Prints information about Snookey2
    print("Welcome to Snookey2 v3.2 created by u/IOnlyPlayAsDrif with the original created by u/Spikeedoo!\n")
    print("Snookey2 is now a downloadable Python Module thanks to mingo to make streaming on RPAN more easier!")
    # print("There is also a new video tutorial if you need help using Snookey2 v3.0! Just type 'tutorial' into the prompt!")
    print("Remember to follow the Reddit TOS and Broadcasting Guidelines here: https://www.redditinc.com/policies/broadcasting-content-policy\n")
    print("The app icon is the official logo to RPAN so credit to Reddit for the logo.\n")
    print("Join the RPAN Discord Server if you need help with Snookey2, or just want to chat with other streamers/viewers!\n{}\n".format(DISCORD_URL))


def commands():
    # Displays available commands with descriptions
    print("The Snookey2 Help Center")
    print("Join the Discord for any support problems! " + DISCORD_URL)
    print()
    print("List of currently available commands:")
    print("(include the quotation marks in the command if specified)")
    print("snookey info - Get info on Snookey2!")
    print("snookey donate - Donate to the Snookey2 developer to support him!")
    print("snookey version - Get the current version of Snookey2 you're on.")
    print("snookey commands - Get a list of commands for Snookey2!")
    print('snookey chat subreddit streamid - Read your stream chat on Snookey2')
    print('snookey stream subreddit "title" - Stream on RPAN on PC using Snookey!')
    print()
    print("The Stream ID is the 6 characters after the last / in the URL.")


def sublist():
    # Display list of RPAN supported subreddits to user
    print()
    print("Here's the list of subreddits for you:")
    print("PAN - The OG subreddit for all livestreams on Wednesday's from Midnight to 5PM PST!")
    for key, val in sublist_dict.items():
        print()
        print(key + " - " + val)
    print("The list and database get updated whenever they add new subreddits and I have the time to add them.")


# def tutorial():
# webbrowser.open("https://www.youtube.com/watch?v=Oi54fiFOoCI&t=2s", new=0)

def discord():
    # Opens RPAN Discord
    webbrowser.open(DISCORD_URL, new=0)


def chat(subreddit, streamid):
    # Retrieves chat messages from stream
    reddit = praw.Reddit(client_id=CHAT_CLIENT_ID, client_secret=CHAT_CLIENT_SECRET, user_agent=CHAT_USER_AGENT)
    subreddit = reddit.subreddit(subreddit)

    print("Connecting to stream chat...")
    print("Note: Emojis may not render properly, and that's something I can't fix.")
    print("If no chat messages pop up in here, and there's chat messages being sent that means you made a mistake in the command. Please try again.")

    for comment in subreddit.stream.comments(skip_existing=True, pause_after=0):
        if comment is None:
            continue
        if comment.parent() == streamid:
            try:
                print(30 * "_")
                print(comment.author)
                print(comment.body)
            except:
                pass


def assert_yn(prompt, invalid_msg="\nPlease select a valid answer (\"yes\" or \"no\")\n"):
    # Shorthand for asking "yes" or "no" questions with input validation
    while True:
        try:
            answer = input(prompt).lower()
            if answer != 'yes' and answer != 'no':
                print(invalid_msg)
            else:
                return True if answer == 'yes' else False
        except KeyboardInterrupt:
            sys.exit()


class Serv(BaseHTTPRequestHandler):
    global user_token
    user_token = ''
    # Get the token from the callback page
    callbackhtml = open('callback.html', 'r').read()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path.startswith('/callback'):
            self.wfile.write(bytes(self.callbackhtml, 'utf-8'))
        if self.path.startswith('/submittoken'):
            self.wfile.write(bytes('<html><body><h1>You may close this tab now.</h1></body></html>', 'utf-8'))
            global user_token
            user_token = self.requestline.split(' ')[1].split('?token=')[1]

def get_token():
    # Obtain auth token using 'Reddit for Android' Client ID
    # Open browser to get access token
    webbrowser.open(auth_url, new=0)
    while True:
        try:
            httpd = HTTPServer(('localhost', 65010), Serv)
            httpd.handle_request()
            httpd.handle_request()

            global user_token
            if user_token != '':
                if len(user_token) < 40:
                    if len(user_token) < 36:
                        print()
                        ays = assert_yn("This access token is in a different format.\nAre you sure this is correct? Type yes or no to answer:\n")
                        if ays is True:
                            print()
                            break
                        else:
                            continue
                    else:
                        break
                elif user_token[0:8].isdigit() is False:
                    if user_token[0:12].isdigit() is False:
                        print()
                        ays = assert_yn("This access token is in a different format.\nAre you sure this is correct? Type yes or no to answer:\n")
                        if ays is True:
                            break
                        else:
                            print()
                            continue
                    else:
                        break
            else:
                user_token = input("Token not found\nType reopen in the field to reopen the webpage if you closed it/didn't load up.\nType discord in the prompt to join the Unoffical RPAN Server for chatting with other streamers and Snookey2 support/bug reports/suggestions!\n")
                options = user_token.lower()
                # if options == "tutorial":
                # print()
                # webbrowser.open("https://www.youtube.com/watch?v=Oi54fiFOoCI&t=2s", new=0)
                # continue
                if options == "reopen":
                    print()
                    webbrowser.open(auth_url, new=0)
                    continue
                elif options == "discord":
                    print()
                    webbrowser.open(DISCORD_URL, new=0)
                    continue
            
        except BaseException as error:
            if isinstance(error, KeyboardInterrupt):  # Exit immediately if requested
                sys.exit()
            print("Unexpected error occured: {}".format(error))
            print("Unexpected error occured, closing program in 10 seconds...")
            time.sleep(10)
            sys.exit(2)
        else:
            break
    return user_token


def request_stream(subreddit, title, token, **request_args):
    # Perform API call to register RPAN stream
    full_token = "Bearer " + token
    broadcast_endpoint = "https://strapi.reddit.com/r/%s/broadcasts?title=%s" % (subreddit, title)
    headers = {
        'User-Agent': 'Project SnooKey/{}'.format(SNOOKEY_VERSION),
        'Authorization': full_token
    }

    return requests.request("POST", url=broadcast_endpoint, headers=headers, **request_args)


def init(subreddit, title, token):
    # Configures and processes request for RPAN stream
    global rpc_enabled
    print("Subreddit selected is " + subreddit + ".")
    print("The title of the stream will be " + title + ".\n")
    print()
    subset = subreddit.lower()

    if subset == "thegamerlounge":
        print()
        ays = assert_yn("This program is not meant to be used to just do random gaming streams, please use this program for things that are worth the limited spots.\nDO NOT do a boring regular gaming stream.\nIf you're going to do a gaming stream, make sure it has something interesting and fun to it.\nIf you want to do just a normal gaming stream and there's already a bunch of other people doing a normal gaming stream on RPAN, please wait until they're done so RPAN isn't flooded with gaming streams.\n\nType yes if you read the whole thing and understand.\n")
        if ays is False:
            sys.exit()

    # url = "https://raw.githubusercontent.com/IOnlyPlayAsDrift/Snookey2/master/accepted-subreddits"
    # r = requests.get(url)
    # content = str([r.text])
    if subset not in available_subs:
        print()
        snf = assert_yn("The subreddit you just typed in couldn't be found in this script's database.\nType yes to move on with " + subreddit + " or type no if you made a mistake.\n")
        if snf is False:
            sys.exit()
    if subset == "pan":
        print()
        print("RPAN is available on Wednesdays from 1AM-5PM PST (times might change).\nPlease keep this in mind.\n")

    # Request broadcast slot
    count = 0
    print("Going to start attempting to start up a stream right now...\n")
    while True:
        stream_req = request_stream(subreddit, title, token, data={})
        if stream_req.ok:
            # Success!  Stream prepped
            response = stream_req.json()
            stream_url = response["data"]["post"]["outboundLink"]["url"]

            if rpc_enabled:
                drp("Streaming " + title + " on r/" + subset + "!", details=stream_url)
            print()
            print("Server Link: rtmp://ingest.redd.it/inbound/")
            print("Your Stream Key: " + response["data"]["streamer_key"])
            print("DON'T share your Stream Key with anyone.")
            print("MAKE SURE you change your stream dimensions to 9:16 or else the stream won't work.")
            print("You can put these into your OBS Settings by going to the Stream section of the settings and switching Service to Custom...")
            print("YOU ARE LIVE: " + stream_url)
            print("\nThis program will close in about an hour.\n")
            time.sleep(180)
            if rpc_enabled:
                drp("Streaming on r/" + subset + " on RPAN!", details=stream_url)
            try:
                time.sleep(3600)
                if rpc_enabled:
                    rpc.close()
                sys.exit()
            except KeyboardInterrupt:
                print("Shutting down...")
                if rpc_enabled:
                    rpc.close()

        else:
            # Failed
            if count == 0 and rpc_enabled:
                drp("Trying to stream on RPAN...", details="Attempting to stream to r/" + subset + "...")
                count += 1

            print()
            print("Stream failed to connect! Trying again in 2 seconds...")
            try:
                print("Error message: " + stream_req.json()["status"])
                time.sleep(2)
            except:
                print("Error message: Invalid subreddit/access code/broadcast title.\nPlease restart the program and try again.\nThis program will automatically close in 10 seconds.")
                time.sleep(10)
                sys.exit(1)


def check_args():
    # Processes arguments passed in by user
    global auth_token
    if len(sys.argv) <= 1:
        info()
        print("Type \"snookey commands\" to see a list of available commands.\n")
        return

    arg_names = ['filename', 'command', 'var1', 'var2']
    args = dict(zip(arg_names, sys.argv))

    if args['command'] == 'stream':
        if 'var2' not in args.keys():
            print('Error. Proper command format: snookey stream subreddit title')
            return
        load_sublist()
        subreddit = args['var1']
        title = args['var2']

        # Ask to enable DRP
        drpask = assert_yn("Would you like to enable Discord Rich Presence?\nIf you say yes, your stream link and title will be put in your Discord status for everyone that looks at it to see!\n")
        if drpask is True:
            discord_init()
            if rpc_enabled:
                drp("Setting up RPAN stream...")

        auth_token = get_token()
        init(subreddit, title, auth_token)
        return
    if args['command'] == 'chat':
        if 'var2' not in args.keys():
            print('Error. Proper command format: snookey chat subreddit streamid')
            return
        load_sublist()
        subreddit = args['var1']
        streamid = args['var2']
        try:
            chat(subreddit, streamid)
        except KeyboardInterrupt:
            pass
        return
    if args['command'] == 'commands':
        commands()
        return
    if args['command'] == 'version':
        print("You are using Snookey2 v{}".format(SNOOKEY_VERSION))
        return
    if args['command'] == 'info':
        info()
        return
    if args['command'] == 'donate':
        donate()
        sys.exit()
    else:  # Display available commands when no args are given
        commands()


def main():
    # Main method
    check_args()

donate_info()  # Is called when loaded by another module or when program starts
