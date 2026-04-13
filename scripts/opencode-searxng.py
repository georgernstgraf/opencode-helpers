#!/usr/bin/env python3
import sys
import json
import requests
import os

# Configuration via environment variables (from opencode.json)
SEARX_URL = os.environ.get("SEARX_URL", "https://claw.graf.priv.at/search")
SEARX_TOKEN = os.environ.get("SEARX_TOKEN")

def search(query, category="general", time_range=None):
    if not SEARX_TOKEN:
        return [{"title": "Error", "url": "", "content": "SEARX_TOKEN not set in environment."}]
    
    headers = {"Authorization": f"Bearer {SEARX_TOKEN}"}
    params = {
        "q": query,
        "format": "json",
        "categories": category
    }
    if time_range:
        params["time_range"] = time_range
    
    try:
        response = requests.get(SEARX_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for r in data.get("results", [])[:10]:
            result = {
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content")
            }
            # Add image specific field if present
            if r.get("img_src"):
                result["img_src"] = r.get("img_src")
            if r.get("thumbnail"):
                result["thumbnail"] = r.get("thumbnail")
                
            results.append(result)
        return results
    except Exception as e:
        return [{"title": "Connection Error", "url": "", "content": str(e)}]

def main():
    # Minimal MCP-compatible JSON-RPC loop
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "opencode-searxng",
                            "version": "0.1.1"
                        }
                    }
                }
                print(json.dumps(response))
            elif method == "notifications/initialized":
                # No response required for notifications
                pass
            elif method == "tools/list": # MCP uses tools/list instead of list_tools
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "searxng_search",
                                "description": "Performs a search via SearXNG. For very recent topics or 'latest' news, always specify a 'time_range'.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "The search query. Use quotes for exact versions (e.g. \"Gemma 4\")."
                                        },
                                        "category": {
                                            "type": "string",
                                            "description": "The search category.",
                                            "enum": ["general", "images", "news", "it", "science"],
                                            "default": "general"
                                        },
                                        "time_range": {
                                            "type": "string",
                                            "description": "Filter results by age. Use 'month' or 'week' for brand new technologies to avoid outdated results.",
                                            "enum": ["day", "week", "month", "year"]
                                        }
                                    },
                                    "required": ["query"]
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response))
            elif method == "tools/call": # MCP uses tools/call instead of call_tool
                args = request.get("params", {}).get("arguments", {})
                query = args.get("query")
                category = args.get("category", "general")
                time_range = args.get("time_range")
                results = search(query, category, time_range)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(results, indent=2)}]
                    }
                }
                print(json.dumps(response))
            sys.stdout.flush()
        except Exception:
            continue

if __name__ == "__main__":
    main()
