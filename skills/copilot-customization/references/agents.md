# [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)

A custom agent is an `*.agent.md` file that gives a role its own instructions, tools, and model; the user selects it in chat, or another agent runs it as a subagent.

## Locations

| Scope | Location |
| --- | --- |
| Workspace | `.github/agents/<name>.agent.md` |
| User | `~/.copilot/agents/<name>.agent.md` |
| Agent Plugins 1.0 package | `com.github.copilot/agents/<name>.agent.md` |

Use a lowercase kebab-case file name with the `.agent.md` suffix.

## Frontmatter

```yaml
---
name: "reviewer"
description: "Assess a finished change against its goal and report defects without fixing them"
tools: ["read", "search", "execute"]
model: ["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]
user-invocable: false
---
```

| Field | Behavior |
| --- | --- |
| `name` | Agent identifier; defaults to the file name, while a plugin agent without `name` gets the plugin-prefixed id, so set `name` in every plugin agent; references to it are case-sensitive |
| `description` | States the role and when to use it; shown in the chat input and read by agents that decide whether to delegate |
| `argument-hint` | Hint text that guides the user's input |
| `tools` | Tool names, tool sets, or `<server>/*` for every tool of an MCP server; `[]` gives no tools, and omitting the field gives the default tools |
| `agents` | Agent names this agent may run as subagents; `*` allows all, `[]` allows none, and omitting the field allows all |
| `model` | One qualified model name, or an ordered list that VS Code tries until a model is available; omitting it uses the model selected in chat |
| `reasoning-effort` | `low`, `medium`, `high`, `xhigh`, or `max`; the model must support the level; the agent-host (Copilot CLI) harness applies it, while the Local harness takes the effort from the user's configuration for the resolved model |
| `user-invocable` | `false` hides the agent from the agent picker, so it runs only as a subagent; defaults to `true` |
| `disable-model-invocation` | `true` stops other agents from running it as a subagent; defaults to `false` |
| `handoffs` | Buttons shown after a response that switch to another agent with the conversation context and a pre-filled prompt |

Each handoff takes `label` (button text), `agent` (target agent), `prompt` (text to send), optional `send` (`true` submits the prompt automatically; defaults to `false`), and optional `model` (qualified model name for the target).

Write model names in qualified form, such as `"Claude Opus 5.5 (copilot)"`.
Leave out `target`, `mcp-servers`, and the deprecated `infer`, because VS Code custom agents do not use them; hooks in frontmatter are outside this skill.

## Tools

| Alias | Grants |
| --- | --- |
| `read` | Reading files |
| `search` | Searching files and text |
| `edit` | Editing files |
| `execute` | Running shell commands |
| `agent` | Running other agents as subagents |
| `web` | Fetching URLs |
| `todo` | Managing a task list |

VS Code ignores a tool name it does not recognize, so a misspelled tool silently removes that capability.

Typical sets:

```yaml
tools: ["read", "search"]             # read-only research
tools: ["read", "search", "edit"]     # editing without a terminal
tools: []                             # conversation only
```

## Invocation and subagents

- The user selects an agent in the agent picker unless it sets `user-invocable: false`.
- Another agent runs it as a subagent when the caller has the `agent` tool and the agent is allowed by the caller's `agents` list.
- An agent named in a caller's `agents` list runs even when it sets `disable-model-invocation: true`, so control who may call an agent through the callers' lists.
- A subagent starts with its task and applicable instructions, not the conversation history, so the task it receives must be self-contained.
- A subagent returns one result and cannot be prompted again; further work needs a new invocation with the full context.
- The caller may pass a `model` with the subagent call, which overrides the agent's `model`; no per-call reasoning effort exists.
- A subagent cannot ask the user questions or use the task list, because those tools are unavailable inside subagents.
- A subagent can run its own subagents only when the user enables `chat.subagents.allowInvocationsFromSubagents`; a package cannot set it.

## Template

````markdown
---
name: "{agent-name}"
description: "{what it owns and when to use it}"
tools: [{smallest set of tools the role needs}]
---

You are {role}: you {own X}; you do not {Y}.

## Constraints

- {Hard limit or action that needs approval}, because {reason}.

## Workflow

{The goal and the approach, as numbered steps only when their order matters.}

{Work} is done when {condition}.

## Output format

```markdown
{Template with {placeholder} slots.}
```
````

- Open the body with the role line, naming what the agent owns and the nearest work it leaves to others.
- Put only hard limits in `Constraints`, each with its reason, and name the safe workflows the agent runs without asking, such as the local tests, because without that permission capable models stop to ask.
- Let the agent ask only when the answer would change the result, and only after it has prepared a concrete, reviewable result, because an early question or review stop ends the work too soon.
- Give an agent that holds the `agent` tool a criterion for when to delegate, such as independent work or work that needs an isolated context, because model families differ in how readily they delegate.
- Add a retry cap, a refusal of out-of-role requests, or a completion condition per phase only where the agent loops, overreaches, or stops early without it.
- Give an agent that returns a result an `Output format` template, because the caller reads the return by its sections.

## Principles

- Give each agent one role.
- Grant the smallest tool set the role needs, and enforce limits through `tools` and `agents` rather than prose, because a tool the agent holds is a capability it may use.
- Treat tool access as capability, not authorization: state in `Constraints` the actions that need the user's approval.
- Give a subagent everything it needs in its task, and have it return open questions and blockers instead of guessing.
- Name agents explicitly in `agents` rather than `*`, and list the agent itself only when recursion is intended, because nesting needs `chat.subagents.allowInvocationsFromSubagents` and stops at five levels.
- Use `handoffs` for stages the user should review before the next one starts, and give a chain of handoffs a progress condition, so that two agents do not pass work back and forth.

## Validate

- [ ] The file sits at a documented location with the `.agent.md` suffix.
- [ ] Frontmatter parses, and `tools`, `agents`, `model` lists, and `handoffs` are arrays where present.
- [ ] Every tool and agent name is spelled exactly, and `agents` comes with the `agent` tool.
- [ ] The agent has one role, the smallest tool set, and hard limits with their reasons.
- [ ] An agent that returns a result has an output template.
- [ ] Every handoff target exists and is user-invocable.
