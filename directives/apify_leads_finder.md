# Apify Leads Finder (People & Niche Search)

Use the `code_crafter/leads-finder` actor to find specific **People** and **Companies** in a niche.
Best for Account Based Marketing (ABM) or targeting specific job titles.

## 🎯 When to Use
- **"CEOs of AI Companies"**, **"Founders in SaaS"**.
- You need **Personal Emails** or **Mobile Phones**.
- You need to target by **Job Title** or **Niche Keywords**.

## 🛠️ Execution Plugin
**Script:** `execution/find_b2b_leads.py`

## 🚀 How to Run

```bash
# Niche Keyword Search
python execution/find_b2b_leads.py \
  --keywords "AI Automation" "Agentic Agents" \
  --job-titles "Founder" "CEO" \
  --locations "United Kingdom" \
  --limit 50

# Corporate Search
python execution/find_b2b_leads.py \
  --industries "Software" "Internet" \
  --employees-min 100 \
  --job-titles "VP of Sales" \
  --locations "United States"
```

## 🛠️ Inputs

| Parameter | Type | Description |
|---|---|---|
| `--keywords` | String | **[NICHE]** Keywords to find in company description. |
| `--job-titles` | List | Target roles (e.g. "CEO", "Founder"). |
| `--locations` | List | Geographic target (e.g. "London", "USA"). |
| `--industries` | List | Broad industry filter. |
| `--seniority` | List | "CXO", "Director", "Manager". |
| `--limit` | Int | Max leads to search. |

## 📊 Output
- Saved to `.tmp/b2b_leads_<date>.json`.
