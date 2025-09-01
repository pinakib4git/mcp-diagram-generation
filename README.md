# Bedrock Strands Agent with MCP Integration

A system that uses AWS Bedrock to generate Python diagrams code, then calls AWS Labs MCP diagram server running in Docker container to generate PNG architecture diagrams.

## Architecture Flow

```
Natural Language → AWS Bedrock → Python Code → Docker MCP Server → PNG Diagram
```

## Quick Start - Streamlit Demo

### Prerequisites
1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS credentials for Bedrock access
3. Ensure Docker is running (for MCP server)

### Run the Demo App

**Option 1: Windows Batch File**
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

### Usage
1. Open the web app (usually at http://localhost:8501)
2. Enter your architecture description (e.g., "Create a serverless analytics pipeline with Lambda, S3, Kinesis, and OpenSearch")
3. Click "Generate Diagram"
4. View the generated Python code and PNG diagram

## Project Structure

- **streamlit_app.py**: Simple web interface for diagram generation
- **agents/bedrock_strands_agent.py**: Main agent using Bedrock + MCP
- **agents/docker_mcp_sdk_client.py**: MCP client using official SDK
- **config/aws_config.py**: AWS configuration management
- **outputs/diagrams/**: Generated PNG diagrams storage
- **awslabs-mcp-servers/**: Official AWS Labs MCP server

## Key Features

- **Natural Language Processing**: Convert plain English to architecture diagrams
- **Official MCP Protocol**: Uses AWS Labs MCP server via Docker
- **Bedrock Integration**: Leverages Claude 3.5 Sonnet for code generation
- **Web Interface**: Simple Streamlit app for easy demonstration
- **PNG Output**: Generates high-quality architecture diagrams