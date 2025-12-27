# 📘 Jarvis User Guide & Mission Manual

This guide translates technical scripts into **actionable business missions**.

---

## 🎯 Mission 1: The "Local B2B" Sweep (Lead Gen)
**Goal**: Find high-ticket local businesses (e.g., Marketing Agencies, Roofers), enrich them with data, and save them to your Master Database.

### Step 1: Scout (Scrape Maps & Auto-Save)
Find businesses in a specific area.
**Note**: This automatically checks your **Master Sheet** for duplicates and only adds new leads.

```bash
# Find 20 Marketing Agencies in Ljubljana
python execution/gmaps_lead_pipeline.py --search "marketing agencies in Ljubljana" --limit 20
```
*Output*: Appends new valid leads directly to your [Master Google Sheet](https://docs.google.com/spreadsheets/d/1KnwGxF_3SKiosU1O64ILqH0KF6jpap1pT4tSUsLX7H0/edit?gid=0#gid=0).

> **✨ Claude 4.5 Active**: This command now uses **Claude 4.5 Sonnet** to read every website. It will automatically find Owners, Founders, and Team Members for you.

### Step 2: Enrich (Find Emails)
The pipeline does this automatically if you didn't disable it. But if you need to re-run enrichment:
```bash
python execution/enrich_emails.py --sheet-url "YOUR_SHEET_URL"
```

---

## 🎯 Mission 2: The "Upwork Sniper"
**Goal**: Automatically find relevant jobs on Upwork and draft hyper-personalized proposals 24/7.

### Step 1: Scan & Draft
Run the scout to check for jobs posted in the last 24 hours (`--days 1`).
```bash
# Find AI/Automation jobs, verified clients only
python execution/upwork_apify_scraper.py --limit 50 --days 1 --verified-payment -o .tmp/upwork_jobs_batch.json
```

### Step 2: Generate Proposals
Have Claude (Opus) read the jobs and write proposals.
```bash
python execution/upwork_proposal_generator.py --input .tmp/upwork_jobs_batch.json
```
*Output*: A Google Sheet with **"One-Click Apply" links** and links to **Drafted Google Docs** for your proposals.

---

## 🎯 Mission 3: The "Content Factory"
**Goal**: Turn raw "talking head" footage into snappy, social-media-ready clips automatically.

### Step 1: Drop & Cut
Process a raw video file to remove silence and "umms".
```bash
# Basic silence removal
python execution/jump_cut_vad_singlepass.py raw_footage.mp4 start_posting.mp4

# Advanced (Remove mistakes when you say "Cut Cut")
python execution/jump_cut_vad_singlepass.py raw.mp4 final.mp4 --detect-restarts
```

---

## 🎯 Mission 4: The "Sales Assistant" (PandaDoc)
**Goal**: Generate a contract/proposal for a specific client you just spoke with.

### Step 1: Create Contract
```bash
python execution/create_proposal.py --client "Acme Corp" --amount 5000 --template "Standard Retainer"
```

---

## 🛠️ Utility Belt
Quick commands for maintaining the station.

- **Check Keys**: `python execution/verify_keys.py` (If restored)
- **Casualize Data**: `python execution/casualize_batch.py` (Clean up "LLC" and shouting CAPS from lead lists)
