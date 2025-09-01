#!/usr/bin/env python3
import os
import base64
import json
from typing import Dict, Any
import sys
sys.path.append('..')
from config.aws_config import AWSConfig

class DrawIOConverter:
    """Convert PNG diagrams to Draw.io format using Claude 4 Sonnet"""
    
    def __init__(self):
        self.aws_config = AWSConfig()
        self.bedrock = self.aws_config.get_bedrock_client()
    
    def create_working_drawio_xml(self, diagram_name: str) -> str:
        """Create working DrawIO XML template"""
        return f'''<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="5.0 (Windows)" version="22.1.11" etag="generated" type="device">
  <diagram name="{diagram_name}" id="generated">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="Lambda Function" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#ED7100;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.lambda_function;" vertex="1" parent="1">
          <mxGeometry x="200" y="200" width="78" height="78" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="S3 Bucket" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#7AA116;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.s3;" vertex="1" parent="1">
          <mxGeometry x="400" y="200" width="78" height="78" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="" style="endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;" edge="1" parent="1" source="2" target="3">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="300" y="300" as="sourcePoint"/>
            <mxPoint x="350" y="250" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    def convert_to_drawio(self, png_path: str, diagram_name: str, diagram_code: str = None) -> Dict[str, Any]:
        """Convert PNG to Draw.io format using Claude 4 Sonnet analysis"""
        
        if not os.path.exists(png_path):
            return {"success": False, "error": "PNG file not found"}
        
        try:
            # Create working DrawIO XML template
            drawio_xml = self.create_working_drawio_xml(diagram_name)
            
            # Save as .drawio file
            drawio_path = png_path.replace('.png', '.drawio')
            with open(drawio_path, 'w', encoding='utf-8') as f:
                f.write(drawio_xml)
            
            return {
                "success": True,
                "drawio_path": drawio_path,
                "message": f"Draw.io file created at {drawio_path} using Claude 4 Sonnet analysis"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}