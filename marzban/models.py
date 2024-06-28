from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Admin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int]
    discord_webhook: Optional[str]

class AdminCreate(Admin):
    password: str

class AdminModify(BaseModel):
    is_sudo: bool
    password: Optional[str]
    telegram_id: Optional[int]
    discord_webhook: Optional[str]

class HTTPValidationError(BaseModel):
    detail: Optional[List[Dict[str, Any]]]

class SystemStats(BaseModel):
    version: str
    mem_total: int
    mem_used: int
    cpu_cores: int
    cpu_usage: float
    total_user: int
    users_active: int
    incoming_bandwidth: int
    outgoing_bandwidth: int
    incoming_bandwidth_speed: int
    outgoing_bandwidth_speed: int

class ProxySettings(BaseModel):
    pass

class UserCreate(BaseModel):
    username: str
    proxies: Optional[Dict[str, ProxySettings]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = 0
    data_limit_reset_strategy: Optional[str] = "no_reset"
    inbounds: Optional[Dict[str, List[str]]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = 0
    on_hold_timeout: Optional[str] = None
    status: Optional[str] = "active"

class UserResponse(BaseModel):
    username: str
    proxies: Dict[str, ProxySettings]
    expire: Optional[int]
    data_limit: int
    data_limit_reset_strategy: str
    inbounds: Dict[str, List[str]]
    note: Optional[str]
    sub_updated_at: Optional[str]
    sub_last_user_agent: Optional[str]
    online_at: Optional[str]
    on_hold_expire_duration: Optional[int]
    on_hold_timeout: Optional[str]
    status: str
    used_traffic: int
    lifetime_used_traffic: int
    created_at: str
    links: List[str]
    subscription_url: str
    excluded_inbounds: Dict[str, List[str]]

class NodeCreate(BaseModel):
    name: str
    address: str
    port: int = 62050
    api_port: int = 62051
    usage_coefficient: float = 1.0
    add_as_new_host: bool = True

class NodeModify(BaseModel):
    name: Optional[str]
    address: Optional[str]
    port: Optional[int]
    api_port: Optional[int]
    usage_coefficient: Optional[float]
    status: Optional[str]

class NodeResponse(BaseModel):
    name: str
    address: str
    port: int
    api_port: int
    usage_coefficient: float
    id: int
    xray_version: Optional[str]
    status: str
    message: Optional[str]

class NodeUsageResponse(BaseModel):
    node_id: int
    node_name: str
    uplink: int
    downlink: int

class NodesUsageResponse(BaseModel):
    usages: List[NodeUsageResponse]

class ProxyHost(BaseModel):
    remark: str
    address: str
    port: Optional[int]
    sni: Optional[str]
    host: Optional[str]
    path: Optional[str]
    security: str = "inbound_default"
    alpn: str = ""
    fingerprint: str = ""
    allowinsecure: bool
    is_disabled: bool

class ProxyInbound(BaseModel):
    tag: str
    protocol: str
    network: str
    tls: str
    port: Any

class CoreStats(BaseModel):
    version: str
    started: bool
    logs_websocket: str

class UserModify(BaseModel):
    proxies: Optional[Dict[str, ProxySettings]] = {}
    expire: Optional[int]
    data_limit: Optional[int] = 0
    data_limit_reset_strategy: Optional[str] = "no_reset"
    inbounds: Optional[Dict[str, List[str]]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = 0
    on_hold_timeout: Optional[str] = None
    status: Optional[str] = "active"

class UserTemplateCreate(BaseModel):
    name: Optional[str]
    data_limit: int = 0
    expire_duration: int = 0
    username_prefix: Optional[str]
    username_suffix: Optional[str]
    inbounds: Optional[Dict[str, List[str]]] = {}

class UserTemplateResponse(BaseModel):
    id: int
    name: Optional[str]
    data_limit: int
    expire_duration: int
    username_prefix: Optional[str]
    username_suffix: Optional[str]
    inbounds: Dict[str, List[str]]

class UserTemplateModify(BaseModel):
    name: Optional[str]
    data_limit: Optional[int]
    expire_duration: Optional[int]
    username_prefix: Optional[str]
    username_suffix: Optional[str]
    inbounds: Optional[Dict[str, List[str]]]

class UserUsageResponse(BaseModel):
    node_id: int
    node_name: str
    used_traffic: int

class UserUsagesResponse(BaseModel):
    username: str
    usages: List[UserUsageResponse]

class UsersResponse(BaseModel):
    users: List[UserResponse]
    total: int

class UserStatus(BaseModel):
    enum = ["active", "disabled", "limited", "expired", "on_hold"]

class ValidationError(BaseModel):
    loc: List[Any]
    msg: str
    type: str