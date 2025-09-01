# Clean Project Structure

## Essential Files Only

```
Architecture-Diagram-MCP/
├── agents/                          # Core application logic
│   ├── bedrock_strands_agent.py    # Main agent with Claude 4 Sonnet
│   ├── docker_mcp_sdk_client.py    # MCP client
│   ├── drawio_converter.py         # PNG to DrawIO converter
│   └── simple_docker_client.py     # Alternative client
├── config/                          # AWS configuration
│   └── aws_config.py               # Bedrock client setup
├── awslabs-mcp-servers/mcp/src/     # MCP server (Docker)
│   └── aws-diagram-mcp-server/     # Only diagram server kept
├── outputs/                         # Generated files
│   ├── diagrams/                   # PNG and DrawIO files
│   └── rekognition/                # Analysis results
├── streamlit_app.py                # Web interface
├── docker-compose.yml              # Container setup
├── requirements.txt                # Dependencies
├── README.md                       # Documentation
├── run_app.bat                     # Windows launcher
├── run_app.py                      # Python launcher
└── .gitignore                      # Git ignore rules
```

## Removed Directories
- All other MCP servers (30+ directories)
- GitHub workflows and documentation
- Sample code and tutorials
- Unused fastapi_gateway
- Utility scripts

## Ready for Git Push
- Clean structure with only essential files
- Proper .gitignore configured
- All functionality preserved