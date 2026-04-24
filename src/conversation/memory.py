from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChatTurn:
    role: str
    content: str


@dataclass
class ConversationMemory:
    turns: list[ChatTurn] = field(default_factory=list)

    def add_turn(self, role: str, content: str) -> None:
        self.turns.append(ChatTurn(role=role, content=content))

    def recent_history(self, max_turns: int = 6) -> list[ChatTurn]:
        return self.turns[-max_turns:]

    def recent_user_messages(self, max_messages: int = 3) -> list[str]:
        user_messages = [turn.content for turn in self.turns if turn.role == "user"]
        return user_messages[-max_messages:]
