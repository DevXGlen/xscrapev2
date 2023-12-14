from playwright.sync_api import sync_playwright
import time
import json
import query_options
import uuid
import os 
from dotenv import load_dotenv

load_dotenv(override=True)

#query_page = f"https://twitter.com/search?f=top&q=({query_word})%20min_replies%3A3%20lang%3Aen%20until%3A2023-08-31%20since%3A2023-07-01&src=typed_query"

query_page = query_options.query_page(query_word=os.getenv("QUERY_WORD"), since=os.getenv('SINCE'), until=os.getenv('UNTIL'))

# print(query_page)

def scrape():
    def check_json(response):
        if "SearchTimeline" in response.url:
            #print({"url": response.url, "body": response.json()})
            if (not os.path.exists(f'query_timelines/{os.getenv("TIMELINE_DIR")}')):
                os.makedirs(f'query_timelines/{os.getenv("TIMELINE_DIR")}')

            with open(f'query_timelines/{os.getenv("TIMELINE_DIR")}/{uuid.uuid4()}.json', 'w', encoding='utf-8') as f:
                json.dump({"url": response.url, "body": response.json(), "query_word":os.getenv('QUERY_WORD')}, f, ensure_ascii=False)
               

    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)

        context = browser.new_context(storage_state="./auth.json")
        print(context.storage_state())

        page = context.new_page()
        #page.set_viewport_size({"width": 1280, "height":1080})
        page.on("response", lambda response: check_json(response))
        page.goto("https://twitter.com/")
        page.goto(query_page)
        time.sleep(3)
        page.wait_for_load_state('domcontentloaded')

        for x in range(int(os.getenv("NUM_SCROLL"))):
            page.keyboard.press('End')
            print(f'scroll no. {x+1}')
            time.sleep(10)
        
        print('done scrolling')
        time.sleep(10)
        print('done scraping')
        context.close()
        browser.close()

scrape()

