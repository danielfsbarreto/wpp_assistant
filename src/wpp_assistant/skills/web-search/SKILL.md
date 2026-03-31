---
name: web-search
description: >
  Internet search and website scraping capabilities. Use this skill when the
  user asks for real-time information, current events, fact-checking, or any
  request that requires looking something up on the web.
allowed-tools: SerperDevTool SerperScrapeWebsiteTool
metadata:
  author: wpp-assistant
  version: "1.0"
---

# Web Search

You can search the internet and scrape website content to answer user questions.

## When to Search

- The user explicitly asks you to look something up.
- The question involves real-time or recent information you don't already know
  (news, weather, prices, event dates, etc.).
- You need to verify a fact before replying.

## How to Search

1. Use **SerperDevTool** to run a Google search and get a list of results.
2. If a result snippet is not enough, use **SerperScrapeWebsiteTool** to fetch
   the full page content from a URL returned by the search.
3. Summarize the relevant information in your own words — do not paste raw HTML
   or overly long excerpts.
4. Always include the source URLs in your reply so the user can fact-check the
   information themselves.
