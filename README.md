# Perplexity API tester

Quick repo to experiment with Perplexity API

## Setup

It needs your API key in an env var called `PERPLEXITY_API_KEY`

## Commentary

- API and Web App give very different responses, see below. Web app isn't constrained by `search_after_date_filter` or `search_before_date_filter` but, even so, the API is not returning as good quality results as the web app.
- Speaking of the date filters: m/d/y format for dates? In an API? Seriously?


## API vs Web App comparison

Using the same user prompt, and running the API via this script vs the web app interface at the same time, I get the results below:

### API
```
Perplexity found 8 articles and provided a structured response for 4 of them. Was able to scrape 1 of the remaining 4.

***** FROM PERPLEXITY JSON *****

Summer Transfer Window 2025 Dates
Sky Sports - 2025-05-14 00:00:00+00:00
https://www.skysports.com/transfer/news/12691/13336561/summer-transfer-window-2025-dates-when-does-it-open-and-close-deadline-day-and-club-world-cup-window-for-premier-league

Women's Football News - May 2025
Regional Newspapers - 2025-05-15 00:00:00+00:00
https://shop.regionalnewspapers.co.uk/womens-football-news---may-2025-4548-p.asp

Barry Ferguson Interview on Rangers Match
RangersTV - 2025-05-17 00:00:00+00:00
https://www.youtube.com/watch?v=d7c_RIQ5c6g

Premier League 2025/26 Season Start Date Confirmed
Sky Sports - 2025-05-14 00:00:00+00:00
https://www.skysports.com/football/news/11661/13258380/premier-league-2025-26-season-start-date-fixture-release-final-day-ahead-of-2026-world-cup-and-christmas-schedule-confirmed

***** ADDITIONAL CITATIONS SCRAPED SEPARATELY *****

Football Scores & Fixtures
www.skysports.com - 2025-05-03 00:00:00
https://www.skysports.com/football-scores-fixtures/2025-05-03
```

### Web app:

```
[
{
    "headline": "Frimpong set for Liverpool medical today; Man Utd want Villa goalkeeper Martinez; Lineker set to leave BBC this week; Arsenal's summer investment plans; Race for Champions League: Epic final day awaits as FIVE teams battle it out",
    "published_date": "2025-05-19",
    "published_by": "Sky Sports",
    "document_url": "https://www.skysports.com/football/news"
},
{
    "headline": "Premier League Fixtures & Results – May 2025: Arsenal clinch Champions League spot, Vardy bids farewell with goal, Everton give Goodison Park perfect send-off",
    "published_date": "2025-05-19",
    "published_by": "Football Web Pages",
    "document_url": "https://www.footballwebpages.co.uk/premier-league/fixtures-results"
},
{
    "headline": "Football Scores & Fixtures – May 2025: Latest Premier League and Scottish Premiership results",
    "published_date": "2025-05-10",
    "published_by": "BBC Sport",
    "document_url": "https://www.bbc.co.uk/sport/football/scores-fixtures/2025-05-10"
},
{
    "headline": "National League news – May 2025: Woking contract extensions, Solihull Moors and Eastleigh player releases, Sutton United departures",
    "published_date": "2025-05-16",
    "published_by": "BBC Sport",
    "document_url": "https://www.bbc.co.uk/sport/football/articles/cg5q575e2d2o"
},
    {
    "headline": "Arsenal plan Gyokeres signing after Zubimendi arrival – Paper Round",
    "published_date": "2025-05-19",
    "published_by": "TNT Sports",
    "document_url": "https://www.tntsports.co.uk/football/"
    }
]
```