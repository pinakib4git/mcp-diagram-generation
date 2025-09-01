#!/usr/bin/env python3
import boto3
import os
from typing import Dict, Any

class AWSConfig:
    """AWS Configuration for us-east-1 region with profile support"""
    
    def __init__(self, profile_name: str = "default", region: str = "us-east-1"):
        self.profile_name = profile_name
        self.region = region
        self.session = boto3.Session(profile_name=profile_name, region_name=region)
    
    def get_bedrock_client(self):
        """Get Bedrock Runtime client"""
        return self.session.client('bedrock-runtime', region_name=self.region)
    
    def get_rekognition_client(self):
        """Get Rekognition client"""
        return self.session.client('rekognition', region_name=self.region)
    
    def get_s3_client(self):
        """Get S3 client for diagram storage"""
        return self.session.client('s3', region_name=self.region)
    
    def validate_credentials(self) -> bool:
        """Validate AWS credentials"""
        try:
            sts = self.session.client('sts')
            sts.get_caller_identity()
            return True
        except Exception:
            return False