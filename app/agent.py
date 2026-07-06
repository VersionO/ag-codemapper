# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.workflow import Workflow, START
from google.adk.events.event import Event
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Initialize GCP Environment dynamically to support both Vertex AI and Gemini API keys
if os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    try:
        _, project_id = google.auth.default()
        if project_id:
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
        else:
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
    except Exception:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

import sys

# Define the shared MCP Toolset for codegraphcontext
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=["-m", "codegraphcontext", "mcp", "start"],
        )
    )
)

def load_text_file(relative_path: str) -> str:
    """Helper to read instructions from a file in the workspace."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, relative_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Strip YAML frontmatter if present
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content.strip()
    except Exception as e:
        return f"Error loading instructions from {relative_path}: {e}"

# Load global configuration and instructions
global_rules = load_text_file("Agents.md")
context_rules = load_text_file(".agents/CONTEXT.md")

# Load skill instructions
pipeline_instr = load_text_file(".agents/skills/pipeline_mapper/skill.md")
architect_instr = load_text_file(".agents/skills/architect_analyzer/skill.md")
explainer_instr = load_text_file(".agents/skills/code_explainer/skill.md")

# Compose system instructions for each agent by appending global rules/directives and context
pipeline_mapper_instruction = f"{pipeline_instr}\n\n=== CONTEXT & OPERATIONAL GUARDRAILS ===\n{context_rules}\n\n=== GLOBAL WORKSPACE RULES & ROUTING ===\n{global_rules}"
architect_analyzer_instruction = f"{architect_instr}\n\n=== CONTEXT & OPERATIONAL GUARDRAILS ===\n{context_rules}\n\n=== GLOBAL WORKSPACE RULES & ROUTING ===\n{global_rules}"
code_explainer_instruction = f"{explainer_instr}\n\n=== CONTEXT & OPERATIONAL GUARDRAILS ===\n{context_rules}\n\n=== GLOBAL WORKSPACE RULES & ROUTING ===\n{global_rules}"

# Define the sub-agents matching the skills
pipeline_mapper_agent = Agent(
    name="pipeline_mapper",
    model="gemini-flash-latest",
    instruction=pipeline_mapper_instruction,
    tools=[mcp_toolset],
)

architect_analyzer_agent = Agent(
    name="architect_analyzer",
    model="gemini-flash-latest",
    instruction=architect_analyzer_instruction,
    tools=[mcp_toolset],
)

code_explainer_agent = Agent(
    name="code_explainer",
    model="gemini-flash-latest",
    instruction=code_explainer_instruction,
    tools=[mcp_toolset],
)

# Router node function
def route_query(node_input: str) -> Event:
    query = str(node_input).lower()
    
    # Matching keywords defined in Routing Matrix
    pipeline_keywords = ["index", "sync", "watch", "graph", "map"]
    architect_keywords = ["health", "dead code", "complexity", "blast radius", "risk", "analyze"]
    explainer_keywords = ["explain", "walkthrough", "behavior", "workflow", "tutorial"]
    
    if any(k in query for k in pipeline_keywords):
        return Event(output=node_input, route="pipeline_mapper")
    elif any(k in query for k in architect_keywords):
        return Event(output=node_input, route="architect_analyzer")
    elif any(k in query for k in explainer_keywords):
        return Event(output=node_input, route="code_explainer")
    
    # Fallback default route
    return Event(output=node_input, route="code_explainer")

# Define Workflow Agent mapping start node to specific skill sub-agents using tuples and dict-based routing
root_agent = Workflow(
    name="ag_codemapper_workflow",
    edges=[
        (START, route_query),
        (route_query, {
            "pipeline_mapper": pipeline_mapper_agent,
            "architect_analyzer": architect_analyzer_agent,
            "code_explainer": code_explainer_agent,
        }),
    ],
    description="Orchestrator for Code Comprehension and Dependency Analysis using specialized sub-skills.",
)

# Initialize the App instance
app = App(
    root_agent=root_agent,
    name="app",
)
