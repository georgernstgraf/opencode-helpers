# Orchestrator Skill

## Purpose
This skill is for managing complex, multi-step tasks that require architectural planning, multi-file coordination, and systematic execution. It transforms a high-level goal into a series of verifiable actions.

## Protocol

### 1. Analysis & Discovery
- Map the current environment using filesystem tools (ls, grep, find).
- Identify core dependencies, configuration files, and existing patterns.
- **Rule**: Never assume a file's structure; read it before proposing changes.

### 2. Strategic Planning
Break the request into a logical sequence of atomic units:
- **Structural**: Configuration, schemas, types, and interfaces.
- **Logic**: Core functions, business rules, and services.
- **Integration**: API endpoints, UI wiring, and entry points.
- **Validation**: Testing, linting, and documentation.

### 3. Execution & Delegation
- Maintain a persistent "Task List" in the conversation. 
- Mark items as [PENDING], [IN PROGRESS], or [COMPLETED].
- If specialized sub-agents are available, delegate the "Logic" or "Validation" units to them.
- **Constraint**: Complete one unit fully before moving to the next to maintain state integrity.

### 5. Parallel Execution Protocol
If the environment supports concurrent tool calls or multiple sub-agents, apply the "Fan-Out" strategy:

- **Prerequisite**: Establish the "Contract" (e.g., TypeScript interfaces, Drizzle schema, or API signatures) before parallelizing.
- **Identification**: Identify independent modules that do not import from one another (e.g., `Service A` and `Service B`, or `Backend Logic` and `Frontend Component`).
- **Dispatch**:
    - **Agent 1 (Logic)**: Implement business rules and unit tests.
    - **Agent 2 (Presentation/UI)**: Build components/views based on the established contract.
    - **Agent 3 (Docs/Refactor)**: Update READMEs and JSDocs based on the new types.
- **Fan-In (Synchronization)**: Once sub-agents return, the Orchestrator must perform a "Integration Check" to verify that all parallel outputs align and the project compiles.

### Parallelization Constraints
- **Shared State**: Never assign two agents to the same file simultaneously to avoid write-conflicts.
- **Dependency blocking**: If Task B requires the output of Task A, they must remain sequential.

### 4. Quality Control
- **Type Safety**: Ensure all new code adheres to the project's typing standards.
- **Verification**: Run local checks (compilation, linting, or dry-runs) after implementation.
- **Scope**: Only modify files directly related to the task. Avoid unsolicited refactoring.

## Operational Constraints
- If a step fails, stop and re-evaluate the plan. Do not proceed with dependent tasks.
- Prioritize "Types/Interfaces first" to establish a contract for implementation.
- Use standard shell utilities to verify the state of the system after changes.

## Usage Triggers
- When a task involves more than three files.
- When the user asks to "Build a feature," "Refactor a module," or "Architect a solution."
- When the path to the solution is not immediately linear.
