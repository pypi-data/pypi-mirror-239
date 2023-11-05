from pydantic import BaseModel, HttpUrl, Field, PositiveInt
from typing import Optional, List

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class Object(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    count_members: Optional[int] = None
    username: Optional[str] = None

class SearchGlobalObjects(BaseModel):
    objects: list[Object]
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OnlineTime(BaseModel):
    type: Optional[str] = None
    approximate_period: Optional[str] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_type: Optional[str] = None

class AbsObject(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Chat(BaseModel):
    object_guid: Optional[str] = None
    access: Optional[list[str]] = None
    count_unseen: Optional[int] = None
    is_mute: Optional[bool] = None
    is_pinned: Optional[bool] = None
    time_string: Optional[str] = None
    last_message: Optional[LastMessage] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[str] = None
    status: Optional[str] = None
    time: Optional[int] = None
    abs_object: Optional[AbsObject] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    is_in_contact: Optional[bool] = None

class ChatReactionSetting(BaseModel):
    reaction_type: Optional[str] = Field(None, description="Type of reactions in chat")
    selected_reactions: Optional[List[str]] = Field(None, description="List of selected reactions in the chat")

class User(BaseModel):
    user_guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    last_online: Optional[int] = None
    bio: Optional[str] = None
    is_deleted: Optional[bool] = None
    is_verified: Optional[bool] = None
    online_time: Optional[OnlineTime] = None

class Channel(BaseModel):
    channel_guid: Optional[str] = Field(None, description="Channel ID")
    channel_title: Optional[str] = Field(None, description="Channel title")
    avatar_thumbnail: Optional[AvatarThumbnail] = Field(None, description="Profile image information")
    count_members: Optional[PositiveInt] = Field(None, description="Number of channel members")
    description: Optional[str] = Field(None, description="Channel description")
    username: Optional[str] = Field(None, description="Channel username")
    is_deleted: Optional[bool] = Field(None, description="Channel deletion status")
    is_verified: Optional[bool] = Field(None, description="Channel verification status")
    share_url: Optional[HttpUrl] = Field(None, description="Channel sharing URL")
    channel_type: Optional[str] = Field(None, description="Channel type")
    sign_messages: Optional[bool] = Field(None, description="Message signing capability status")
    chat_reaction_setting: Optional[ChatReactionSetting] = Field(None, description="Conversation reaction settings")

class GetObjectByUsername(BaseModel):
    exist: Optional[bool] = None
    type: Optional[str] = None
    user: Optional[User] = None
    channel: Optional[Channel] = None
    chat: Optional[Chat] = None
    timestamp: Optional[str] = None
    is_in_contact: Optional[bool] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OpenChatData(BaseModel):
    object_guid: Optional[str] = None
    object_type: Optional[str] = None
    message_id: Optional[int] = None

class LinkData(BaseModel):
    type: Optional[str] = None
    link_url: Optional[str] = None
    open_chat_data: Optional[OpenChatData] = None

class GetLinkFromAppUrl(BaseModel):
    link: Optional[LinkData] = None

class ChatGuidType(BaseModel):
    type: Optional[str]
    object_guid: Optional[str]

class MessageInfo(BaseModel):
    message_id: Optional[str]
    type: Optional[str]
    text: Optional[str]
    is_mine: Optional[bool]

class ChatInfo(BaseModel):
    time_string: Optional[str]
    last_message: Optional[MessageInfo]
    time: Optional[int]
    last_message_id: Optional[str]
    group_voice_chat_id: Optional[str]

class ChatUpdate(BaseModel):
    object_guid: Optional[str]
    action: Optional[str]
    chat: Optional[ChatInfo]
    updated_parameters: Optional[list[str]]
    timestamp: Optional[str]
    type: Optional[str]

class PerformerData(BaseModel):
    type: Optional[str]
    object_guid: Optional[str]

class EventData(BaseModel):
    type: Optional[str]
    performer_object: Optional[PerformerData]

class MessageData(BaseModel):
    message_id: Optional[str]
    text: Optional[str]
    time: Optional[str]
    is_edited: Optional[bool]
    type: Optional[str]
    event_data: Optional[EventData]

class MessageUpdate(BaseModel):
    message_id: Optional[str]
    action: Optional[str]
    message: Optional[MessageData]
    updated_parameters: Optional[list[str]]
    timestamp: Optional[str]
    prev_message_id: Optional[str]
    object_guid: Optional[str]
    type: Optional[str]
    state: Optional[str]

class GroupVoiceChatData(BaseModel):
    voice_chat_id: Optional[str]
    state: Optional[str]
    join_muted: Optional[bool]
    participant_count: Optional[int]
    title: Optional[str]
    version: Optional[int]

class ChannelVoiceChatData(BaseModel):
    voice_chat_id: Optional[str]
    state: Optional[str]
    join_muted: Optional[bool]
    participant_count: Optional[int]
    title: Optional[str]
    version: Optional[int]

class GroupVoiceChatUpdate(BaseModel):
    voice_chat_id: Optional[str]
    group_guid: Optional[str]
    action: Optional[str]
    group_voice_chat: Optional[GroupVoiceChatData]
    updated_parameters: Optional[list[str]]
    timestamp: Optional[str]
    chat_guid_type: Optional[ChatGuidType]

class ChannelVoiceChatUpdate(BaseModel):
    voice_chat_id: Optional[str]
    channel_guid: Optional[str]
    action: Optional[str]
    channel_voice_chat: Optional[ChannelVoiceChatData]
    updated_parameters: Optional[list[str]]
    timestamp: Optional[str]
    chat_guid_type: Optional[ChatGuidType]

class ExistGroupVoiceChat(BaseModel):
    voice_chat_id: Optional[str]
    state: Optional[str]
    join_muted: Optional[bool]
    participant_count: Optional[int]
    title: Optional[str]
    version: Optional[int]

class ExistChannelVoiceChat(BaseModel):
    voice_chat_id: Optional[str]
    state: Optional[str]
    join_muted: Optional[bool]
    participant_count: Optional[int]
    title: Optional[str]
    version: Optional[int]

class CreateVoiceCall(BaseModel):
    status: Optional[str]
    chat_update: Optional[ChatUpdate]
    message_update: Optional[MessageUpdate]
    group_voice_chat_update: Optional[GroupVoiceChatUpdate]
    channel_voice_chat_update: Optional[ChannelVoiceChatUpdate]
    exist_group_voice_chat: Optional[ExistGroupVoiceChat]
    exist_channel_voice_chat: Optional[ExistChannelVoiceChat]
    _client: Optional[str]
    original_update: Optional[str]