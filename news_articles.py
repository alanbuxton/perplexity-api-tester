'''
    Based on 
'''
from datetime import date, timedelta, datetime
import os
import requests
from typing import List
from newspaper import Article, ArticleException
import re
import json


def get_articles():
    user_command = get_user_command()
    print(f"User command: {user_command}")
    payload = build_payload(user_command)
    response = get_news(payload)
    perplexity_articles, missing_citations, citation_count = parse_perplexity_response(response)
    scraped_articles = scrape_missing_citations(missing_citations)
    print( (f"Perplexity found {citation_count} articles and provided a structured "
            f"response for {len(perplexity_articles)} of them. Was able to scrape "
            f"{len(scraped_articles)} of the remaining {citation_count - len(perplexity_articles)}."))
    return perplexity_articles, scraped_articles

def get_news(payload: dict):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}"}
    response = requests.post(url, headers=headers, json=payload).json()
    return response

def get_user_command():
    return ("Tell me recent news about developments in UK football. "
            "For each source cited in your response, provide a separate summary of that source's content. "
            "Please output a JSON object containing the following fields: "
            "Please output a list of JSON objects with one JSON object per source with the following fields: "
            "headline, published_date, published_by, document_url")

def build_payload(user_command: str, date_to: date = date.today()):
    date_from = date_to - timedelta(days=90)

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content":  user_command
            },
        ],
        "response_format": { "type": "json_schema",
                            "json_schema": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "headline": { "type": "string" },
                                            "published_date": { "type": "string", "format": "date-time" },
                                            "published_by": { "type": "string" },
                                            "document_url": { "type": "string" }
                                        },
                                        "required": ["headline", "summary_text", "published_date", "published_by", "document_url"]
                                    }
                                }
                            }
                            } ,
        "web_search_options": {
            "search_context_size": "medium"
        },
        "search_after_date_filter": date_from.strftime("%m/%d/%Y"),
        "search_before_date_filter": date_to.strftime("%m/%d/%Y"),
    }
    return payload

def scrape_missing_citations(missing_citations: set):
    articles = []
    for url in missing_citations:
        article = scrape_article(url)
        if article is not None:
            articles.append(article)
    return articles

def scrape_article(url: str):
    article = Article(url)
    try:
        article.download()
        article.parse()
        domain = re.findall('https?://(.+?)/.+', url)[0]
        if article.publish_date is None:
            print(f"{url} has no publish date, ignoring")
            return
        return {
            "headline": article.title,
            "published_date": article.publish_date,
            "published_by": domain,
            "document_url": url,
        }
    except ArticleException as e:
        print(f"Couldn't download {url}")
    except IndexError as e:
        print(f"Couldn't find expected data {e}")

def pplx_to_articles(perplexity_content: dict, citations: List[str]):
    remaining_citations = set(citations)
    articles = []
    for item in perplexity_content:
        pub_date = datetime.fromisoformat(item["published_date"]) # Needs Python 3.11 or higher to work
        item["published_date"] = pub_date
        articles.append(item)
        remaining_citations.discard(item["document_url"])
    return articles, remaining_citations

def parse_perplexity_response(response):
    citations = response['citations']
    content = response['choices'][0]['message']['content']
    perplexity_content = json.loads(content)
    articles, missing_citations = pplx_to_articles(perplexity_content, citations)
    return articles, missing_citations, len(citations)

def print_articles(arts):
    for art in arts:
        print()
        print(art['headline'])
        print(f"{art['published_by']} - {art['published_date']}")
        print(art['document_url'])

if __name__ == "__main__":
    perplexity_articles, scraped_articles = get_articles()
    print()
    print("***** FROM PERPLEXITY JSON *****")
    print_articles(perplexity_articles)
    print()
    print("***** ADDITIONAL CITATIONS SCRAPED SEPARATELY *****")
    print_articles(scraped_articles)          