import asyncio
from datetime import datetime

from marzban import MarzbanAPI, AdminCreate, UserCreate, NodeCreate, UserTemplateCreate, AdminModify, UserModify, \
    UserTemplateModify, NodeModify, ProxySettings


async def main():
    # Create an API client
    api = MarzbanAPI(base_url="http://marzban-api.com")

    # Create an API client via SSH Tunnel
    # api = MarzbanAPI(
    #     base_url="http://127.0.0.1",
    #     ssh_username='root',  # user name on server
    #     ssh_host='99.240.220.100',  # IP or hostname of the server
    #     ssh_port=22,  # ssh port
    #     ssh_private_key_path='C:/Users/User/.ssh/id_rsa',  # Path to your private key
    #     ssh_key_passphrase='sshpassphrase',  # Passphrase for private key if set
    #     ssh_password='',  # SSH password (if you use password authentication)
    #     local_bind_host='127.0.0.1',  # IP on your machine where you use this code
    #     local_bind_port=8020,  # Port on your machine where you use this code
    #     remote_bind_host='127.0.0.1',  # Marzban IP on your server
    #     remote_bind_port=8000  # Marzban port on your server
    # )

    # Obtain admin token
    token = await api.get_token(username="admin", password="admin")

    # Administrators management
    # Get the current admin
    current_admin = await api.get_current_admin(token=token.access_token)
    print("Current Admin:", current_admin)

    # Create a new admin
    new_admin = AdminCreate(username="admin2", is_sudo=False, password="new_password", telegram_id=123456789,
                            discord_webhook="https://discord.com/api/webhooks/...")
    created_admin = await api.create_admin(admin=new_admin, token=token.access_token)
    print("Created Admin:", created_admin)

    # Modify admin details
    modified_admin = await api.modify_admin(username="admin2",
                                            admin=AdminModify(is_sudo=False, password="new_password2"),
                                            token=token.access_token)
    print("Modified Admin:", modified_admin)

    # Remove an admin
    await api.remove_admin(username="admin2", token=token.access_token)
    print("Removed Admin: new_admin")

    # Get a list of admins
    admins = await api.get_admins(token=token.access_token, offset=0, limit=10)
    print("Admins:", admins)

    # System stats
    system_stats = await api.get_system_stats(token=token.access_token)
    print("System Stats:", system_stats)

    # Users management
    # Add a new user
    new_user = UserCreate(username="new_user", proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
                          inbounds={'vless': ['VLESS TCP REALITY']})
    added_user = await api.add_user(user=new_user, token=token.access_token)
    print("Added User:", added_user)

    # Get user information
    user_info = await api.get_user(username="new_user", token=token.access_token)
    print("User Info:", user_info)

    # Modify user details
    modified_user = await api.modify_user(username="new_user", user=UserModify(data_limit=1073741824),
                                          token=token.access_token)
    print("Modified User:", modified_user)

    # Remove a user
    await api.remove_user(username="new_user", token=token.access_token)
    print("Removed User: new_user")

    # Reset user data usage
    reset_user_data = await api.reset_user_data_usage(username="new_user", token=token.access_token)
    print("Reset User Data Usage:", reset_user_data)

    # Revoke user subscription
    revoked_user_subscription = await api.revoke_user_subscription(username="new_user", token=token.access_token)
    print("Revoked User Subscription:", revoked_user_subscription)

    # Get a list of users
    users = await api.get_users(token=token.access_token, offset=0, limit=10)
    print("Users:", users)

    # Reset data usage for all users
    await api.reset_users_data_usage(token=token.access_token)
    print("Reset All Users Data Usage")

    # Get user data usage
    user_usage = await api.get_user_usage(username="new_user", token=token.access_token, start="2023-01-01",
                                          end="2023-12-31")
    print("User Usage:", user_usage)

    # Set owner for a user
    owner_set = await api.set_owner(username="new_user", admin_username="admin", token=token.access_token)
    print("Set Owner:", owner_set)

    # Get list of expired users
    expired_users = await api.get_expired_users(token=token.access_token,
                                                expired_before=datetime.fromisoformat("2024-10-10T00:00:00+00:00")
                                                )
    print("Expired Users:", expired_users)

    # Delete expired users
    deleted_expired_users = await api.delete_expired_users(
        token=token.access_token,
        expired_before=datetime.fromisoformat("2024-10-10T00:00:00+00:00")
    )
    print("Deleted Expired Users:", deleted_expired_users)

    # User templates management
    # Get list of user templates
    user_templates = await api.get_user_templates(token=token.access_token, offset=0, limit=10)
    print("User Templates:", user_templates)

    # Add a new user template
    new_template = UserTemplateCreate(name="template1", data_limit=1073741824, expire_duration=2592000,
                                      username_prefix="user_", username_suffix="_template")
    added_template = await api.add_user_template(template=new_template, token=token.access_token)
    print("Added User Template:", added_template)

    # Get user template by ID
    template_info = await api.get_user_template(template_id=added_template.id, token=token.access_token)
    print("User Template Info:", template_info)

    # Modify user template
    modified_template = await api.modify_user_template(template_id=added_template.id,
                                                       template=UserTemplateModify(name="template1_updated"),
                                                       token=token.access_token)
    print("Modified User Template:", modified_template)

    # Remove user template
    await api.remove_user_template(template_id=added_template.id, token=token.access_token)
    print("Removed User Template:", added_template.id)

    # Nodes management
    # Add a new node
    new_node = NodeCreate(name="Node1", address="192.168.1.1")
    added_node = await api.add_node(node=new_node, token=token.access_token)
    print("Added Node:", added_node)

    # Get node information
    node_info = await api.get_node(node_id=added_node.id, token=token.access_token)
    print("Node Info:", node_info)

    # Modify node details
    modified_node = await api.modify_node(node_id=added_node.id, node=NodeModify(name="Node1_Updated"),
                                          token=token.access_token)
    print("Modified Node:", modified_node)

    # Remove node
    await api.remove_node(node_id=added_node.id, token=token.access_token)
    print("Removed Node:", added_node.id)

    # Reconnect node
    await api.reconnect_node(node_id=added_node.id, token=token.access_token)
    print("Reconnected Node:", added_node.id)

    # Get list of nodes
    nodes = await api.get_nodes(token=token.access_token)
    print("Nodes:", nodes)

    # Get node usage statistics
    nodes_usage = await api.get_usage(token=token.access_token, start="2023-01-01", end="2023-12-31")
    print("Nodes Usage:", nodes_usage)

    # Getting node settings
    node_settings = await api.get_node_settings(token=token.access_token)
    print("Node Settings:", node_settings)

    # Getting user subscription information with token
    user_subscription_info = await api.get_user_subscription_info(url=user_info.subscription_url)
    print("User Subscription Info:", user_subscription_info)

    # Getting user usage statistics
    user_usage = await api.get_user_usage(url=user_info.subscription_url, start="2023-01-01")
    print("User Usage:", user_usage)

    # Getting user subscription by client type
    # Accepts only clients that require a JSON response. Example: sing-box.
    user_subscription_client = await api.get_user_subscription_with_client_type(url=user_info.subscription_url,
                                                                                client_type="sing-box")
    print("User Subscription with Client Type:", user_subscription_client)

    # Closing the API client
    await api.close()

# Run the main async function
asyncio.run(main())
