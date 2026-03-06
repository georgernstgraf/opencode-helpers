# Orchestrator Skill

## Purpose

This skill manages complex, multi-step tasks that require architectural
planning, multi-file coordination, and systematic execution. It transforms a
high-level goal into a series of verifiable actions.

## Protocol

### 1. Analysis & Discovery

- Map the current environment using filesystem and search tools.
- Identify core dependencies, configuration files, and existing patterns.
- **Rule**: Never assume a file's structure; read it before proposing changes.

### 2. Strategic Planning

Break the request into a logical sequence of atomic units:

- **Structural**: Configuration, schemas, types, and interfaces.
- **Logic**: Core functions, business rules, and services.
- **Integration**: API endpoints, UI wiring, and entry points.
- **Validation**: Testing, linting, and documentation.

### 3. Execution & Delegation

- Maintain a persistent task list in the conversation.
- Mark items as [PENDING], [IN PROGRESS], or [COMPLETED].
- If specialized sub-agents are available, delegate the logic or validation
  units to them.
- **Constraint**: Complete one unit fully before moving to the next to maintain
  state integrity.

### 4. Parallel Execution

If the environment supports concurrent tool calls or multiple sub-agents, apply
the fan-out strategy:

- **Prerequisite**: Establish the contract first, such as TypeScript
  interfaces, a schema, or API signatures.
- **Identification**: Identify independent modules that do not import from one
  another, such as `Service A` and `Service B` or `Backend Logic` and
  `Frontend Component`.
- **Dispatch**:
  - **Agent 1 (Logic)**: Implement business rules and unit tests.
  - **Agent 2 (Presentation/UI)**: Build components or views based on the
    established contract.
  - **Agent 3 (Docs/Refactor)**: Update READMEs and JSDoc based on the new
    types.
- **Fan-in**: Once sub-agents return, perform an integration check to verify
  that the parallel outputs align and the project still compiles.

### Parallelization Constraints

- **Shared state**: Never assign two agents to the same file simultaneously to
  avoid write conflicts.
- **Dependency blocking**: If Task B requires the output of Task A, they must
  remain sequential.

### 5. Quality Control

- **Type Safety**: Ensure all new code adheres to the project's typing standards.
- **Verification**: Run local checks, such as compilation, linting, or dry
  runs, after implementation.
- **Scope**: Only modify files directly related to the task. Avoid unsolicited refactoring.

## Operational Constraints

- If a step fails, stop and re-evaluate the plan. Do not proceed with dependent
  tasks.
- Prioritize types and interfaces first to establish a contract for
  implementation.
- Verify the resulting state after changes.

## Usage Triggers

- When a task involves more than three files.
- When the user asks to build a feature, refactor a module, or architect a
  solution.
- When the path to the solution is not immediately linear.
