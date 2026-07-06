# ag-codemapper Project Context & Secure Coding Standards

## Core Operational Guardrails
1. **Source of Truth**: All analysis MUST be based on live MCP context via `codegraphcontext`.
2. **Strict Encapsulation**: You are prohibited from accessing, reading, or reporting on environment configuration files, security credentials, or CI/CD artifacts (e.g., `mcp_config.json`, `setup_env.sh`, `package.json`, and `.env`). You are prohibited from automatically crawling siblings or parent directories. You must only interact with the exact file path(s)\target file(s) provided by the user in the prompt. 
3. **Focused Execution**: If a user asks about a specific file, you must treat all other files in that directory as "out-of-scope" unless you explicitly state why cross-referencing is required for the analysis.
4. **Visualization Mandatory**: Every analysis report (Architect or Explainer) MUST generate a flowchart-mode URL using `visualize_graph_query` and embed it in the final `.md` report.
5. **Mandatory Report Archiving**: Every analysis must be finalized as an `.md` report saved to the `/output` folder.

## Skill Execution Patterns
- **Pipeline Mapper**: Before finalizing any reports, you MUST perform a synchronization audit by running `uv run python -m codegraphcontext update <folder>` to ensure the database state is current.
- **Architect Analyzer**: Always focus on architectural risks (coupling, complexity, blast radius). Blast radius assessment must be performed at the symbol/function level before file level.
- **Code Explainer**: Always synthesize a holistic view combining raw code logic, global semantic search, and MCP-identified framework patterns.

## Visualization & User Guidance
* Whenever providing a flowchart link, you MUST generate a flowchart-mode URL using `visualize_graph_query` and embed it in the final `.md` report. 
* To ensure the graph database is synchronized with the filesystem (and free of deleted/unrelated files), you MUST run the database update command (e.g., `uv run python -m codegraphcontext update <folder>`) before finalizing the report. 
* When presenting the flowchart URL embedded in the final .md report, you MUST explicitly instruct the user to run the update command and start the visualization server (`uv run python -m codegraphcontext visualize`) first to prevent connection errors or displaying stale files.

## Standard Footer
Every response must conclude with:
"Analysis performed using live CodeGraphContext MCP. Data source: Live Session. Report archived: /output/[filename].md"