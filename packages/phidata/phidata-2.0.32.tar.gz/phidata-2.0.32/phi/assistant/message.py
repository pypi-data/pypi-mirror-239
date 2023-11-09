from typing import List, Any, Optional, Dict

from pydantic import BaseModel, ConfigDict

from phi.assistant.exceptions import ThreadIdNotSet, MessageIdNotSet
from phi.utils.log import logger

try:
    from openai import OpenAI
    from openai.types.beta.threads.thread_message import ThreadMessage as OpenAIThreadMessage
except ImportError:
    logger.error("`openai` not installed")
    raise


class Message(BaseModel):
    # -*- Message settings
    # Message id which can be referenced in API endpoints.
    id: Optional[str] = None
    # The object type, populated by the API. Always thread.message.
    object: Optional[str] = None

    # The entity that produced the message. One of user or assistant.
    role: Optional[str] = None
    # The content of the message in array of text and/or images.
    content: List[Any] | str

    # The thread ID that this message belongs to.
    # Required to create/get a message.
    thread_id: Optional[str] = None
    # If applicable, the ID of the assistant that authored this message.
    assistant_id: Optional[str] = None
    # If applicable, the ID of the run associated with the authoring of this message.
    run_id: Optional[str] = None
    # A list of file IDs that the assistant should use.
    # Useful for tools like retrieval and code_interpreter that can access files.
    # A maximum of 10 files can be attached to a message.
    file_ids: Optional[List[Any]] = None
    # Files attached to this message.
    files: Optional[List[Any]] = None

    # Set of 16 key-value pairs that can be attached to an object.
    # This can be useful for storing additional information about the object in a structured format.
    # Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    metadata: Optional[Dict[str, Any]] = None

    # The Unix timestamp (in seconds) for when the message was created.
    created_at: Optional[int] = None

    openai: Optional[OpenAI] = None
    openai_message: Optional[OpenAIThreadMessage] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_dict(self) -> Dict[str, Any]:
        _dict: Dict[str, Any] = {
            "role": self.role,
            "content": self.content,
        }
        if self.file_ids:
            _dict["file_ids"] = self.file_ids
        if self.metadata:
            _dict["metadata"] = self.metadata
        return _dict

    @property
    def client(self) -> OpenAI:
        return self.openai or OpenAI()

    def load_from_openai(self, openai_message: OpenAIThreadMessage):
        self.id = openai_message.id
        self.object = openai_message.object
        self.role = openai_message.role
        self.content = openai_message.content
        self.created_at = openai_message.created_at

    def create(self) -> OpenAIThreadMessage:
        if self.thread_id is None:
            raise ThreadIdNotSet("Thread.id not set")

        request_body: Dict[str, Any] = {}
        if self.file_ids:
            _file_ids = self.file_ids or []
            # if self.files:
            #     for _file in self.files:
            #         _file_ids.append(_file.get_id())
            request_body["file_ids"] = _file_ids
        if self.metadata:
            request_body["metadata"] = self.metadata

        if not isinstance(self.content, str):
            raise TypeError("Message.content must be a string for create()")

        self.openai_message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=self.content, **request_body
        )
        self.load_from_openai(self.openai_message)
        return self.openai_message

    def get(self, use_cache: bool = True) -> OpenAIThreadMessage:
        if self.openai_message is not None and use_cache:
            return self.openai_message

        if self.thread_id is None:
            raise ThreadIdNotSet("Thread.id not set")

        _message_id = self.id or self.openai_message.id if self.openai_message else None
        if _message_id is not None:
            self.openai_message = self.client.beta.threads.messages.retrieve(
                thread_id=self.thread_id,
                message_id=_message_id,
            )
            self.load_from_openai(self.openai_message)
            return self.openai_message
        raise MessageIdNotSet("Message.id not set")

    def get_or_create(self, use_cache: bool = True) -> OpenAIThreadMessage:
        try:
            return self.get(use_cache=use_cache)
        except MessageIdNotSet:
            return self.create()

    def update(self) -> OpenAIThreadMessage:
        try:
            message_to_update = self.get()
            if message_to_update is not None:
                request_body: Dict[str, Any] = {}
                if self.metadata:
                    request_body["metadata"] = self.metadata

                self.openai_message = self.client.beta.threads.messages.update(
                    thread_id=message_to_update.thread_id,
                    message_id=message_to_update.id,
                    **request_body,
                )
                self.load_from_openai(self.openai_message)
                return self.openai_message
        except (ThreadIdNotSet, MessageIdNotSet):
            logger.warning("Message not available")
            raise
