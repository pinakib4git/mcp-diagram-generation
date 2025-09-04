#!/usr/bin/env python3
import asyncio
import json
import os
import base64
from typing import Dict, Any
import sys
sys.path.append('..')

from config.aws_config import AWSConfig
from agents.docker_mcp_sdk_client import DockerMCPSDKClient

class BedrockStrandsAgent:
    """Bedrock Strands Agent with MCP server integration"""
    
    def __init__(self, aws_profile: str = "default"):
        self.aws_config = AWSConfig(profile_name=aws_profile)
        self.bedrock = self.aws_config.get_bedrock_client()
        self.mcp_client = DockerMCPSDKClient()
        self.output_dir = "outputs"
        os.makedirs(f"{self.output_dir}/diagrams", exist_ok=True)
        os.makedirs(f"{self.output_dir}/rekognition", exist_ok=True)
        
    async def analyze_image_with_rekognition(self, image_path: str, user_prompt: str) -> Dict[str, Any]:
        """Analyze image using Rekognition MCP server with Bedrock enhancement"""
        
        # Use Bedrock to determine best Rekognition operation
        system_prompt = """You are an AWS Rekognition expert. Based on the user's request, determine the best Rekognition operation.
        
Available operations: detect_labels, detect_text, detect_moderation_labels, recognize_celebrities
        
Return only the operation name."""
        
        request_body = {
            "messages": [
                {"role": "user", "content": [{"text": f"{system_prompt}\n\nUser request: {user_prompt}"}]}
            ],
            "inferenceConfig": {"temperature": 0.1, "maxTokens": 100}
        }
        
        try:
            response = self.bedrock.converse(modelId="us.anthropic.claude-sonnet-4-20250514-v1:0", **request_body)
            operation = response['output']['message']['content'][0]['text'].strip()
            
            # Call Rekognition MCP server directly
            mcp_result = await self.mcp_client.call_rekognition_server(image_path, operation)
            
            # Save results
            result_file = os.path.join(f"{self.output_dir}/rekognition", f"analysis_{operation}.json")
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump({
                    "user_prompt": user_prompt,
                    "operation": operation,
                    "image_path": image_path,
                    "mcp_result": mcp_result
                }, f, indent=2)
            
            return {
                "success": True,
                "operation": operation,
                "result": mcp_result,
                "output_file": result_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Rekognition analysis failed: {e}"
            }
    
    async def generate_architecture_diagram(self, user_prompt: str, diagram_name: str) -> Dict[str, Any]:
        """Generate architecture diagram using MCP server with Bedrock"""
        
        system_prompt = """Generate ONLY Python diagrams code. Use ONLY these verified AWS services with proper icons:
from diagrams.saas.observability import *
from diagrams.saas.crm import *
from diagrams.saas.identity import *
from diagrams.saas.chat import *
from diagrams.saas.recommendation import *
from diagrams.saas.cdn import *
from diagrams.saas.communication import *
from diagrams.saas.media import *
from diagrams.saas.logging import *
from diagrams.saas.security import *
from diagrams.saas.social import *
from diagrams.saas.alerting import *
from diagrams.saas.analytics import *
from diagrams.saas.automation import *
from diagrams.saas.filesharing import *
from diagrams.onprem.vcs import *
from diagrams.onprem.database import *
from diagrams.onprem.gitops import *
from diagrams.onprem.workflow import *
from diagrams.onprem.etl import *
from diagrams.onprem.inmemory import *
from diagrams.onprem.identity import *
from diagrams.onprem.network import *
from diagrams.onprem.proxmox import *
from diagrams.onprem.cd import *
from diagrams.onprem.container import *
from diagrams.onprem.certificates import *
from diagrams.onprem.mlops import *
from diagrams.onprem.dns import *
from diagrams.onprem.compute import *
from diagrams.onprem.logging import *
from diagrams.onprem.registry import *
from diagrams.onprem.security import *
from diagrams.onprem.client import *
from diagrams.onprem.groupware import *
from diagrams.onprem.iac import *
from diagrams.onprem.analytics import *
from diagrams.onprem.messaging import *
from diagrams.onprem.tracing import *
from diagrams.onprem.ci import *
from diagrams.onprem.search import *
from diagrams.onprem.storage import *
from diagrams.onprem.auth import *
from diagrams.onprem.monitoring import *
from diagrams.onprem.aggregator import *
from diagrams.onprem.queue import *
from diagrams.gis.database import *
from diagrams.gis.cli import *
from diagrams.gis.server import *
from diagrams.gis.python import *
from diagrams.gis.organization import *
from diagrams.gis.cplusplus import *
from diagrams.gis.mobile import *
from diagrams.gis.javascript import *
from diagrams.gis.desktop import *
from diagrams.gis.ogc import *
from diagrams.gis.java import *
from diagrams.gis.routing import *
from diagrams.gis.data import *
from diagrams.gis.geocoding import *
from diagrams.gis.format import *
from diagrams.elastic.saas import *
from diagrams.elastic.observability import *
from diagrams.elastic.elasticsearch import *
from diagrams.elastic.orchestration import *
from diagrams.elastic.security import *
from diagrams.elastic.beats import *
from diagrams.elastic.enterprisesearch import *
from diagrams.elastic.agent import *
from diagrams.programming.runtime import *
from diagrams.programming.framework import *
from diagrams.programming.flowchart import *
from diagrams.programming.language import *
from diagrams.gcp.storage import *
from diagrams.generic.database import *
from diagrams.generic.blank import *
from diagrams.generic.network import *
from diagrams.generic.virtualization import *
from diagrams.generic.place import *
from diagrams.generic.device import *
from diagrams.generic.compute import *
from diagrams.generic.os import *
from diagrams.generic.storage import *
from diagrams.k8s.others import *
from diagrams.k8s.rbac import *
from diagrams.k8s.network import *
from diagrams.k8s.ecosystem import *
from diagrams.k8s.compute import *
from diagrams.k8s.chaos import *
from diagrams.k8s.infra import *
from diagrams.k8s.podconfig import *
from diagrams.k8s.controlplane import *
from diagrams.k8s.clusterconfig import *
from diagrams.k8s.storage import *
from diagrams.k8s.group import *
from diagrams.aws.cost import *
from diagrams.aws.ar import *
from diagrams.aws.general import *
from diagrams.aws.database import *
from diagrams.aws.management import *
from diagrams.aws.ml import *
from diagrams.aws.game import *
from diagrams.aws.enablement import *
from diagrams.aws.network import *
from diagrams.aws.quantum import *
from diagrams.aws.iot import *
from diagrams.aws.robotics import *
from diagrams.aws.migration import *
from diagrams.aws.mobile import *
from diagrams.aws.compute import *
from diagrams.aws.media import *
from diagrams.aws.engagement import *
from diagrams.aws.security import *
from diagrams.aws.devtools import *
from diagrams.aws.integration import *
from diagrams.aws.business import *
from diagrams.aws.analytics import *
from diagrams.aws.blockchain import *
from diagrams.aws.storage import *
from diagrams.aws.satellite import *
from diagrams.aws.enduser import *
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, ECS, EC2
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis, Glue, Athena
from diagrams.aws.network import APIGateway, VPC
from diagrams.aws.security import IAM, KMS
from diagrams.aws.ml import Sagemaker
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.database import RDS, Dynamodb


FOR UNSUPPORTED SERVICES (outside of the list above):
- Use generic Lambda() with descriptive labels like Lambda("Security Service")
- Or use IAM() for security-related services

Return ONLY the Python code, no explanations."""
        
        request_body = {
            "messages": [
                {"role": "user", "content": [{"text": f"{system_prompt}\n\nUser request: {user_prompt}"}]}
            ],
            "inferenceConfig": {"temperature": 0.1, "maxTokens": 8192}
        }
        
        try:
            response = self.bedrock.converse(modelId="us.anthropic.claude-sonnet-4-20250514-v1:0", **request_body)
            diagram_code = response['output']['message']['content'][0]['text']
            
            # Extract code from markdown
            if "```python" in diagram_code:
                diagram_code = diagram_code.split("```python")[1].split("```")[0].strip()
            elif "```" in diagram_code:
                diagram_code = diagram_code.split("```")[1].split("```")[0].strip()
            
            # Clean up any remaining markdown or formatting issues
            diagram_code = diagram_code.replace('\r\n', '\n').replace('\r', '\n')
            # Fix escaped quotes that might cause issues
            diagram_code = diagram_code.replace('\\"', '"')
            # Remove any trailing backslashes that might escape quotes
            lines = diagram_code.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.rstrip('\\')  # Remove trailing backslashes
                if line.strip():
                    cleaned_lines.append(line)
            diagram_code = '\n'.join(cleaned_lines)
            
            # Validate and fix syntax
            try:
                compile(diagram_code, '<string>', 'exec')
            except SyntaxError as e:
                print(f"Syntax error detected: {e}")
                print(f"Generated code: {diagram_code}")
                # Try to fix common issues
                diagram_code = diagram_code.replace('"', '"').replace('"', '"')  # Fix smart quotes
                diagram_code = diagram_code.replace(''', "'").replace(''', "'")  # Fix smart apostrophes
                # Fix string literal and parenthesis issues
                lines = diagram_code.split('\n')
                fixed_lines = []
                open_parens = 0
                
                for i, line in enumerate(lines):
                    # Check for unterminated strings
                    if '"' in line:
                        quote_count = line.count('"')
                        if quote_count % 2 != 0:  # Odd number of quotes
                            line = line.rstrip() + '"'  # Add closing quote
                    
                    # Track parentheses
                    open_parens += line.count('(') - line.count(')')
                    fixed_lines.append(line)
                
                # Close any unclosed parentheses
                if open_parens > 0:
                    fixed_lines.append(')' * open_parens)
                
                # Ensure code ends properly
                last_line = fixed_lines[-1].strip() if fixed_lines else ''
                if not last_line or (not last_line.endswith((')', '"', "'")) and '>>' not in last_line):
                    # Add a simple connection if code seems incomplete
                    if 'api_gateway' in diagram_code and 'ingestion_lambda' in diagram_code:
                        fixed_lines.append('    api_gateway >> ingestion_lambda')
                
                diagram_code = '\n'.join(fixed_lines)
                try:
                    compile(diagram_code, '<string>', 'exec')
                    print("Fixed syntax error")
                except SyntaxError as e2:
                    return {"success": False, "error": f"Syntax error in generated code: {e2}\n\nGenerated code:\n{diagram_code}"}
            
            # Call MCP server with generated code
            mcp_result = await self.mcp_client.call_diagram_server(
                diagram_code, 
                diagram_name, 
                os.path.abspath(self.output_dir + "/diagrams/generated-diagrams")
            )
            
            # Save results
            result_file = os.path.join(f"{self.output_dir}/diagrams", "architecture_result.json")
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump({
                    "user_prompt": user_prompt,
                    "diagram_code": diagram_code,
                    "mcp_result": mcp_result
                }, f, indent=2)
            
            return {
                "success": True,
                "diagram_code": diagram_code,
                "result": mcp_result,
                "output_file": result_file
            }
            
        except Exception as e:
            print(f"Full error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Diagram generation failed: {e}. Make sure Docker is running and MCP server is available."
            }