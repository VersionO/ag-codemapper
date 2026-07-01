# Agentic CodeMapper: Multi-Skill Agent Deep Code Analysis

[![Kaggle Capstone](https://img.shields.io/badge/Kaggle-Capstone_Project-blue)](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/overview)

**Agentic CodeMapper** is a specialized AI agent built using the Google Agent Development Kit (ADK) that streamlines codebase navigation and architectural understanding. By utilizing a single-agent, multi-skill architecture, it provides autonomous indexing, deep code analysis, and context-aware explanations.

---

## 💡 The Problem
Developers often spend up to 40% of their time mapping existing codebases rather than building new features. Traditional documentation is often outdated or missing, leading to slow onboarding and high risks of unintended "blast radius" effects during code changes. **Agentic CodeMapper** solves this by using a multi-skill agentic approach to turn opaque repositories into structured, navigable knowledge.

## 🏗️ Architecture
Agentic CodeMapper operates as a **single-agent system with multi-skill capabilities**. It uses a sophisticated routing mechanism to invoke specific skills based on user intent:

* **Pipeline Mapping Skill:** Handles indexing and dependency synchronization.
* **Architectural Analysis Skill:** Evaluates code complexity and impact/blast radius.
* **Code Explanation Skill:** Delivers human-readable walkthroughs and workflow logic.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Python 3.10+**: Verify by running `python3 --version`. If needed, download it from [python.org](https://www.python.org/downloads/).
* **`uv` Package Manager**: Used for high-performance dependency management. Install via:
    * *macOS/Linux:* `curl -LsSf https://astral.sh/uv/install.sh | sh`
    * *Windows (PowerShell):* `irm https://astral.sh/uv/install.ps1 | iex`

### 2. Initial Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/VersionO/ag-codemapper.git
    cd ag-codemapper
    ```

2. **Run the setup script:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

3. **Configure Environment & MCP:**
    * **Environment:** If a `.env` file is not detected, the script will create one from `.env.template` and terminate. Open it, configure your authentication (Gemini API Key or Vertex AI), and re-run `./setup.sh`.
    * **MCP Auto-Configuration:** The script will automatically use `mcp_config.json.template` to generate a `mcp_config.json` file, dynamically populating it with the absolute path of your local repository.

4. **Antigravity IDE Setup:**
    * Open your project folder in the Antigravity IDE.
    * Click on the three dots (Additional Options) at the top right corner.
    * Select **MCP Servers**.
    * Click **Manage MCP Servers**.
    * Choose **View raw config**.
    * Paste the content of your generated `mcp_config.json` into this file and click **Save**.

### 3. Usage
Once your MCP server is configured and your project is loaded in the Antigravity IDE:

1. Open the **Chat** or **Agent** interface within the IDE.
2. Ensure your code to be analyzed is placed in a sub-folder within your project root (e.g., `./code_to_analyze/`).
3. Use the following prompt to trigger the agent's multi-skill analysis:

    **Example Prompt:**
    > Please analyze files in "./code_to_analyze/" using your skills for pipeline mapping, architectural analysis, and code explanation.

### 4. Outputs
The agent stores all generated insights in the `/output` folder.
* **Graph Visualization:** A link to the generated architectural graph will be provided in the agent's response, allowing you to visualize dependencies and logic flows.

---

## 🔗 MCP Integration
Agentic CodeMapper utilizes the **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)** to securely interface with your local files.

* **MCP Server Name:** [`codegraphcontext`](https://github.com/CodeGraphContext/CodeGraphContext)
* **Primary Tools:** Used for filesystem traversal, recursive code parsing, and structural dependency extraction.

## 🛡️ Security & Privacy Protocols
* **Credential Isolation:** We do not store credentials in the source code. The `.env` file is explicitly ignored by Git.
* **Template-Based Setup:** A `.env.template` file guides you through required variables.
* **Local-First:** Your code analysis remains local, ensuring your proprietary architecture never leaves your secure environment.

## ⚖️ Evaluation Compliance
* **Multi-Skill Agent (ADK):** Orchestrates three distinct skills for modular analysis.
* **MCP Server:** Implements local file system context retrieval using the `codegraphcontext` toolset.
* **Agent Skills:** Demonstrates intent-based skill routing.

---

## 📝 License
MIT License

---
*Project Origin: Developed as the Capstone Project for [Kaggle’s 5-Day AI Agents: Intensive Vibe Coding Course with Google](https://www.kaggle.com/learn-guide/5-day-agents-vibecoding).*
