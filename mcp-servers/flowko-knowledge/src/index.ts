#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { createClient } from "@supabase/supabase-js";
// import dotenv from "dotenv"; // REMOVED
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// dotenv.config(); // REMOVED: Env vars are passed via MCP config, preventing console noise

// Create debug log file
const logFile = path.join(__dirname, "../debug.log");
function log(message: string) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  try {
    fs.appendFileSync(logFile, logMessage);
  } catch (e) {
    // Ignore logging errors to prevent crashing
  }
  // console.error(message); // REMOVED: Prevent stderr output from breaking JSON-RPC
}

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const VOYAGE_API_KEY = process.env.VOYAGE_API_KEY;

if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY || !VOYAGE_API_KEY) {
  console.error("Missing required environment variables");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

async function generateEmbedding(text: string): Promise<number[]> {
  const response = await fetch("https://api.voyageai.com/v1/embeddings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${VOYAGE_API_KEY}`,
    },
    body: JSON.stringify({
      input: [text],
      model: "voyage-3-large",
      input_type: "document",
    }),
  });

  if (!response.ok) {
    throw new Error(`Voyage AI API error: ${response.statusText}`);
  }

  const data = await response.json();
  const embedding = data.data[0].embedding;
  log(`Generated embedding: length=${embedding.length}, first 5 values=[${embedding.slice(0, 5).join(', ')}]`);
  return embedding;
}

async function searchKnowledge(
  query: string,
  options: {
    limit?: number;
    threshold?: number;
    language?: string;
    category?: string;
  } = {}
) {
  const {
    limit = 5,
    threshold = 0.6,
    language,
    category,
  } = options;

  const queryEmbedding = await generateEmbedding(query);

  log(`Calling match_embeddings with threshold=${threshold}, limit=${limit}`);
  log(`Query embedding type: ${typeof queryEmbedding}, isArray: ${Array.isArray(queryEmbedding)}`);

  // Convert array to string format for PostgreSQL vector type
  const embeddingString = `[${queryEmbedding.join(',')}]`;
  log(`Embedding string format (first 100 chars): ${embeddingString.substring(0, 100)}`);

  const { data, error } = await supabase.rpc("match_embeddings", {
    query_embedding: embeddingString,
    match_threshold: threshold,
    match_count: limit,
    filter_language: language || null,
    filter_category: category || null,
    boost_source: null,
    boost_amount: 0.0,
  });

  if (error) {
    log(`Supabase error: ${JSON.stringify(error)}`);
    throw new Error(`Supabase error: ${error.message}`);
  }

  log(`Search results: ${data?.length || 0} matches found`);
  if (data && data.length > 0) {
    log(`Top result similarity: ${data[0].similarity}`);
  }
  return data;
}

const server = new Server(
  {
    name: "flowko-knowledge",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_flowko_knowledge",
        description:
          "Search the Flowko knowledge base for information about AI automation, business strategies, workflows, and technical documentation. Returns relevant chunks of content with similarity scores.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "The search query",
            },
            limit: {
              type: "number",
              description: "Maximum number of results (default: 5, max: 10)",
              default: 5,
            },
            threshold: {
              type: "number",
              description: "Minimum similarity score 0-1 (default: 0.6)",
              default: 0.6,
            },
            language: {
              type: "string",
              description: "Filter by language: en or sl",
              enum: ["en", "sl"],
            },
            category: {
              type: "string",
              description: "Filter by category",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "list_flowko_documents",
        description:
          "List all documents in the Flowko knowledge base with their titles, categories, and metadata.",
        inputSchema: {
          type: "object",
          properties: {
            language: {
              type: "string",
              description: "Filter by language: en or sl",
              enum: ["en", "sl"],
            },
            category: {
              type: "string",
              description: "Filter by category",
            },
          },
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "search_flowko_knowledge") {
      const { query, limit, threshold, language, category } = args as {
        query: string;
        limit?: number;
        threshold?: number;
        language?: string;
        category?: string;
      };

      const results = await searchKnowledge(query, {
        limit: Math.min(limit || 5, 10),
        threshold: threshold || 0.6,
        language,
        category,
      });

      if (!results || results.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `No relevant information found for: "${query}"\n\nTry:\n- Using different keywords\n- Lowering the threshold (currently ${threshold || 0.6})\n- Removing language/category filters`,
            },
          ],
        };
      }

      let response = `Found ${results.length} relevant results for: "${query}"\n\n`;

      results.forEach((result: any, index: number) => {
        response += `## Result ${index + 1}: ${result.doc_title}\n`;
        response += `**Source:** ${result.doc_source}\n`;
        response += `**Language:** ${result.doc_language}\n`;
        response += `**Categories:** ${result.doc_categories?.join(", ") || "None"}\n`;
        response += `**Similarity:** ${(result.similarity * 100).toFixed(1)}%\n\n`;
        response += `**Content:**\n${result.chunk_content}\n\n`;
        response += `---\n\n`;
      });

      return {
        content: [
          {
            type: "text",
            text: response,
          },
        ],
      };
    }

    if (name === "list_flowko_documents") {
      const { language, category } = args as {
        language?: string;
        category?: string;
      };

      let query = supabase.from("knowledge_documents").select("*");

      if (language) {
        query = query.eq("language", language);
      }

      if (category) {
        query = query.contains("categories", [category]);
      }

      const { data, error } = await query.order("created_at", {
        ascending: false,
      });

      if (error) {
        throw new Error(`Supabase error: ${error.message}`);
      }

      let response = `Found ${data.length} documents in Flowko knowledge base\n\n`;

      data.forEach((doc: any) => {
        response += `## ${doc.title}\n`;
        response += `- **ID:** ${doc.id}\n`;
        response += `- **Source:** ${doc.source}\n`;
        response += `- **Language:** ${doc.language}\n`;
        response += `- **Categories:** ${doc.categories?.join(", ") || "None"}\n`;
        response += `- **Created:** ${new Date(doc.created_at).toLocaleDateString()}\n\n`;
      });

      return {
        content: [
          {
            type: "text",
            text: response,
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${errorMessage}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  log("Flowko Knowledge MCP Server running");
  log("Connected to Supabase knowledge base");
  log("Tools: search_flowko_knowledge, list_flowko_documents");
  log(`Debug log file: ${logFile}`);
}

main().catch((error) => {
  log(`Server error: ${error}`);
  process.exit(1);
});
