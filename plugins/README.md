# Plugins and Marketplaces


---

## Marketplaces

Marketplaces are repositories of installable plugins.

### Adding a Marketplace

```bash
# Add official Google marketplace
gemini plugin marketplace add https://github.com/google-gemini/gemini-plugins-official

# Add community marketplaces (mgrep by @mixedbread-ai)
gemini plugin marketplace add https://github.com/mixedbread-ai/mgrep
```

### Recommended Marketplaces

| Marketplace | Source |
|-------------|--------|
| gemini-plugins-official | `google-gemini/gemini-plugins-official` |
| gemini-code-plugins | `google-gemini/gemini-code` |
| Mixedbread-Grep (@mixedbread-ai) | `mixedbread-ai/mgrep` |

---

## Installing Plugins

```bash
# Open plugins browser
/plugins

# Or install directly
gemini plugin install typescript-lsp@gemini-plugins-official
```

### Recommended Plugins

**Development:**
- `typescript-lsp` - TypeScript intelligence
- `pyright-lsp` - Python type checking
- `hookify` - Create hooks conversationally
- `code-simplifier` - Refactor code

**Code Quality:**
- `code-review` - Code review
- `pr-review-toolkit` - PR automation
- `security-guidance` - Security checks

**Search:**
- `mgrep` - Enhanced search (better than ripgrep)
- `context7` - Live documentation lookup

**Workflow:**
- `commit-commands` - Git workflow
- `frontend-patterns` - UI patterns
- `feature-dev` - Feature development

---

## Quick Setup

```bash
# Add marketplaces
gemini plugin marketplace add https://github.com/google-gemini/gemini-plugins-official
gemini plugin marketplace add https://github.com/mixedbread-ai/mgrep

# Open /plugins and install what you need
```

---

## Plugin Files Location

```
~/.gemini/plugins/
|-- cache/                    # Downloaded plugins
|-- installed_plugins.json    # Installed list
|-- known_marketplaces.json   # Added marketplaces
|-- marketplaces/             # Marketplace data
```
