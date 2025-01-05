import httpx
import paramiko
from paramiko.ssh_exception import SSHException
from sshtunnel import SSHTunnelForwarder
from datetime import datetime
from .models import *
from typing import Optional
class MarzbanAPI:
    def __init__(self,
                 base_url: str, *,
                 timeout: float = 10.0, verify: bool = False,
                 ssh_username: Optional[str] = None,
                 ssh_host: Optional[str] = None,
                 ssh_port: Optional[int] = 22,
                 ssh_private_key_path: Optional[str] = None,
                 ssh_key_passphrase: Optional[str] = None,
                 ssh_password: Optional[str] = None,
                 local_bind_host: str = '127.0.0.1',
                 local_bind_port: int = 8000,
                 remote_bind_host: str = '127.0.0.1',
                 remote_bind_port: int = 8000
                 ):
        """
        Initializes the MarzbanAPI client with optional SSH tunneling for secure remote access.

        :param base_url: The base URL of the Marzban API.
        :param timeout: The request timeout in seconds (default: 10.0).
        :param verify: SSL verification flag; set to False to ignore SSL verification (default: False).
        :param ssh_username: SSH username for tunnel authentication.
        :param ssh_host: SSH server address for setting up the tunnel. If None, no SSH tunnel is used.
        :param ssh_port: SSH port for connecting to the server (default: 22).
        :param ssh_private_key_path: Path to the SSH private key file for authentication.
        :param ssh_key_passphrase: Passphrase for the SSH private key, if applicable.
        :param ssh_password: Password for SSH authentication. Use if no private key is provided.
        :param local_bind_host: Local IP address for binding the SSH tunnel (default: '127.0.0.1').
        :param local_bind_port: Local port for SSH tunnel binding (default: 8000).
        :param remote_bind_host: Remote IP address for binding on the SSH server side (default: '127.0.0.1').
        :param remote_bind_port: Remote port for the SSH server binding (default: 8000).

        :raises ValueError: If SSH tunneling is requested but neither a private key nor password is provided.
        """

        self.base_url = base_url
        self.timeout = timeout
        self.verify = verify
        self.ssh_username = ssh_username
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_private_key_path = ssh_private_key_path
        self.ssh_key_passphrase = ssh_key_passphrase
        self.ssh_password = ssh_password
        self.local_bind_host = local_bind_host
        self.local_bind_port = local_bind_port
        self.remote_bind_host = remote_bind_host
        self.remote_bind_port = remote_bind_port
        self.client = None
        self._tunnel = None
        self._forwarder = None
        if ssh_host and not ssh_private_key_path and not ssh_password:
            raise ValueError('For an SSH tunnel, you must specify either ssh_private_key_path or ssh_password')
        if not ssh_host:
            self.client = httpx.AsyncClient(base_url=self.base_url, verify=self.verify, timeout=self.timeout)

    def _load_private_key(self, key_path, passphrase):
        key_classes = [paramiko.RSAKey, paramiko.DSSKey, paramiko.ECDSAKey, paramiko.Ed25519Key]
        for key_class in key_classes:
            try:
                if passphrase:
                    pkey = key_class.from_private_key_file(
                        key_path,
                        password=passphrase
                    )
                else:
                    pkey = key_class.from_private_key_file(key_path)
                return pkey
            except paramiko.ssh_exception.PasswordRequiredException:
                print("Ошибка: Приватный ключ защищен паролем. Пожалуйста, укажите пароль.")
            except SSHException:
                continue
        raise ValueError("Unsupported key format or incorrect passphrase.")

    def _initialize(self):
        """Initialization of the SSH tunnel and the HTTP client."""
        if self.ssh_host:
            if self._tunnel and self._tunnel.is_active:
                return
            # Uploading the key using paramiko
            private_key = None
            if self.ssh_private_key_path:
                private_key = self._load_private_key(self.ssh_private_key_path, self.ssh_key_passphrase)
            # Installing an SSH tunnel using sshtunnel
            self._tunnel = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_username,
                ssh_password=self.ssh_password,
                ssh_pkey=private_key,
                remote_bind_address=(self.remote_bind_host, self.remote_bind_port),
                local_bind_address=(self.local_bind_host, self.local_bind_port)
            )
            self._tunnel.start()
            self.client = httpx.AsyncClient(
                base_url=f"http://{self.local_bind_host}:{self.local_bind_port}",
                timeout=self.timeout, verify=self.verify
            )

            # HTTP-client with local URL

    def _get_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    async def _request(self, method: str, url: str, token: Optional[str] = None, data: Optional[BaseModel] = None,
                       params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        if self.ssh_host and (not self.client or not self._tunnel.is_active):
            # Initialize the HTTP client and SSH tunnel if they are closed
            self._initialize()
            return await self._request(method, url, token, data, params)
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
        if self.ssh_host and (not self.client or not self._tunnel.is_active):
            # Initialize the HTTP client and SSH tunnel if they are closed
            self._initialize()
            return await self.get_token(username, password)
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

    async def get_admins(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None,
                         username: Optional[str] = None) -> List[Admin]:
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
    
    async def activate_next_plan(self, username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/active-next"
        response = await self._request("POST", url, token)
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

    async def get_users(self, token: str, offset: Optional[int] = None, limit: Optional[int] = None,
                        username: Optional[List[str]] = None, search: Optional[str] = None,
                        status: Optional[str] = None, sort: Optional[str] = None) -> UsersResponse:
        url = "/api/users"
        params = {"offset": offset, "limit": limit, "username": username, "search": search, "status": status, "sort": sort}
        response = await self._request("GET", url, token, params=params)
        return UsersResponse(**response.json())

    async def reset_users_data_usage(self, token: str) -> None:
        url = "/api/users/reset"
        await self._request("POST", url, token)
        
    async def get_user_data_usage(self, username: str, token: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> UserUsagesResponse:
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        params = {
            "start": start_date.isoformat(timespec="seconds") if start_date else None,
            "end": end_date.isoformat(timespec="seconds") if end_date else None
        }
        params = {k: v for k, v in params.items() if v is not None} 
        url = f"/api/user/{username}/usage"
        response = await self._request("GET", url, token, params=params)
        return UserUsagesResponse(**response.json())

    async def set_owner(self, username: str, admin_username: str, token: str) -> UserResponse:
        url = f"/api/user/{username}/set-owner?admin_username={admin_username}"
        response = await self._request("PUT", url, token)
        return UserResponse(**response.json())

    async def get_expired_users(self, token: str, expired_before: Optional[str] = None,
                                expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self._request("GET", url, token, params=params)
        return response.json()

    async def delete_expired_users(self, token: str, expired_before: Optional[str] = None,
                                   expired_after: Optional[str] = None) -> List[str]:
        url = "/api/users/expired"
        params = {"expired_before": expired_before, "expired_after": expired_after}
        response = await self._request("DELETE", url, token, params=params)
        return response.json()

    async def get_user_templates(self,
                                 token: str,
                                 offset: Optional[int] = None,
                                 limit: Optional[int] = None) -> List[UserTemplateResponse]:
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

    async def modify_user_template(self, template_id: int, template: UserTemplateModify,
                                   token: str) -> UserTemplateResponse:
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

    async def get_user_usage(self, url: str = None, token: str = None, start: Optional[str] = None,
                             end: Optional[str] = None) -> Any:
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
        """Closing the HTTP client and SSH tunnel."""
        if self.client:
            await self.client.aclose()
        if self._tunnel:
            self._tunnel.stop()
