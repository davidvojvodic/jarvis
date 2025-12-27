# Jarvis: AI Business Automation Station
## 🚀 Purpose
Jarvis is your "Home Station for Business"—an agentic workflow engine designed to automate the core revenue-generating activities of your business.

**Core Philosophy:**
- **Interface**: Pure Chat. You command, Jarvis executes.
- **Execution**: Hybrid (Local & Cloud/Modal). Heavy jobs run on Modal, quick tasks run locally.
- **Architecture**: 3-Layer (Directive -> Orchestration -> Execution).
## 📚 User Guide
**[👉 Click here to read the "Mission Manual"](USER_GUIDE.md)** for copy-pasteable commands to run your automation.
---
## 📂 Complete File Inventory
This section details **every single file** in the codebase, categorized by its function in the automation pipeline.
### 1. Directives (`directives/`)
*These are the "Brains" or SOPs. They describe WHAT to do.*
| File | Purpose |
| :--- | :--- |

| `gmaps_lead_generation.md` | **[ACTIVE - METHOD 1]** SOP for Local Business leads (Google Maps). Best for bulk. |
| `scrape_leads.md` | **[ACTIVE - METHOD 2]** SOP for People/Niche leads (B2B Finder). Best for specific roles. |

| `instantly_autoreply.md` | SOP for handling cold email replies automatically using AI. |
| `create_proposal.md` | SOP for generating PandaDoc sales proposals from client data. |
| `upwork_scrape_apply.md` | SOP for the Upwork automation loop (Find Job -> Write Proposal). |
| `jump_cut_vad.md` | SOP for the automated video editing workflow. |
| `setup_api_keys.md` | Guide for setting up the required `.env` keys. |
| `setup_google_cloud_credentials.md` | Guide for authenticating Google Cloud (Sheets/Drive). |
### 2. Execution Scripts (`execution/`)
*These are the "Hands". They are deterministic Python scripts that DO the work.*
#### 🕵️ Lead Generation
| File | Purpose |
| :--- | :--- |
| `gmaps_lead_pipeline.py` | **[MAIN]** Orchestrates the Google Maps pipeline: Scrapes Maps -> Scrapes Website -> Enriches -> Saves to Sheet. |
| `gmaps_parallel_pipeline.py` | **[ADVANCED]** A parallelized version of the maps pipeline that saves to Sheets incrementally. |
| `scrape_google_maps.py` | Standalone script to scrape Google Maps data (used by the pipeline). |
| `scrape_apify.py` | Generic Apify scraper wrapper. |
| `scrape_apify_parallel.py` | Parallelized generic Apify scraper for large jobs. |
| `enrich_emails.py` | Uses Anymail Finder/Hunter to find emails for a list of domains. |
| `extract_website_contacts.py` | **[CLAUDE 4.5]** Uses Claude 4.5 Sonnet to deep-read websites and find Owner/Team info. |

#### ⚡ Cold Outreach
| File | Purpose |
| :--- | :--- |
| `instantly_create_campaigns.py` | Automates campaign creation in Instantly.ai. |
| `instantly_autoreply.py` | AI agent that reads email replies and drafts responses. |
#### 💼 Upwork & Sales
| File | Purpose |
| :--- | :--- |
| `upwork_scraper.py` | Basic Upwork RSS feed scraper. |
| `upwork_apify_scraper.py` | Advanced Upwork scraper (using Apify actors). |
| `upwork_proposal_generator.py` | Generates cover letters for identified Upwork jobs. |
| `create_proposal.py` | Generates PDF proposals via PandaDoc API. |
| `welcome_client_emails.py` | Sends onboarding emails to new clients. |
| `onboarding_post_kickoff.py` | Admin tasks after a client kickoff call. |
#### 🎬 Content & Video
| File | Purpose |
| :--- | :--- |
| `jump_cut_vad_singlepass.py` | Removes silence/dead-air from video files (Voice Activity Detection). |
| `insert_3d_transition.py` | Inserts transition effects between video clips. |
#### � Utilities & Core
| File | Purpose |
| :--- | :--- |
| `webhooks.json` | Configuration file mapping webhook slugs to Directives. |
| `update_sheet.py` | Helper to batch update Google Sheets. |
| `read_sheet.py` | Helper to read Google Sheets. |
| `append_to_sheet.py` | Helper to append rows to Google Sheets. |
| `setup_google_auth.py` | helper script to generate `token.json` from `credentials.json`. |
| `casualize_*.py` | Batch scripts (`batch`, `city_names`, `company_names`, `first_names`) to clean up raw data for outreach. |
### 3. Root Files
*Configuration and Documentation.*
| File | Purpose |
| :--- | :--- |
| `documentation.md` | **[THIS FILE]** The master inventory and explanation of the codebase. |
| `USER_GUIDE.md` | The "Instruction Manual" with copy-paste commands for the user. |
| `AGENTS.md` | System instructions for the AI agents. |
| `GEMINI.md` | System instructions specific to the Gemini agent. |
| `CLAUDE.md` | System instructions specific to the Claude agent. |
| `.env` | **[CRITICAL]** Stores API Keys (OpenAI, Anthropic, Google, Apify, etc.). |
| `credentials.json` | OAuth2 Client Secret for Google Cloud. |
| `token.json` | OAuth2 User Token for Google Cloud (generated from credentials). |
| `.gitignore` | Git configuration (ignores `.env`, `*.json` credentials, etc.). |
| `tsconfig.json` | TypeScript configuration (for potential TS migrations). |
| `package-lock.json` | Exact version lock for Node.js dependencies. |
| `.env.example` | Template for environment variables (safe to share). |
| `package.json` / `requirements.txt` | Dependency definitions. |
## 🛠️ Configuration Checklist
To run this system, you need:
1.  **Google Cloud Project**: With Sheets & Drive APIs enabled.
2.  **`credentials.json`**: Downloaded from Google Cloud.
3.  **`.env`**: Populated with keys for Apify, Anthropic, Instantly, etc.
