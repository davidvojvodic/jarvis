# Flowko Knowledge MCP Server

A Model Context Protocol (MCP) server that connects AI agents to the Flowko knowledge base (Supabase + pgvector).

## 🚀 Capabilities

- **Topic Search**: Semantic search over Notion documents using Voyage AI embeddings.
- **Document List**: List available documents and metadata.

## 🛠️ Setup & specific Configuration

This server is designed to run locally within the `jarvis` workspace.

### 1. Build
```bash
npm install
npm run build
```

### 2. Configure (Auto-Detect)

We provide a script to automatically verify your OS and configure the paths for your local machine (Windows, Mac, or Linux).

```bash
# Run from the root of the repo
python execution/setup_local_mcps.py
```

This will:
1. Find your `mcp_config.json` (or ask for its location).
2. Inject the absolute paths to this server.
3. Set the required API keys.

## 📝 Logging
To ensure clean JSON-RPC communication over `stdio`:
- **Console Output**: DISABLED. No `console.log` or `console.error` is used.
- **File Logging**: All logs are written to `debug.log` in this directory.

## 🤖 Tools

### `search_flowko_knowledge`
Search the knowledge base.
- `query` (string): The search query.
- `limit` (number): Max results (default 5).
- `threshold` (number): Similarity threshold (0-1).

### `list_flowko_documents`
List available documents.
- `language` (string): 'en' or 'sl'.
- `category` (string): Filter by category.
