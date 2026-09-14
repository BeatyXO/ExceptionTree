# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""Minimal replay-protected consumer proving typed IC-to-IC reuse of ExceptionTree."""

from genlayer import *
from dataclasses import dataclass

OUTCOME_ALLOW = 1


@gl.contract_interface
class IExceptionTree:
    class View:
        def is_outcome(
            self,
            case_id: u256,
            expected_definition_hash: str,
            expected_case_hash: str,
            required_outcome: u8,
        ) -> bool: ...

    class Write:
        pass


@allow_storage
@dataclass
class Execution:
    case_id: u256
    action_hash: str
    definition_hash: str
    case_hash: str
    executor: Address


def is_hex_hash(value: str) -> bool:
    text = str(value)
    if len(text) != 64:
        return False
    for char in text.lower():
        if char not in "0123456789abcdef":
            return False
    return True


class ExceptionGate(gl.Contract):
    exceptiontree_address: Address
    executions: TreeMap[u256, Execution]
    used_actions: TreeMap[str, u8]
    execution_count: u256

    def __init__(self, exceptiontree_address: Address):
        self.exceptiontree_address = exceptiontree_address
        self.execution_count = u256(0)

    @gl.public.write
    def execute_if_allowed(
        self,
        case_id: u256,
        expected_definition_hash: str,
        expected_case_hash: str,
        action_hash: str,
    ) -> u256:
        action = str(action_hash).lower()
        if not is_hex_hash(action):
            raise gl.vm.UserError("action_hash must be a 64-character hex digest")
        if self.used_actions.get(action) is not None:
            raise gl.vm.UserError("action replay rejected")

        tree = IExceptionTree(self.exceptiontree_address)
        allowed = tree.view().is_outcome(
            case_id,
            str(expected_definition_hash).lower(),
            str(expected_case_hash).lower(),
            u8(OUTCOME_ALLOW),
        )
        if not allowed:
            raise gl.vm.UserError("ExceptionTree does not establish ALLOW for the pinned case and ruleset")

        execution_id = u256(int(self.execution_count) + 1)
        self.executions[execution_id] = Execution(
            case_id=case_id,
            action_hash=action,
            definition_hash=str(expected_definition_hash).lower(),
            case_hash=str(expected_case_hash).lower(),
            executor=gl.message.sender_address,
        )
        self.used_actions[action] = u8(1)
        self.execution_count = execution_id
        return execution_id

    @gl.public.view
    def get_execution(self, execution_id: u256) -> dict:
        if int(execution_id) <= 0 or int(execution_id) > int(self.execution_count):
            raise gl.vm.UserError("execution does not exist")
        item = self.executions[execution_id]
        return {
            "execution_id": int(execution_id),
            "case_id": int(item.case_id),
            "action_hash": item.action_hash,
            "definition_hash": item.definition_hash,
            "case_hash": item.case_hash,
            "executor": str(item.executor),
        }
