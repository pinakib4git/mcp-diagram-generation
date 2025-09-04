@echo off
echo Building Docker images for Bedrock Strands Agent with Enhanced DrawIO Converter...

echo.
echo Step 1: Building MCP Diagram Server...
cd awslabs-mcp-servers\mcp\src\aws-diagram-mcp-server
docker build -t awslabs/aws-diagram-mcp-server:latest .
cd ..\..\..\..\

echo.
echo Step 2: Building Main Application...
docker build -t bedrock-strands-agent:latest .

echo.
echo Step 3: Starting services with docker-compose...
docker-compose up -d

echo.
echo Build complete! Services are running:
echo - Main App: http://localhost:8501
echo - MCP Server: Container running in background
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down