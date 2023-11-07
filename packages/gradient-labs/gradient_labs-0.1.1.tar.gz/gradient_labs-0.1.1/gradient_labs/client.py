import json
import requests
from .errors import ResponseError
from .types import ParticipantType, Conversation
from datetime import datetime
from pytz import UTC
from typing import Any

API_BASE_URL = "https://api.gradient-labs.ai"
USER_AGENT = f"Gradient Labs Python"


class Client:
    def __init__(self, *, api_key: str, base_url: str = API_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def start_conversation(
        self,
        *,
        id: str,
        customer_id: str,
        metadata: Any = None,
        timeout: int = None,
    ) -> Conversation:
        body = self._post(
            "conversations",
            {
                "id": id,
                "customer_id": customer_id,
                "metadata": metadata,
            },
            timeout=timeout,
        )

        return Conversation(
            id=body["id"],
            customer_id=body["customer_id"],
            created=body["created"],
            updated=body["updated"],
            metadata=body["metadata"],
            status=body["status"],
        )

    def add_message(
        self,
        *,
        conversation_id: str,
        id: str,
        body: str,
        participant_id: str,
        participant_type: ParticipantType,
        created: datetime = None,
        timeout: int = None,
    ) -> None:
        if created is None:
            created = datetime.now()

        body = self._post(
            f"conversations/{conversation_id}/messages",
            {
                "id": id,
                "body": body,
                "participant_id": participant_id,
                "participant_type": participant_type,
                "created": UTC.localize(created).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
            timeout=timeout,
        )

    def cancel_conversation(self, *, id: str, timeout: int = None) -> None:
        requests.put(
            f"{self.base_url}/conversations/{id}/cancel",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": USER_AGENT,
            },
            timeout=timeout,
        )

    def _post(self, path: str, body: Any, timeout: int = None):
        url = f"{self.base_url}/{path}"

        rsp = requests.post(
            url,
            json=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": USER_AGENT,
            },
            timeout=timeout,
        )

        if rsp.status_code != 200:
            raise ResponseError(rsp)

        return rsp.json()
