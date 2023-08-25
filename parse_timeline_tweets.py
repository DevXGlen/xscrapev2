import json 
import timeline_tweet as tt
from glob import glob
import dl_img
import os 
from dotenv import load_dotenv
import io
import log as l

load_dotenv()

def create_timeline_dir():
    if (not os.path.exists(f'timeline_tweets/{os.getenv("TIMELINE_DIR")}')):
        os.makedirs(f'timeline_tweets/{os.getenv("TIMELINE_DIR")}')
        with open(f"timeline_tweets/{os.getenv('TIMELINE_DIR')}/log.json",'w', encoding='utf-8') as jf:
            json.dump([], jf, ensure_ascii=False)        

def process_timelines(path_str=f'query_timelines/{os.getenv("QUERY_TIME_DIR")}/*'):
    directory = glob(path_str)
    for timeline_collections in directory:
        #print(timeline_collections)
        try:
             with open(timeline_collections, 'r', encoding='utf-8') as tl_file:
                tl_json =  json.load(tl_file)
                tl_collection = tl_json['body']['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']
                parse_timeline_collection(tl_collection, query_word=tl_json['query_word'])
        except Exception as e:
            print("process_timelines error:", timeline_collections)


def parse_timeline_collection(timeline_collection, query_word='fun'):
    log_fpath = f"timeline_tweets/{os.getenv('TIMELINE_DIR')}/log.json"
    log = {}
    for timeline_tweet in timeline_collection:
        log['entry_id'] = ''
        log['tweet_status'] = ''
        log['image_status'] = ''
        try:
            # get required tweet info from timeline tweet
            parsed_tt = tt.parse_timeline_tweet(timeline_tweet)
            parsed_tt['query_word'] = query_word

            log['entry_id'] = parsed_tt['entry_id']

            try:
                for img_url in parsed_tt['image_urls']:
                    img_file_path = dl_img.download_image(img_url)
                    parsed_tt['images'].append(img_file_path)
                log['image_status'] = 'success'
            except:
                #print(f'{parsed_tt["entry_id"]}: error on requesting image')
                log['image_status'] = 'error'
            

            # save parsed timeline tweet to new json file 
            with open(f"timeline_tweets/{os.getenv('TIMELINE_DIR')}/{parsed_tt['entry_id']}.json",'w', encoding='utf-8') as ptt:
                json.dump(parsed_tt, ptt, ensure_ascii=False)
                log['tweet_status'] = 'success'
                print(f'{parsed_tt["entry_id"]} done')
                #print(parsed_tt['entity_id'], ' success 200')
        except Exception as e:
            log['tweet_status'] = 'error'
        finally:
            l.update_log(log_fpath, log)            


create_timeline_dir()
process_timelines()



