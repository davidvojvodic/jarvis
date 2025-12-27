# Generic Lead Scraping (Bulk)

**Method 3: Legacy / Bulk Listings**

## 🎯 Goal
Scrape large raw lists of websites using generic Apify actors.
Use this when you just need volume (1000+ leads) and don't need the precision of Maps or the Person-matching of Leads Finder.

## 🛠️ Execution Plugin
- `execution/scrape_apify.py`
- `execution/scrape_apify_parallel.py`

## 🚀 Process
1.  **Scrape**: Run the scraper to get a JSON list of domains.
2.  **Upload**: Use `execution/update_sheet.py`.
3.  **Enrich**: Run `execution/enrich_emails.py` to find valid emails.

*Note: For most B2B needs, use `directives/gmaps_lead_generation.md` or `directives/apify_leads_finder.md` instead.*
