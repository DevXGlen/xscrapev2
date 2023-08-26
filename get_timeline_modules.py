from playwright.sync_api import sync_playwright
import json 
import uuid
import time 
import os 
from dotenv import load_dotenv
from glob import glob
import re

load_dotenv()

def create_convo_dir():
    if (not os.path.exists(f'query_conversations/{os.getenv("QUERY_CONVO_DIR")}')):
        os.makedirs(f'query_conversations/{os.getenv("QUERY_CONVO_DIR")}') 

def scrape(tweet_id="404", timeline_tweet_url="https://twitter.com", query_word="fun", reply_count=10):
    num_scroll = 1
    num_scroll += reply_count // 15

    if num_scroll > 10:
        num_scroll = 10

    def check_json(response):
        if "TweetDetail" in response.url:
            #print({"url": response.url, "body": response.json()})
            with open(f'query_conversations/{os.getenv("QUERY_CONVO_DIR")}/{tweet_id}-{uuid.uuid4()}.json', 'w', encoding='utf-8') as f:
                json.dump({"url": response.url, "body": response.json(), "parent_tweet_id":tweet_id, "parent_tweet_url":timeline_tweet_url, "parent_reply_count":reply_count, "query_word":query_word}, f, ensure_ascii=False)
                
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)

        context = browser.new_context(storage_state="./auth.json")
        #print(context.storage_state())

        page = context.new_page()
        #page.set_viewport_size({"width": 1280, "height":1080})
        page.on("response", lambda response: check_json(response))
        page.goto(timeline_tweet_url)
        time.sleep(3)
        page.wait_for_load_state('domcontentloaded')

        for x in range(num_scroll):
            page.keyboard.press('End')
            #print(f'scroll no. {x+1}')
            time.sleep(3)
        
            try:
                show_more = page.get_by_role('button', name=re.compile('Show more replies', re.IGNORECASE), exact=True)
                time.sleep(3)
                if (show_more.is_visible()):
                    show_more.click()
                time.sleep(2)
            except:
                pass

            try:
                show = page.get_by_role('button', name=re.compile('Show', re.IGNORECASE), exact=True)
                time.sleep(3)
                if (show.is_visible()):
                    show.click()
                time.sleep(2)
            except:
                pass
        
        print('done scrolling')
        time.sleep(3)
        print(f'{tweet_id} conversations successfully scraped*')
        context.close()
        browser.close()

def crawl_timeline_tweets(path_str=f'timeline_tweets/{os.getenv("TIMELINE_DIR")}/*'):
    directory = glob(path_str)
    for fpath in directory:
        file = open(fpath, encoding='utf-8')
        timeline_tweet = json.load(file)

        try:
            tweet_id = timeline_tweet['id_str']
            timeline_tweet_url = timeline_tweet['tweet_url']
            query_word = timeline_tweet['query_word']
            reply_count = timeline_tweet['reply_count']

            if (tweet_id and timeline_tweet_url and query_word and reply_count):
                scrape(tweet_id=tweet_id, timeline_tweet_url=timeline_tweet_url, query_word=query_word, reply_count=reply_count)
        except:
            pass
     


create_convo_dir()
crawl_timeline_tweets()
#scrape(tweet_id="1692869430668362004", timeline_tweet_url="https://twitter.com/OctaFX/status/1620820258641612801", query_word='deped', reply_count=151)