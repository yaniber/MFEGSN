"""
MCP Server for PDF RAG System
Provides tools for PDF extraction, indexing, and querying
"""
import logging
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from pdf_extractor.extractor import PDFExtractor
from rag_indexer.indexer import RAGIndexer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
server = Server("pdf-rag-server")

# Initialize components
pdf_extractor = PDFExtractor()
rag_indexer = RAGIndexer()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="extract_pdf",
            description="Extract text, figures, and references from a PDF file and convert to Markdown",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "Path to the PDF file to extract"
                    },
                    "index": {
                        "type": "boolean",
                        "description": "Whether to automatically index the extracted content (default: true)"
                    }
                },
                "required": ["pdf_path"]
            }
        ),
        Tool(
            name="index_document",
            description="Index a document in the RAG vector database for semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Unique identifier for the document"
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content to index"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata dictionary"
                    }
                },
                "required": ["doc_id", "content"]
            }
        ),
        Tool(
            name="query_documents",
            description="Query the RAG database to find relevant document chunks",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query text to search for"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="update_document",
            description="Update an existing document in the RAG database",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Document ID to update"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata dictionary"
                    }
                },
                "required": ["doc_id", "content"]
            }
        ),
        Tool(
            name="delete_document",
            description="Delete a document from the RAG database",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Document ID to delete"
                    }
                },
                "required": ["doc_id"]
            }
        ),
        Tool(
            name="list_documents",
            description="List all indexed documents in the RAG database",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_collection_stats",
            description="Get statistics about the RAG document collection",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="extract_all_pdfs",
            description="Extract and index all PDFs in the pdfs directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "boolean",
                        "description": "Whether to automatically index the extracted content (default: true)"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "extract_pdf":
            pdf_path = arguments["pdf_path"]
            should_index = arguments.get("index", True)
            
            result = pdf_extractor.extract_pdf(pdf_path)
            
            if should_index:
                doc_id = Path(pdf_path).stem
                rag_indexer.index_document(
                    doc_id=doc_id,
                    content=result["markdown"],
                    metadata={
                        "source": result["source_pdf"],
                        "markdown_path": result["markdown_path"]
                    }
                )
                result["indexed"] = True
                result["doc_id"] = doc_id
            
            return [TextContent(
                type="text",
                text=f"Successfully extracted PDF to {result['markdown_path']}\n"
                     f"Extracted {len(result.get('references', []))} references\n"
                     f"Indexed: {result.get('indexed', False)}"
            )]
        
        elif name == "index_document":
            doc_id = arguments["doc_id"]
            content = arguments["content"]
            metadata = arguments.get("metadata")
            
            rag_indexer.index_document(doc_id, content, metadata)
            
            return [TextContent(
                type="text",
                text=f"Successfully indexed document: {doc_id}"
            )]
        
        elif name == "query_documents":
            query = arguments["query"]
            n_results = arguments.get("n_results", 5)
            
            results = rag_indexer.query(query, n_results)
            
            response = f"Query: {query}\n\n"
            response += f"Found {len(results['results'])} results:\n\n"
            
            for i, (doc, metadata, distance) in enumerate(zip(
                results['results'],
                results['metadatas'],
                results['distances']
            )):
                response += f"Result {i+1} (relevance: {1-distance:.3f}):\n"
                response += f"Document: {metadata.get('doc_id', 'unknown')}\n"
                response += f"Content: {doc[:200]}...\n\n"
            
            return [TextContent(type="text", text=response)]
        
        elif name == "update_document":
            doc_id = arguments["doc_id"]
            content = arguments["content"]
            metadata = arguments.get("metadata")
            
            rag_indexer.update_document(doc_id, content, metadata)
            
            return [TextContent(
                type="text",
                text=f"Successfully updated document: {doc_id}"
            )]
        
        elif name == "delete_document":
            doc_id = arguments["doc_id"]
            rag_indexer.delete_document(doc_id)
            
            return [TextContent(
                type="text",
                text=f"Successfully deleted document: {doc_id}"
            )]
        
        elif name == "list_documents":
            docs = rag_indexer.list_documents()
            
            return [TextContent(
                type="text",
                text=f"Indexed documents ({len(docs)}):\n" + "\n".join(f"- {doc}" for doc in docs)
            )]
        
        elif name == "get_collection_stats":
            stats = rag_indexer.get_collection_stats()
            
            return [TextContent(
                type="text",
                text=f"Collection Statistics:\n"
                     f"Total documents: {stats['total_documents']}\n"
                     f"Total chunks: {stats['total_chunks']}\n"
                     f"Documents: {', '.join(stats['documents'])}"
            )]
        
        elif name == "extract_all_pdfs":
            should_index = arguments.get("index", True)
            results = pdf_extractor.extract_all_pdfs()
            
            if should_index:
                for result in results:
                    doc_id = Path(result["source_pdf"]).stem
                    rag_indexer.index_document(
                        doc_id=doc_id,
                        content=result["markdown"],
                        metadata={
                            "source": result["source_pdf"],
                            "markdown_path": result["markdown_path"]
                        }
                    )
            
            return [TextContent(
                type="text",
                text=f"Successfully extracted {len(results)} PDFs\n"
                     f"Indexed: {should_index}"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
