# T3 Code documentation evidence - 2026-10-12

Scope: Official T3 Code repository documentation and implementation on `main`, read on 2026-10-12. The quoted lines are the evidence; an implementation mapping describes what T3 passes to a provider, not a complete guarantee about that provider's filesystem behavior.

## Q1. Runtime modes: reads, writes, commands, network, and location

T3 documents Supervised (`approval-required`) as asking for commands and file changes; Auto-accept edits as approving edits while other actions may ask; Auto as provider automatic review; and Full access as allowing commands and edits without approval prompts. Its Codex adapter maps those modes respectively to `readOnly`, `workspaceWrite`, `workspaceWrite`, and `dangerFullAccess` sandbox policies, with the approval policies shown below. not documented: an exhaustive inside/outside workspace matrix for file reads, writes, shell commands, and network in each mode. The user guide says providers enforce permissions differently, so the mode label alone is not a complete access specification. Looked at the permission modes guide and both provider adapters cited below.

Evidence:

- [Permission modes, lines 11-16](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L11-L16): “Supervised | Requests approval for commands and file changes.”; “Full access | Allows commands and edits without approval prompts.”
- [Permission modes, lines 14-15](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L14-L15): “Auto-accept edits | Approves file edits automatically; other actions can still require approval.”; “Auto | Uses the provider's automatic review to approve routine actions and ask about others.”
- [Codex adapter, lines 664-700](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L664-L700): “approvalPolicy: \"untrusted\"”; “type: \"readOnly\"”; “type: \"workspaceWrite\"”; “type: \"dangerFullAccess\"”.
- [Permission modes, lines 21-25](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L21-L25): “Providers enforce permissions differently. Some read-only actions can proceed in Supervised.”

## Q2. Claude versus Codex sandbox and settings transport

Yes, T3 applies provider-specific controls: Codex receives an explicit per-turn `sandboxPolicy`, `approvalPolicy`, and reviewer; Claude receives a Claude Agent SDK `permissionMode`, tool configuration, and sometimes a permission callback. The Claude adapter maps the four T3 modes to `default`, `acceptEdits`, `auto`, and `bypassPermissions` in its ordinary mapping; its code also handles explicit runtime policy overrides. These are distinct provider mechanisms, and the T3 documentation does not state that they yield identical filesystem boundaries.

Evidence:

- [Provider constraints, lines 3-6](https://github.com/pingdotgg/t3code/blob/main/docs/internals/providers.md#L3-L6): “Provider protocols, account ownership, permissions, and capabilities belong at the adapter boundary.”
- [Codex adapter, lines 664-700](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L664-L700): “readonly approvalPolicy”; “readonly approvalsReviewer”; “readonly sandboxPolicy”.
- [Codex adapter, lines 779-792](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L779-L792): “cwd: input.runtimePolicy.cwd”; “approvalsReviewer: runtimeModeDefaults.approvalsReviewer”; “sandboxPolicy”.
- [Claude adapter, lines 1698-1707](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1698-L1707): “case \"approval-required\":”; “return \"default\"”; “return \"acceptEdits\"”; “return \"bypassPermissions\"”.
- [Claude adapter, lines 1721-1752](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1721-L1752): “readOnlyTools”; “installPermissionCallback”; “allowDangerouslySkipPermissions”.

## Q3. Extra readable or writable directories in provider instances

T3 exposes instance environment variables and provider-specific settings, including launch arguments for Claude and Codex. The Claude adapter parses its launch arguments into SDK `extraArgs` and sets `additionalDirectories` to the working and attachment directories; the Codex launcher passes launch arguments to `codex app-server`. not documented: a T3-supported provider-instance setting or `add-dir` recipe that guarantees an arbitrary extra path is readable or writable under a given mode. The cited code shows configuration channels, not an access grant for the proposed shared folder. Looked at the provider instance contract, settings schema, launch-argument helper, and both provider guides.

Evidence:

- [Provider instance contract, lines 124-131](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/providerInstance.ts#L124-L131): “environment: Schema.optionalKey(ProviderInstanceEnvironment)”; “config: Schema.optionalKey(Schema.Unknown)”.
- [Settings schema, lines 635-640](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/settings.ts#L635-L640): “Additional CLI arguments passed to codex app-server on session start.”
- [Settings schema, lines 684-689](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/settings.ts#L684-L689): “Additional CLI arguments passed on session start.”
- [Claude adapter, lines 975-979 and 1059-1067](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1059-L1067): “extraArgs”; “additionalDirectories”; “input.cwd”; “input.attachmentsDir”.
- [Codex launch arguments, lines 12-15](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/provider/codexLaunchArgs.ts#L12-L15): “\"app-server\", ...codexLaunchArgv(launchArgs)”.

## Q4. Delegated-task inheritance and privilege ceiling

`delegate_task` inherits provider, model, runtime mode, and interaction mode when omitted. The official orchestration document says a child runtime mode may remain equal or become narrower than its parent's and cannot escalate privileges. It does not specify a separately inherited filesystem sandbox object; the selected child provider applies its own runtime mode and policy. A child targeting a provider with fewer offered modes can step down to a supported mode.

Evidence:

- [Orchestrator MCP server, lines 210-245](https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L210-L245): “Provider, model, runtime mode, and interaction mode inherit from the parent when omitted.”
- [Orchestrator MCP server, lines 240-245](https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L240-L245): “an inherited mode steps down to the broadest mode the target offers.”
- [Orchestrator MCP server, lines 460-463](https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L460-L463): “A child runtime mode may stay equal to or become narrower than the parent mode. It may not escalate privileges.”

## Q5. Global instructions, skills, and shared configuration

T3 documents use of the provider's existing configuration: Claude uses Claude Code's login and configuration, including its config-directory skills; Codex can use an existing CLI login and config, and its account modes can share a Codex home. not documented: T3 itself loading `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or following links from either file to a shared folder. The Claude adapter requests the Claude Code preset system prompt; the cited T3 docs and code do not describe the provider's instruction-file discovery rules. Looked at both provider guides, the Claude adapter, and the permission modes guide.

Evidence:

- [Claude provider guide, lines 1-5](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md#L1-L5): “T3 Code uses Claude Code's login and configuration.”
- [Claude provider guide, lines 68-72](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md#L68-L72): “Claude skills come from the config directory's `skills` folder and the project's `.claude/skills` folder.”
- [Codex provider guide, lines 22-26](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md#L22-L26): “T3 Code can use your installed Codex and its existing login.”
- [Codex provider guide, lines 34-38](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md#L34-L38): “The accounts share Codex sessions and configuration while keeping their own login and available models.”
- [Claude adapter, lines 1052-1057](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1052-L1057): “systemPrompt: { type: \"preset\", preset: \"claude_code\"”.

## Q6. Reading a path outside the project

Yes. T3's internal documentation explicitly says a project is an organizational boundary rather than a filesystem sandbox, and that its `filesystem:read` client scope can reach absolute paths outside a project when the server account can read them. This client scope is separate from an agent's provider sandbox. T3 also says a path in the prompt does not grant filesystem access and that provider sandbox and approval rules remain in force.

Evidence:

- [Environment auth, lines 103-109](https://github.com/pingdotgg/t3code/blob/main/docs/internals/environment-auth.md#L103-L109): “Projects are organizational boundaries, not filesystem sandboxes.”; “`filesystem:read` permits reading files the server account can read, including absolute paths outside a project.”
- [Remote access, lines 286-288](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md#L286-L288): “These scopes control direct file access from the client.”
- [Provider constraints, lines 132-138](https://github.com/pingdotgg/t3code/blob/main/docs/internals/providers.md#L132-L138): “A path in the prompt does not grant filesystem access. Keep provider sandbox and approval rules in force”.
