import os
import json
import logging

class AgentRegistry:
    def __init__(self, workspace_root: str):
        self.root = workspace_root
        self.registry = {}
        self._index_agents()

    def _index_agents(self):
        # Maps semantic aliases to physical paths
        self.registry = {
            "python-expert": "agents/python-reviewer.md",
            "runtime-engineer": "agents/runtime-guard.md",
            "security-reviewer": "agents/security-audit.md",
            "python-reviewer": "agents/python-reviewer.md",
            "runtime-guard": "agents/runtime-guard.md",
            "security-audit": "agents/security-audit.md"
        }
        # Scan filesystem to augment registry
        for d in ["agents", ".agents", ".codex/agents"]:
            path = os.path.join(self.root, d)
            if os.path.exists(path):
                for root_dir, _, files in os.walk(path):
                    for f in files:
                        if f.endswith(".md"):
                            name = f.replace(".md", "")
                            if name not in self.registry:
                                self.registry[name] = os.path.relpath(os.path.join(root_dir, f), self.root)

    def get_physical_path(self, name: str) -> str:
        return self.registry.get(name, "")
