"""FastAPI backend for Tax Assistant chatbot with streaming tool calls."""

import json
import logging
import os
import re
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Configuration (all required via environment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
VAULT_PATH = Path(os.getenv("OBSIDIAN_VAULT"))

# Validate required configuration
if not all([OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, VAULT_PATH]):
    missing = [k for k, v in {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "OPENAI_BASE_URL": OPENAI_BASE_URL,
        "OPENAI_MODEL": OPENAI_MODEL,
        "OBSIDIAN_VAULT": os.getenv("OBSIDIAN_VAULT"),
    }.items() if not v]
    raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tax Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    history: list[dict] | None = None  # [{"role": "user/assistant", "content": "..."}]


# Tool definitions
TOOLS = [
    # search_notes is disabled - use crawl_from_index instead for graph-based exploration
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "search_notes",
    #         "description": "Search for notes in the Obsidian vault by content or frontmatter.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "query": {"type": "string", "description": "The search query text"},
    #                 "limit": {"type": "integer", "description": "Max results (default 5, max 20)", "default": 5},
    #             },
    #             "required": ["query"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read a specific note from the vault by its path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the note relative to vault root",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_multiple_notes",
            "description": "Read multiple notes at once (max 10).",
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of note paths (max 10)",
                    }
                },
                "required": ["paths"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories in the vault.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path relative to vault root",
                        "default": "/",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_vault_stats",
            "description": "Get vault statistics.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_backlinks",
            "description": "Find all notes that link to a given note (backlinks).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the note to find backlinks for",
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Recursion depth for backlinks of backlinks (default 1, max 3)",
                        "default": 1,
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_outlinks",
            "description": "Find all notes that a given note links to (outlinks). Can recurse to build a connected subgraph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the note to find outlinks for",
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Recursion depth for following links (default 1, max 3)",
                        "default": 1,
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explore_note_graph",
            "description": "Recursively explore the graph around a note, following both backlinks and outlinks. Returns a connected subgraph of related notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Starting note path"},
                    "depth": {
                        "type": "integer",
                        "description": "Recursion depth (default 2, max 3)",
                        "default": 2,
                    },
                    "max_notes": {
                        "type": "integer",
                        "description": "Maximum notes to return (default 20)",
                        "default": 20,
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_indices",
            "description": "Get all index files (_index.md) in the vault. These organize content by category and contain wikilinks to related notes. Use this FIRST to understand what topics are available.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "crawl_from_index",
            "description": "Crawl from an index file, following wikilinks to gather related content. Returns content from all linked notes. Use this after get_indices to deep-dive into a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the index file (e.g., '03 - Topics/_index.md')",
                    },
                    "max_notes": {
                        "type": "integer",
                        "description": "Maximum notes to crawl (default 10, max 20)",
                        "default": 10,
                    },
                    "filter_links": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: only follow these specific link names",
                    },
                },
                "required": ["path"],
            },
        },
    },
]


def extract_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                items = value[1:-1].split(",")
                frontmatter[key.strip()] = [
                    i.strip().strip('"') for i in items if i.strip()
                ]
            else:
                frontmatter[key.strip()] = value.strip('"')
    return frontmatter


def remove_frontmatter(content: str) -> str:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


# Tool implementations
def tool_search_notes(query: str, limit: int = 5) -> list[dict]:
    results = []
    limit = min(limit, 20)
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]

    for md_file in VAULT_PATH.rglob("*.md"):
        try:
            content = md_file.read_text()
            body = remove_frontmatter(content)
            fm = extract_frontmatter(content)
            title = fm.get("title", md_file.stem)

            # Skip index files
            if md_file.name == "_index.md":
                continue

            score = 0

            # Bonus for exact filename match
            filename = md_file.stem.lower()
            if query_lower in filename:
                score += 10
            elif any(word in filename for word in query_words):
                score += 5

            # Bonus for title match
            title_lower = title.lower()
            if query_lower in title_lower:
                score += 8
            elif any(word in title_lower for word in query_words):
                score += 4

            # Word matches in content
            for w in query_words:
                if w in body.lower():
                    score += 1

            if score == 0:
                continue

            results.append(
                {
                    "path": str(md_file.relative_to(VAULT_PATH)),
                    "title": title,
                    "score": score,
                    "excerpt": body[:200] + "..." if len(body) > 200 else body,
                }
            )
        except Exception:
            continue
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def tool_read_note(path: str) -> dict:
    note_path = VAULT_PATH / path
    if not note_path.exists():
        return {"error": f"Note not found: {path}"}
    try:
        content = note_path.read_text()
        fm = extract_frontmatter(content)
        body = remove_frontmatter(content)
        return {"path": path, "title": fm.get("title", note_path.stem), "content": body}
    except Exception as e:
        return {"error": str(e)}


def tool_read_multiple_notes(paths: list[str]) -> list[dict]:
    results = []
    for path in paths[:10]:
        result = tool_read_note(path)
        results.append(result)
    return results


def tool_list_directory(path: str = "/") -> dict:
    dir_path = VAULT_PATH / path.lstrip("/")
    if not dir_path.exists() or not dir_path.is_dir():
        return {"error": f"Directory not found: {path}"}
    items = [
        {
            "name": i.name,
            "type": "directory" if i.is_dir() else "file",
            "path": str(i.relative_to(VAULT_PATH)),
        }
        for i in sorted(dir_path.iterdir())
    ]
    return {"path": path, "items": items}


def tool_get_vault_stats() -> dict:
    notes = list(VAULT_PATH.rglob("*.md"))
    return {"totalNotes": len(notes)}


def extract_wikilinks(content: str) -> set[str]:
    """Extract [[wikilinks]] from markdown content."""
    # Match [[link]] or [[link|display text]]
    pattern = r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]"
    return set(m.lower() for m in re.findall(pattern, content))


def find_note_by_name(name: str) -> Path | None:
    """Find a note by its name (without path)."""
    name_lower = name.lower().replace(".md", "")
    for md_file in VAULT_PATH.rglob("*.md"):
        if md_file.stem.lower() == name_lower:
            return md_file
    return None


def tool_get_backlinks(path: str, depth: int = 1) -> dict:
    """Find all notes that link to a given note, with optional recursion."""
    depth = min(depth, 3)

    # Find the target note
    note_path = VAULT_PATH / path
    if not note_path.exists():
        # Try finding by name
        note_path = find_note_by_name(path)
        if not note_path:
            return {"error": f"Note not found: {path}"}

    target_name = note_path.stem.lower()

    visited = set()
    backlinks = []

    def find_backlinks_recursive(target: str, current_depth: int) -> list[dict]:
        if current_depth > depth or target in visited:
            return []
        visited.add(target)

        found = []
        for md_file in VAULT_PATH.rglob("*.md"):
            try:
                content = md_file.read_text()
                links = extract_wikilinks(content)

                # Check if this note links to target
                if target.lower() in links or target.lower().replace(" ", "-") in links:
                    rel_path = str(md_file.relative_to(VAULT_PATH))
                    if rel_path.lower() not in visited:
                        fm = extract_frontmatter(content)
                        found.append(
                            {
                                "path": rel_path,
                                "title": fm.get("title", md_file.stem),
                                "depth": current_depth,
                            }
                        )

                        # Recurse for backlinks of backlinks
                        if current_depth < depth:
                            deeper = find_backlinks_recursive(
                                md_file.stem, current_depth + 1
                            )
                            found.extend(deeper)
            except Exception:
                continue

        return found

    backlinks = find_backlinks_recursive(target_name, 1)

    return {
        "source": path,
        "depth": depth,
        "backlinks": backlinks[:50],  # Limit results
        "total": len(backlinks),
    }


def tool_get_outlinks(path: str, depth: int = 1) -> dict:
    """Find all notes that a given note links to, with optional recursion."""
    depth = min(depth, 3)

    note_path = VAULT_PATH / path
    if not note_path.exists():
        note_path = find_note_by_name(path)
        if not note_path:
            return {"error": f"Note not found: {path}"}

    visited = set()
    outlinks = []

    def find_outlinks_recursive(source_path: Path, current_depth: int) -> list[dict]:
        if current_depth > depth:
            return []

        rel_path = str(source_path.relative_to(VAULT_PATH))
        if rel_path.lower() in visited:
            return []
        visited.add(rel_path.lower())

        try:
            content = source_path.read_text()
        except Exception:
            return []

        links = extract_wikilinks(content)
        found = []

        for link_name in links:
            # Find the linked note
            linked_note = find_note_by_name(link_name)
            if linked_note:
                linked_rel_path = str(linked_note.relative_to(VAULT_PATH))
                if linked_rel_path.lower() not in visited:
                    try:
                        fm = extract_frontmatter(linked_note.read_text())
                        found.append(
                            {
                                "path": linked_rel_path,
                                "title": fm.get("title", linked_note.stem),
                                "depth": current_depth,
                            }
                        )

                        # Recurse
                        if current_depth < depth:
                            deeper = find_outlinks_recursive(
                                linked_note, current_depth + 1
                            )
                            found.extend(deeper)
                    except Exception:
                        continue

        return found

    outlinks = find_outlinks_recursive(note_path, 1)

    return {
        "source": path,
        "depth": depth,
        "outlinks": outlinks[:50],
        "total": len(outlinks),
    }


def tool_explore_note_graph(path: str, depth: int = 2, max_notes: int = 20) -> dict:
    """Recursively explore the graph around a note (both backlinks and outlinks)."""
    depth = min(depth, 3)
    max_notes = min(max_notes, 50)

    note_path = VAULT_PATH / path
    if not note_path.exists():
        note_path = find_note_by_name(path)
        if not note_path:
            return {"error": f"Note not found: {path}"}

    visited = set()
    graph = {"nodes": [], "edges": []}

    def explore_recursive(current_path: Path, current_depth: int) -> None:
        rel_path = str(current_path.relative_to(VAULT_PATH))
        if rel_path.lower() in visited or len(graph["nodes"]) >= max_notes:
            return

        visited.add(rel_path.lower())

        try:
            content = current_path.read_text()
            fm = extract_frontmatter(content)
        except Exception:
            return

        # Add node
        graph["nodes"].append(
            {
                "path": rel_path,
                "title": fm.get("title", current_path.stem),
                "depth": current_depth,
            }
        )

        if current_depth >= depth:
            return

        # Find outlinks
        links = extract_wikilinks(content)
        for link_name in links:
            linked_note = find_note_by_name(link_name)
            if linked_note:
                linked_rel = str(linked_note.relative_to(VAULT_PATH))

                # Add edge
                graph["edges"].append({"source": rel_path, "target": linked_rel})

                # Recurse
                if linked_rel.lower() not in visited:
                    explore_recursive(linked_note, current_depth + 1)

        # Find backlinks
        target_name = current_path.stem.lower()
        for md_file in VAULT_PATH.rglob("*.md"):
            if len(graph["nodes"]) >= max_notes:
                break
            try:
                other_content = md_file.read_text()
                other_links = extract_wikilinks(other_content)
                if target_name in other_links:
                    other_rel = str(md_file.relative_to(VAULT_PATH))

                    # Add edge (backlink direction)
                    graph["edges"].append({"source": other_rel, "target": rel_path})

                    if other_rel.lower() not in visited:
                        explore_recursive(md_file, current_depth + 1)
            except Exception:
                continue

    explore_recursive(note_path, 0)

    return {
        "start": path,
        "depth": depth,
        "nodes": graph["nodes"][:max_notes],
        "edges": graph["edges"][: max_notes * 2],
        "total_nodes": len(graph["nodes"]),
        "total_edges": len(graph["edges"]),
    }


def tool_get_indices() -> dict:
    """Get all index files with their full content for context.

    Finds files by frontmatter property type: index
    """
    indices = []

    for md_file in VAULT_PATH.rglob("*.md"):
        try:
            content = md_file.read_text()
            fm = extract_frontmatter(content)

            # Check if this is an index file by frontmatter type
            if fm.get("type") != "index":
                continue

            body = remove_frontmatter(content)
            links = extract_wikilinks(content)

            # Extract section headers as categories
            categories = []
            for line in content.split("\n"):
                if line.startswith("## "):
                    cat = line[3:].strip()
                    if not cat.startswith("```"):
                        categories.append(cat)

            folder = md_file.parent.name

            indices.append(
                {
                    "path": str(md_file.relative_to(VAULT_PATH)),
                    "title": fm.get("title", folder + " Index"),
                    "folder": folder,
                    "categories": categories[:15],
                    "link_count": len(links),
                    "links": list(links)[:100],  # All links for crawling
                    "content": body[:5000],  # Full index content for context
                }
            )
        except Exception:
            continue

    return {"indices": indices, "total": len(indices)}


def find_index_by_type(path: str) -> Path | None:
    """Find an index file by path or by frontmatter type: index."""
    # Try direct path first
    index_path = VAULT_PATH / path
    if index_path.exists():
        return index_path

    # Search all markdown files for type: index in frontmatter
    for md_file in VAULT_PATH.rglob("*.md"):
        try:
            content = md_file.read_text()
            fm = extract_frontmatter(content)
            if fm.get("type") == "index":
                # Match by path or folder name
                if (
                    path.lower() in str(md_file).lower()
                    or path.lower() in md_file.parent.name.lower()
                ):
                    return md_file
        except Exception:
            continue

    return None


def tool_crawl_from_index(
    path: str, max_notes: int = 10, filter_links: list[str] | None = None
) -> dict:
    """Crawl from an index file, following wikilinks to gather content."""
    max_notes = min(max_notes, 20)

    # Find the index file by frontmatter type
    index_path = find_index_by_type(path)

    if not index_path:
        return {"error": f"Index not found: {path}"}

    try:
        index_content = index_path.read_text()
        links = extract_wikilinks(index_content)
    except Exception as e:
        return {"error": str(e)}

    # Filter links if specified
    if filter_links:
        filter_lower = [f.lower() for f in filter_links]
        links = [l for l in links if any(f in l.lower() for f in filter_lower)]

    # Crawl each linked note
    crawled = []
    crawled_paths = set()

    for link_name in links:
        if len(crawled) >= max_notes:
            break

        # Find the linked note
        linked_note = find_note_by_name(link_name)
        if not linked_note:
            continue

        rel_path = str(linked_note.relative_to(VAULT_PATH))
        if rel_path.lower() in crawled_paths:
            continue

        crawled_paths.add(rel_path.lower())

        try:
            content = linked_note.read_text()
            fm = extract_frontmatter(content)
            body = remove_frontmatter(content)

            crawled.append(
                {
                    "path": rel_path,
                    "title": fm.get("title", linked_note.stem),
                    "content": body[:2000],  # Truncate for context
                    "links": list(extract_wikilinks(content))[:10],
                }
            )
        except Exception:
            continue

    return {
        "index_path": str(index_path.relative_to(VAULT_PATH)),
        "total_links": len(links),
        "crawled_count": len(crawled),
        "notes": crawled,
    }


def execute_tool(name: str, arguments: dict) -> Any:
    if name == "search_notes":
        return tool_search_notes(arguments.get("query", ""), arguments.get("limit", 5))
    if name == "read_note":
        return tool_read_note(arguments.get("path", ""))
    if name == "read_multiple_notes":
        return tool_read_multiple_notes(arguments.get("paths", []))
    if name == "list_directory":
        return tool_list_directory(arguments.get("path", "/"))
    if name == "get_vault_stats":
        return tool_get_vault_stats()
    if name == "get_backlinks":
        return tool_get_backlinks(arguments.get("path", ""), arguments.get("depth", 1))
    if name == "get_outlinks":
        return tool_get_outlinks(arguments.get("path", ""), arguments.get("depth", 1))
    if name == "explore_note_graph":
        return tool_explore_note_graph(
            arguments.get("path", ""),
            arguments.get("depth", 2),
            arguments.get("max_notes", 20),
        )
    if name == "get_indices":
        return tool_get_indices()
    if name == "crawl_from_index":
        return tool_crawl_from_index(
            arguments.get("path", ""),
            arguments.get("max_notes", 10),
            arguments.get("filter_links"),
        )
    return {"error": f"Unknown tool: {name}"}


async def execute_tool_async(name: str, arguments: dict) -> Any:
    """Execute tool and broadcast node visits to WebSocket clients."""
    import asyncio

    logger.info(f"execute_tool_async called: {name}")
    result = execute_tool(name, arguments)
    logger.info(
        f"execute_tool_async result type: {type(result)}, connections: {len(manager.active_connections)}"
    )

    # Broadcast visited nodes to WebSocket clients
    if name == "crawl_from_index" and isinstance(result, dict):
        notes = result.get("notes", [])
        index_path = result.get("index_path", "").replace("/", "_").replace(".md", "")
        logger.info(f"Broadcasting {len(notes)} notes from crawl")

        for note in notes:
            note_id = note.get("path", "").replace("/", "_").replace(".md", "")
            # Broadcast node
            await manager.broadcast(
                {
                    "type": "node",
                    "id": note_id,
                    "label": note.get("title", ""),
                    "path": note.get("path", ""),
                    "node_type": "topic",
                }
            )
            # Broadcast edge from index to this note
            if index_path:
                await manager.broadcast(
                    {
                        "type": "edge",
                        "id": f"edge_{index_path}_{note_id}",
                        "source": index_path,
                        "target": note_id,
                    }
                )
            await asyncio.sleep(0.05)

    elif name == "read_note" and isinstance(result, dict) and "error" not in result:
        note_path = arguments.get("path", "")
        note_id = note_path.replace("/", "_").replace(".md", "")
        logger.info(f"Broadcasting read_note: {note_path}")
        await manager.broadcast(
            {
                "type": "node",
                "id": note_id,
                "label": result.get("title", note_path.split("/")[-1]),
                "path": note_path,
                "node_type": "note",
            }
        )
        # Create edge from parent index if in a subfolder
        if "/" in note_path:
            folder = note_path.rsplit("/", 1)[0]
            index_id = f"{folder}/_index".replace("/", "_").replace(".md", "")
            await manager.broadcast(
                {
                    "type": "edge",
                    "id": f"edge_{index_id}_{note_id}",
                    "source": index_id,
                    "target": note_id,
                }
            )

    elif name == "read_multiple_notes" and isinstance(result, list):
        logger.info(f"Broadcasting {len(result)} notes from read_multiple_notes")
        for note in result:
            if isinstance(note, dict) and "error" not in note:
                note_path = note.get("path", "")
                note_id = note_path.replace("/", "_").replace(".md", "")
                await manager.broadcast(
                    {
                        "type": "node",
                        "id": note_id,
                        "label": note.get(
                            "title",
                            note_path.split("/")[-1] if "/" in note_path else note_path,
                        ),
                        "path": note_path,
                        "node_type": "note",
                    }
                )
                # Create edge from parent index
                if "/" in note_path:
                    folder = note_path.rsplit("/", 1)[0]
                    index_id = f"{folder}/_index".replace("/", "_").replace(".md", "")
                    await manager.broadcast(
                        {
                            "type": "edge",
                            "id": f"edge_{index_id}_{note_id}",
                            "source": index_id,
                            "target": note_id,
                        }
                    )

    elif name == "get_indices" and isinstance(result, dict):
        indices = result.get("indices", [])
        logger.info(f"Broadcasting {len(indices)} indices")
        for idx in indices:
            idx_id = idx.get("path", "").replace("/", "_").replace(".md", "")
            await manager.broadcast(
                {
                    "type": "node",
                    "id": idx_id,
                    "label": idx.get("title", ""),
                    "path": idx.get("path", ""),
                    "node_type": "index",
                }
            )

    return result


def format_tool_result(result: Any, max_len: int = 500) -> str:
    """Format tool result for streaming."""
    if isinstance(result, list):
        formatted = []
        for item in result[:5]:
            if isinstance(item, dict):
                title = item.get("title", item.get("path", "unknown"))
                formatted.append(f"- {title}")
        if len(result) > 5:
            formatted.append(f"... and {len(result) - 5} more")
        return "\n".join(formatted)
    if isinstance(result, dict):
        if "error" in result:
            return f"Error: {result['error']}"
        return json.dumps(result, indent=2)[:max_len]
    return str(result)[:max_len]


def extract_highlight_paths(result: Any) -> list[str]:
    """Extract file paths from tool result for graph highlights. Excludes _index.md files."""
    paths = []
    if isinstance(result, dict):
        # get_indices - skip, we don't want to highlight index files
        # crawl_from_index result
        if "notes" in result and isinstance(result["notes"], list):
            for note in result["notes"]:
                if isinstance(note, dict) and "path" in note:
                    path = note["path"]
                    if "_index.md" not in path:
                        paths.append(path)
        # explore_note_graph result
        if "nodes" in result and isinstance(result["nodes"], list):
            for node in result["nodes"]:
                if isinstance(node, dict) and "path" in node:
                    path = node["path"]
                    if "_index.md" not in path:
                        paths.append(path)
        # get_backlinks result
        if "backlinks" in result and isinstance(result["backlinks"], list):
            for bl in result["backlinks"]:
                if isinstance(bl, dict) and "path" in bl:
                    path = bl["path"]
                    if "_index.md" not in path:
                        paths.append(path)
        if "source" in result:
            path = result["source"]
            if "_index.md" not in path:
                paths.append(path)
        # get_outlinks result
        if "outlinks" in result and isinstance(result["outlinks"], list):
            for ol in result["outlinks"]:
                if isinstance(ol, dict) and "path" in ol:
                    path = ol["path"]
                    if "_index.md" not in path:
                        paths.append(path)
    elif isinstance(result, list):
        # search_notes result
        for item in result:
            if isinstance(item, dict) and "path" in item:
                path = item["path"]
                if "_index.md" not in path:
                    paths.append(path)
    return paths[:30]  # Limit to 30 paths


SYSTEM_PROMPT = """You are a tax assistant with access to an Obsidian vault of IRS tax documentation.

## Vault Structure
The vault is organized with INDEX FILES that serve as hubs:
- `01 - Tax Forms/_index.md` - All tax forms organized by type
- `02 - Publications/_index.md` - IRS publications with key topics
- `03 - Topics/_index.md` - Tax topics cross-linked to forms/publications
- `04 - Assets/_index.md` - Supporting documents

## How to Search
1. FIRST: Call `get_indices` to see all available indices with their content and wikilinks
2. THEN: Call `crawl_from_index` on the relevant index to gather all related notes at once
3. Use `filter_links` parameter to only crawl specific topics (e.g., filter_links=["IRA", "Roth"])

## Tools
- `get_indices` - Returns all index files with their full content (categories, wikilinks)
- `crawl_from_index` - Follows wikilinks from an index and returns content from linked notes
- `read_note` - Read a single note by path
- `explore_note_graph` - Explore the graph around a note (backlinks + outlinks)

## Tips
- The indices contain [[wikilinks]] that point to related notes
- Use `crawl_from_index` with `filter_links` to narrow down to specific topics
- Always cite your sources by mentioning the note title or path
- Be concise but thorough"""


async def generate_response(
    message: str, client: httpx.AsyncClient, history: list[dict] | None = None
) -> AsyncGenerator[str]:
    """Generate response with streaming tool calls."""

    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history
    if history:
        for msg in history:
            if msg.get("role") in ("user", "assistant") and msg.get("content"):
                messages.append({"role": msg["role"], "content": msg["content"]})

    # Add current message
    messages.append({"role": "user", "content": message})

    max_iterations = 50  # High limit for complex queries

    for iteration in range(max_iterations):
        # Stream the LLM request
        try:
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": messages,
                    "tools": TOOLS,
                    "tool_choice": "auto",
                    "max_tokens": 2048,
                },
                timeout=60.0,
            )

            if response.status_code != 200:
                yield f"data: {json.dumps({'type': 'error', 'content': f'API error: {response.status_code}'})}\n\n"
                return

            data = response.json()
            choice = data.get("choices", [{}])[0]
            assistant_message = choice.get("message", {})

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
            return

        # Check for tool calls
        tool_calls = assistant_message.get("tool_calls", [])

        if tool_calls:
            # Stream tool call events
            for idx, tc in enumerate(tool_calls):
                func = tc.get("function", {})
                tool_name = func.get("name", "unknown")
                tool_id = tc.get("id", f"call_{iteration}_{idx}")
                try:
                    tool_args = json.loads(func.get("arguments", "{}"))
                except:
                    tool_args = {}

                # Send tool call event with ID
                yield f"data: {json.dumps({'type': 'tool_call', 'id': tool_id, 'name': tool_name, 'args': tool_args})}\n\n"

                # Execute tool
                result = await execute_tool_async(tool_name, tool_args)
                result_str = format_tool_result(result)

                # Extract paths for graph highlighting
                highlight_paths = extract_highlight_paths(result)

                # Send tool result event with ID and highlight paths
                yield f"data: {json.dumps({'type': 'tool_result', 'id': tool_id, 'name': tool_name, 'result': result_str, 'paths': highlight_paths})}\n\n"

                # Add to messages
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": json.dumps(result)
                        if isinstance(result, (dict, list))
                        else str(result),
                    }
                )

            # Add assistant message with tool calls
            messages.append(assistant_message)
            continue

        # No tool calls - stream the final response
        content = assistant_message.get("content") or ""
        logger.info(
            f"📝 Final response: {len(content)} chars, finish_reason: {choice.get('finish_reason')}"
        )
        if content:
            # Stream content character by character for better UX
            words = content.split(" ")
            for i, word in enumerate(words):
                chunk = word + (" " if i < len(words) - 1 else "")
                yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
            # Signal done
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # If no content and no tool calls, something is wrong
        logger.warning(f"⚠️ No content and no tool calls at iteration {iteration}")
        break

    yield f"data: {json.dumps({'type': 'done'})}\n\n"


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat with streaming tool calls."""

    async def event_stream():
        async with httpx.AsyncClient(timeout=120.0) as client:
            async for chunk in generate_response(
                request.message, client, request.history
            ):
                yield chunk

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}


@app.get("/health")
async def health():
    return {"status": "ok", "vault": str(VAULT_PATH), "model": OPENAI_MODEL}


@app.get("/tools")
async def list_tools():
    return {"tools": TOOLS}


@app.get("/graph")
async def get_graph():
    """Get the vault graph structure for visualization."""
    import re

    nodes = []
    edges = []
    node_map = {}  # path -> id mapping

    # Walk through vault and collect all markdown files
    for md_file in VAULT_PATH.rglob("*.md"):
        rel_path = str(md_file.relative_to(VAULT_PATH))
        node_id = f"node_{len(nodes)}"
        node_map[rel_path] = node_id

        # Get file name without extension
        name = md_file.stem

        # Determine node type based on path
        if "Tax Forms" in rel_path:
            node_type = "form"
            color = "#6366f1"
        elif "Publications" in rel_path:
            node_type = "publication"
            color = "#10b981"
        elif "Instructions" in rel_path:
            node_type = "instructions"
            color = "#f59e0b"
        else:
            node_type = "note"
            color = "#64748b"

        nodes.append(
            {
                "id": node_id,
                "type": "default",
                "data": {"label": name, "path": rel_path, "type": node_type},
                "position": {"x": 0, "y": 0},
                "style": {
                    "backgroundColor": color,
                    "color": "white",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                },
            }
        )

    # Second pass: find links between notes
    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    for md_file in VAULT_PATH.rglob("*.md"):
        rel_path = str(md_file.relative_to(VAULT_PATH))
        source_id = node_map.get(rel_path)
        if not source_id:
            continue

        try:
            content = md_file.read_text()
            for match in link_pattern.finditer(content):
                target_name = match.group(1).split("|")[0].split("#")[0]
                # Find target node
                for target_path, target_id in node_map.items():
                    if target_name in target_path or target_path.endswith(
                        f"{target_name}.md"
                    ):
                        edges.append(
                            {
                                "id": f"edge_{source_id}_{target_id}",
                                "source": source_id,
                                "target": target_id,
                                "animated": False,
                                "style": {"stroke": "#94a3b8", "strokeWidth": 1},
                            }
                        )
                        break
        except Exception:
            pass

    return {"nodes": nodes, "edges": edges}


# Connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        logger.info(
            f"Broadcasting to {len(self.active_connections)} connections: {message.get('type')}"
        )
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
                logger.info("Sent to connection")
            except Exception as e:
                logger.warning(f"Broadcast failed: {e}")


manager = ConnectionManager()


@app.websocket("/ws/traversal")
async def websocket_traversal(websocket: WebSocket):
    """WebSocket endpoint for real-time graph traversal visualization."""
    await manager.connect(websocket)
    try:
        # Keep connection alive, just wait for close
        while True:
            # This will block until client closes connection
            await websocket.receive()
    except Exception:
        pass
    finally:
        manager.disconnect(websocket)


async def stream_traversal(
    index_path: str, max_notes: int, filter_links: list[str] | None = None
) -> AsyncGenerator[dict]:
    """Stream traversal events as nodes are visited."""

    # Find the index file
    index_file = _find_index_by_path_ws(index_path)
    if not index_file:
        yield {"type": "error", "message": f"Index not found: {index_path}"}
        return

    # Read index and extract links
    content = index_file.read_text()
    links = extract_wikilinks(content)

    if filter_links:
        filter_lower = [f.lower() for f in filter_links]
        links = {lnk for lnk in links if any(f in lnk.lower() for f in filter_lower)}

    # Track visited nodes
    visited = set()
    node_map = {}  # path -> node_id
    node_counter = 0

    # Add the index node first
    index_rel = str(index_file.relative_to(VAULT_PATH))
    node_map[index_rel] = f"node_{node_counter}"
    node_counter += 1

    yield {
        "type": "node",
        "id": node_map[index_rel],
        "label": index_file.stem,
        "path": index_rel,
        "node_type": "index",
    }
    visited.add(index_rel.lower())

    # Process linked notes
    for link_name in list(links)[:max_notes]:
        # Find the actual file
        linked_file = _find_note_by_name_ws(link_name)
        if not linked_file:
            continue

        rel_path = str(linked_file.relative_to(VAULT_PATH))
        if rel_path.lower() in visited:
            continue

        visited.add(rel_path.lower())

        # Create node
        if rel_path not in node_map:
            node_map[rel_path] = f"node_{node_counter}"
            node_counter += 1

        # Determine node type
        if "Tax Forms" in rel_path:
            node_type = "form"
        elif "Publications" in rel_path:
            node_type = "publication"
        elif "Instructions" in rel_path:
            node_type = "instructions"
        elif "Assets" in rel_path:
            node_type = "asset"
        else:
            node_type = "topic"

        yield {
            "type": "node",
            "id": node_map[rel_path],
            "label": linked_file.stem,
            "path": rel_path,
            "node_type": node_type,
        }

        # Add edge from index to this node
        yield {
            "type": "edge",
            "id": f"edge_{node_map[index_rel]}_{node_map[rel_path]}",
            "source": node_map[index_rel],
            "target": node_map[rel_path],
        }

        # Find internal links within this note
        try:
            note_content = linked_file.read_text()
            internal_links = extract_wikilinks(note_content)

            for internal_link in internal_links:
                internal_file = _find_note_by_name_ws(internal_link)
                if not internal_file:
                    continue

                internal_rel = str(internal_file.relative_to(VAULT_PATH))

                # Add internal node if not exists
                if internal_rel not in node_map:
                    node_map[internal_rel] = f"node_{node_counter}"
                    node_counter += 1

                    # Determine type
                    if "Tax Forms" in internal_rel:
                        int_type = "form"
                    elif "Publications" in internal_rel:
                        int_type = "publication"
                    elif "Instructions" in internal_rel:
                        int_type = "instructions"
                    elif "Assets" in internal_rel:
                        int_type = "asset"
                    else:
                        int_type = "topic"

                    yield {
                        "type": "node",
                        "id": node_map[internal_rel],
                        "label": internal_file.stem,
                        "path": internal_rel,
                        "node_type": int_type,
                    }

                # Add edge
                yield {
                    "type": "edge",
                    "id": f"edge_{node_map[rel_path]}_{node_map[internal_rel]}",
                    "source": node_map[rel_path],
                    "target": node_map[internal_rel],
                }
        except Exception:
            pass

    yield {"type": "complete", "total_nodes": len(node_map)}


def _find_note_by_name_ws(name: str) -> Path | None:
    """Find a note file by its name (without extension) for WebSocket."""
    name_lower = name.lower()

    # Try exact match first
    for md_file in VAULT_PATH.rglob("*.md"):
        if md_file.stem.lower() == name_lower:
            return md_file

    # Try partial match
    for md_file in VAULT_PATH.rglob("*.md"):
        if name_lower in md_file.stem.lower():
            return md_file

    return None


def _find_index_by_path_ws(path: str) -> Path | None:
    """Find an index file by path or name for WebSocket."""
    # Try exact path
    full_path = VAULT_PATH / path
    if full_path.exists():
        return full_path

    # Find by frontmatter type=index
    for md_file in VAULT_PATH.rglob("*.md"):
        try:
            content = md_file.read_text()
            fm = extract_frontmatter(content)
            if fm.get("type") == "index" and (
                path.lower() in str(md_file).lower()
                or path.lower() in md_file.parent.name.lower()
            ):
                return md_file
        except Exception:
            continue

    return None
