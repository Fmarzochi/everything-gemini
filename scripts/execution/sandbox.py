import os
from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class SandboxPolicy:
    allowed_commands: Set[str] = field(default_factory=lambda: {"python3", "pytest", "git", "npm", "node"})
    blocked_commands: Set[str] = field(default_factory=lambda: {"rm", "sudo", "mkfs", "dd", "shutdown", "reboot", "chmod"})
    allowed_dirs: List[str] = field(default_factory=lambda: ["scripts/", "tests/", "commands/", "skills/", "agents/"])

@dataclass
class ValidationResult:
    is_valid: bool
    reason: str = ""

class SandboxController:
    def __init__(self, workspace_root: str):
        self.root = os.path.abspath(workspace_root)
        self.policy = SandboxPolicy()

    def validate_command(self, cmd: List[str]) -> ValidationResult:
        base_cmd = cmd[0]
        if base_cmd in self.policy.blocked_commands:
            return ValidationResult(False, f"Command '{base_cmd}' is blocked.")
        if base_cmd not in self.policy.allowed_commands:
            return ValidationResult(False, f"Command '{base_cmd}' is not in allowed list.")
        return ValidationResult(True)

    def validate_working_directory(self, cwd: str) -> ValidationResult:
        abs_cwd = os.path.abspath(cwd)
        if not abs_cwd.startswith(self.root):
            return ValidationResult(False, "Directory outside workspace root.")
        
        rel_path = os.path.relpath(abs_cwd, self.root)
        if rel_path == ".":
            return ValidationResult(True)
        
        # Check if the rel_path starts with one of the allowed directories
        for d in self.policy.allowed_dirs:
            # Need to remove trailing slash from allowed_dirs for check
            if rel_path.startswith(d.rstrip('/')):
                return ValidationResult(True)
            
        return ValidationResult(False, f"Directory '{rel_path}' restricted for execution.")

    def validate_execution(self, cmd: List[str], cwd: str) -> ValidationResult:
        cmd_res = self.validate_command(cmd)
        if not cmd_res.is_valid:
            return cmd_res
        return self.validate_working_directory(cwd)
