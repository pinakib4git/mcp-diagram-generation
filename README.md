# Bedrock Strands Agent with Enhanced DrawIO Converter

A comprehensive system that uses AWS Bedrock to generate Python diagrams code, calls AWS Labs MCP diagram server to create PNG architecture diagrams, and automatically converts them to DrawIO format with enhanced service detection.

## Enhanced Architecture Flow

```
Natural Language → AWS Bedrock → Python Code → MCP Server → PNG Diagram
                                     ↓
                             Enhanced DrawIO Converter
                                     ↓
                         DrawIO XML (51 Services Supported)
```

## Key Features

- **Enhanced DrawIO Converter**: Supports 51 services across AWS, Kubernetes, Generic, and Container platforms
- **Intelligent Service Detection**: Analyzes Python diagram code for accurate service identification
- **Connection Flow Analysis**: Parses `>>` operators to create proper connector sequences
- **Multi-Platform Support**: AWS, Kubernetes, Generic/OnPrem, Docker, Programming languages
- **Docker Deployment**: Complete containerized solution

## Quick Start - Docker Deployment

### Prerequisites
1. Docker and Docker Compose installed
2. AWS credentials configured
3. Git repository cloned

### Deploy with Docker

**Windows:**
```bash
build-docker.bat
```

**Linux/macOS:**
```bash
chmod +x build-docker.sh
./build-docker.sh
```

**Manual Docker Compose:**
```bash
docker-compose up --build -d
```

### Access the Application
1. Open web browser to http://localhost:8501
2. Enter architecture description (e.g., "Create serverless analytics pipeline with Lambda, Kinesis, S3, and Athena")
3. Click "Generate Diagram"
4. View generated PNG and DrawIO files with proper service detection

## Local Development

### Prerequisites
1. Python 3.11+
2. Install dependencies: `pip install -r requirements.txt`
3. Configure AWS credentials for Bedrock access
4. Docker running (for MCP server)

### Run Locally

**Option 1: Windows Batch**
```bash
run_app.bat
```

**Option 2: Python Script**
```bash
python run_app.py
```

**Option 3: Direct Streamlit**
```bash
streamlit run streamlit_app.py
```

## Enhanced DrawIO Converter Features

### Supported Services (51 total)

#### AWS Services (38)
- **Compute**: Lambda, ECS, EC2, Fargate, Batch
- **Storage**: S3, EFS, FSx
- **Database**: RDS, DynamoDB, Redshift, ElastiCache, DocumentDB
- **Analytics**: Kinesis, Glue, Athena, EMR, QuickSight
- **Network**: API Gateway, VPC, ELB, CloudFront, Route 53
- **Integration**: SQS, SNS, EventBridge, Step Functions
- **Security**: IAM, KMS, Cognito, WAF, GuardDuty
- **ML/AI**: SageMaker, Bedrock, Comprehend, Rekognition

#### Other Platforms (13)
- **Kubernetes**: Pod, Service, Deployment, ConfigMap
- **Generic/OnPrem**: Database, Server, Client, Network, Storage
- **Container**: Docker, Container
- **Programming**: Python, Java, Node.js, React

### Advanced Capabilities
- **Code Analysis**: Detects services from Python diagram code patterns
- **Flow Parsing**: Analyzes `>>` connections for proper sequencing
- **Service Ordering**: Uses topological sort for logical positioning
- **DrawIO Integration**: Generates proper XML with AWS4 shapes and colors

## Project Structure

- **agents/drawio_converter.py**: Enhanced DrawIO converter with 51 services
- **agents/bedrock_strands_agent.py**: Main agent using Bedrock + MCP
- **agents/docker_mcp_sdk_client.py**: MCP client using official SDK
- **config/aws_config.py**: AWS configuration management
- **streamlit_app.py**: Web interface for diagram generation
- **Dockerfile**: Container definition for main application
- **docker-compose.yml**: Multi-service deployment configuration
- **outputs/diagrams/**: Generated PNG and DrawIO files
- **awslabs-mcp-servers/**: Official AWS Labs MCP server

## Architecture Benefits

- **Comprehensive Service Support**: 51 services across multiple platforms
- **Intelligent Detection**: Accurate service identification from code
- **Proper Flow Representation**: Connections follow actual architecture flow
- **Container Deployment**: Scalable Docker-based solution
- **Multi-Format Output**: PNG diagrams + DrawIO files for editing

## Docker Services

### Main Application Container
- **Image**: `bedrock-strands-agent:latest`
- **Port**: 8501
- **Features**: Enhanced DrawIO converter, Bedrock integration, Streamlit UI

### MCP Diagram Server Container
- **Image**: `awslabs/aws-diagram-mcp-server:latest`
- **Purpose**: Python diagrams to PNG conversion
- **Integration**: Seamless communication with main application

## Documentation

- **DOCKER_DEPLOYMENT.md**: Complete Docker deployment guide
- **README.md**: This file - project overview and quick start
- **CLEAN_PROJECT_STRUCTURE.md**: Project organization details

For detailed Docker deployment instructions, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md).