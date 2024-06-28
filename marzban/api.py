import httpx
from typing import Any, Dict, Optional, List
from .models import *

class MarzbanAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    def _get_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

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
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return Admin(**response.json())

    async def create_admin(self, admin: AdminCreate, token: str) -> Admin:
        url = "/api/admin"
        response = await self.client.post(url, json=admin.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return Admin(**response.json())

    async def modify_admin(self, username: str, admin: AdminModify, token: str) -> Admin:
        url = f"/api/admin/{username}"
        response = await self.client.put(url, json=admin.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return Admin(**response.json())

    async def remove_admin(self, username: str, token: str) -> None:
        url = f"/api/admin/{username}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
    
    async def get_admins(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None, username: Optional[str] = None) -> List[Admin]:
        url = "/api/admins"
        params = {"offset": offset, "limit": limit, "username": username}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return [Admin(**admin) for admin in response.json()]

    async def get_system_stats(self, token: str) -> SystemStats:
        url = "/api/system"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return SystemStats(**response.json())

    async def get_inbounds(self, token: str) -> Dict[str, List[ProxyInbound]]:
        url = "/api/inbounds"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_hosts(self, token: str) -> Dict [str, List[ProxyHost]]:
        url = "/api/hosts"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()
    
    async def modify_hosts(self, hosts: Dict[str, List[ProxyHost]], token: str) -> Dict[str, List[ProxyHost]]:
        url = "/api/hosts"
        response = await self.client.put(url, json=hosts, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_core_stats(self, token: str) -> CoreStats:
        url = "/api/core"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return CoreStats(**response.json())

    async def restart_core(self, token: str) -> None:
        url = "/api/core/restart"
        response = await self.client.post(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def get_core_config(self, token: str) -> Dict[str, Any]:
        url = "/api/core/config"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def modify_core_config(self, config: Dict[str, Any], token: str) -> Dict[str, Any]:
        url = "/api/core/config"
        response = await self.client.put(url, json=config, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def add_user(self, user: UserCreate, token: str) -> UserResponse:
        url = "/api/user"
        response = await self.client.post(url, json=user.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return UserResponse(**response.json())

    async def get_user(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return UserResponse(**response.json())

    async def modify_user(self, username: str, user: UserModify, token: str) -> UserResponse:
        url = f"/api/user/{username}"
        response = await self.client.put(url, json=user.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return UserResponse(**response.json())

    async def remove_user(self, username: str, token: str) -> None:
        url = f"/api/user/{username}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def reset_user_data_usage(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/reset"
        response = await self.client.post(url, headers=self._get_headers(token))
        response.raise_for_status()
        return UserResponse(**response.json())

    async def revoke_user_subscription(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/revoke_sub"
        response = await self.client.post(url, headers=self._get_headers(token))
        response.raise_for_status()
        return UserResponse(**response.json())

    async def get_users(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None, username: Optional[List[str]] = None, status: Optional[str] = None, sort: Optional[str] = None) -> UsersResponse:
        url = "/api/users"
        params = {"offset": offset, "limit": limit, "username": username, "status": status, "sort": sort}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return UsersResponse(**response.json())

    async def reset_users_data_usage(self, token: str) -> None:
        url = "/api/users/reset"
        response = await self.client.post(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def get_user_usage(self, username: str, token: str, start: Optional[str] = None, end: Optional[str] = None) -> UserUsagesResponse:
        url = f"/api/user/{username}/usage"
        params = {"start": start, "end": end}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return UserUsagesResponse(**response.json())

    async def set_owner(self, username: str, admin_username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/set-owner"
        params = {"admin_username": admin_username}
        response = await self.client.put(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return UserResponse(**response.json())

    async def get_expired_users(self, token: str, expired_before: Optional[str] = None, expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return response.json()

    async def delete_expired_users(self, token: str, expired_before: Optional[str] = None, expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self.client.delete(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return response.json()

    async def get_user_templates(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None) -> List[UserTemplateResponse]:
        url = "/api/user_template"
        params = {"offset": offset, "limit": limit}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return [UserTemplateResponse(**template) for template in response.json()]

    async def add_user_template(self, template: UserTemplateCreate, token: str) -> UserTemplateResponse:
        url = "/api/user_template"
        response = await self.client.post(url, json=template.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return UserTemplateResponse(**response.json())

    async def get_user_template(self, template_id: int, token: str) -> UserTemplateResponse:
        url = f"/api/user_template/{template_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return UserTemplateResponse(**response.json())

    async def modify_user_template(self, template_id: int, template: UserTemplateModify, token: str) -> UserTemplateResponse:
        url = f"/api/user_template/{template_id}"
        response = await self.client.put(url, json=template.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return UserTemplateResponse(**response.json())

    async def remove_user_template(self, template_id: int, token: str) -> None:
        url = f"/api/user_template/{template_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def get_node_settings(self, token: str) -> Dict[str, Any]:
        url = "/api/node/settings"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def add_node(self, node: NodeCreate, token: str) -> NodeResponse:
        url = "/api/node"
        response = await self.client.post(url, json=node.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return NodeResponse(**response.json())

    async def get_node(self, node_id: int, token: str) -> NodeResponse:
        url = f"/api/node/{node_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return NodeResponse(**response.json())

    async def modify_node(self, node_id: int, node: NodeModify, token: str) -> NodeResponse:
        url = f"/api/node/{node_id}"
        response = await self.client.put(url, json=node.dict(), headers=self._get_headers(token))
        response.raise_for_status()
        return NodeResponse(**response.json())

    async def remove_node(self, node_id: int, token: str) -> None:
        url = f"/api/node/{node_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def reconnect_node(self, node_id: int, token: str) -> None:
        url = f"/api/node/{node_id}/reconnect"
        response = await self.client.post(url, headers=self._get_headers(token))
        response.raise_for_status()

    async def get_nodes(self, token: str) -> List[NodeResponse]:
        url = "/api/nodes"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return [NodeResponse(**node) for node in response.json()]

    async def get_usage(self, token: str, start: Optional[str] = None, end: Optional[str] = None) -> NodesUsageResponse:
        url = "/api/nodes/usage"
        params = {"start": start, "end": end}
        response = await self.client.get(url, headers=self._get_headers(token), params=params)
        response.raise_for_status()
        return NodesUsageResponse(**response.json())

    async def close(self):
        await self.client.aclose()