import subprocess
import json
import logging
import os
from typing import Optional, Any, Dict
from dataclasses import dataclass
from llm.core.types import ToolCall
from llm.session_recorder import SessionRecorder

# Configuração minimalista
logging.basicConfig(level=logging.INFO, format='%(asctime)s [Dispatcher] %(message)s')
logger = logging.getLogger("dispatcher")

@dataclass
class HookResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    is_veto: bool = False

class Dispatcher:
    """
    Dispatcher endurecido. Responsável pela governança síncrona,
    normalização de falhas e validação de contratos de payload.
    """

    def __init__(self, hook_path: str, recorder: SessionRecorder):
        if not os.path.exists(hook_path) or not os.access(hook_path, os.X_OK):
            if not os.path.exists(hook_path):
                raise FileNotFoundError(f"Hook não encontrado: {hook_path}")
        self.hook_path = hook_path
        self.recorder = recorder

    def dispatch(self, tool_call: ToolCall, session_id: Optional[str] = None) -> Optional[ToolCall]:
        logger.info(f"Interceptando: {tool_call.name} (Sessão: {session_id or 'N/A'})")
        
        self.recorder.record("intercept", {"tool": tool_call.name, "params": tool_call.arguments})

        payload = {
            "tool": tool_call.name,
            "params": tool_call.arguments,
            "context": {
                "session_id": session_id or "default",
                "runtime_source": "gemini-provider"
            }
        }
        # 1. Execução Segura
        result = self._execute_hook(payload, session_id)

        # 2. Normalização de Falhas
        if not result.success:
            logger.warning(f"Hook vetou ou falhou: {result.error}")
            self.recorder.record("veto", {"tool": tool_call.name, "reason": result.error})
            return None

        # 3. Validação de Schema (Hardening)
        validated = self._validate_and_reconstruct(result.data, tool_call)

        if validated:
            self.recorder.record("mutation", {"original": tool_call.arguments, "mutated": validated.arguments})
            logger.info("Mutação detectada e validada.")
        else:
            self.recorder.record("veto", {"tool": tool_call.name, "reason": "invalid_schema"})

        return validated

    def _execute_hook(self, payload: Dict[str, Any], session_id: str) -> HookResult:
        try:
            # Execução síncrona do hook com injeção de ambiente
            env = os.environ.copy()
            env["PROJECT_ROOT"] = os.getcwd()
            env["SESSION_ID"] = session_id

            process = subprocess.run(
                ['node', self.hook_path],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=5,
                env=env
            )

            # Tratamento de stderr (Apenas se crítico)
            if process.returncode != 0:
                return HookResult(success=False, error=f"Exit code {process.returncode}: {process.stderr}")

            data = json.loads(process.stdout)
            return HookResult(success=True, data=data)

        except subprocess.TimeoutExpired:
            return HookResult(success=False, error="Timeout atingido", is_veto=True)
        except json.JSONDecodeError:
            return HookResult(success=False, error="Saída malformada (JSON inválido)")
        except Exception as e:
            return HookResult(success=False, error=str(e))


            # Tratamento de stderr (Apenas se crítico)
            # Regra: Veta se exit code != 0. stderr só veta se acompanhado de erro de código.
            if process.returncode != 0:
                return HookResult(success=False, error=f"Exit code {process.returncode}: {process.stderr}")

            data = json.loads(process.stdout)
            return HookResult(success=True, data=data)

        except subprocess.TimeoutExpired:
            return HookResult(success=False, error="Timeout atingido", is_veto=True)
        except json.JSONDecodeError:
            return HookResult(success=False, error="Saída malformada (JSON inválido)")
        except Exception as e:
            return HookResult(success=False, error=str(e))

    def _validate_and_reconstruct(self, data: Dict[str, Any], original: ToolCall) -> Optional[ToolCall]:
        # Validação mínima de schema
        if "tool" not in data or "params" not in data:
            logger.error("Payload mutado inválido (missing keys)")
            return None
        
        if not isinstance(data["params"], dict):
            logger.error("Payload mutado inválido (params não é dict)")
            return None

        return ToolCall(
            id=original.id,
            name=data["tool"],
            arguments=data["params"]
        )
