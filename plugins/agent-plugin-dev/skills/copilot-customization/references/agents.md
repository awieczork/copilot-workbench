# [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)

A custom agent is an `*.agent.md` file that gives a role its own instructions, tools, and model; the user selects it in chat, or another agent runs it as a subagent.

## Locations

| Scope | Location |
| --- | --- |
| Workspace | `.github/agents/<name>.agent.md` |
| User | `~/.copilot/agents/<name>.agent.md` |
| Copilot-format plugin | `agents/<name>.agent.md` |
| Agent Plugins 1.0 | `com.github.copilot/agents/<name>.agent.md` |

For plugin scope, read the root manifest to select the declared [plugin format](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference#plugin-formats) before choosing a location.
Use a lowercase kebab-case file name with the `.agent.md` suffix.

## Frontmatter

```yaml
---
name: "reviewer"
description: "Assess a finished change against its goal and report defects without fixing them"
tools: ["read", "search", "execute"]
model: ["<preferred model identifier>", "<fallback model identifier>"]
user-invocable: false
---
```

| Field | Behavior |
| --- | --- |
| `name` | Agent identifier; defaults to the file name, while a plugin agent without `name` gets the plugin-prefixed id, so set `name` in every plugin agent; references to it are case-sensitive |
| `description` | States the role and when to use it; shown in the chat input and read by agents that decide whether to delegate |
| `argument-hint` | Hint text that guides the user's input |
| `tools` | Tool names, tool sets, or `<server>/*` for every tool of an MCP server; `[]` gives no tools, and omitting the field gives the default tools |
| `agents` | In Local, agent names this agent may run as subagents; `["*"]` allows all, `[]` allows none, and omitting the field allows all; the Copilot schema does not accept this field |
| `model` | One model identifier, or an ordered list tried until a model is available; identifiers depend on the harness. In Copilot, omitting it uses the model selected in chat; Local subagents follow the Local model selection order |
| `reasoning-effort` | `low`, `medium`, `high`, `xhigh`, or `max`; the model must support the level; Copilot Agent Host sessions apply it, while the Local agent takes the effort from the user's configuration for the resolved model |
| `user-invocable` | `false` hides the agent from the agent picker, so it runs only as a subagent; defaults to `true` |
| `disable-model-invocation` | `true` stops other agents from running it as a subagent; defaults to `false` |
| `handoffs` | In Local, buttons shown after a response that switch to another agent with the conversation context and a pre-filled prompt |

Each handoff takes `label` (button text), `agent` (target agent), `prompt` (text to send), optional `send` (`true` submits the prompt automatically; defaults to `false`), and optional `model` (qualified model name for the target).

Leave out the deprecated `infer`, because VS Code still reads it and it overrides `disable-model-invocation`; leave out `mcp-servers`, which only the GitHub cloud agent reads, and `target`, unless the agent must be limited to one environment; hooks in frontmatter are outside this skill.

## Tools

The built-in aliases below are available in Copilot; tool availability and membership depend on the harness and session.
Use tool completions for qualified client or extension tools instead of assuming that a Local identifier maps to a Copilot tool.

| Alias | Grants |
| --- | --- |
| `read` | Reading files |
| `search` | Searching files and text |
| `edit` | Editing files |
| `execute` | Running shell commands |
| `agent` | Running other agents as subagents |
| `web` | Web tools; in Local, `web/fetch`, `web/githubRepo`, and `web/githubTextSearch` |
| `todo` | Managing a task list |

Local ignores unavailable tools, so check the intended harness's available tools before relying on a capability.

## Invocation and subagents

In the Local agent:

- The user selects an agent in the agent picker unless it sets `user-invocable: false`.
- Another agent runs it as a subagent when the delegating agent has the `agent` tool and the agent is allowed by the delegating agent's `agents` list.
- An agent named in a delegating agent's `agents` list runs even when it sets `disable-model-invocation: true`, so control who may call an agent through the delegating agents' lists.
- A subagent starts with its task and applicable instructions, not the conversation history, so the task it receives must be self-contained.
- A subagent returns one result and cannot be prompted again; further work needs a new invocation with the full context.
- The delegating agent may pass a `model` with the subagent call, which overrides the agent's `model`; no per-call reasoning effort exists.
- A subagent cannot ask the user questions or use the task list, because those tools are unavailable inside subagents.
- A subagent can run its own subagents only when the user enables `chat.subagents.allowInvocationsFromSubagents`; a package cannot set it, and nesting stops at five levels.

## Template

````markdown
---
name: "{agent-name}"
description: "{Use when ...}. {What it owns.}"
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

## Principles

- Give each agent one role, and open the body with the role line, naming what the agent owns and the nearest work it leaves to others.
- Grant the smallest tool set the role needs, and use supported `tools` restrictions rather than relying on prose; in Local, also use `agents` to restrict delegation.
- Put only hard limits in `Constraints`, each with its reason, including the actions that need the user's approval.
- Give an agent that holds the `agent` tool a criterion for when to delegate, such as independent work or work that needs an isolated context, because model families differ in how readily they delegate.
- When using `agents` in Local, name agents explicitly rather than `["*"]`, and list the agent itself only when recursion is intended.
- In Local, use `handoffs` for stages the user should review before the next one starts, and give a chain of handoffs a progress condition, so that two agents do not pass work back and forth.

## Validate

- [ ] The file sits at a documented location with the `.agent.md` suffix.
- [ ] Frontmatter parses, `tools`, `agents`, and `handoffs` are arrays where present, and `model` is a string or an array.
- [ ] Every tool and agent name is spelled exactly, and `agents` comes with the `agent` tool.
- [ ] An agent that returns a result has an output template.
- [ ] Every handoff target exists and is user-invocable.
