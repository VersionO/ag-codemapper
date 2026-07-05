# Agentic CodeMapper: Multi-Skill Agent Deep Code Analysis

[![Kaggle Capstone](https://img.shields.io/badge/Kaggle-Capstone_Project-blue)](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/overview)

**Agentic CodeMapper** is a specialized AI agent built using the Google Agent Development Kit (ADK) that streamlines codebase navigation and architectural understanding. By utilizing a single-agent, multi-skill architecture, it provides autonomous indexing, deep code analysis, and context-aware explanations.

---

## ⚠️ The Problem
Developers often spend up to 40% of their time mapping codebases rather than building features. Traditional documentation is frequently outdated, leading to slow onboarding and high risks of unintended "blast radius" effects. Furthermore, relying on cloud-based AI to analyze proprietary code necessitates uploading sensitive business logic to external servers, creating a significant security dilemma.

## 💡 The Solution
**Agentic-CodeMapper** is an advanced orchestrator built using the **Google Agent Development Kit (ADK) 2.0**. It leverages the **CodeGraphContext (CGC)** MCP server to transform a codebase into a symbol-level graph, enabling precise, context-aware dependency analysis. The system offers several key advantages:

*   **Privacy-First Design**: While the system defaults to Gemini or Vertex AI / Google Cloud for initial setup, the ADK architecture utilizes a `LiteLlm` interface, allowing developers to swap the cloud-based backend for a local, private LLM (via Ollama or other providers) to ensure proprietary logic remains on-device.
*   **Modular Automation**: The system is generated via the ADK CLI to wire custom skills (`.agents/`) and structured workflows (`Agents.md`) into a cohesive agent runner, enabling deep structural analysis without the overhead of complex cloud-based deployments.
*   **Contextual Filtering**: By integrating the **CGC MCP server**, we move beyond simple `.gitignore` rules. The system intelligently indexes only the relevant structural graph—functions, classes, and inheritance—preventing "token spam" from environment files or build artifacts and ensuring the model focuses exclusively on the logic that matters.
---

## 🏛️ Architecture
Agentic CodeMapper operates as a **single-agent system with multi-skill capabilities**, governed by a strict configuration framework that defines the agent's behavior and operational scope.

### Foundational Components
*   **`Agents.md`**: Acts as the Global Orchestrator Directive, defining routing protocols, skill definitions, and the mandatory execution flow for the agent.
*   **`CONTEXT.md`**: Establishes the core operational guardrails, enforcing strict encapsulation, visualization requirements, and mandatory reporting standards.

### Multi-Skill Capabilities
The agent employs a sophisticated routing mechanism to invoke specific skills based on user intent:
*   **Pipeline Mapper**: Handles indexing and dependency synchronization.
*   **Architectural Analyzer**: Evaluates code complexity, coupling, and impact/blast radius at the symbol/function level.
*   **Code Explainer**: Synthesizes holistic walkthroughs combining raw code logic, global semantic search, and identified framework patterns.

### Routing & Execution
The system maps incoming queries to domain-specific skill definitions found in `.agents/skills/`. By maintaining a clear separation between infrastructure (Pipeline Mapping), diagnostics (Architectural Analysis), and logic (Code Explainer), the agent ensures efficient, modular, and secure code comprehension.

---

## 🛠️ Development Process
This project was developed through an iterative process of architectural design, hands-on testing, and CLI-driven orchestration:

1.  **Foundational Design**: We established the system's logic by creating the core skill definitions within `.agents/`, the workflow directives in `Agents.md`, and the operational guardrails in `CONTEXT.md`.
2.  **IDE Testing & Refinement**: We performed iterative testing within the Antigravity IDE, utilizing terminal commands to resolve dependency conflicts and refine the `mcp_config.json` configuration until the agent connection was fully functional.
3.  **Environment Setup**: We developed and refined the `setup.sh` script to streamline the creation of the virtual environment and ensure minimal-step configuration for any user cloning the repository.
4.  **CLI-Driven Generation**: With the core logic solidified, we generated the `app/agent.py` runner using the ADK 2.0 CLI with the following prompt:
    
    > "Use ADK 2.0 to generate the app/agent.py and configuration for ag-codemapper. I have already defined the skills in .agents/, the CONTEXT.md, and the workflow in agent.md. Please wire these existing skills into the agent runner to execute the dependency analysis without creating any deployment files."

    *Developers can manually modify the `app/agent.py` runner or the associated configuration files to point to local, private LLM instances (such as Ollama or other self-hosted providers), allowing you to maintain full data sovereignty as your requirements evolve.*
5.  **Validation**: Post-generation, we finalized security configurations (including specialized ignore files like `.gitignore`) and validated the system by generating live analysis reports and accessing interactive flowchart graphs locally within the Antigravity IDE.

---

## 🔗 MCP Integration
Agentic CodeMapper utilizes the **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)** to securely interface with your local files.

* **MCP Server:** [CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext)
* **Primary Tools:** Used for filesystem traversal, recursive code parsing, and structural dependency extraction.

---

## ⚙️ Setup Instructions

### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Python 3.10+**: Verify by running `python3 --version`. If needed, download it from [python.org](https://www.python.org/downloads/).
* **`uv` Package Manager**: Used for high-performance dependency management. Install via:
    * *macOS/Linux:* `curl -LsSf https://astral.sh/uv/install.sh | sh`
    * *Windows (PowerShell):* `irm https://astral.sh/uv/install.ps1 | iex`

<br>

### 2. Initial Setup
1. **Clone the repository:**
    ```bash
    git clone https://github.com/VersionO/ag-codemapper.git
    cd ag-codemapper
    ```

2. **Run the setup script:**
    ```bash
    chmod +x setup.sh
    source setup.sh
    ```
   *(Note: You must use `source setup.sh` rather than `./setup.sh`. Using `source` ensures that your API keys and configuration settings are exported directly into your current terminal session; running it with `./` would execute the script in a temporary sub-process, causing the environment configuration to be lost immediately upon completion.)*

3. **Configure Environment & MCP:**
    * **Environment:** If a `.env` file is not detected, the script will create one from `.env.template` and terminate. Open it, configure your authentication (Gemini API Key or Vertex AI), and re-run `./setup.sh`.
    * **MCP Auto-Configuration:** The script will automatically use `mcp_config.json.template` to generate a `mcp_config.json` file, dynamically populating it with the absolute path of your local repository.

- **Antigravity IDE Setup:**
    * Open your project folder in the Antigravity IDE.
    * Click on the three dots (Additional Options) at the top right corner.
    * Select **MCP Servers**.
    * Click **Manage MCP Servers**.
    * Click **View raw config** as shown below:
      
      ![MCP Config.png](assets/MCP%20Config.png)

    * Select all content of the `~/.gemini/config/mcp_config.json`, and paste the content of your generated `mcp_config.json` into this file and click **Save**.
<br>

### 3. Implementation
Once your MCP server is configured and your project is loaded in the Antigravity IDE:

1. Open the **Chat** or **Agent** view within the IDE.
2. Ensure your code to be analyzed is placed in a sub-folder within your project root (e.g., `./Test/`).
3. Use the following prompt to trigger the agent's multi-skill analysis:

    **Example Prompt:**
    > Please analyze files in "./Test/" using your skills for pipeline mapping, architectural analysis, and code explanation.

<br>

### 4. Outputs
The agent stores all generated insights in the `/output` folder as structured Markdown files.

* **Report Example**: You can view a [Sample Analysis Report](examples/analysis_report.md) to see how the system compiles structural dependencies and architectural risks.

* **Visualization Link**: Every analysis includes a link to the visual graph. 
  > **Note**: To prevent connection errors, you must run the update command and start the visualization server (`uv run python -m codegraphcontext visualize`) before accessing this link.
  
  ![Visualization Link](assets/Visualization%20Link.png)

* **Graph Flowchart**: Once the server is active, the link renders an interactive flowchart representing the codebase dependencies and logic flows:

  ![Graph 1 - App.py Flowchart](assets/Graph%201%20-%20App.py%20Flowchart.png)

  ![Graph 2 - App.py Flowchart](assets/Graph%202%20-%20App.py%20Flowchart.png)

---

## 🛡️ Security & Privacy Protocols
* **Credential Isolation:** We do not store credentials in the source code; the `.env` file is explicitly protected by being ignored across Git, the agent's `CONTEXT.md`, and the MCP via the `CGCignore` file.
* **Streamlined Configuration:** The `.env` file is used exclusively by the `setup.sh` script to export necessary environment configurations for the Gemini API or Vertex AI / Google Cloud; it is never committed to your repository.
* **Path Privacy & Local Setup:** We utilize a `.mcp_config.template` to locally map your project's directory paths to generate the `mcp_config.json` file. This ensures your local folder structure is handled securely and is not exposed in the codebase.
* **Template-Based Setup:** We provide both `.env.template` and `.mcp_config.template` files to guide you through the necessary variables without risking the exposure of your actual credentials or environment paths.
* **Local-First Architecture:** By design, your code analysis is executed locally, ensuring that your proprietary business logic and architecture never leave your secure, private environment.

---

## 📝 License
MIT License

---
*Project Origin: Developed as the Capstone Project for [Kaggle’s 5-Day AI Agents: Intensive Vibe Coding Course with Google](https://www.kaggle.com/learn-guide/5-day-agents-vibecoding).*
