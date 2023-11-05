from pydantic import BaseModel
from typing import Optional, Union

class FileInline(BaseModel):
    file_id: Optional[str]
    mime: Optional[str]
    dc_id: Optional[str]
    access_hash_rec: Optional[str]
    file_name: Optional[str]
    thumb_inline: Optional[str]
    music_performer: Optional[str]
    width: Optional[int]
    height: Optional[int]
    time: Optional[int]
    size: Optional[int]
    type: Optional[str]

class Message(BaseModel):
    message_id: Optional[str]
    text: Optional[str]
    file_inline: Optional[FileInline]
    time: Optional[str]
    is_edited: Optional[bool]
    type: Optional[str]
    author_type: Optional[str]
    author_object_guid: Optional[str]

class MessageUpdate(BaseModel):
    message_id: Optional[str]
    action: Optional[str]
    message: Optional[Message]
    updated_parameters: Optional[list]
    timestamp: Optional[str]
    prev_message_id: Optional[str]
    object_guid: Optional[str]
    type: Optional[str]
    state: Optional[str]

class LastMessage(BaseModel):
    message_id: Optional[str]
    type: Optional[str]
    text: Optional[str]
    author_object_guid: Optional[str]
    is_mine: Optional[bool]
    author_title: Optional[str]
    author_type: Optional[str]

class Chat(BaseModel):
    time_string: Optional[str]
    last_message: Optional[LastMessage]  # از مدل LastMessage برای این متغیر استفاده شده است
    last_seen_my_mid: Optional[str]
    last_seen_peer_mid: Optional[str]
    status: Optional[str]
    time: Optional[int]
    last_message_id: Optional[str]

class ChatUpdate(BaseModel):
    object_guid: Optional[str]
    action: Optional[str]
    chat: Optional[Chat]
    updated_parameters: Optional[list]
    timestamp: Optional[str]
    type: Optional[str]

class SendMessage(BaseModel):
    message_update: Optional[MessageUpdate]
    status: Optional[str]
    chat_update: Optional[ChatUpdate]
    _client: Optional[str]
    original_update: Optional[str]