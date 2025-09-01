#!/usr/bin/env python3
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Dict, Any
from agents.drawio_converter import DrawIOConverter

class DockerMCPSDKClient:
    """MCP Client that calls Docker container as MCP server using official SDK"""
    
    def __init__(self):
        self.drawio_converter = DrawIOConverter()
    
    async def call_diagram_server(self, diagram_code: str, filename: str = "architecture_diagram", workspace_dir: str = None) -> Dict[str, Any]:
        """Call Docker MCP server using official MCP SDK"""
        
        if not workspace_dir:
            # Docker maps ./outputs/diagrams to /workspace, MCP saves to /workspace/generated-diagrams
            workspace_dir = os.path.abspath("outputs/diagrams/generated-diagrams")
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Use persistent Docker container as MCP server
        server_params = StdioServerParameters(
            command="docker",
            args=[
                "exec", "-i",
                "mcp-diagram-server",
                "awslabs.aws-diagram-mcp-server"
            ]
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize MCP session
                    await session.initialize()
                    
                    # Call generate_diagram tool
                    result = await session.call_tool(
                        "generate_diagram",
                        {
                            "code": diagram_code,
                            "filename": filename,
                            "workspace_dir": "/workspace"
                        }
                    )
                    
                    # Extract content from MCP result
                    if hasattr(result, 'content') and result.content:
                        content = result.content[0] if isinstance(result.content, list) else result.content
                        result_text = content.text if hasattr(content, 'text') else str(content)
                        
                        # Parse the actual file path from MCP response
                        import json
                        try:
                            mcp_response = json.loads(result_text)
                            if 'path' in mcp_response:
                                # MCP server saves to /workspace/generated-diagrams/filename.png
                                # This maps to outputs/diagrams/generated-diagrams/filename.png
                                container_path = mcp_response['path']
                                if '/workspace/generated-diagrams/' in container_path:
                                    filename_from_path = container_path.split('/')[-1]
                                    actual_path = os.path.join("outputs", "diagrams", "generated-diagrams", filename_from_path)
                                else:
                                    actual_path = os.path.join(workspace_dir, f"{filename}.png")
                            else:
                                actual_path = os.path.join(workspace_dir, f"{filename}.png")
                        except:
                            actual_path = os.path.join(workspace_dir, f"{filename}.png")
                        
                        # Normalize path separators
                        actual_path = os.path.normpath(actual_path)
                        
                        # Also create Draw.io version with diagram code
                        drawio_result = self.drawio_converter.convert_to_drawio(actual_path, filename, diagram_code)
                        
                        return {
                            "success": True, 
                            "result": result_text, 
                            "image_path": actual_path,
                            "drawio_result": drawio_result
                        }
                    else:
                        actual_path = os.path.join(workspace_dir, f"{filename}.png")
                        
                        # Also create Draw.io version with diagram code
                        drawio_result = self.drawio_converter.convert_to_drawio(actual_path, filename, diagram_code)
                        
                        return {
                            "success": True, 
                            "result": str(result), 
                            "image_path": actual_path,
                            "drawio_result": drawio_result
                        }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def call_rekognition_server(self, image_path: str, operation: str) -> Dict[str, Any]:
        return {"success": False, "error": "Rekognition not implemented"}