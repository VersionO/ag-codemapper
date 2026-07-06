#!/bin/bash
# ag-codemapper environment setup

# 1. Verification: Check for .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file missing. Creating from template..."
    cp .env.template .env
    echo "⚠️  Please edit the .env file with your credentials and run this script again."
    exit 1
fi

# 2. Load and Validate Configuration
# Check if the script is being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "❌ Error: This script must be run using 'source setup.sh' to load environment variables correctly."
    exit 1
else
    export $(grep -v '^#' .env | xargs)
fi

echo "🔍 Verifying configuration..."

if [ "$GOOGLE_GENAI_USE_ENTERPRISE" = "TRUE" ]; then
    # Check for required project ID
    if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
        echo "❌ Error: GOOGLE_GENAI_USE_ENTERPRISE is TRUE, but GOOGLE_CLOUD_PROJECT is missing."
        exit 1
    fi
    
    # Check if the user is actually logged into gcloud
    if ! gcloud auth application-default print-access-token &> /dev/null; then
        echo "⚠️  Vertex AI mode detected, but you are not logged into Google Cloud!"
        echo "   Please run these commands to authenticate:"
        echo "   1. gcloud auth application-default login"
        echo "   2. gcloud config set project $GOOGLE_CLOUD_PROJECT"
        exit 1
    fi
    
    echo "✅ Authentication Mode: Vertex AI (Google Cloud) - Authenticated"

elif [ "$GOOGLE_GENAI_USE_ENTERPRISE" = "FALSE" ]; then
    # Check for required API Key
    if [ -z "$GEMINI_API_KEY" ]; then
        echo "❌ Error: GOOGLE_GENAI_USE_ENTERPRISE is FALSE, but GEMINI_API_KEY is missing."
        exit 1
    fi
    echo "✅ Authentication Mode: Gemini API Key - Set"

else
    echo "❌ Error: GOOGLE_GENAI_USE_ENTERPRISE must be TRUE or FALSE in your .env file."
    exit 1
fi

# 3. Setup Venv using uv (or standard python if uv is missing)
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment..."
    if command -v uv &> /dev/null; then
        uv venv .venv
    else
        python3 -m venv .venv
    fi
fi
source .venv/bin/activate

# 4. Install Python dependencies using uv (faster and more reliable)
echo "📦 Installing Python dependencies..."
if command -v uv &> /dev/null; then
    uv sync
else
    # Fallback to pip if uv is not installed
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 5. Setup Node/MCP dependencies
echo "📦 Configuring Node-based MCP tools..."
if command -v npm &> /dev/null; then
    # We only run npm install if package.json exists
    if [ -f "package.json" ]; then
        npm install
        echo "✅ Node environment is ready."
    fi
else
    echo "⚠️  npm not found. Skipping Node package initialization."
fi

# 6. Generate Config from template
if [ -f "mcp_config.json.template" ]; then
    echo "⚙️ Generating mcp_config.json..."
    # Replace the placeholder with the absolute path
    sed "s|{{PROJECT_ROOT}}|$(pwd)|g" mcp_config.json.template > mcp_config.json
    echo "--------------------------------------------------------"
    echo "mcp_config.json generated successfully!"
    echo "Please copy the contents of the following MCP configuration for your Antigravity IDE:"
    cat mcp_config.json
    echo ""
    echo "If you need instructions on how to add this to your IDE,"
    echo "refer to the 'Antigravity IDE Setup' section in README.md."
    echo "--------------------------------------------------------"
else
    echo "❌ Error: mcp_config.json.template not found."
fi

# 7. Finalize directories
echo "📁 Preparing graph and data directories..."
mkdir -p .codegraph_db
mkdir -p Output/

echo "✅ Environment successfully synchronized and stabilized."