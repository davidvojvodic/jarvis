# Social Media Content Automation Directive

## 🎯 Goal
Automate B2B Lead Gen content for Instagram & Facebook.
**Interactive Planning** (Human Approval) → **Automated Asset Generation** (Caption + Visual).

## 🏗️ Architecture

| Component | Technology |
|-----------|------------|
| **Orchestrator** | `execution/social_orchestrator.py` (CLI Menu) |
| **Planning** | Gemini 3 Flash Preview (via AI Studio API Key) |
| **Captions** | Gemini 3 Flash Preview |
| **Images** | **Nano Banana Pro** (gemini-3-pro-image-preview) |
| **Videos** | Veo 3.1 (via Vertex AI) |
| **Storage** | Google Drive + Google Sheets |
| **Config** | `social_config.json` |

## 📋 Core Files

| File | Purpose |
|------|---------|
| `execution/social_orchestrator.py` | Main CLI menu - runs everything |
| `execution/plan_content.py` | Generates 7-day content plan |
| `execution/generate_captions.py` | Writes IG/FB optimized captions |
| `execution/generate_visuals.py` | Creates images/videos |
| `execution/format_social_sheet.py` | Auto-formats the Google Sheet |
| `execution/reset_social_sheet.py` | Clears sheet (use carefully!) |
| `social_config.json` | Niche, tone, pillars, platforms |

## 🛠️ Workflow

### Run Command
```bash
python execution/social_orchestrator.py
```

### Option 1: Plan New Content
1. Reads `social_config.json` for themes/pillars
2. Uses **Gemini 3 Flash Preview** to propose 7-day plan (with Visual Prompts)
3. **Interactive**: Displays plan → You approve (y) or reject (n)
4. Saves to Sheet as `Status="Pending"` + Auto-formats columns

### Option 2: Generate Assets
1. Scans Sheet for `Status="Pending"` rows
2. **You can edit the Sheet first** (modify topics, prompts, dates)
3. Type `generate` to confirm
4. **For each row**:
   - Generates Caption (Gemini 3)
   - Generates Image (Nano Banana Pro) or Video (Veo 3.1)
   - Uploads to Google Drive
   - Updates Sheet: Caption, Drive Link, Status → "Generated"

## 📊 Google Sheet Structure

| Column | Content |
|--------|---------|
| A: Topic | What the post is about |
| B: Format | Carousel, Reel, Static, Video |
| C: Status | Pending → Generated |
| D: Date | Scheduled date |
| E: Context/Notes | Context for caption |
| F: Visual Prompt | Prompt for image generation |
| G: Caption | Generated caption |
| H: Visual Path | Google Drive link |

## ⚙️ Configuration

**`.env` Variables:**
```
GEMINI_API_KEY=AIza...          # For Gemini 3 / Nano Banana Pro
GOOGLE_CLOUD_PROJECT=key-chalice-482314-h4
GOOGLE_SHEET_ID_SOCIAL=10_qy7MNkavJLuuQ7MxT_wqb76mzfIgNARPVS-obZk-s
```

**`social_config.json`:**
```json
{
  "niche": "Lead Generation for B2B",
  "platforms": ["Instagram", "Facebook"],
  "tone": "Professional yet Engaging",
  "content_pillars": ["Cold Email", "Automation", "Lead Qualification"]
}
```

## ⚠️ Troubleshooting
- **Auth Error**: Run `python execution/setup_auth.py`
- **Empty Sheet**: Run `python execution/reset_social_sheet.py`
- **Model 404**: Check `GEMINI_API_KEY` is set in `.env`
