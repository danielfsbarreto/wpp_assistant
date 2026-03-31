import json
import os
import sqlite3
import time
from pathlib import Path
from uuid import uuid4

from wpp_assistant.types import Conversation
from wpp_assistant.types.whatsapp_message import AnyWhatsappMessage, _resolve_message


class ConversationRepository:
    CONVERSATION_GAP_HOURS = 48

    def __init__(self, db_path: str | None = None):
        path = db_path or os.getenv(
            "MESSAGE_DB_PATH",
            str(Path.cwd() / "data" / "messages.db"),
        )
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path, timeout=30) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    phone_number TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    last_message_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_conversations_phone
                ON conversations(phone_number)
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    message_json TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                ON messages(conversation_id)
                """
            )

    def resolve_conversation(self, phone_number: str) -> Conversation:
        now = int(time.time())
        gap_seconds = self.CONVERSATION_GAP_HOURS * 3600

        with sqlite3.connect(self.db_path, timeout=30) as conn:
            row = conn.execute(
                """
                SELECT id, last_message_at FROM conversations
                WHERE phone_number = ?
                ORDER BY last_message_at DESC
                LIMIT 1
                """,
                (phone_number,),
            ).fetchone()

            if row and (now - row[1]) < gap_seconds:
                return self.get_conversation(row[0])

            conversation_id = str(uuid4())
            conn.execute(
                """
                INSERT INTO conversations (id, phone_number, created_at, last_message_at)
                VALUES (?, ?, ?, ?)
                """,
                (conversation_id, phone_number, now, now),
            )
            return Conversation(
                id=conversation_id, phone_number=phone_number, messages=[]
            )

    def save_messages(
        self,
        conversation_id: str,
        messages: list[AnyWhatsappMessage],
    ) -> None:
        if not messages:
            return

        with sqlite3.connect(self.db_path, timeout=30) as conn:
            phone_number = conn.execute(
                "SELECT phone_number FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()[0]

            rows = [
                (
                    conversation_id,
                    phone_number,
                    int(msg.timestamp),
                    json.dumps(msg.model_dump() if hasattr(msg, "model_dump") else msg),
                )
                for msg in messages
            ]
            max_ts = max(r[2] for r in rows)

            conn.executemany(
                """
                INSERT INTO messages (conversation_id, phone_number, timestamp, message_json)
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )
            conn.execute(
                """
                UPDATE conversations SET last_message_at = MAX(last_message_at, ?)
                WHERE id = ?
                """,
                (max_ts, conversation_id),
            )

    def get_conversation(self, conversation_id: str) -> Conversation:
        with sqlite3.connect(self.db_path, timeout=30) as conn:
            phone_number = conn.execute(
                "SELECT phone_number FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()[0]

            rows = conn.execute(
                """
                SELECT message_json FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp ASC, id ASC
                """,
                (conversation_id,),
            ).fetchall()

        messages = [_resolve_message(json.loads(row[0])) for row in rows]
        return Conversation(
            id=conversation_id, phone_number=phone_number, messages=messages
        )
