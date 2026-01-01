# Jarvis: Complete Workflow Documentation

> **Master Reference** for all automation workflows. Each section contains quick start commands, flow diagrams, file references, and configuration details.

---

# 📱 1. Social Content Automation

## 🚀 Quick Start
```bash
python execution/social_orchestrator.py
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    social_orchestrator.py                       │
│                      (ENTRY POINT)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    Option 1         Option 2        Option 3
     (Plan)         (Generate)        (Exit)
```

## 📁 File Reference

### 🎯 Core Files (You Interact With)
| File | Purpose |
|------|---------|
| `social_orchestrator.py` | **The ONLY script you run** - CLI menu |
| `social_config.json` | Your settings (niche, tone, platforms) |
| Google Sheet | Your content calendar - edit before generating |

### ⚙️ Execution Files (Called Automatically)
| File | Called By | Uses |
|------|-----------|------|
| `plan_content.py` | Option 1 | Gemini 3 Flash Preview |
| `format_social_sheet.py` | Option 1 (after) | gspread |
| `generate_captions.py` | Option 2 | Gemini 3 Flash Preview |
| `generate_visuals.py` | Option 2 | Nano Banana Pro / Veo 3.1 |
| `analyze_brand_voice.py` | Called by Generator | RAG Agent (Supabase) |

### 🔧 Utility Files
| File | Purpose |
|------|---------|
| `utils_auth.py` | OAuth for Google services |
| `utils_genai.py` | Google Gen AI client |
| `utils_drive.py` | Google Drive uploads |

## 🔄 Option 1: Plan New Content
```
social_orchestrator.py
        │
        ▼
  plan_content.py
        │
        ├── Reads: social_config.json
        ├── Uses: Gemini 3 Flash Preview
        ├── Generates: 7-day content plan
        │
        ▼
  [You Review Plan on Screen]
        │
   y/n? ├── y: Save to Google Sheet (Status="Pending")
        │
        ▼
  format_social_sheet.py (auto)
        │
        └── Formats columns, aligns text
```
**Output:** Rows in Sheet with Status="Pending"

## 🔄 Option 2: Generate Assets
```
social_orchestrator.py
        │
        ├── Reads: Sheet rows where Status="Pending"
        │
        ▼ (For EACH pending row)
        │
        ├── Checks: Brand Voice (analyze_brand_voice.py)
        │   └── Generates/Refreshes: brand_context.txt
        │
        ├─────────────────┬─────────────────┐
        ▼                 ▼                 ▼
generate_captions.py  generate_visuals.py  utils_drive.py
        │                 │                 │
        │                 ├── Image:        │
        │                 │   Nano Banana   │
        │                 │                 │
        │                 ├── Video:        │
        │                 │   Veo 3.1       │
        │                 │                 │
        ▼                 ▼                 ▼
   Caption            .tmp/assets/      Drive Link
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
                   Update Sheet:
                   - Caption → Column G
                   - Drive Link → Column H
                   - Status → "Generated"
```

## 📊 Google Sheet Columns
| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Topic | Format | Status | Date | Context | Visual Prompt | Caption | Visual Path |

## ⚙️ Configuration

**`.env`**
```
GEMINI_API_KEY=AIza...
GOOGLE_CLOUD_PROJECT=key-chalice-482314-h4
GOOGLE_SHEET_ID_SOCIAL=10_qy7...
```

**`social_config.json`**
```json
{
  "niche": "Lead Generation for B2B",
  "platforms": ["Instagram", "Facebook"],
  "tone": "Professional yet Engaging",
  "content_pillars": ["Cold Email", "Automation"]
}
```

## 🤖 AI Models
| Task | Model |
|------|-------|
| Planning | Gemini 3 Flash Preview |
| Captions | Gemini 3 Flash Preview |
| Images | **Nano Banana Pro** (gemini-3-pro-image-preview) |
| Videos | Veo 3.1 |

---

# 🕵️ 2. Google Maps Lead Generation

## 🚀 Quick Start
```bash
python execution/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 25
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    gmaps_lead_pipeline.py                       │
│                      (ENTRY POINT)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
 Step 1              Step 2               Step 3
Google Maps        Website Scrape      Claude Extract
  Scrape           + DuckDuckGo         Contacts
    │                    │                    │
    ▼                    ▼                    ▼
 Basic Info         Raw HTML            Structured
(name,phone,       Content from         Contacts:
 address)          contact pages        Owner, Team
    │                    │                    │
    └────────────────────┴────────────────────┘
                         │
                         ▼
                   Step 4: Save
                  to Google Sheet
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `gmaps_lead_pipeline.py` | **Main script** - runs full pipeline |
| `gmaps_parallel_pipeline.py` | Parallel version (faster, incremental saves) |

### ⚙️ Execution Files (Called by Pipeline)
| File | Purpose | AI Used |
|------|---------|---------|
| `scrape_google_maps.py` | Apify Maps actor | - |
| `extract_website_contacts.py` | Deep website scraping | Claude 4.5 Sonnet |

### 🔧 Utility Files
| File | Purpose |
|------|---------|
| `utils_auth.py` | Google OAuth |
| `append_to_sheet.py` | Append leads |

## 🔄 Pipeline Flow
```
gmaps_lead_pipeline.py
        │
        ▼
  Step 1: Google Maps Scrape
        │
        ├── Uses: Apify compass/crawler-google-places
        ├── Returns: name, phone, address, website, rating
        │
        ▼
  Step 2: Website Enrichment (per business)
        │
        ├── Fetches: Main page + up to 5 contact pages
        │   (/contact, /about, /team, /about-us, /our-team)
        │
        ├── DuckDuckGo Search:
        │   "{business} owner email contact"
        │
        ▼
  Step 3: Claude Extraction
        │
        ├── Uses: Claude 4.5 Sonnet
        ├── Extracts: owner_name, owner_email, team_contacts
        │
        ▼
  Step 4: Google Sheet
        │
        ├── Deduplicates by lead_id (MD5 hash of name|address)
        └── Appends new leads only
```

## 📊 Output Schema (36 fields)

### Business Basics (from Google Maps)
| Field | Example |
|-------|---------|
| `business_name` | "Austin Plumbing Co" |
| `phone` | "+1-512-555-0100" |
| `website` | "https://austinplumbing.com" |
| `address` | "123 Main St, Austin, TX" |
| `rating` | 4.8 |
| `review_count` | 234 |

### Extracted Contacts (from Claude)
| Field | Example |
|-------|---------|
| `owner_name` | "John Smith" |
| `owner_title` | "Founder & CEO" |
| `owner_email` | "john@austinplumbing.com" |
| `team_contacts` | `[{"name": "Jane", "title": "Manager"}]` |
| `emails` | "info@company.com, john@company.com" |

### Social & Metadata
| Field | Example |
|-------|---------|
| `facebook` | "https://facebook.com/austinplumbing" |
| `linkedin` | "https://linkedin.com/company/..." |
| `lead_id` | "a1b2c3d4..." (for deduplication) |
| `scraped_at` | "2024-01-15T10:30:00Z" |

## ⚙️ Configuration

**`.env`**
```
APIFY_API_TOKEN=apify_api_...
ANTHROPIC_API_KEY=sk-ant-...
```

**CLI Arguments**
| Argument | Default | Description |
|----------|---------|-------------|
| `--search` | Required | "plumbers in Austin TX" |
| `--limit` | 10 | Max businesses to scrape |
| `--workers` | 3 | Parallel enrichment workers |
| `--sheet-url` | - | Append to existing sheet |

## 🤖 AI Models
| Task | Model |
|------|-------|
| Contact Extraction | Claude 4.5 Sonnet |

---

# 🕵️ 3. B2B Lead Scraping (Apify)

## 🚀 Quick Start
```bash
# Small scrape (<1000)
python execution/scrape_apify.py --industry "Software Agencies" --location "United States" --limit 100

# Large scrape (1000+)
python execution/scrape_apify_parallel.py --total_count 4000 --location "United States" --strategy regions
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│              scrape_apify.py / scrape_apify_parallel.py         │
│                        (ENTRY POINT)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
 Step 1              Step 2               Step 3
Test Scrape         Full Scrape         Email Enrich
 (25 leads)         (verify 80%         (AnyMailFinder)
    │                match)                  │
    │                    │                   │
    ▼                    ▼                   ▼
  Verify           .tmp/leads           Google Sheet
 Industry            .json              (DELIVERABLE)
  Match
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `scrape_apify.py` | Single scrape (<1000 leads) |
| `scrape_apify_parallel.py` | Parallel scrape (1000+ leads) |
| `enrich_emails.py` | Add missing emails |
| `update_sheet.py` | Save to Google Sheet |

### 🔧 Utility Files
| File | Purpose |
|------|---------|
| `classify_leads_llm.py` | LLM classification (optional) |

## 🔄 Small Scrape Flow (<1000 leads)
```
scrape_apify.py
        │
        ▼
  Step 1: Test Scrape (25 leads)
        │
        ├── Uses: Apify code_crafter/leads-finder
        ├── Output: .tmp/test_leads.json
        │
        ▼
  Step 2: Verify Industry Match
        │
        ├── Check: 20/25 (80%) match target industry?
        ├── Pass: Continue to full scrape
        ├── Fail: Refine keywords
        │
        ▼
  Step 3: Full Scrape
        │
        ├── Output: .tmp/leads_[timestamp].json
        │
        ▼
  Step 4: Upload to Google Sheet
        │
        ├── Uses: update_sheet.py
        │
        ▼
  Step 5: Enrich Missing Emails
        │
        ├── Uses: enrich_emails.py
        ├── API: AnyMailFinder (bulk)
        │
        ▼
  OUTPUT: Google Sheet URL (DELIVERABLE)
```

## 🔄 Large Scrape Flow (1000+ leads)
```
scrape_apify_parallel.py
        │
        ▼
  Geographic Partitioning (NO EXTRA COST)
        │
        ├── US: 4-way (Northeast, Southeast, Midwest, West)
        ├── EU: 4-way (Western, Southern, Northern, Eastern)
        ├── UK: 4-way (SE England, N England, Scotland, SW)
        │
        ▼
  Parallel Scrape (4 workers)
        │
        ├── 4 partitions × 1000 = 4000 total
        ├── Auto-deduplicate across regions
        │
        ▼
  Same Steps 4-5 as above
```

## ⚙️ Configuration

**`.env`**
```
APIFY_API_TOKEN=apify_api_...
ANYMAILFINDER_API_KEY=...
```

**CLI Arguments**
| Argument | Default | Description |
|----------|---------|-------------|
| `--industry` | Required | "Software Agencies" |
| `--location` | Required | "United States" |
| `--total_count` | 100 | Number of leads |
| `--strategy` | regions | regions/metros/apac/global |
| `--no-email-filter` | - | Scrape without email requirement |

## 🤖 AI Models
| Task | Model |
|------|-------|
| Lead Classification (optional) | GPT-4 |

---

# ⚡ 4. Cold Email Auto-Reply

## 🚀 Quick Start
```
Webhook-triggered (Instantly.ai sends events automatically)
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    Instantly.ai Webhook                         │
│                 (Triggers on email reply)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              instantly_autoreply.py
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
 Step 1              Step 2               Step 3
Parse Reply        Lookup KB            Generate Reply
(from webhook)     (Google Sheet)       (AI + Research)
    │                    │                    │
    └────────────────────┴────────────────────┘
                         │
                         ▼
                  Step 4: Send
                  via Instantly API
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `instantly_autoreply.py` | Main auto-reply engine |
| `instantly_create_campaigns.py` | Campaign creation helper |

## 🔄 Reply Flow
```
Instantly Webhook Event
        │
        ├── Payload: reply_text, campaign_id, lead_email
        │
        ▼
  Step 1: Parse Reply
        │
        ├── Extract: reply content, subject, sender
        │
        ▼
  Step 2: Lookup Knowledge Base
        │
        ├── Sheet: 1QS7MYDm6RUTzzTWoMfX-0G9NzT5EoE2KiCE7iR1DBLM
        ├── Find: campaign ID → Knowledge Base + Reply Examples
        │
        ├── No KB found? → Skip (no reply)
        │
        ▼
  Step 3: Generate Reply
        │
        ├── Uses: AI with extended thinking
        ├── Research: web_search for sender/company
        ├── Tone: Concise, confident, friendly
        │
        ├── Skip conditions:
        │   - Confirmed call (no reply needed)
        │   - "UNSUBSCRIBE", "remove me"
        │
        ▼
  Step 4: Send via Instantly API
        │
        ├── API: instantly_send_reply
        └── Format: HTML with <br> line breaks
```

## 📊 Knowledge Base Sheet Structure
| ID | Campaign Name | Knowledge Base | Reply Examples |
|----|---------------|----------------|----------------|
| abc123 | Dental Outreach | [context...] | [examples...] |

## ⚙️ Configuration

**`.env`**
```
INSTANTLY_API_KEY=...
```

**Webhook Payload Fields**
| Field | Description |
|-------|-------------|
| `campaign_id` | UUID of campaign |
| `lead_email` | Prospect email |
| `email_id` | Reply-to UUID |
| `reply_text` | Full reply content |

---

# 💼 5. PandaDoc Proposal Creation

## 🚀 Quick Start
```bash
python execution/create_proposal.py < input.json
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                      User Input                                 │
│         (Bullet Points OR Call Transcript)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                create_proposal.py
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
 Step 1              Step 2               Step 3
Client Research    Generate Content    Create in PandaDoc
(web scrape)       (AI expansion)      (API call)
    │                    │                    │
    └────────────────────┴────────────────────┘
                         │
                         ▼
                  Step 4: Send
                  Follow-Up Email
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `create_proposal.py` | Main proposal generator |
| `welcome_client_emails.py` | Onboarding emails |
| `onboarding_post_kickoff.py` | Post-call admin |

## 🔄 Proposal Flow
```
User provides:
- Option A: Structured bullet points
- Option B: Call transcript

        │
        ▼
  Step 1: Client Research (Optional)
        │
        ├── Fetch: Client website landing/about page
        ├── Analyze: Brand voice, keywords, context
        │
        ▼
  Step 2: Generate Content
        │
        ├── Expand: 4 Problems → Strategic paragraphs
        ├── Expand: 4 Benefits → Implementation focus
        ├── Generate: Footers, slugs, dates
        │
        ▼
  Step 3: Create in PandaDoc
        │
        ├── API: PandaDoc document creation
        ├── Output: internalLink for editing
        │
        ▼
  Step 4: Send Follow-Up Email
        │
        ├── Gmail API with HTML formatting
        └── 2-4 numbered sections with deliverables
```

## 📊 Input JSON Structure
```json
{
  "client": {
    "firstName": "John",
    "lastName": "Smith",
    "email": "john@company.com",
    "company": "Acme Corp"
  },
  "project": {
    "title": "AI Automation Implementation",
    "problems": {
      "problem01": "[Expanded Problem 1]",
      "problem02": "[Expanded Problem 2]"
    },
    "benefits": {
      "benefit01": "[Expanded Benefit 1]",
      "benefit02": "[Expanded Benefit 2]"  
    },
    "monthOneInvestment": "$5,000",
    "monthTwoInvestment": "$3,000"
  }
}
```

## ⚙️ Configuration

**`.env`**
```
PANDADOC_API_KEY=...
GMAIL_... (OAuth credentials)
```

---

# 💼 6. Upwork Automation

## 🚀 Quick Start
```bash
# Step 1: Scrape jobs
python execution/upwork_apify_scraper.py --limit 50 --days 1 --verified-payment -o .tmp/jobs.json

# Step 2: Generate proposals
python execution/upwork_proposal_generator.py --input .tmp/jobs.json --workers 5
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                   upwork_apify_scraper.py                       │
│                      (STEP 1: SCRAPE)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                  .tmp/jobs.json
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                upwork_proposal_generator.py                     │
│                   (STEP 2: GENERATE)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  Cover Letter      Proposal Doc     Google Sheet
  (35 words max)    (Google Doc)     (with links)
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `upwork_apify_scraper.py` | Scrape Upwork jobs |
| `upwork_proposal_generator.py` | Generate cover letters + proposals |
| `upwork_scraper.py` | Basic RSS scraper (legacy) |

## 🔄 Full Flow
```
Step 1: Scrape Jobs
        │
        ├── Uses: Apify upwork-vibe~upwork-job-scraper
        ├── Keywords: automation, ai agent, n8n, gpt, workflow
        ├── Output: .tmp/upwork_jobs_batch.json
        │
        ▼
Step 2: Generate Proposals (per job)
        │
        ├── Contact Discovery:
        │   └── Uses: Claude Opus 4.5
        │   └── Finds: Name from description or company
        │
        ├── Cover Letter (35 words max):
        │   └── "Hi. I work with [thing] daily & just built
        │        a [thing]. Free walkthrough: [LINK]"
        │
        ├── Proposal Doc:
        │   └── Creates: Google Doc with full proposal
        │   └── Format: Conversational, 4-6 steps
        │
        ▼
Step 3: Output to Google Sheet
        │
        ├── Columns: Title, URL, Budget, Skills, Apply Link,
        │            Cover Letter, Proposal Doc
        │
        └── One-click apply: /nx/proposals/job/{id}/apply/
```

## 📊 Output Sheet Columns
| Column | Description |
|--------|-------------|
| Keyword | Search term that found job |
| Title | Job title |
| Budget | Fixed/hourly range |
| Skills | Top 5 required skills |
| Client Spent | Total $ spent on platform |
| **Apply Link** | One-click apply URL |
| **Cover Letter** | Personalized pitch |
| **Proposal Doc** | Google Doc link |

## ⚙️ Configuration

**`.env`**
```
APIFY_API_TOKEN=apify_api_...
ANTHROPIC_API_KEY=sk-ant-...
```

**CLI Arguments**
| Argument | Default | Description |
|----------|---------|-------------|
| `--limit` | 50 | Max jobs to scrape |
| `--days` | 1 | Jobs from last N days |
| `--verified-payment` | - | Only verified clients |
| `--workers` | 5 | Parallel Opus calls |

## 🤖 AI Models
| Task | Model |
|------|-------|
| Contact Discovery | Claude Opus 4.5 |
| Cover Letter | Claude Opus 4.5 |
| Proposal | Claude Opus 4.5 |

---

# 🎬 7. Video Jump Cut Editor

## 🚀 Quick Start
```bash
python execution/jump_cut_vad_singlepass.py input.mp4 output.mp4 --enhance-audio
```

## 📊 System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                  jump_cut_vad_singlepass.py                     │
│                      (ENTRY POINT)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
 Step 1              Step 2               Step 3
Extract Audio      Silero VAD          Concatenate
  (WAV)            (detect speech)       Segments
    │                    │                    │
    │        Optional:   │                    │
    │        "cut cut"   │                    │
    │        detection   │                    │
    └────────────────────┴────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Audio Enhance      LUT Color         Final MP4
 (EQ, compress,     Grading           (H.264)
  loudness)         (.cube)
```

## 📁 File Reference

### 🎯 Core Files
| File | Purpose |
|------|---------|
| `jump_cut_vad_singlepass.py` | Main editor (Silero VAD) |
| `insert_3d_transition.py` | Add transitions between clips |

## 🔄 Processing Flow
```
input.mp4
        │
        ▼
  Step 1: Extract Audio
        │
        ├── Format: WAV (for VAD processing)
        │
        ▼
  Step 2: Silero VAD
        │
        ├── Neural voice activity detection
        ├── Finds: Speech segments
        ├── Ignores: Breathing, background noise
        │
        ├── Optional: "cut cut" detection
        │   └── Removes mistake + previous segment
        │
        ▼
  Step 3: Concatenate
        │
        ├── Merge close segments (--merge-gap)
        ├── Add padding (--padding)
        ├── Preserve intro (--keep-start)
        │
        ▼
  Step 4: Enhancements (optional)
        │
        ├── Audio: EQ, compression, -16 LUFS
        ├── Video: LUT color grading
        │
        ▼
  output.mp4
        │
        └── Hardware encoding (Apple Silicon) or libx264
```

## ⚙️ Configuration

**CLI Arguments**
| Argument | Default | Description |
|----------|---------|-------------|
| `--min-silence` | 0.5 | Minimum silence gap to cut (seconds) |
| `--min-speech` | 0.25 | Minimum speech duration to keep |
| `--padding` | 100 | Padding around speech (ms) |
| `--enhance-audio` | false | Apply audio chain |
| `--detect-restarts` | false | Enable "cut cut" detection |
| `--apply-lut` | - | Path to .cube LUT file |

## 🤖 AI Models
| Task | Model |
|------|-------|
| Voice Detection | Silero VAD (neural) |
| Restart Detection | Whisper (optional) |

---

# 📋 Master AI Model Reference

| Model | Used By | Purpose |
|-------|---------|---------|
| **Gemini 3 Flash Preview** | Social Content | Planning, Captions |
| **Nano Banana Pro** | Social Content | Image Generation |
| **Veo 3.1** | Social Content | Video Generation |
| **Claude 4.5 Sonnet** | GMaps Lead Gen | Contact Extraction |
| **Claude Opus 4.5** | Upwork | Proposals, Cover Letters |
| **Silero VAD** | Video Editor | Voice Activity Detection |
| **Whisper** | Video Editor | Transcription |

---

# ⚙️ Master Configuration

## Required `.env` Keys
```
# Google Cloud
GEMINI_API_KEY=AIza...
GOOGLE_CLOUD_PROJECT=key-chalice-482314-h4

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Apify
APIFY_API_TOKEN=apify_api_...

# Email
INSTANTLY_API_KEY=...
ANYMAILFINDER_API_KEY=...

# Other
PANDADOC_API_KEY=...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

## Google OAuth Files
| File | Purpose |
|------|---------|
| `credentials.json` | OAuth client secret |
| `token.json` | User token (generated) |

## Setup Command
```bash
python execution/setup_auth.py
```
