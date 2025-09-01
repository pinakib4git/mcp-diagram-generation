#!/usr/bin/env python3
import subprocess
import os
import json
from typing import Dict, Any

class SimpleDockerClient:
    """Simple Docker client that avoids MCP SDK issues"""
    
    async def call_diagram_server(self, diagram_code: str, filename: str = "architecture_diagram", workspace_dir: str = None) -> Dict[str, Any]:
        """Call Docker MCP server directly without SDK"""
        
        if not workspace_dir:
            workspace_dir = os.path.abspath("outputs/diagrams/generated-diagrams")
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Create a temporary Python file with the diagram code
        temp_file = os.path.join(workspace_dir, f"{filename}_temp.py")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(diagram_code)
        
        try:
            # Run Docker container to execute the diagram code
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{workspace_dir}:/workspace",
                "-w", "/workspace",
                "python:3.11-slim",
                "sh", "-c", 
                f"pip install diagrams && python {filename}_temp.py"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            if result.returncode == 0:
                # Check if PNG was created
                png_path = os.path.join(workspace_dir, f"{filename}.png")
                if os.path.exists(png_path):
                    return {
                        "success": True,
                        "result": {"status": "success", "message": "Diagram generated"},
                        "image_path": png_path
                    }
                else:
                    return {"success": False, "error": "PNG file not created"}
            else:
                return {"success": False, "error": f"Docker error: {result.stderr}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def call_rekognition_server(self, image_path: str, operation: str) -> Dict[str, Any]:
        return {"success": False, "error": "Rekognition not implemented"}