from dotmap import DotMap

def parse_timeline_tweet(timeline_tweet): 

    try:
        timeline_tweet = DotMap(timeline_tweet)
    except:
        print('something wrong with dotmap')

    tt = DotMap()

    # entry id
    tt.entry_id = timeline_tweet.entryId

    # entry type
    tt.entry_type = timeline_tweet.content.entryType

    # views
    tt.views_count = timeline_tweet.content.itemContent.tweet_results.result.views.count

    # views state 
    tt.views_state = timeline_tweet.content.itemContent.tweet_results.result.views.state

    # bookmark count
    tt.bookmark_count = timeline_tweet.content.itemContent.tweet_results.result.legacy.bookmark_count

    # location 
    tt.location = timeline_tweet.content.itemContent.tweet_results.result.core.user_results.result.legacy.location

    # conversation_id_str
    tt.conversation_id_str = timeline_tweet.content.itemContent.tweet_results.result.legacy.conversation_id_str

    # created_at
    tt.created_at = timeline_tweet.content.itemContent.tweet_results.result.legacy.created_at

    # favorite count
    tt.favorite_count = timeline_tweet.content.itemContent.tweet_results.result.legacy.favorite_count

    # tweet text
    tt.tweet_text = timeline_tweet.content.itemContent.tweet_results.result.legacy.full_text

    # lang 
    tt.lang = timeline_tweet.content.itemContent.tweet_results.result.legacy.lang

    # quote count 
    tt.quote_count = timeline_tweet.content.itemContent.tweet_results.result.legacy.quote_count

    # reply count
    tt.reply_count = timeline_tweet.content.itemContent.tweet_results.result.legacy.reply_count

    # retweet count 
    tt.retweet_couont = timeline_tweet.content.itemContent.tweet_results.result.legacy.retweet_count

    # user id str 
    tt.user_id_str = timeline_tweet.content.itemContent.tweet_results.result.legacy.user_id_str

    # id str 
    tt.id_str = timeline_tweet.content.itemContent.tweet_results.result.legacy.id_str

    # image urls
    media = timeline_tweet.content.itemContent.tweet_results.result.legacy.entities.media
    tt.image_urls = []
    if (type(media) is list):
        for m in media:
            if (m.type.lower() == 'photo'):
                tt.image_urls.append(m.media_url_https)
    
    # image files 
    tt.images = []

    # screen name 
    tt.screen_name = timeline_tweet.content.itemContent.tweet_results.result.core.user_results.result.legacy.screen_name

    # tweet url 
    tt.tweet_url = ""
    if tt.screen_name != {} and tt.id_str != {}:
        tt.tweet_url = f"https://twitter.com/{tt.screen_name}/status/{tt.id_str}"

    # replies json 
    tt.replies = []

    return tt 