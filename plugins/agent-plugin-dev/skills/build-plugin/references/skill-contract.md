# Plugin skill contract

A plugin skill owns the access path, procedure, safety gate, and common failure cases for one system or task.

## Authoring rules

- Put each skill's procedure and boundaries in its own `SKILL.md` so users can install the package independently of this repository.
- Keep required scripts and reference material inside the skill directory and link to them with relative paths.
- State the exact trigger, purpose, and nearest excluded case in `description`, because the body is not available until the skill loads.
- Keep the frontmatter `name` equal to the skill directory name and use only lowercase letters, digits, and single hyphens.
- Write gates as explicit allow-lists with the look-alike cases they refuse.
- Leave rules owned by another skill in that skill and name it only at the procedure step that needs it.
- Ask the owner only when the answer changes the result; return unresolved owner decisions when acting as a subagent.
- Describe the checks actually run and distinguish static validation from client or runtime verification.

## Resources

Keep the main `SKILL.md` focused on the procedure every invocation needs.
Move conditional detail into a directly linked reference and keep reusable scripts for behavior that must be consistent across runs.
Make scripts non-interactive, keep their output concise, and report errors with the expected input or state.
