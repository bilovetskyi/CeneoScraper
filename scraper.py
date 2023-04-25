import requests
from bs4 import BeautifulSoup
import json


#product_code = input("Please enter the product code: ")
product_code = "129910940"
print(product_code)

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"


#def get(dom, sel):
#    return dom.select_one(sel)

#def get_stripped_element_checked(dom, sel):
#    el = get_element(dom, sel)
#    return el.text.strip() if el else None

#def get_stripped_element(dom, sel):
#    return get_element(dom, sel).text.strip()

def get_element(dom, sel = None, attribute = None, return_list= False):
    try:
        if return_list:
            return ", ".join([tag.text.strip() for tag in dom.select(sel)])
        if attribute:
            if sel:
                return dom.select_one(sel)[attribute].strip()
            
            return dom[attribute]
        
        return dom.select_one(sel).text.strip()
    except (AttributeError, TypeError):
        return None


all_opinions = []

selectors = {
    "opinion_id" : [None, "data-entry-id"],
    "author" : ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "score": ["span.user-post__score-count"],
    "description": [ "div.user-post__text"],
    "pros": ["div.review-feature__col:has( > div.review-feature__title--positives)> div.review-feature__item", None, True],
    "cons": ["div.review-feature__col:has( > div.review-feature__title--negatives)> div.review-feature__item", None, True],
    "like": ["span[id^=votes-yes]"],
    "dislike": ["span[id^=votes-no]"],
    "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"]


}



while url:
    response = requests.get(url)
    print("2222")
    print(url)
    if response.status_code == requests.codes.ok:   
        page_dom = BeautifulSoup(response.text, "html.parser")
        opinions = page_dom.select("div.js_product-review")
    
        if len(opinions)>0:
            print(f"There are opinions about procudt with {product_code} code.")
            

            for opinion in opinions:
                # opinion_id = opinion["data-entry-id"]
                # author = get_element(opinion, "span.user-post__author-name")
                
                # recommendation = get_element(opinion, "span.user-post__author-recomendation > em")
                
                
                # score = get_element(opinion, "span.user-post__score-count")
                # description = get_element(opinion, "div.user-post__text")
            
                # pros = get_element(opinion, "div.review-feature__col:has( > div.review-feature__title--positives)> div.review-feature__item", return_list=True)
                # cons = get_element(opinion, "div.review-feature__col:has( > div.review-feature__title--negatives)> div.review-feature__item", return_list=True)

                # like = get_element(opinion, "span[id^=votes-yes]")

                # dislike = get_element(opinion, "span[id^=votes-no]")

                # publish_date = get_element(opinion, "span.user-post__published > time:nth-child(1)", "datetime")
              
                # purchase_date = get_element(opinion, "span.user-post__published > time:nth-child(2)", "datetime")
                
                single_opinion = {}
                for key, value in selectors.items():
                    single_opinion[key] = get_element(opinion, *value)
                    
                single_opinion["recommendation"] = True if single_opinion["recommendation"] == "Polecam" else False if single_opinion["recommendation"] == "Nie polecam" else None


                all_opinions.append(single_opinion)
            
            next_page = get_element(page_dom, "a.pagination__next", "href")
            url = f"https://ceneo.pl/{next_page}"

            print(url)

        else:
            print(f"There are no opinions about procudt with {product_code} code.")
            url = None

    else:
        print("The product does not exist")
        url = None

if len(all_opinions) > 0:
    with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions,jf, indent=4, ensure_ascii=False)