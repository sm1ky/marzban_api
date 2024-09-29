from pydantic import BaseModel, field_validator, ValidationInfo, AfterValidator, ValidationError
from typing import Optional, List, Dict, Any, ClassVar, Annotated

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Admin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None

class AdminCreate(Admin):
    password: str

class AdminModify(BaseModel):
    is_sudo: bool
    password: Optional[str] = None
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None

class HTTPValidationError(BaseModel):
    detail: Optional[List[Dict[str, Any]]] = None

class ProxySettings(BaseModel):
    id: Optional[str] = None
    flow: Optional[str] = None
    
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
    username: Optional[str] = None
    proxies: Optional[Dict[str, ProxySettings]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[str] = None
    inbounds: Optional[Dict[str, List[str]]] = None
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    status: Optional[str] = None
    admin: Optional[Admin] = None
    used_traffic: Optional[int] = None
    lifetime_used_traffic: Optional[int] = None
    created_at: Optional[str] = None
    links: Optional[List[str]] = []
    subscription_url: Optional[str] = None
    subscription_token: Optional[str] = None
    excluded_inbounds: Optional[Dict[str, List[str]]] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.subscription_token and self.subscription_url:
            self.subscription_token = self.subscription_url.split('/')[-1]

class NodeCreate(BaseModel):
    name: str
    address: str
    port: int = 62050
    api_port: int = 62051
    usage_coefficient: float = 1.0
    add_as_new_host: bool = True

class NodeModify(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    api_port: Optional[int] = None
    usage_coefficient: Optional[float] = None
    status: Optional[str] = None

class NodeResponse(BaseModel):
    name: str
    address: str
    port: int
    api_port: int
    usage_coefficient: float
    id: int
    xray_version: Optional[str] = None
    status: str
    message: Optional[str] = None

class NodeUsageResponse(BaseModel):
    node_id: Optional[int] = None
    node_name: Optional[str] = None
    uplink: Optional[int] = None
    downlink: Optional[int] = None

class NodesUsageResponse(BaseModel):
    usages: List[NodeUsageResponse]

class ProxyHost(BaseModel):
    remark: str
    address: str
    port: Optional[int] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
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
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[str] = None
    inbounds: Optional[Dict[str, List[str]]] = None
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    status: Optional[str] = None

class UserTemplateCreate(BaseModel):
    name: Optional[str] = None
    data_limit: int = 0
    expire_duration: int = 0
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[str, List[str]]] = {}

class UserTemplateResponse(BaseModel):
    id: int
    name: Optional[str] = None
    data_limit: int
    expire_duration: int
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Dict[str, List[str]]

class UserTemplateModify(BaseModel):
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[str, List[str]]] = None

class UserUsageResponse(BaseModel):
    node_id: Optional[int]
    node_name: Optional[str]
    used_traffic: Optional[int]

class UserUsagesResponse(BaseModel):
    username: str
    usages: List[UserUsageResponse]

class UsersResponse(BaseModel):
    users: List[UserResponse]
    total: int

class UserStatus(BaseModel):
    enum: ClassVar[List[str]] = ["active", "disabled", "limited", "expired", "on_hold"]

class ValidationError(BaseModel):
    loc: List[Any]
    msg: str
    type: str

class SubscriptionUserResponse(BaseModel):
    proxies: Dict[str, Any]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: str = "no_reset"
    inbounds: Dict[str, List[str]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    auto_delete_in_days: Optional[int] = None
    username: str
    status: str
    used_traffic: int
    lifetime_used_traffic: int = 0
    created_at: str
    links: List[str] = []
    subscription_url: str = ""
    excluded_inbounds: Dict[str, List[str]] = {}
    admin: Optional[Admin] = None
    
class SystemStats(BaseModel):
    version: Optional[str] = None
    mem_total: Optional[int] = None
    mem_used: Optional[int] = None
    cpu_cores: Optional[int] = None
    cpu_usage: Optional[float] = None
    total_user: Optional[int] = None
    users_active: Optional[int] = None
    incoming_bandwidth: Optional[int] = None
    outgoing_bandwidth: Optional[int] = None
    incoming_bandwidth_speed: Optional[int] = None
    outgoing_bandwidth_speed: Optional[int] = None