"Go to page with specified parameters"
"""
query_word: str -> query word 
min_replies: int -> minimum number of replies from a specific timeline tweet 
lang: str -> language of the tweet 
until: str (yyyy-mm-dd) -> until date of the tweet 
since: str (yyyy-mm-dd) -> since date of the tweet 
"""
import os 
from dotenv import load_dotenv

def query_page(query_word='twitter', min_replies=3, lang="en", until="2023-08-31", since="2023-07-01"):
    query_page = "https://twitter.com/"

    try:
        query_word = query_word.replace(' ', '%20')

        #query_page = f"https://twitter.com/search?f=top&q={query_word}%20min_replies%3A{min_replies}%20lang%3A{lang}%20until%3A{until}%20since%3A{since}&src=spelling_expansion_revert_click"

        query_page = f"https://twitter.com/search?q={query_word}%20min_replies%3A{min_replies}%20lang%3A{lang}%20until%3A{until}%20since%3A{since}%20-filter%3Areplies&src=spelling_expansion_revert_click"
    except:
        print("Error occured on get_params().")
        return(query_page)

    return query_page



