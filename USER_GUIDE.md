# 📘 Jarvis User Guide & Mission Manual

> Your complete guide to using Jarvis - the AI Business Automation Station.

| vs `documentation.md` | **`USER_GUIDE.md` (This File)** | **`documentation.md`** |
|:---|:---|:---|
| **Role** | 🚀 **The Pilot's Checklist** | 🔧 **The Engineering Manual** |
| **Focus** | **Action** ("Run this") | **Reference** ("How it works") |
| **Use When** | You want to **do work** or **prompt the AI** | You need to **debug**, **configure**, or **code** |
| **Content** | Prompts, Missions, Workflows | File Maps, API Specs, System Arch |

---

## 🏗️ How Jarvis Works

Jarvis uses a **3-Layer Architecture** that separates *what to do* from *how to do it*:

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: DIRECTIVES                          │
│                                                                 │
│   📁 Location: directives/                                      │
│   📝 Format: Markdown files (.md)                               │
│   🎯 Purpose: "What to do" - SOPs written in plain English      │
│                                                                 │
│   Examples:                                                     │
│   • social_content_automation.md                                │
│   • gmaps_lead_generation.md                                    │
│   • upwork_scrape_apply.md                                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LAYER 2: ORCHESTRATION                         │
│                                                                 │
│   🤖 Actor: AI Agent (Claude/Gemini)                            │
│   🎯 Purpose: Decision-making, routing, error handling          │
│                                                                 │
│   The AI:                                                       │
│   • Reads directives to understand the task                     │
│   • Calls the right execution scripts                           │
│   • Handles errors and adapts                                   │
│   • Updates directives with learnings                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LAYER 3: EXECUTION                            │
│                                                                 │
│   📁 Location: execution/                                       │
│   🐍 Format: Python scripts (.py)                               │
│   🎯 Purpose: "Do the work" - Deterministic, reliable code      │
│                                                                 │
│   Examples:                                                     │
│   • social_orchestrator.py                                      │
│   • gmaps_lead_pipeline.py                                      │
│   • upwork_proposal_generator.py                                │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 Why This Matters

- **You don't need to code** - Just edit directives in plain English
- **AI reads instructions** - It follows your SOPs automatically
- **Self-improving** - Learnings get added to directives over time
- **Reliable execution** - Python scripts are tested and deterministic

---

## 📂 Understanding Directives

### What Are Directives?

Directives are **instruction manuals** for the AI. Each directive is a Markdown file that describes:
- **What** the task accomplishes
- **When** to use it
- **How** to execute it step-by-step
- **What** outputs to expect

### Where to Find Them

```
jarvis/
├── directives/                          ← All directives live here
│   ├── social_content_automation.md     ← Social media workflow
│   ├── gmaps_lead_generation.md         ← Google Maps leads
│   ├── scrape_leads.md                  ← B2B people finder
│   ├── upwork_scrape_apply.md           ← Upwork automation
│   ├── instantly_autoreply.md           ← Email auto-reply
│   ├── create_proposal.md               ← PandaDoc proposals
│   ├── jump_cut_vad.md                  ← Video editing
│   └── setup_api_keys.md                ← Setup guide
```

### How to Read a Directive

Every directive follows this structure:

| Section | What It Contains |
|---------|------------------|
| **Goal** | Business outcome in plain English |
| **Inputs** | What you need to provide |
| **Process** | Step-by-step workflow |
| **Execution** | Actual commands to run |
| **Outputs** | What you get back |
| **Troubleshooting** | Common issues and fixes |
| **Learnings** | Tips discovered over time |

### How to Trigger a Directive

#### Method A: Ask the AI Orchestrator (Recommended) 💬

Simply tell the AI what you want. The AI reads the directive and orchestrates the entire workflow:

```
"Find me 25 plumbers in Austin and save them to the lead sheet"
```

The AI will:
1. Identify that you need `gmaps_lead_generation.md` directive
2. Read the directive to understand the workflow
3. Run `gmaps_lead_pipeline.py` with your parameters
4. Report results back to you

**More prompts that trigger directives:**
```
"Plan a week of social media content"           → social_content_automation.md
"Scrape 50 Upwork jobs with proposals"          → upwork_scrape_apply.md
"Edit video.mp4 and remove silences"            → jump_cut_vad.md
"Get 1000 SaaS leads in the US"                 → scrape_leads.md
"Create a proposal for Acme Corp, $5000/month"  → create_proposal.md
```

#### Method B: Run Commands Directly
Open the directive, find the **Execution** section, and run the command:
```bash
python execution/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 25
```

#### Method C: Use the Orchestrator (Interactive)
Some workflows have interactive menus:
```bash
python execution/social_orchestrator.py
```

### How to Modify Directives

1. **Open the .md file** in any text editor
2. **Edit the instructions** - AI will follow new instructions next time
3. **Add learnings** - Document what works and what doesn't
4. **Save** - Changes take effect immediately

**Example**: To change the default number of content days from 7 to 5:
```markdown
# Before
├── Generates: 7-day content plan

# After  
├── Generates: 5-day content plan
```

---

## 📋 Directive Quick Reference

| Directive | Example Prompt | Direct Command |
|-----------|----------------|----------------|
| [`social_content_automation.md`](directives/social_content_automation.md) | *"Plan a week of social content"* | `python execution/social_orchestrator.py` |
| [`gmaps_lead_generation.md`](directives/gmaps_lead_generation.md) | *"Find 25 plumbers in Austin"* | `python execution/gmaps_lead_pipeline.py --search "..." --limit 25` |
| [`scrape_leads.md`](directives/scrape_leads.md) | *"Get 1000 SaaS leads in US"* | `python execution/scrape_apify_parallel.py --total_count 1000` |
| [`upwork_scrape_apply.md`](directives/upwork_scrape_apply.md) | *"Find today's Upwork AI jobs"* | `python execution/upwork_apify_scraper.py --limit 50` |
| [`instantly_autoreply.md`](directives/instantly_autoreply.md) | *(Webhook-triggered)* | Automatic |
| [`create_proposal.md`](directives/create_proposal.md) | *"Create proposal for Acme"* | `python execution/create_proposal.py < input.json` |
| [`jump_cut_vad.md`](directives/jump_cut_vad.md) | *"Edit video.mp4, remove silences"* | `python execution/jump_cut_vad_singlepass.py in.mp4 out.mp4` |

---

## 💬 Prompt Examples by Directive

Use these prompts when talking to the AI orchestrator. Copy, paste, and modify for your needs:

### 📱 Social Content Prompts
```
"Plan a week of social media content for my B2B lead gen business"
"Generate assets for all pending content in the sheet"
"Create 7 days of Instagram content about cold email tips"
"Run the social content orchestrator"
```

### 🕵️ Google Maps Lead Prompts
```
"Find me 50 marketing agencies in Ljubljana, Slovenia"
"Scrape 25 dentists in Miami FL with their owner emails"
"Get me local business leads for HVAC contractors in Denver"
"Run gmaps lead gen for plumbers in Austin, limit 30"
```

### 🕵️ B2B Lead Finder Prompts
```
"Find 1000 SaaS company leads in the United States"
"Scrape B2B leads: software agencies in Europe, 500 total"
"Get me 2000 marketing agency leads with email enrichment"
"Run lead scraping for fintech startups in UK, 500 leads"
```

### 💼 Upwork Automation Prompts
```
"Find today's Upwork jobs for AI automation"
"Scrape 50 Upwork jobs from the last 24 hours, verified clients only"
"Generate proposals for the Upwork jobs I just scraped"
"Run the full Upwork workflow: scrape then generate proposals"
```

### 💼 Proposal Generator Prompts
```
"Create a proposal for Acme Corp, $5000/month AI automation project"
"Generate a PandaDoc proposal from this call transcript: [paste transcript]"
"Make a sales proposal for [client] with these problems: [list]"
```

### 🎬 Video Editing Prompts
```
"Edit my video raw_footage.mp4 and remove all silences"
"Process this video with audio enhancement: video.mp4"
"Run jump cut on my recording, detect 'cut cut' as mistakes"
```

---

# 🎯 Missions

Each mission is a complete business workflow with detailed instructions.

---

## 🎯 Mission 1: Social Content Factory

> **Goal**: Automate your social media content pipeline - from ideation to published assets.

### 📂 Directive
[`directives/social_content_automation.md`](directives/social_content_automation.md)

### 🚀 Quick Start
```bash
python execution/social_orchestrator.py
```

### 📋 Detailed Steps

#### Step 1: Configure Your Content Strategy
Edit `social_config.json` with your niche and tone:
```json
{
  "niche": "Lead Generation for B2B",
  "platforms": ["Instagram", "Facebook"],
  "tone": "Professional yet Engaging",
  "content_pillars": ["Cold Email", "Automation", "Lead Qualification"]
}
```

#### Step 2: Plan Content (Option 1)
```
┌─────────────────────────────────────────┐
│     Select Option 1: Plan New Content   │
└────────────────────┬────────────────────┘
                     │
                     ▼
          AI generates 7-day plan
                     │
                     ▼
          You review on screen
                     │
            ┌────────┴────────┐
            ▼                 ▼
          [y] Save         [n] Discard
            │
            ▼
   Sheet updated with "Pending" rows
```

#### Step 3: Review & Edit (Optional)
- Open your Google Sheet
- Modify topics, dates, or visual prompts
- Change formats (Carousel → Reel)

#### Step 4: Generate Assets (Option 2)
```
┌─────────────────────────────────────────┐
│    Select Option 2: Generate Assets     │
└────────────────────┬────────────────────┘
                     │
                     ▼
         Type "generate" to confirm
                     │
                     ▼
      For each "Pending" row:
      ├── Generate Caption (Gemini 3)
      ├── Generate Image (Nano Banana Pro)
      │   └── Uses 'analyze_brand_voice.py' to enforce brand style
      ├── Upload to Google Drive
      └── Update Sheet → "Generated"
```

### 📦 What You Get
- **Google Sheet** with full content calendar
- **Captions** optimized for Instagram/Facebook
- **Images/Videos** in Google Drive
- **Drive Links** for easy access

### 💡 Tips
- Run Option 1 weekly to plan ahead
- Edit Visual Prompts for better images
- Use "Carousel" format for educational content
- Use "Reel" format for engagement

---

## 🎯 Mission 2: Local B2B Lead Sweep

> **Goal**: Find local businesses from Google Maps with deep owner/contact enrichment.

### 📂 Directive
[`directives/gmaps_lead_generation.md`](directives/gmaps_lead_generation.md)

### 🚀 Quick Start
```bash
python execution/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 25
```

### 📋 Detailed Steps

#### Step 1: Define Your Search
```bash
# Format: "[business type] in [location]"
python execution/gmaps_lead_pipeline.py \
  --search "marketing agencies in Ljubljana" \
  --limit 50
```

#### Step 2: Pipeline Runs Automatically
```
┌─────────────────────────────────────────┐
│         gmaps_lead_pipeline.py          │
└────────────────────┬────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
Google Maps      Website          Claude 4.5
  Scrape         Scrape           Extraction
    │                │                │
    │           Fetches:         Extracts:
    │           • Main page      • Owner name
    │           • /contact       • Owner email
    │           • /about         • Team contacts
    │           • /team          │
    │                │                │
    └────────────────┴────────────────┘
                     │
                     ▼
              Google Sheet
         (with 36 fields per lead)
```

#### Step 3: Check Your Sheet
Output automatically saved to your [Master Lead Sheet](https://docs.google.com/spreadsheets/d/1KnwGxF_3SKiosU1O64ILqH0KF6jpap1pT4tSUsLX7H0/).

### 📦 What You Get
| Field | Example |
|-------|---------|
| Business Name | "Austin Plumbing Co" |
| Phone | "+1-512-555-0100" |
| Website | "https://austinplumbing.com" |
| Owner Name | "John Smith" |
| Owner Email | "john@austinplumbing.com" |
| Team Contacts | Manager, salespeople, etc. |
| Social Links | Facebook, LinkedIn, Instagram |

### 💡 Tips
- Include location in search: "plumbers in Austin TX" ✓
- Use `--workers 5` for faster processing
- Run same search twice = auto-skip duplicates
- ~10-15% of sites block scrapers (normal)

---

## 🎯 Mission 3: B2B People Finder

> **Goal**: Find specific professionals (by role, industry) at scale with email enrichment.

### 📂 Directive
[`directives/scrape_leads.md`](directives/scrape_leads.md)

### 🚀 Quick Start
```bash
# Small scrape
python execution/scrape_apify.py --industry "Software Agencies" --location "United States" --limit 100

# Large scrape (1000+)
python execution/scrape_apify_parallel.py --total_count 4000 --location "United States" --strategy regions
```

### 📋 Detailed Steps

#### Step 1: Test Scrape (25 leads)
```bash
python execution/scrape_apify.py \
  --industry "SaaS Companies" \
  --location "United States" \
  --limit 25 \
  --no-email-filter
```

#### Step 2: Verify Quality
- Check output: Are 80%+ leads matching your industry?
- **Pass** → Continue to full scrape
- **Fail** → Refine keywords

#### Step 3: Full Scrape
```bash
# For 1000+ leads, use parallel processing
python execution/scrape_apify_parallel.py \
  --total_count 4000 \
  --location "United States" \
  --strategy regions \
  --no-email-filter
```

#### Step 4: Enrich Emails
```bash
python execution/enrich_emails.py "YOUR_SHEET_URL"
```
Uses AnyMailFinder bulk API (~1000 emails in 5 minutes).

### 📦 What You Get
- **Google Sheet** with all leads
- **Enriched emails** from AnyMailFinder
- **Company data**: Industry, size, location

### 💡 Tips
- Use `--strategy regions` for US (4-way geographic split)
- Use `--strategy global` for worldwide
- Always run email enrichment after scraping

---

## 🎯 Mission 4: Upwork Sniper

> **Goal**: Find relevant Upwork jobs and auto-generate personalized proposals.

### 📂 Directive
[`directives/upwork_scrape_apply.md`](directives/upwork_scrape_apply.md)

### 🚀 Quick Start
```bash
# Step 1: Scrape jobs
python execution/upwork_apify_scraper.py --limit 50 --days 1 --verified-payment -o .tmp/jobs.json

# Step 2: Generate proposals
python execution/upwork_proposal_generator.py --input .tmp/jobs.json --workers 5
```

### 📋 Detailed Steps

#### Step 1: Scrape Jobs
```bash
python execution/upwork_apify_scraper.py \
  --limit 50 \
  --days 1 \
  --verified-payment \
  -o .tmp/upwork_jobs_batch.json
```

Keywords automatically searched:
- automation, ai agent, n8n, gpt
- workflow, api integration, scraping

#### Step 2: Generate Proposals
```bash
python execution/upwork_proposal_generator.py \
  --input .tmp/upwork_jobs_batch.json \
  --workers 5
```

For each job:
- Discovers contact name (from description)
- Writes 35-word cover letter
- Creates full Google Doc proposal

### 📦 What You Get
| Column | Description |
|--------|-------------|
| Title | Job title |
| Budget | Fixed/hourly |
| **Apply Link** | One-click apply URL |
| **Cover Letter** | Ready to paste |
| **Proposal Doc** | Google Doc link |

### 💡 Tips
- Run daily for fresh jobs (`--days 1`)
- Use `--verified-payment` to filter serious clients
- Cover letters are intentionally short (under 35 words)
- Edit proposal docs before submitting

---

## 🎯 Mission 5: Cold Email Auto-Reply

> **Goal**: Automatically respond to cold email replies with AI-generated, personalized responses.

### 📂 Directive
[`directives/instantly_autoreply.md`](directives/instantly_autoreply.md)

### 🚀 How It Works
This mission is **webhook-triggered**. When someone replies to your Instantly campaign:

```
┌─────────────────────────────────────────┐
│         Instantly.ai Webhook            │
│        (Reply event triggers)           │
└────────────────────┬────────────────────┘
                     │
                     ▼
             instantly_autoreply.py
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
Lookup KB       Research          Generate
(Sheet)         (Web search)      Reply
    │                │                │
    └────────────────┴────────────────┘
                     │
                     ▼
            Send via Instantly API
```

### 📋 Setup Steps

#### Step 1: Create Knowledge Base
Add campaigns to Sheet `1QS7MYDm6RUTzzTWoMfX-0G9NzT5EoE2KiCE7iR1DBLM`:

| ID | Campaign Name | Knowledge Base | Reply Examples |
|----|---------------|----------------|----------------|
| abc123 | Dental Outreach | [your context] | [example replies] |

#### Step 2: Configure Webhook
Point Instantly webhook to your endpoint.

### 📦 What You Get
- **Automatic replies** to positive responses
- **Research-informed** personalization
- **Smart skipping** of "unsubscribe" or confirmed meetings

### 💡 Tips
- Quality of Knowledge Base = quality of replies
- Add example replies to match your tone
- System auto-skips negative responses

---

## 🎯 Mission 6: Sales Proposal Generator

> **Goal**: Generate professional PandaDoc proposals from call transcripts or bullet points.

### 📂 Directive
[`directives/create_proposal.md`](directives/create_proposal.md)

### 🚀 Quick Start
```bash
python execution/create_proposal.py < input.json
```

### 📋 Detailed Steps

#### Step 1: Prepare Input
Create JSON with client info and project details:
```json
{
  "client": {
    "firstName": "John",
    "lastName": "Smith", 
    "email": "john@acme.com",
    "company": "Acme Corp"
  },
  "project": {
    "title": "AI Automation Implementation",
    "problems": {
      "problem01": "Manual lead qualification",
      "problem02": "Slow response times"
    },
    "benefits": {
      "benefit01": "Automated lead scoring",
      "benefit02": "24/7 response capability"
    },
    "monthOneInvestment": "$5,000"
  }
}
```

#### Step 2: Generate Proposal
```bash
python execution/create_proposal.py < proposal_input.json
```

### 📦 What You Get
- **PandaDoc proposal** ready for editing
- **Follow-up email** auto-sent to client
- **Internal link** for your review

---

## 🎯 Mission 7: Video Content Editor

> **Goal**: Remove silences and mistakes from talking-head videos automatically.

### 📂 Directive
[`directives/jump_cut_vad.md`](directives/jump_cut_vad.md)

### 🚀 Quick Start
```bash
# Basic silence removal
python execution/jump_cut_vad_singlepass.py input.mp4 output.mp4

# With audio enhancement
python execution/jump_cut_vad_singlepass.py input.mp4 output.mp4 --enhance-audio

# With mistake removal (say "cut cut" during recording)
python execution/jump_cut_vad_singlepass.py input.mp4 output.mp4 --detect-restarts
```

### 📋 Recording Workflow

#### With "Cut Cut" Restart Detection
1. Start recording
2. Speak naturally
3. Make a mistake → Say **"cut cut"** → Pause → Redo
4. Script removes the mistake automatically

#### Parameters
| Flag | Effect |
|------|--------|
| `--enhance-audio` | EQ, compression, loudness normalization |
| `--detect-restarts` | Remove "cut cut" + previous segment |
| `--min-silence 0.8` | Keep more natural pauses |
| `--padding 150` | More breathing room between cuts |

### 📦 What You Get
- **Edited MP4** with silences removed
- **Stats**: Original vs new duration, % removed
- **Hardware acceleration** on Apple Silicon

---

## 🧠 8. RAG Agent & Knowledge Base

> **Goal**: Chat with your internal business knowledge (Notion, docs) via the AI Agent.

### 🚀 Capabilities
The RAG (Retrieval Augmented Generation) Agent has direct access to your company's knowledge base. It can semantic search your documents to answer questions about:
- Pricing and Services
- Internal Processes
- Business Strategies
- Past Projects

### 💬 Example Prompts
```
"What AI services do we offer at Flowko?"
"Summarize our pricing strategy for B2B leads."
"How do we handle client onboarding?"
"Find documents about 'automation workflows'."
```

### 🔧 How It Works
1. **Knowledge Source**: Notion documents (synced via n8n).
2. **Vector DB**: Supabase `knowledge_documents` table with `pgvector`.
3. **Connection**: `flowko-knowledge` MCP server.
4. **Action**: The Agent calls `search_flowko_knowledge` to find relevant chunks before answering.

---

## 🛠️ Utility Commands

Quick commands for maintenance:

```bash
# Setup authentication
python execution/setup_auth.py

# Format the social sheet
python execution/format_social_sheet.py

# Reset social sheet (CAUTION: clears everything)
python execution/reset_social_sheet.py

# Clean up lead names (remove "LLC", fix CAPS)
python execution/casualize_batch.py
```

---

## ⚠️ Troubleshooting

### Authentication Errors
```bash
# Regenerate OAuth token
python execution/setup_auth.py
```

### "Model not found" / 404 Errors
- Check `GEMINI_API_KEY` is set in `.env`
- Verify API key is valid at [aistudio.google.com](https://aistudio.google.com)

### "Sheet is empty"
```bash
python execution/reset_social_sheet.py
```

### Apify Errors
- Check `APIFY_API_TOKEN` in `.env`
- Verify token at [console.apify.com](https://console.apify.com)

### Rate Limits
- Reduce `--workers` for parallel operations
- Add delays between API calls

---

## 📋 Quick Reference Card

### Daily Commands
```bash
# Morning: Check Upwork
python execution/upwork_apify_scraper.py --limit 50 --days 1 --verified-payment -o .tmp/jobs.json
python execution/upwork_proposal_generator.py --input .tmp/jobs.json

# Content: Plan week's social
python execution/social_orchestrator.py  # Select Option 1

# Leads: Find 25 new businesses
python execution/gmaps_lead_pipeline.py --search "dentists in Miami FL" --limit 25
```

### Weekly Commands
```bash
# Generate social assets
python execution/social_orchestrator.py  # Select Option 2

# Large lead scrape
python execution/scrape_apify_parallel.py --total_count 1000 --location "United States"
```
