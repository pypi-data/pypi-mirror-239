from pydantic import BaseModel
from typing import Optional, List

class FileInline(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    thumb_inline: Optional[str] = None
    music_performer: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    time: Optional[int] = None
    size: Optional[int] = None
    type: Optional[str] = None

class ForwardedFrom(BaseModel):
    type_from: Optional[str] = None
    message_id: Optional[str] = None
    object_guid: Optional[str] = None

class PollOption(BaseModel):
    options: Optional[List[str]] = []
    poll_status: Optional[dict] = None
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None

class Poll(BaseModel):
    poll_id: Optional[str] = None
    question: Optional[str] = None
    options: Optional[List[str]] = None
    poll_status: Optional[dict] = None
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class MessageData(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    file_inline: Optional[FileInline] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    author_type: Optional[str] = None
    author_object_guid: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    poll: Optional[Poll] = None

class AbsObject(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Message(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    file_inline: Optional[FileInline] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    author_type: Optional[str] = None
    author_object_guid: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    poll: Optional[Poll] = None
    object_guid: Optional[str] = None
    message: Optional[MessageData] = None
    abs_object: Optional[AbsObject] = None
    last_seen_peer_mid: Optional[int] = None

class MessageUpdate(BaseModel):
    message_id: Optional[str] = None
    action: Optional[str] = None
    message: Optional[Message] = None
    updated_parameters: Optional[list] = None
    timestamp: Optional[str] = None
    prev_message_id: Optional[str] = None
    object_guid: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_title: Optional[str] = None
    author_type: Optional[str] = None

class Chat(BaseModel):
    time_string: Optional[str] = None
    last_message: Optional[LastMessage] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[int] = None
    status: Optional[str] = None
    time: Optional[int] = None
    last_message_id: Optional[str] = None

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[Chat] = None
    updated_parameters: Optional[list] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None

class SendMessage(BaseModel):
    message_update: Optional[MessageUpdate] = None
    status: Optional[str] = None
    chat_update: Optional[ChatUpdate] = None

class EditMessage(BaseModel):
    message_update: Optional[MessageUpdate] = None
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class DeleteMessages(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    message_updates: Optional[List[MessageUpdate]] = []
    _client: Optional[str] = None
    original_update: Optional[str] = None

class RequestSendFile(BaseModel):
    id: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_send: Optional[str] = None
    upload_url: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class ForwardMessages(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    message_updates: Optional[List[MessageUpdate]] = []
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class PollStatus(BaseModel):
    state: Optional[str] = None
    selection_index: Optional[int] = None
    percent_vote_options: Optional[list[int]] = None
    total_vote: Optional[int] = None
    show_total_votes: Optional[bool] = None

class VotePoll(BaseModel):
    poll_status: Optional[PollStatus] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SetPinMessage(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesUpdates(BaseModel):
    updated_messages: Optional[List[MessageUpdate]] = []
    new_state: Optional[int] = None
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SearchGlobalMessages(BaseModel):
    messages: Optional[List[Message]] = []
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesByID(BaseModel):
    messages: Optional[List[Message]] = []
    timestamp: Optional[int] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesInterval(BaseModel):
    messages: Optional[List[Message]] = []
    state: Optional[str] = None
    new_has_continue: Optional[bool] = None
    old_has_continue: Optional[bool] = None
    new_min_id: Optional[int] = None
    old_max_id: Optional[int] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class Reactions(BaseModel):
    user_guids: Optional[List] = []
    reaction_count: Optional[int] = None
    emoji_char: Optional[str] = None
    reaction_id: Optional[int] = None
    is_selected: Optional[bool] = None

class Reacion(BaseModel):
    reactions: Optional[List[Reactions]] = []