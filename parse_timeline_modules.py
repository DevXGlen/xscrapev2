import json 
from glob import glob
import module_tweet as mt 
from dotenv import load_dotenv
import log as l
import os
import dl_img

load_dotenv(override=True)

def create_convo_dir():
    if (not os.path.exists(f'conversation_tweets/{os.getenv("CONVO_DIR")}')):
        os.makedirs(f'conversation_tweets/{os.getenv("CONVO_DIR")}')
        with open(f"conversation_tweets/{os.getenv('CONVO_DIR')}/log.json",'w', encoding='utf-8') as jf:
            json.dump([], jf, ensure_ascii=False)   

def process_timeline_modules_collection(path_str=f'query_conversations/{os.getenv("QUERY_CONVO_DIR")}/*'):
    directory = glob(path_str)
    for timeline_modules in directory:
        #print(timeline_modules)
        try:
             with open(timeline_modules, 'r', encoding='utf-8') as tl_file:
                tl_json =  json.load(tl_file)
                tl_module_collection = tl_json['body']['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
                parse_timeline_module_collection(tl_module_collection, parent_tweet_id=tl_json['parent_tweet_id'], parent_tweet_url=tl_json['parent_tweet_url'], query_word=tl_json['query_word'])
        except Exception as e:
            print("process_timeline_modules_collection error:", e)


def parse_timeline_module_collection(timeline_module_collection, parent_tweet_id, parent_tweet_url, query_word):
    log_fpath = f"conversation_tweets/{os.getenv('CONVO_DIR')}/log.json"
    log = {}
    for timeline_module in timeline_module_collection:
        log['entry_id'] = ''
        log['tweet_status'] = ''
        log['image_status'] = ''
        try:
            parsed_mt = mt.parse_module_tweet(timeline_module)
            parsed_mt['parent_tweet_id'] = parent_tweet_id 
            parsed_mt['parent_tweet_url'] = parent_tweet_url
            parsed_mt['query_word'] = query_word

            log['entry_id'] = parsed_mt["entry_id"]

            try:
                for img_url in parsed_mt['image_urls']:
                    img_file_path = dl_img.download_image(img_url)
                    parsed_mt['images'].append(img_file_path)
                log['image_status'] = 'success'
            except:
                #print(f'{parsed_mt["entry_id"]}: error on requesting image')
                log['image_status'] = 'error'

            with open(f"conversation_tweets/{os.getenv('CONVO_DIR')}/{parsed_mt['entry_id']}.json",'w', encoding='utf-8') as pmt:
                json.dump(parsed_mt, pmt, ensure_ascii=False)
                log['tweet_status'] = 'success'
                print(f'{parsed_mt["entry_id"]} done')
        except Exception as e:
            #print(e)
            log['tweet_status'] = 'error'
        finally:
            l.update_log(log_fpath, log) 

create_convo_dir()
process_timeline_modules_collection()