from pydantic import BaseModel
from typing import Optional

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_title: Optional[str] = None
    author_type: Optional[str] = None

class ChatAccess(BaseModel):
    access: Optional[list[str]] = []
    count_unseen: Optional[int] = None
    is_mute: Optional[bool] = None
    is_pinned: Optional[bool] = None
    time_string: Optional[str] = None
    last_message: Optional[LastMessage] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[str] = None
    status: Optional[str] = None
    time: Optional[int] = None
    pinned_message_id: Optional[str] = None
    abs_object: Optional[dict] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    slow_mode_duration: Optional[int] = None
    group_my_last_send_time: Optional[int] = None
    pinned_message_ids: Optional[list[str]] = []

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[ChatAccess] = None
    updated_parameters: Optional[list[str]] = []
    timestamp: Optional[str] = None
    type: Optional[str] = None

class LeaveGroup(BaseModel):
    chat_update: Optional[ChatUpdate]
    _client: Optional[str]
    original_update: Optional[str]

class Group(BaseModel):
    group_guid: Optional[str]
    group_title: Optional[str]
    count_members: Optional[int]
    is_deleted: Optional[bool]
    is_verified: Optional[bool]
    slow_mode: Optional[int]
    chat_history_for_new_members: Optional[str]
    event_messages: Optional[bool]
    chat_reaction_setting: Optional[dict]

class Chat(BaseModel):
    object_guid: Optional[str]
    action: Optional[str]
    access: Optional[list[str]]
    count_unseen: Optional[int]
    is_mute: Optional[bool]
    is_pinned: Optional[bool]
    time_string: Optional[str]
    last_message: Optional[dict]
    last_seen_my_mid: Optional[str]
    last_seen_peer_mid: Optional[str]
    status: Optional[str]
    time: Optional[int]
    abs_object: Optional[dict]
    is_blocked: Optional[bool]
    last_message_id: Optional[str]
    last_deleted_mid: Optional[str]
    slow_mode_duration: Optional[int]

class MessageUpdate(BaseModel):
    message_id: Optional[str]
    action: Optional[str]
    message: Optional[dict]
    updated_parameters: Optional[list[str]]
    timestamp: Optional[str]
    prev_message_id: Optional[str]
    object_guid: Optional[str]
    type: Optional[str]
    state: Optional[str]

class JoinGroup(BaseModel):
    group: Optional[Group]
    is_valid: Optional[bool]
    chat_update: Optional[Chat]
    message_update: Optional[MessageUpdate]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[dict]

class AddGroup(BaseModel):
    group: Optional[Group]
    chat_update: Optional[Chat]
    message_update: Optional[MessageUpdate]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[dict]

class RemoveGroup(BaseModel):
    chat_update: Optional[Chat]
    _client: Optional[str]
    original_update: Optional[dict]

class GetGroupInfo(BaseModel):
    group: Optional[Group]
    chat: Optional[Chat]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[dict]
    message_update: Optional[MessageUpdate]

class GroupLink(BaseModel):
    join_link: Optional[str]
    _client: Optional[str]
    original_update: Optional[dict]

class EditGroupInfo(BaseModel):
    group: Optional[Group]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[dict]

class OnlineTime(BaseModel):
    type: Optional[str]
    approximate_period: Optional[str]

class InChatMemberList(BaseModel):
    member_type: Optional[str]
    member_guid: Optional[str]
    first_name: Optional[str]
    is_verified: Optional[bool]
    is_deleted: Optional[bool]
    promoted_by_object_guid: Optional[str]
    promoted_by_object_type: Optional[str]
    join_type: Optional[str]
    online_time: Optional[OnlineTime]

class InChatMember(BaseModel):
    in_chat_member: Optional[InChatMemberList]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class BanGroupMember(BaseModel):
    group: Optional[Group]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class AvatarThumbnail(BaseModel):
    file_id: Optional[str]
    mime: Optional[str]
    dc_id: Optional[str]
    access_hash_rec: Optional[str]

class AddedInChatMember(BaseModel):
    member_type: Optional[str]
    member_guid: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_thumbnail: Optional[AvatarThumbnail]
    is_verified: Optional[bool]
    is_deleted: Optional[bool]
    last_online: Optional[int]
    join_type: Optional[str]
    username: Optional[str]
    online_time: Optional[OnlineTime]

class AddGroupMembers(BaseModel):
    chat_update: Optional[ChatUpdate]
    message_update: Optional[MessageUpdate]
    added_in_chat_members: Optional[list[AddedInChatMember]]
    timestamp: Optional[str]
    group: Optional[Group]
    _client: Optional[str]
    original_update: Optional[str]

class InChatGroupMember(BaseModel):
    member_type: Optional[str]
    member_guid: Optional[str]
    first_name: Optional[str]
    is_verified: Optional[bool]
    is_deleted: Optional[bool]
    last_online: Optional[int]
    join_type: Optional[str]
    online_time: Optional[OnlineTime]
    promoted_by_object_guid: Optional[str]
    promoted_by_object_type: Optional[str]

class GetAllGroupMembers(BaseModel):
    in_chat_members: Optional[list[InChatGroupMember]]
    next_start_id: Optional[str]
    has_continue: Optional[bool]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class GetGroupAdminMembers(BaseModel):
    in_chat_members: Optional[list[InChatGroupMember]]
    next_start_id: Optional[str]
    has_continue: Optional[bool]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class GetGroupMentionList(BaseModel):
    in_chat_members: Optional[list[InChatGroupMember]]
    next_start_id: Optional[str]
    has_continue: Optional[bool]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class GetGroupDefaultAccess(BaseModel):
    access_list: Optional[list]
    _client: Optional[str]
    original_update: Optional[str]

class OnlineTime(BaseModel):
    type: Optional[str]
    approximate_period: Optional[str]

class TopParticipants(BaseModel):
    member_type: Optional[str]
    member_guid: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_thumbnail: Optional[AvatarThumbnail]
    is_verified: Optional[bool]
    is_deleted: Optional[bool]
    username: Optional[str]
    online_time: Optional[OnlineTime]

class GroupPreviewByJoinLink(BaseModel):
    is_valid: Optional[bool]
    group: Optional[Group]
    has_joined: Optional[bool]
    top_participants: Optional[list[TopParticipants]]
    timestamp: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]

class DeleteNoAccessGroupChat(BaseModel):
    chat_update: Optional[ChatUpdate]
    status: Optional[str]
    _client: Optional[str]
    original_update: Optional[str]