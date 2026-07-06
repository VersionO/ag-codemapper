---
name: code_explainer
description: Holistic behavioral walkthrough combining direct source code analysis, global semantic search, and structural MCP context.
---

# Code Explainer Skill

This skill provides behavioral insights by synthesizing raw source code logic, global semantic search results, and architectural dependency patterns.

## Policies Enforced
1. **Holistic Lens**: Combine direct file-reading, global `find_code` retrieval, and MCP-tool querying to build a complete view of the implementation.
2. **Structural Mapping**: Every explanation must map low-level implementation details to high-level framework patterns identified by MCP tools.
3. **Multi-Level Disclosure**: Every explanation must contain:
   - **High-Level Intent**: The business/architectural purpose.
   - **Structural Workflow**: System-level interaction (via MCP).
   - **Detailed Implementation**: Logic flow (via file access and `find_code`).
4. **Report Generation**: All explanations must be finalized as an `.md` file in `/output`.

## Global Tool Integration
* You have full authorization to use the global toolset:
    * **`find_code`**: Use this to perform semantic searches and retrieve specific logic definitions across the codebase before applying structural MCP context.
    * **`visualize_graph_query`**: Use this to generate mandatory flowchart links for all explanations.
    * **`generate_report`**: Use this to compile and save your final analysis as an `.md` file.

## Instructions
1. **Discovery**:
   - Use `find_code` (Global) to retrieve the logic definition of the target scope.
   - Use `codegraphcontext` tools (e.g., `find_java_spring_beans`, `find_java_spring_endpoints`) to identify the node’s structural role (callers, dependencies, and framework annotations).

2. **Synthesis**:
   - Trace the logical workflow found in the source code.
   - Link the code to its framework lifecycle (e.g., managed bean, controller endpoint) provided by the MCP tools.

3. **Format Response (to be saved as .md)**:
   - **High-level Intent**: Summary of the feature.
   - **Structural Workflow**: Step-by-step description of system-level interactions.
   - **Detailed Implementation**: Technical breakdown of the logic flow found via `find_code` and direct file inspection.
   - **Risk/Health Assessment**: Architectural concerns.
   - **Visualization Link**: Include the mandatory flowchart-mode URL.