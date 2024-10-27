import httpx
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
from .models import *

class MarzbanAPI:
    def __init__(self, base_url: str, *, timeout: float = 10.0, verify: bool = False):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, verify=verify, timeout=timeout)

    def _get_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    async def _request(self, method: str, url: str, token: Optional[str] = None, data: Optional[BaseModel] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        headers = self._get_headers(token) if token else {}
        json_data = data.model_dump(exclude_none=True) if data else None
        params = {k: v for k, v in (params or {}).items() if v is not None}
        response = await self.client.request(method, url, headers=headers, json=json_data, params=params)
        response.raise_for_status()
        return response

    async def get_token(self, username: str, password: str) -> Token:
        url = "/api/admin/token"
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
        response = await self.client.post(url, data=payload)
        response.raise_for_status()
        return Token(**response.json())

    async def get_current_admin(self, token: str) -> Admin:
        url = "/api/admin"
        response = await self._request("GET", url, token)
        return Admin(**response.json())

    async def create_admin(self, admin: AdminCreate, token: str) -> Admin:
        url = "/api/admin"
        response = await self._request("POST", url, token, data=admin)
        return Admin(**response.json())

    async def modify_admin(self, username: str, admin: AdminModify, token: str) -> Admin:
        url = f"/api/admin/{username}"
        response = await self._request("PUT", url, token, data=admin)
        return Admin(**response.json())

    async def remove_admin(self, username: str, token: str) -> None:
        url = f"/api/admin/{username}"
        await self._request("DELETE", url, token)

    async def get_admins(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None, username: Optional[str] = None) -> List[Admin]:
        url = "/api/admins"
        params = {"offset": offset, "limit": limit, "username": username}
        response = await self._request("GET", url, token, params=params)
        return [Admin(**admin) for admin in response.json()]

    async def get_system_stats(self, token: str) -> SystemStats:
        url = "/api/system"
        response = await self._request("GET", url, token)
        return SystemStats(**response.json())

    async def get_inbounds(self, token: str) -> Dict[str, List[ProxyInbound]]:
        url = "/api/inbounds"
        response = await self._request("GET", url, token)
        return response.json()

    async def get_hosts(self, token: str) -> Dict[str, List[ProxyHost]]:
        url = "/api/hosts"
        response = await self._request("GET", url, token)
        return response.json()
    
    async def modify_hosts(self, hosts: Dict[str, List[ProxyHost]], token: str) -> Dict[str, List[ProxyHost]]:
        url = "/api/hosts"
        response = await self._request("PUT", url, token, data=hosts)
        return response.json()

    async def get_core_stats(self, token: str) -> CoreStats:
        url = "/api/core"
        response = await self._request("GET", url, token)
        return CoreStats(**response.json())

    async def restart_core(self, token: str) -> None:
        url = "/api/core/restart"
        await self._request("POST", url, token)

    async def get_core_config(self, token: str) -> Dict[str, Any]:
        url = "/api/core/config"
        response = await self._request("GET", url, token)
        return response.json()

    async def modify_core_config(self, config: Dict[str, Any], token: str) -> Dict[str, Any]:
        url = "/api/core/config"
        response = await self._request("PUT", url, token, data=config)
        return response.json()

    async def add_user(self, user: UserCreate, token: str) -> UserResponse:
        url = "/api/user"
        response = await self._request("POST", url, token, data=user)
        return UserResponse(**response.json())

    async def get_user(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}"
        response = await self._request("GET", url, token)
        return UserResponse(**response.json())

    async def modify_user(self, username: str, user: UserModify, token: str) -> UserResponse:
        url = f"/api/user/{username}"
        response = await self._request("PUT", url, token, data=user)
        return UserResponse(**response.json())

    async def remove_user(self, username: str, token: str) -> None:
        url = f"/api/user/{username}"
        await self._request("DELETE", url, token)

    async def reset_user_data_usage(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/reset"
        response = await self._request("POST", url, token)
        return UserResponse(**response.json())

    async def revoke_user_subscription(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/revoke_sub"
        response = await self._request("POST", url, token)
        return UserResponse(**response.json())

    async def get_users(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None, username: Optional[List[str]] = None, status: Optional[str] = None, sort: Optional[str] = None) -> UsersResponse:
        url = "/api/users"
        params = {"offset": offset, "limit": limit, "username": username, "status": status, "sort": sort}
        response = await self._request("GET", url, token, params=params)
        return UsersResponse(**response.json())

    async def reset_users_data_usage(self, token: str) -> None:
        url = "/api/users/reset"
        await self._request("POST", url, token)

    async def get_user_usage(self, username: str, token: str, start: Optional[str] = None, end: Optional[str] = None) -> UserUsagesResponse:
        url = f"/api/user/{username}/usage"
        params = {"start": start, "end": end}
        response: httpx.Response = await self._request("GET", url, token, params=params)
        return UserUsagesResponse(**response.json())

    async def set_owner(self, username: str, admin_username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/set-owner?admin_username={admin_username}"
        response = await self._request("PUT", url, token)
        return UserResponse(**response.json())

    async def get_expired_users(self, token: str, expired_before: Optional[str] = None, expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self._request("GET", url, token, params=params)
        return response.json()

    async def delete_expired_users(self, token: str, expired_before: Optional[str] = None, expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self._request("DELETE", url, token, params=params)
        return response.json()

    async def get_user_templates(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None) -> List[UserTemplateResponse]:
        url = "/api/user_template"
        params = {"offset": offset, "limit": limit}
        response = await self._request("GET", url, token, params=params)
        return [UserTemplateResponse(**template) for template in response.json()]

    async def add_user_template(self, template: UserTemplateCreate, token: str) -> UserTemplateResponse:
        url = "/api/user_template"
        response = await self._request("POST", url, token, data=template)
        return UserTemplateResponse(**response.json())

    async def get_user_template(self, template_id: int, token: str) -> UserTemplateResponse:
        url = f"/api/user_template/{template_id}"
        response = await self._request("GET", url, token)
        return UserTemplateResponse(**response.json())

    async def modify_user_template(self, template_id: int, template: UserTemplateModify, token: str) -> UserTemplateResponse:
        url = f"/api/user_template/{template_id}"
        response = await self._request("PUT", url, token, data=template)
        return UserTemplateResponse(**response.json())
    
    async def remove_user_template(self, template_id: int, token: str) -> None:
        url = f"/api/user_template/{template_id}"
        await self._request("DELETE", url, token)

    async def get_node_settings(self, token: str) -> Dict[str, Any]:
        url = "/api/node/settings"
        response = await self._request("GET", url, token)
        return response.json()

    async def add_node(self, node: NodeCreate, token: str) -> NodeResponse:
        url = "/api/node"
        response = await self._request("POST", url, token, data=node)
        return NodeResponse(**response.json())

    async def get_node(self, node_id: int, token: str) -> NodeResponse:
        url = f"/api/node/{node_id}"
        response = await self._request("GET", url, token)
        return NodeResponse(**response.json())

    async def modify_node(self, node_id: int, node: NodeModify, token: str) -> NodeResponse:
        url = f"/api/node/{node_id}"
        response = await self._request("PUT", url, token, data=node)
        return NodeResponse(**response.json())

    async def remove_node(self, node_id: int, token: str) -> None:
        url = f"/api/node/{node_id}"
        await self._request("DELETE", url, token)

    async def reconnect_node(self, node_id: int, token: str) -> None:
        url = f"/api/node/{node_id}/reconnect"
        await self._request("POST", url, token)

    async def get_nodes(self, token: str) -> List[NodeResponse]:
        url = "/api/nodes"
        response = await self._request("GET", url, token)
        return [NodeResponse(**node) for node in response.json()]

    async def get_usage(self, token: str, start: Optional[str] = None, end: Optional[str] = None) -> NodesUsageResponse:
        url = "/api/nodes/usage"
        params = {"start": start, "end": end}
        response = await self._request("GET", url, token, params=params)
        return NodesUsageResponse(**response.json())

    async def get_user_subscription_info(self, url: str = None, token: str = None) -> SubscriptionUserResponse:
        if url:
            # Use the provided URL if it is given
            final_url = url + "/info"
        elif token:
            # Form the URL using the token if it is provided
            final_url = f"/sub/{token}/info"
        else:
            raise ValueError("Either url or token must be provided")
        
        response = await self._request("GET", final_url)
        return SubscriptionUserResponse(**response.json())

    async def get_user_usage(self, url: str = None, token: str = None, start: Optional[str] = None, end: Optional[str] = None) -> Any:
        if url:
            # Use the provided URL if it is given
            final_url = url + "/usage"
        elif token:
            # Form the URL using the token if it is provided
            final_url = f"/sub/{token}/usage"
        else:
            raise ValueError("Either url or token must be provided")
        
        params = {"start": start, "end": end}
        response = await self._request("GET", final_url, params=params)
        return response.json()

    async def get_user_subscription_with_client_type(self, client_type: str, url: str = None, token: str = None) -> Any:
        if url:
            # Use the provided URL if it is given
            final_url = url + f"/{client_type}"
        elif token:
            # Form the URL using the token if it is provided
            final_url = f"/sub/{token}/{client_type}"
        else:
            raise ValueError("Either url or token must be provided")
        
        response = await self._request("GET", final_url)
        return response.json()

    async def close(self):
        await self.client.aclose()
