from dotmap import DotMap

def parse_module_tweet(module_tweet): 

    try:
        module_tweet = DotMap(module_tweet)
    except:
        print('something wrong with dotmap')
    
    mt = DotMap()
    
    # entry id
    mt.entry_id = module_tweet.entryId
    
    # entry type
    mt.entry_type = module_tweet.content.entryType
    
    # location 
    mt.location = module_tweet.content['items'][0].item.itemContent.tweet_results.result.core.user_results.result.legacy.location
    
    # module id_str
    mt.id_str = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.id_str

    # tweet text
    mt.tweet_text = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.full_text

    # lang 
    mt.lang = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.lang

    # user id str 
    mt.user_id_str = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.user_id_str

    # in reply to id str
    mt.in_reply_to_status_id_str = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.in_reply_to_status_id_str

    # images 
    media = module_tweet.content['items'][0].item.itemContent.tweet_results.result.legacy.entities.media
    mt.image_urls = []
    if (type(media) is list):
        for m in media:
            if (m.type.lower() == 'photo'):
                mt.image_urls.append(m.media_url_https)
    
    # image files 
    mt.images = []

    # screen name 
    mt.screen_name = module_tweet.content['items'][0].item.itemContent.tweet_results.result.core.user_results.result.legacy.screen_name

    # tweet url 
    mt.tweet_url = ""
    if mt.screen_name != {} and mt.id_str != {}:
        mt.tweet_url = f"https://twitter.com/{mt.screen_name}/status/{mt.id_str}"

    return mt 