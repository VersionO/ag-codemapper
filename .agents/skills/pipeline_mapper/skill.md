---
name: pipeline_mapper
description: Manages the graph database lifecycle, synchronization, and health of the project structure in real-time.
---

# Pipeline Mapper Skill

This skill acts as the infrastructure gatekeeper, ensuring the CodeGraphContext (CGC) database is accurately synchronized with the filesystem at all times.

## Policies Enforced
1. **Targeted Sync**: Indexing must always be scoped to user-defined targets to preserve system resources.
2. **Verification**: Never assume the database state; always use status checks before reporting success.
3. **Report Generation**: All sync reports must be finalized as an `.md` file in the `/output` folder.

## Global Tool Integration
* You have full authorization to use the global toolset:
    * **`generate_report`**: Use this to compile sync statuses and infrastructure health reports into structured `.md` files.
    * **`visualize_graph_query`**: Use this to generate mandatory flowchart links to be included in the final generated reports.

## Instructions
1. **Target Discovery**: Use `list_indexed_repositories` to verify if the requested path is already indexed.
2. **Execute Mapping**: Call `add_code_to_graph` or `add_package_to_graph` strictly on the path provided by the user.
3. **Synchronization Audit**: After indexing, use `list_indexed_repositories` to verify the state update.
4. **Format Response (to be saved as .md)**:
   - **Sync Status**: (Success/Failure)
   - **Indexed Paths**: (Verified list of paths now in the graph)
   - **Infrastructure Health**: (Active watch status)

## Tool Definitions
* **`add_code_to_graph`**: Executes a full parse of a local directory into the graph. *Use when: A new project is loaded.*
* **`add_package_to_graph`**: Indexes third-party library metadata. *Use when: Integrating external frameworks.*
* **`watch_directory`**: Enables real-time filesystem watchers. *Use when: Starting an active coding session.*
* **`unwatch_directory`**: Disables monitoring. *Use when: Closing a workspace to free memory.*
* **`list_watched_paths`**: Returns a manifest of current watchers. *Use when: Auditing system resource usage.*
* **`list_indexed_repositories`**: Returns all repositories in the database. *Use when: Confirming if a project is indexed.*
* **`delete_repository`**: Purges indexed data. *Use when: Performing a hard reset.*