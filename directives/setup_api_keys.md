# How to Get Required API Keys

## 1. Anthropic API Key (Critical)
**Purpose**: Powers the "Brain" (Claude) for reasoning, writing emails, and parsing data.
1.  Go to [console.anthropic.com](https://console.anthropic.com/).
2.  Sign up/Log in.
3.  Go to **Settings** > **API Keys**.
4.  Click **Create Key**. Name it "Jarvis".
5.  Copy the key (`sk-ant-...`).

## 2. Apify API Token (Critical)
**Purpose**: Powers web scraping (Google Maps, Upwork, etc.).
1.  Go to [console.apify.com](https://console.apify.com/).
2.  Sign up/Log in.
3.  Go to **Settings** > **Integrations**.
4.  Look for **Personal API token**.
5.  Copy the token (`apify_api_...`).

## 3. Instantly API Key
**Purpose**: Automates cold email campaigns and replies.
1.  Login to [Instantly.ai](https://app.instantly.ai/).
2.  Go to **Settings** (gear icon) > **Integrations** (or API).
3.  Click **Create API Key**. Name it "Jarvis".
4.  Copy the key.

## 4. Slack Webhook URL
**Purpose**: Sends notifications to your Slack workspace.
1.  Go to [api.slack.com/apps](https://api.slack.com/apps).
2.  Click **Create New App** > **From scratch**.
3.  Name it "Jarvis" and select your Workspace.
4.  In the sidebar, click **Incoming Webhooks**.
5.  Toggle **Activate Incoming Webhooks** to **On**.
6.  Click **Add New Webhook to Workspace**.
7.  Select the channel (e.g., `#general` or `#jarvis-logs`).
8.  Copy the **Webhook URL** (`https://hooks.slack.com/services/...`).

## 5. Trigger.dev API Key (Cloud Scheduler)
**Purpose**: Runs your scripts on a schedule (e.g., daily at 9am).
1.  Go to [trigger.dev](https://trigger.dev/).
2.  Sign up/Log in.
3.  Create a Project named "Jarvis".
4.  Go to **API Keys** (Side menu).
5.  Copy the **Server API Key** (`trt_...`).
6.  Copy the **API URL** (usually `https://api.trigger.dev`).

## 6. Other Keys (Optional/Later)
-   **PandaDoc**: [Settings > Integrations > API Dashboard](https://app.pandadoc.com/). (Required for `create_proposal.py`)
-   **Anymail Finder**: [Settings > API](https://app.anymailfinder.com/). (Required for `enrich_emails.py`)
