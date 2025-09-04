#!/usr/bin/env python3
import os
import base64
import json
from typing import Dict, Any, List
import sys
sys.path.append('..')
from config.aws_config import AWSConfig

class DrawIOConverter:
    """Convert PNG diagrams to Draw.io format with enhanced AWS service detection"""
    
    def __init__(self):
        self.aws_config = AWSConfig()
        self.bedrock = self.aws_config.get_bedrock_client()
        
        # Comprehensive service templates for DrawIO (AWS + other packages)
        self.aws_services = {
            # AWS Compute
            'lambda': {'shape': 'mxgraph.aws4.lambda_function', 'fillColor': '#ED7100', 'label': 'Lambda Function'},
            'ecs': {'shape': 'mxgraph.aws4.ecs', 'fillColor': '#FF9900', 'label': 'Amazon ECS'},
            'ec2': {'shape': 'mxgraph.aws4.ec2', 'fillColor': '#FF9900', 'label': 'EC2 Instance'},
            'fargate': {'shape': 'mxgraph.aws4.fargate', 'fillColor': '#FF9900', 'label': 'AWS Fargate'},
            'batch': {'shape': 'mxgraph.aws4.batch', 'fillColor': '#FF9900', 'label': 'AWS Batch'},
            
            # AWS Storage
            's3': {'shape': 'mxgraph.aws4.s3', 'fillColor': '#7AA116', 'label': 'S3 Bucket'},
            'efs': {'shape': 'mxgraph.aws4.efs', 'fillColor': '#7AA116', 'label': 'EFS'},
            'fsx': {'shape': 'mxgraph.aws4.fsx', 'fillColor': '#7AA116', 'label': 'FSx'},
            
            # AWS Database
            'rds': {'shape': 'mxgraph.aws4.rds', 'fillColor': '#3F48CC', 'label': 'RDS Database'},
            'dynamodb': {'shape': 'mxgraph.aws4.dynamodb', 'fillColor': '#3F48CC', 'label': 'DynamoDB'},
            'redshift': {'shape': 'mxgraph.aws4.redshift', 'fillColor': '#3F48CC', 'label': 'Redshift'},
            'elasticache': {'shape': 'mxgraph.aws4.elasticache', 'fillColor': '#3F48CC', 'label': 'ElastiCache'},
            'documentdb': {'shape': 'mxgraph.aws4.documentdb', 'fillColor': '#3F48CC', 'label': 'DocumentDB'},
            
            # AWS Analytics
            'kinesis': {'shape': 'mxgraph.aws4.kinesis_data_streams', 'fillColor': '#8C4FFF', 'label': 'Kinesis Data Streams'},
            'glue': {'shape': 'mxgraph.aws4.glue', 'fillColor': '#8C4FFF', 'label': 'AWS Glue'},
            'athena': {'shape': 'mxgraph.aws4.athena', 'fillColor': '#FF9900', 'label': 'Amazon Athena'},
            'emr': {'shape': 'mxgraph.aws4.emr', 'fillColor': '#8C4FFF', 'label': 'EMR'},
            'quicksight': {'shape': 'mxgraph.aws4.quicksight', 'fillColor': '#8C4FFF', 'label': 'QuickSight'},
            
            # AWS Network
            'api_gateway': {'shape': 'mxgraph.aws4.api_gateway', 'fillColor': '#FF4F8B', 'label': 'API Gateway'},
            'vpc': {'shape': 'mxgraph.aws4.vpc', 'fillColor': '#FF4F8B', 'label': 'VPC'},
            'elb': {'shape': 'mxgraph.aws4.elastic_load_balancing', 'fillColor': '#FF4F8B', 'label': 'Load Balancer'},
            'cloudfront': {'shape': 'mxgraph.aws4.cloudfront', 'fillColor': '#FF4F8B', 'label': 'CloudFront'},
            'route53': {'shape': 'mxgraph.aws4.route_53', 'fillColor': '#FF4F8B', 'label': 'Route 53'},
            
            # AWS Integration
            'sqs': {'shape': 'mxgraph.aws4.sqs', 'fillColor': '#FF4F8B', 'label': 'SQS Queue'},
            'sns': {'shape': 'mxgraph.aws4.sns', 'fillColor': '#FF4F8B', 'label': 'SNS Topic'},
            'eventbridge': {'shape': 'mxgraph.aws4.eventbridge', 'fillColor': '#FF4F8B', 'label': 'EventBridge'},
            'stepfunctions': {'shape': 'mxgraph.aws4.step_functions', 'fillColor': '#FF4F8B', 'label': 'Step Functions'},
            
            # AWS Security
            'iam': {'shape': 'mxgraph.aws4.iam', 'fillColor': '#DD344C', 'label': 'IAM Role'},
            'kms': {'shape': 'mxgraph.aws4.kms', 'fillColor': '#DD344C', 'label': 'KMS Key'},
            'cognito': {'shape': 'mxgraph.aws4.cognito', 'fillColor': '#DD344C', 'label': 'Cognito'},
            'waf': {'shape': 'mxgraph.aws4.waf', 'fillColor': '#DD344C', 'label': 'WAF'},
            'guardduty': {'shape': 'mxgraph.aws4.guardduty', 'fillColor': '#DD344C', 'label': 'GuardDuty'},
            
            # AWS ML/AI
            'sagemaker': {'shape': 'mxgraph.aws4.sagemaker', 'fillColor': '#01A88D', 'label': 'SageMaker'},
            'bedrock': {'shape': 'mxgraph.aws4.bedrock', 'fillColor': '#01A88D', 'label': 'Bedrock'},
            'comprehend': {'shape': 'mxgraph.aws4.comprehend', 'fillColor': '#01A88D', 'label': 'Comprehend'},
            'rekognition': {'shape': 'mxgraph.aws4.rekognition', 'fillColor': '#01A88D', 'label': 'Rekognition'},
            
            # Kubernetes
            'pod': {'shape': 'mxgraph.k8s.pod', 'fillColor': '#326CE5', 'label': 'Pod'},
            'service': {'shape': 'mxgraph.k8s.service', 'fillColor': '#326CE5', 'label': 'Service'},
            'deployment': {'shape': 'mxgraph.k8s.deployment', 'fillColor': '#326CE5', 'label': 'Deployment'},
            'configmap': {'shape': 'mxgraph.k8s.configmap', 'fillColor': '#326CE5', 'label': 'ConfigMap'},
            
            # Generic/OnPrem
            'database': {'shape': 'mxgraph.basic.database', 'fillColor': '#4285F4', 'label': 'Database'},
            'server': {'shape': 'mxgraph.basic.server', 'fillColor': '#34A853', 'label': 'Server'},
            'client': {'shape': 'mxgraph.basic.client', 'fillColor': '#FBBC04', 'label': 'Client'},
            'network': {'shape': 'mxgraph.basic.network', 'fillColor': '#EA4335', 'label': 'Network'},
            'storage': {'shape': 'mxgraph.basic.storage', 'fillColor': '#9AA0A6', 'label': 'Storage'},
            
            # Docker/Container
            'docker': {'shape': 'mxgraph.docker.docker', 'fillColor': '#2496ED', 'label': 'Docker'},
            'container': {'shape': 'mxgraph.docker.container', 'fillColor': '#2496ED', 'label': 'Container'},
            
            # Programming Languages
            'python': {'shape': 'mxgraph.programming.python', 'fillColor': '#3776AB', 'label': 'Python'},
            'java': {'shape': 'mxgraph.programming.java', 'fillColor': '#ED8B00', 'label': 'Java'},
            'nodejs': {'shape': 'mxgraph.programming.nodejs', 'fillColor': '#339933', 'label': 'Node.js'},
            'react': {'shape': 'mxgraph.programming.react', 'fillColor': '#61DAFB', 'label': 'React'}
        }
    
    def detect_services_from_code(self, diagram_code: str) -> List[str]:
        """Detect AWS services from Python diagram code"""
        detected_services = []
        
        # Comprehensive service detection from code patterns
        service_mappings = {
            # AWS Compute
            'Lambda(': 'lambda', 'ECS(': 'ecs', 'EC2(': 'ec2', 'Fargate(': 'fargate', 'Batch(': 'batch',
            
            # AWS Storage
            'S3(': 's3', 'EFS(': 'efs', 'FSx(': 'fsx',
            
            # AWS Database
            'RDS(': 'rds', 'Dynamodb(': 'dynamodb', 'Redshift(': 'redshift', 
            'ElastiCache(': 'elasticache', 'DocumentDB(': 'documentdb',
            
            # AWS Analytics
            'Kinesis(': 'kinesis', 'Glue(': 'glue', 'Athena(': 'athena', 
            'EMR(': 'emr', 'QuickSight(': 'quicksight',
            
            # AWS Network
            'APIGateway(': 'api_gateway', 'VPC(': 'vpc', 'ELB(': 'elb', 
            'CloudFront(': 'cloudfront', 'Route53(': 'route53',
            
            # AWS Integration
            'SQS(': 'sqs', 'SNS(': 'sns', 'EventBridge(': 'eventbridge', 
            'StepFunctions(': 'stepfunctions',
            
            # AWS Security
            'IAM(': 'iam', 'KMS(': 'kms', 'Cognito(': 'cognito', 
            'WAF(': 'waf', 'GuardDuty(': 'guardduty',
            
            # AWS ML/AI
            'Sagemaker(': 'sagemaker', 'Bedrock(': 'bedrock', 
            'Comprehend(': 'comprehend', 'Rekognition(': 'rekognition',
            
            # Kubernetes
            'Pod(': 'pod', 'Service(': 'service', 'Deployment(': 'deployment', 
            'ConfigMap(': 'configmap',
            
            # Generic
            'Database(': 'database', 'Server(': 'server', 'Client(': 'client',
            
            # Container/Docker
            'Docker(': 'docker', 'Container(': 'container'
        }
        
        for code_pattern, service_key in service_mappings.items():
            if code_pattern in diagram_code:
                detected_services.append(service_key)
        
        # Default if none detected
        if not detected_services:
            detected_services = ['lambda', 's3']
            
        return detected_services
    
    def parse_clusters_and_services(self, diagram_code: str) -> Dict[str, Any]:
        """Parse clusters, services, and connections from diagram code"""
        lines = diagram_code.split('\n')
        clusters = {}  # cluster_name -> {services: [], label: str}
        services = {}  # service_var -> {type: str, cluster: str}
        connections = []
        current_cluster = None
        
        # Parse clusters and services
        for line in lines:
            line = line.strip()
            
            # Detect cluster start: with Cluster("name"):
            if 'with Cluster(' in line and ':' in line:
                cluster_match = line.split('Cluster(')[1].split(')')[0].strip('"\'')
                current_cluster = cluster_match
                clusters[current_cluster] = {'services': [], 'label': cluster_match}
            
            # Detect service assignments
            elif '=' in line and any(service in line for service in ['Lambda(', 'S3(', 'Kinesis(', 'ECS(', 'APIGateway(', 'Dynamodb(', 'RDS(', 'SQS(', 'SNS(', 'Glue(', 'Athena(']):
                var_name = line.split('=')[0].strip()
                service_patterns = {
                    'Lambda(': 'lambda', 'S3(': 's3', 'Kinesis(': 'kinesis', 'ECS(': 'ecs', 
                    'APIGateway(': 'api_gateway', 'Dynamodb(': 'dynamodb', 'Glue(': 'glue', 
                    'Athena(': 'athena', 'RDS(': 'rds', 'SQS(': 'sqs', 'SNS(': 'sns',
                    'EMR(': 'emr', 'Redshift(': 'redshift', 'ELB(': 'elb', 'CloudFront(': 'cloudfront'
                }
                for pattern, service_type in service_patterns.items():
                    if pattern in line:
                        services[var_name] = {'type': service_type, 'cluster': current_cluster}
                        if current_cluster and current_cluster in clusters:
                            clusters[current_cluster]['services'].append(var_name)
                        break
            
            # Parse connections
            elif '>>' in line:
                parts = [p.strip() for p in line.split('>>')]
                for i in range(len(parts) - 1):
                    source_var = parts[i]
                    target_var = parts[i + 1]
                    if source_var in services and target_var in services:
                        connections.append((source_var, target_var))
        
        return {
            'clusters': clusters,
            'services': services,
            'connections': connections
        }
    
    def parse_service_flow(self, diagram_code: str) -> List[tuple]:
        """Parse service connection flow from diagram code (legacy method)"""
        parsed = self.parse_clusters_and_services(diagram_code)
        # Convert to service type connections for backward compatibility
        type_connections = []
        for source_var, target_var in parsed['connections']:
            source_type = parsed['services'][source_var]['type']
            target_type = parsed['services'][target_var]['type']
            type_connections.append((source_type, target_type))
        return type_connections
    
    def order_services_by_flow(self, services: List[str], connections: List[tuple]) -> List[str]:
        """Order services based on connection flow for proper positioning"""
        if not connections:
            return services
        
        # Build adjacency graph
        graph = {service: [] for service in services}
        in_degree = {service: 0 for service in services}
        
        for source, target in connections:
            if source in graph and target in graph:
                graph[source].append(target)
                in_degree[target] += 1
        
        # Topological sort to get proper order
        ordered = []
        queue = [service for service in services if in_degree[service] == 0]
        
        while queue:
            current = queue.pop(0)
            ordered.append(current)
            
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Add any remaining services not in the flow
        for service in services:
            if service not in ordered:
                ordered.append(service)
        
        return ordered
    
    def detect_services_from_filename(self, png_path: str) -> List[str]:
        """Fallback: Detect AWS services based on filename patterns"""
        filename = os.path.basename(png_path).lower()
        detected_services = []
        
        patterns = {
            'lambda': ['lambda', 'serverless', 'function'],
            's3': ['s3', 'storage', 'bucket'],
            'kinesis': ['kinesis', 'streaming', 'stream'],
            'glue': ['glue', 'etl', 'transform'],
            'ecs': ['ecs', 'container', 'docker'],
            'rds': ['rds', 'database', 'mysql', 'postgres'],
            'dynamodb': ['dynamo', 'nosql'],
            'api_gateway': ['api', 'gateway', 'rest'],
            'sqs': ['sqs', 'queue', 'message'],
            'sns': ['sns', 'notification', 'topic'],
            'vpc': ['vpc', 'network', 'subnet'],
            'emr': ['emr', 'hadoop', 'spark'],
            'redshift': ['redshift', 'warehouse', 'analytics']
        }
        
        for service, keywords in patterns.items():
            if any(keyword in filename for keyword in keywords):
                detected_services.append(service)
        
        return detected_services or ['lambda', 's3']
    
    def create_service_xml(self, service_key: str, cell_id: int, x: int, y: int) -> str:
        """Create XML for a specific AWS service"""
        service = self.aws_services.get(service_key, self.aws_services['lambda'])
        
        return f'''        <mxCell id="{cell_id}" value="{service['label']}" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={service['fillColor']};strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape={service['shape']};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="78" height="78" as="geometry"/>
        </mxCell>'''
    
    def create_connection_xml(self, cell_id: int, source_id: int, target_id: int) -> str:
        """Create XML for connection between services"""
        return f'''        <mxCell id="{cell_id}" value="" style="endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;" edge="1" parent="1" source="{source_id}" target="{target_id}">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="300" y="300" as="sourcePoint"/>
            <mxPoint x="350" y="250" as="targetPoint"/>
          </mxGeometry>
        </mxCell>'''
    
    def create_cluster_xml(self, cluster_name: str, cell_id: int, x: int, y: int, width: int, height: int) -> str:
        """Create XML for a cluster/group container"""
        return f'''        <mxCell id="{cell_id}" value="{cluster_name}" style="swimlane;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;startSize=30;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>'''
    
    def create_service_xml_in_cluster(self, service_key: str, cell_id: int, x: int, y: int, parent_id: int) -> str:
        """Create XML for a service within a cluster"""
        service = self.aws_services.get(service_key, self.aws_services['lambda'])
        
        return f'''        <mxCell id="{cell_id}" value="{service['label']}" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={service['fillColor']};strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape={service['shape']};" vertex="1" parent="{parent_id}">
          <mxGeometry x="{x}" y="{y}" width="78" height="78" as="geometry"/>
        </mxCell>'''
    
    def analyze_connection_flow(self, connections: List[tuple], services: Dict[str, Any]) -> Dict[str, int]:
        """Analyze connection flow to determine optimal service positioning"""
        # Build flow graph to determine layers
        in_degree = {}
        out_degree = {}
        
        for service_var in services.keys():
            in_degree[service_var] = 0
            out_degree[service_var] = 0
        
        for source, target in connections:
            if source in services and target in services:
                out_degree[source] += 1
                in_degree[target] += 1
        
        # Assign flow levels (0 = input, higher = downstream)
        flow_levels = {}
        processed = set()
        
        # Start with services that have no inputs (entry points)
        current_level = 0
        while len(processed) < len(services):
            level_services = []
            for service_var in services.keys():
                if service_var not in processed:
                    # Check if all dependencies are processed
                    dependencies_ready = True
                    for source, target in connections:
                        if target == service_var and source not in processed:
                            dependencies_ready = False
                            break
                    
                    if dependencies_ready:
                        level_services.append(service_var)
            
            if not level_services:  # Avoid infinite loop
                for service_var in services.keys():
                    if service_var not in processed:
                        level_services.append(service_var)
                        break
            
            for service_var in level_services:
                flow_levels[service_var] = current_level
                processed.add(service_var)
            
            current_level += 1
        
        return flow_levels
    
    def create_optimized_connection_xml(self, cell_id: int, source_id: int, target_id: int, 
                                      source_pos: tuple, target_pos: tuple) -> str:
        """Create optimized connection XML with better routing"""
        sx, sy = source_pos
        tx, ty = target_pos
        
        # Determine connection style based on relative positions
        if abs(sx - tx) > abs(sy - ty):  # Horizontal flow
            if sx < tx:  # Left to right
                exit_x, exit_y = "1", "0.5"  # Right side of source
                entry_x, entry_y = "0", "0.5"  # Left side of target
            else:  # Right to left
                exit_x, exit_y = "0", "0.5"  # Left side of source
                entry_x, entry_y = "1", "0.5"  # Right side of target
        else:  # Vertical flow
            if sy < ty:  # Top to bottom
                exit_x, exit_y = "0.5", "1"  # Bottom of source
                entry_x, entry_y = "0.5", "0"  # Top of target
            else:  # Bottom to top
                exit_x, exit_y = "0.5", "0"  # Top of source
                entry_x, entry_y = "0.5", "1"  # Bottom of target
        
        return f'''        <mxCell id="{cell_id}" value="" style="endArrow=classic;html=1;rounded=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;exitPerimeter=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;entryPerimeter=0;strokeWidth=2;strokeColor=#666666;" edge="1" parent="1" source="{source_id}" target="{target_id}">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="{sx + 39}" y="{sy + 39}" as="sourcePoint"/>
            <mxPoint x="{tx + 39}" y="{ty + 39}" as="targetPoint"/>
          </mxGeometry>
        </mxCell>'''
    
    def create_layered_drawio_xml(self, diagram_name: str, diagram_code: str) -> str:
        """Create DrawIO XML with optimized layout and connector positioning"""
        parsed = self.parse_clusters_and_services(diagram_code)
        clusters = parsed['clusters']
        services = parsed['services']
        connections = parsed['connections']
        
        # Analyze flow for optimal positioning
        flow_levels = self.analyze_connection_flow(connections, services)
        
        all_xml = []
        service_positions = {}  # service_var -> (cell_id, x, y)
        cell_id = 2
        
        # Enhanced layout parameters
        cluster_base_width = 250
        cluster_base_height = 180
        cluster_spacing = 80
        service_spacing = 120
        level_spacing = 200
        
        # Organize clusters by flow levels
        cluster_levels = {}
        for cluster_name, cluster_data in clusters.items():
            if cluster_data['services']:
                # Use minimum flow level of services in cluster
                min_level = min(flow_levels.get(svc, 0) for svc in cluster_data['services'])
                if min_level not in cluster_levels:
                    cluster_levels[min_level] = []
                cluster_levels[min_level].append(cluster_name)
        
        # Create clusters with flow-based positioning
        for level, cluster_names in sorted(cluster_levels.items()):
            cluster_y = 100 + (level * level_spacing)
            cluster_x = 50
            
            for cluster_name in cluster_names:
                cluster_data = clusters[cluster_name]
                
                # Calculate cluster size based on service count
                service_count = len(cluster_data['services'])
                services_per_row = min(3, service_count)
                rows = (service_count + services_per_row - 1) // services_per_row
                
                cluster_width = cluster_base_width + (services_per_row - 1) * 50
                cluster_height = cluster_base_height + (rows - 1) * 100
                
                cluster_id = cell_id
                cell_id += 1
                
                # Create cluster container
                all_xml.append(self.create_cluster_xml(cluster_name, cluster_id, cluster_x, cluster_y, cluster_width, cluster_height))
                
                # Position services within cluster in grid layout
                service_x = 30
                service_y = 50
                col = 0
                
                for service_var in cluster_data['services']:
                    service_type = services[service_var]['type']
                    service_id = cell_id
                    cell_id += 1
                    
                    all_xml.append(self.create_service_xml_in_cluster(service_type, service_id, service_x, service_y, cluster_id))
                    service_positions[service_var] = (service_id, cluster_x + service_x, cluster_y + service_y)
                    
                    col += 1
                    if col >= services_per_row:
                        col = 0
                        service_x = 30
                        service_y += 100
                    else:
                        service_x += service_spacing
                
                cluster_x += cluster_width + cluster_spacing
        
        # Add standalone services organized by flow levels
        standalone_services = {var: data for var, data in services.items() if data['cluster'] is None}
        standalone_levels = {}
        
        for service_var in standalone_services:
            level = flow_levels.get(service_var, 0)
            if level not in standalone_levels:
                standalone_levels[level] = []
            standalone_levels[level].append(service_var)
        
        for level, service_vars in sorted(standalone_levels.items()):
            standalone_y = 100 + (level * level_spacing)
            standalone_x = 50
            
            for service_var in service_vars:
                service_data = services[service_var]
                service_id = cell_id
                cell_id += 1
                
                all_xml.append(self.create_service_xml(service_data['type'], service_id, standalone_x, standalone_y))
                service_positions[service_var] = (service_id, standalone_x, standalone_y)
                
                standalone_x += 180
        
        # Create optimized connections
        connection_id = cell_id
        for source_var, target_var in connections:
            if source_var in service_positions and target_var in service_positions:
                source_id, sx, sy = service_positions[source_var]
                target_id, tx, ty = service_positions[target_var]
                all_xml.append(self.create_optimized_connection_xml(connection_id, source_id, target_id, (sx, sy), (tx, ty)))
                connection_id += 1
        
        content = '\n'.join(all_xml)
        
        return f'''<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="5.0 (Windows)" version="22.1.11" etag="generated" type="device">
  <diagram name="{diagram_name}" id="generated">
    <mxGraphModel dx="1800" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{content}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    def create_enhanced_drawio_xml(self, diagram_name: str, services: List[str], connections: List[tuple] = None) -> str:
        """Create enhanced DrawIO XML with optimized flat layout"""
        
        # Reorder services based on connection flow
        if connections:
            ordered_services = self.order_services_by_flow(services, connections)
        else:
            ordered_services = services
        
        # Create service position mapping with improved layout
        service_positions = {}  # service -> (cell_id, x, y)
        services_xml = []
        
        # Enhanced layout parameters
        services_per_row = min(4, len(ordered_services))
        x_spacing = 180
        y_spacing = 150
        x_start = 100
        y_start = 150
        
        cell_id = 2
        
        # Create service cells with grid positioning
        for i, service in enumerate(ordered_services):
            row = i // services_per_row
            col = i % services_per_row
            
            x_pos = x_start + (col * x_spacing)
            y_pos = y_start + (row * y_spacing)
            
            services_xml.append(self.create_service_xml(service, cell_id, x_pos, y_pos))
            service_positions[service] = (cell_id, x_pos, y_pos)
            cell_id += 1
        
        # Create optimized connections
        connections_xml = []
        connection_id = cell_id
        
        if connections:
            # Use parsed connections with optimized routing
            for source_service, target_service in connections:
                if source_service in service_positions and target_service in service_positions:
                    source_id, sx, sy = service_positions[source_service]
                    target_id, tx, ty = service_positions[target_service]
                    connections_xml.append(self.create_optimized_connection_xml(connection_id, source_id, target_id, (sx, sy), (tx, ty)))
                    connection_id += 1
        else:
            # Default linear connections with better routing
            for i in range(len(ordered_services) - 1):
                source_service = ordered_services[i]
                target_service = ordered_services[i + 1]
                source_id, sx, sy = service_positions[source_service]
                target_id, tx, ty = service_positions[target_service]
                connections_xml.append(self.create_optimized_connection_xml(connection_id, source_id, target_id, (sx, sy), (tx, ty)))
                connection_id += 1
        
        services_content = '\n'.join(services_xml)
        connections_content = '\n'.join(connections_xml)
        
        return f'''<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="5.0 (Windows)" version="22.1.11" etag="generated" type="device">
  <diagram name="{diagram_name}" id="generated">
    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="1000" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{services_content}
{connections_content}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    def create_working_drawio_xml(self, diagram_name: str) -> str:
        """Create basic DrawIO XML template (legacy method)"""
        return self.create_enhanced_drawio_xml(diagram_name, ['lambda', 's3'], None)
    
    def convert_to_drawio(self, png_path: str, diagram_name: str, diagram_code: str = None) -> Dict[str, Any]:
        """Convert PNG to Draw.io format using diagram code metadata with cluster support"""
        
        if not os.path.exists(png_path):
            return {"success": False, "error": "PNG file not found"}
        
        try:
            if diagram_code:
                # Check if diagram has clusters
                if 'with Cluster(' in diagram_code:
                    # Use layered approach for cluster-based diagrams
                    drawio_xml = self.create_layered_drawio_xml(diagram_name, diagram_code)
                    parsed = self.parse_clusters_and_services(diagram_code)
                    detected_services = [s['type'] for s in parsed['services'].values()]
                    detection_method = "layered_diagram_code"
                else:
                    # Use flat approach for simple diagrams
                    detected_services = self.detect_services_from_code(diagram_code)
                    service_connections = self.parse_service_flow(diagram_code)
                    drawio_xml = self.create_enhanced_drawio_xml(diagram_name, detected_services, service_connections)
                    detection_method = "flat_diagram_code"
            else:
                # Fallback to filename detection
                detected_services = self.detect_services_from_filename(png_path)
                drawio_xml = self.create_enhanced_drawio_xml(diagram_name, detected_services, None)
                detection_method = "filename"
            
            # Save as .drawio file
            drawio_path = png_path.replace('.png', '.drawio')
            with open(drawio_path, 'w', encoding='utf-8') as f:
                f.write(drawio_xml)
            
            return {
                "success": True,
                "drawio_path": drawio_path,
                "detected_services": detected_services,
                "detection_method": detection_method,
                "message": f"Draw.io file created using {detection_method} with services: {', '.join(detected_services)}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}