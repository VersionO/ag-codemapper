---
name: architect_analyzer
description: Diagnostic tool for structural analysis, complexity, and impact assessment using live MCP context.
---

# Architect Analyzer Skill

This skill performs automated structural diagnostics and impact assessments to evaluate technical debt and architectural integrity based on live codebase state.

## Policies Enforced
1. **Scope**: Focus exclusively on architectural risks (coupling, complexity, reachability, blast radius).
2. **Access Hierarchy**: Perform all analysis via live MCP graph queries.
3. **Impact Granularity**: Blast radius must be assessed at the smallest possible scope (symbol/function level) before scaling to the file level.
4. **Actionability**: Every identified risk or impact item must be accompanied by a suggestion for resolution or testing.
5. **Report Generation**: All assessments must be finalized as an `.md` report saved to the `/output` folder.

## Global Tool Integration
* You have full authorization to use the global toolset:
    * **`find_code`**: Use to retrieve logic before performing complexity analysis.
    * **`visualize_graph_query`**: Use to generate mandatory flowchart links for all impact assessments.
    * **`generate_report`**: Use to compile findings into structured `.md` files.

## Instructions
1. **Impact Analysis (Blast Radius)**:
   - Use `analyze_code_relationships` to identify incoming/outgoing references.
   - Analyze downstream nodes to determine ripple effects.
   - **Categorize Impact**: Low (Localized), Medium (Internal interfaces), High (Public APIs/Global).

2. **Quantify Health**:
   - Use `calculate_cyclomatic_complexity` for critical paths.
   - Use `find_most_complex_functions` to identify refactoring targets.

3. **Format Response (to be saved as .md)**:
   - **Health/Impact Summary**: (Pass/Warning/Fail or Low/Medium/High)
   - **Key Findings**: (List risks/affected symbols with paths)
   - **Remediation Plan**: (Actionable steps)
   - **Visualization Link**: Include the mandatory flowchart-mode URL.

## Tool Definitions
* **`analyze_code_relationships`**: Maps call-stacks and dependencies. *Use when: Assessing 'blast radius'.*
* **`calculate_cyclomatic_complexity`**: Measures branch complexity. *Use when: Investigating fragile/high-risk logic.*
* **`find_most_complex_functions`**: Aggregates high-complexity blocks. *Use when: Prioritizing technical debt.*
* **`execute_cypher_query`**: Performs custom deep-dives (e.g., circular dependency detection).
* **`get_repository_stats`**: Summarizes graph scale for health baselines.