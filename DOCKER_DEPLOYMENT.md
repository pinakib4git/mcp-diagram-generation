# Docker Deployment Guide

## Overview
This guide covers deploying the Bedrock Strands Agent with Enhanced DrawIO Converter using Docker containers.

## Architecture
```
┌─────────────────────────────────────┐
│     Bedrock Strands Agent           │
│  - Enhanced DrawIO Converter        │
│  - 51 AWS/K8s/Generic Services      │
│  - Connection Flow Analysis         │
│  - Streamlit Web Interface          │
│  Port: 8501                         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│     AWS Labs MCP Server             │
│  - Python Diagrams Generation      │
│  - PNG Output                       │
│  - Docker Container                 │
└─────────────────────────────────────┘
```

## Quick Start

### Windows
```bash
# Build and start all services
build-docker.bat

# Or manually:
docker-compose up --build -d
```

### Linux/macOS
```bash
# Make script executable
chmod +x build-docker.sh

# Build and start all services
./build-docker.sh

# Or manually:
docker-compose up --build -d
```

## Services

### Main Application (bedrock-strands-agent)
- **Image**: `bedrock-strands-agent:latest`
- **Port**: 8501
- **Features**:
  - Enhanced DrawIO Converter with 51 services
  - Connection flow analysis
  - AWS Bedrock integration
  - Streamlit web interface

### MCP Diagram Server
- **Image**: `awslabs/aws-diagram-mcp-server:latest`
- **Purpose**: Generate PNG diagrams from Python code
- **Volume**: `./outputs/diagrams:/workspace`

## Configuration

### Environment Variables
```yaml
environment:
  - AWS_PROFILE=default
  - PYTHONPATH=/app
  - PYTHONUNBUFFERED=1
```

### Volumes
```yaml
volumes:
  - ./outputs:/app/outputs  # Main app outputs
  - ./outputs/diagrams:/workspace  # MCP server workspace
```

## Usage

1. **Access Web Interface**
   ```
   http://localhost:8501
   ```

2. **Generate Architecture Diagram**
   - Enter description (e.g., "Create serverless analytics pipeline")
   - Click "Generate Diagram"
   - View PNG and DrawIO outputs

3. **Enhanced DrawIO Features**
   - Automatic service detection from code
   - Proper connection sequencing
   - 51 supported services across AWS, K8s, Generic platforms

## Docker Commands

### Build Images
```bash
# Build MCP server
cd awslabs-mcp-servers/mcp/src/aws-diagram-mcp-server
docker build -t awslabs/aws-diagram-mcp-server:latest .

# Build main application
docker build -t bedrock-strands-agent:latest .
```

### Manage Services
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

### Individual Container Management
```bash
# Run main app only
docker run -p 8501:8501 -v ./outputs:/app/outputs bedrock-strands-agent:latest

# Run MCP server only
docker run -v ./outputs/diagrams:/workspace awslabs/aws-diagram-mcp-server:latest
```

## Troubleshooting

### Common Issues

1. **Port 8501 already in use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8502:8501"  # Use different host port
   ```

2. **AWS credentials not found**
   ```bash
   # Mount AWS credentials
   volumes:
     - ~/.aws:/root/.aws:ro
   ```

3. **Permission issues with volumes**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER outputs/
   ```

### Logs and Debugging
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs bedrock-strands-agent
docker-compose logs mcp-diagram-server

# Follow logs in real-time
docker-compose logs -f
```

## Development

### Local Development with Docker
```bash
# Mount source code for development
docker run -p 8501:8501 \
  -v ./agents:/app/agents \
  -v ./config:/app/config \
  -v ./outputs:/app/outputs \
  bedrock-strands-agent:latest
```

### Updating Images
```bash
# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d
```

## Production Deployment

### Security Considerations
1. **Use secrets for AWS credentials**
2. **Enable HTTPS with reverse proxy**
3. **Restrict network access**
4. **Use non-root user in containers**

### Scaling
```yaml
# docker-compose.yml for scaling
services:
  bedrock-strands-agent:
    deploy:
      replicas: 3
    ports:
      - "8501-8503:8501"
```

## Enhanced Features in Docker

### DrawIO Converter Capabilities
- **51 Services**: AWS, Kubernetes, Generic, Container, Programming
- **Flow Analysis**: Parses `>>` connections from code
- **Service Ordering**: Topological sort for proper positioning
- **Multi-Platform**: Supports diverse architecture patterns

### Integration Benefits
- **Seamless**: Works with existing MCP server
- **Scalable**: Container-based deployment
- **Portable**: Runs anywhere Docker is available
- **Maintainable**: Clean separation of concerns