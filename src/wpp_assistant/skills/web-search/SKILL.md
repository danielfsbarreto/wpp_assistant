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

## Rules

1. Search when the user asks to look something up, or the question involves
   real-time info you don't already know.
2. Flow: SerperDevTool → optionally SerperScrapeWebsiteTool for full pages.
3. Summarize in your own words — no raw HTML. Always include source URLs.

See `references/` for detailed search and scraping guidelines.
