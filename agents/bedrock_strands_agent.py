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
            response = self.bedrock.converse(modelId="anthropic.claude-4-sonnet-20250109-v1:0", **request_body)
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

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, ECS, EC2
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis, Glue, Athena
from diagrams.aws.network import APIGateway, VPC
from diagrams.aws.security import IAM, KMS
from diagrams.aws.ml import Sagemaker
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.database import RDS, DynamoDB

VERIFIED SERVICES ONLY:
- Lambda() for AWS Lambda
- APIGateway() for API Gateway
- Kinesis() for Kinesis Data Streams
- ECS() for ECS containers
- EC2() for EC2 instances
- S3() for S3 storage
- Glue() for AWS Glue ETL
- Athena() for Amazon Athena
- Sagemaker() for SageMaker
- RDS() for RDS databases
- DynamoDB() for DynamoDB
- VPC() for VPC networking
- KMS() for encryption
- IAM() for permissions
- SQS() for queues
- SNS() for notifications

FOR UNSUPPORTED SERVICES (Config, Security Hub, GuardDuty):
- Use generic Lambda() with descriptive labels like Lambda("Security Service")
- Or use IAM() for security-related services

Return ONLY the Python code, no explanations."""
        
        request_body = {
            "messages": [
                {"role": "user", "content": [{"text": f"{system_prompt}\n\nUser request: {user_prompt}"}]}
            ],
            "inferenceConfig": {"temperature": 0.1, "maxTokens": 400}
        }
        
        try:
            response = self.bedrock.converse(modelId="anthropic.claude-4-sonnet-20250109-v1:0", **request_body)
            diagram_code = response['output']['message']['content'][0]['text']
            
            # Extract code from markdown
            if "```python" in diagram_code:
                diagram_code = diagram_code.split("```python")[1].split("```")[0].strip()
            elif "```" in diagram_code:
                diagram_code = diagram_code.split("```")[1].split("```")[0].strip()
            
            # Validate and fix syntax
            try:
                compile(diagram_code, '<string>', 'exec')
            except SyntaxError as e:
                print(f"Syntax error detected: {e}")
                # Try to fix common issues
                diagram_code = diagram_code.replace('"', '"').replace('"', '"')  # Fix smart quotes
                diagram_code = diagram_code.replace(''', "'").replace(''', "'")  # Fix smart apostrophes
                try:
                    compile(diagram_code, '<string>', 'exec')
                    print("Fixed syntax error")
                except SyntaxError:
                    return {"success": False, "error": f"Syntax error in generated code: {e}"}
            
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
            return {
                "success": False,
                "error": str(e),
                "message": f"Diagram generation failed: {e}"
            }