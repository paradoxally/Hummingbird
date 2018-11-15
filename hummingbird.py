import sys
import spotipy
import spotipy.util as util
import time
import twitter
import config

def get_twitter_bio():
    return twitter.VerifyCredentials().description

def update_twitter_bio(now_playing):
    separator = "" if now_playing == "" else "//"
    description = "%s %s %s" % (twitter_bio, separator, now_playing)

    # print "Twitter bio: %s\nSeparator: %s\nNow playing: %s" % (twitter_bio, separator, now_playing)

    twitter.UpdateProfile(description = description)
    return

def get_currently_playing():
    sp = spotipy.Spotify(auth = spotify)
    result = sp.current_user_playing_track()
    now_playing = ""

    # Result code 204 means the user doesn't have app open, guard against this
    if result is not None:
        # Check if track is currently playing or paused
        is_playing = result["is_playing"]
        track = result["item"]["name"]
        artist = result["item"]["artists"][0]["name"]

        if is_playing:
            now_playing = "currently playing: %s by %s" % (track.lower(), artist.lower())
            print "Currently playing: " + now_playing
        else:
            print "Track currently stopped"
    else:
        print "No track is being played"

    return now_playing

scope = 'user-read-currently-playing user-read-playback-state'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

spotify = util.prompt_for_user_token(username,
                scope, 
                client_id = config.sp_client_id, 
                client_secret = config.sp_client_secret, 
                redirect_uri = config.sp_redirect_uri)

twitter = twitter.Api(consumer_key = config.twt_consumer_key,
                  consumer_secret = config.twt_consumer_secret,
                  access_token_key = config.twt_token_key,
                  access_token_secret = config.twt_token_secret)
twitter_bio = get_twitter_bio()

if spotify:
    now_playing = ""

    while True:
        playing = get_currently_playing()

        if playing != now_playing:
            print "Currently playing has changed or stopped, update bio..."
            now_playing = playing
            print "Now playing: " + now_playing
            update_twitter_bio(now_playing)

        time.sleep(5)
else:
    print "Can't get token for", username
