#!/usr/bin/env python3
import streamlit as st
import asyncio
import os
from agents.bedrock_strands_agent import BedrockStrandsAgent

# Fix for asyncio in Streamlit
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        else:
            return asyncio.run(coro)
    except RuntimeError:
        return asyncio.run(coro)

st.set_page_config(
    page_title="MCP Architecture Diagram Generator",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ MCP Architecture Diagram Generator")
st.markdown("Generate AWS architecture diagrams using natural language with Bedrock + MCP")

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BedrockStrandsAgent()
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = ''
if 'selected_name' not in st.session_state:
    st.session_state.selected_name = 'architecture_diagram_DE'

# Sample prompts section
st.subheader("📋 Sample Architecture Prompts")
st.markdown("Click on any sample below to use it as a starting point:")

# Icon limitations info
with st.expander("⚠️ AWS Service Icon Limitations"):
    st.markdown("""
    **Supported AWS Services with proper icons:**
    - Lambda, ECS, EC2 (Compute)
    - S3 (Storage)
    - Kinesis, Glue, Athena (Analytics)
    - APIGateway, VPC (Network)
    - IAM, KMS (Security)
    - RDS, DynamoDB (Database)
    - SQS, SNS (Integration)
    - SageMaker (ML)
    
    **Unsupported services** (Config, Security Hub, GuardDuty, etc.) will use generic Lambda icons with descriptive labels.
    """)

sample_prompts = {
    "Kinesis Data Streaming with ECS": "Build a simple Kinesis based Data Streaming Architecture. The Data gets processed by ECS.",
    "Serverless Analytics Pipeline": "Build a Serverless architecture with APIGateway, Lambda, Glue and Athena to show end to end Data ingestion and analytics. Add SageMaker for AIML need."
}

col_samples = st.columns(len(sample_prompts))
for i, (title, sample_prompt) in enumerate(sample_prompts.items()):
    with col_samples[i]:
        if st.button(f"📝 {title}", key=f"sample_{i}"):
            st.session_state.selected_prompt = sample_prompt
            st.session_state.selected_name = title.lower().replace(" ", "_")

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    prompt = st.text_area(
        "Describe your AWS architecture:",
        value=st.session_state.get('selected_prompt', ''),
        placeholder="Example: Create a serverless analytics pipeline with Lambda, S3, Kinesis, and OpenSearch",
        height=100
    )

with col2:
    diagram_name = st.text_input(
        "Diagram name:",
        value=st.session_state.get('selected_name', 'architecture_diagram_DE'),
        placeholder="my_diagram"
    )

if st.button("Generate Diagram", type="primary"):
    if prompt:
        with st.spinner("Generating architecture diagram..."):
            try:
                # Run async function with proper parameters
                result = run_async(st.session_state.agent.generate_architecture_diagram(prompt, diagram_name))
                
                if result['success']:
                    st.success("✅ Diagram generated successfully!")
                    
                    # Show generated code
                    with st.expander("Generated Python Code"):
                        st.code(result['diagram_code'], language='python')
                    
                    # Show diagram - get image path from MCP result
                    diagram_path = result.get('result', {}).get('image_path')
                    
                    # Try multiple possible paths
                    possible_paths = [
                        diagram_path,
                        os.path.join("outputs", "diagrams", "generated-diagrams", f"{diagram_name}.png"),
                        os.path.join("outputs", "diagrams", f"{diagram_name}.png")
                    ]
                    
                    image_found = False
                    for path in possible_paths:
                        if path and os.path.exists(path):
                            st.image(path, caption=f"Architecture Diagram: {diagram_name}")
                            st.success(f"📁 Diagram saved at: {path}")
                            image_found = True
                            break
                    
                    if not image_found:
                        st.warning("Diagram generated but image file not found. Check outputs/diagrams/generated-diagrams/ folder.")
                        with st.expander("Debug: Result Structure"):
                            st.json(result)
                        
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
                    if 'error' in result:
                        st.error(f"Details: {result['error']}")
                    with st.expander("Debug Info"):
                        st.json(result)
                        st.write("Check if Docker is running and MCP server image is available")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.error("This might be due to:")
                st.error("1. Docker not running")
                st.error("2. MCP server image not available")
                st.error("3. AWS credentials not configured")
                st.error("4. Missing dependencies (run: pip install -r requirements.txt)")
                import traceback
                with st.expander("Full Error Traceback"):
                    st.code(traceback.format_exc())
    else:
        st.warning("Please enter a description for your architecture.")

# Footer
st.markdown("---")
st.markdown("**Architecture Flow:** Natural Language → AWS Bedrock → Python Code → Docker MCP Server → PNG Diagram")