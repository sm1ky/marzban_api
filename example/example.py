import asyncio
from marzban import MarzbanAPI, AdminCreate, UserCreate, NodeCreate, UserTemplateCreate, AdminModify, UserModify, UserTemplateModify, NodeModify, ProxySettings

async def main():
    # Создание клиента API
    api = MarzbanAPI(base_url="http://marzban-api.com")

    # Получение токена администратора
    token = await api.get_token(username="admin", password="admin")

    # Работа с администраторами
    ## Получение текущего администратора
    current_admin = await api.get_current_admin(token=token.access_token)
    print("Current Admin:", current_admin)

    ## Создание нового администратора
    new_admin = AdminCreate(username="admin2", is_sudo=False, password="new_password", telegram_id=123456789, discord_webhook="https://discord.com/api/webhooks/...")
    created_admin = await api.create_admin(admin=new_admin, token=token.access_token)
    print("Created Admin:", created_admin)

    ## Изменение данных администратора
    modified_admin = await api.modify_admin(username="admin2", admin=AdminModify(is_sudo=False, password="new_password2"), token=token.access_token)
    print("Modified Admin:", modified_admin)

    ## Удаление администратора
    await api.remove_admin(username="admin2", token=token.access_token)
    print("Removed Admin: new_admin")

    ## Получение списка администраторов
    admins = await api.get_admins(token=token.access_token, offset=0, limit=10)
    print("Admins:", admins)

    # Работа с системной статистикой
    system_stats = await api.get_system_stats(token=token.access_token)
    print("System Stats:", system_stats)

    # Работа с пользователями
    ## Добавление нового пользователя
    new_user = UserCreate(username="new_user", proxies={"vless": ProxySettings(flow="xtls-rprx-vision")}, inbounds={'vless': ['VLESS TCP REALITY']})
    added_user = await api.add_user(user=new_user, token=token.access_token)
    print("Added User:", added_user)

    ## Получение информации о пользователе
    user_info = await api.get_user(username="new_user", token=token.access_token)
    print("User Info:", user_info)

    ## Изменение данных пользователя
    modified_user = await api.modify_user(username="new_user", user=UserModify(data_limit=1073741824), token=token.access_token)
    print("Modified User:", modified_user)

    ## Удаление пользователя
    await api.remove_user(username="new_user", token=token.access_token)
    print("Removed User: new_user")

    ## Сброс использования данных пользователя
    reset_user_data = await api.reset_user_data_usage(username="new_user", token=token.access_token)
    print("Reset User Data Usage:", reset_user_data)

    ## Отмена подписки пользователя
    revoked_user_subscription = await api.revoke_user_subscription(username="new_user", token=token.access_token)
    print("Revoked User Subscription:", revoked_user_subscription)

    ## Получение списка пользователей
    users = await api.get_users(token=token.access_token, offset=0, limit=10)
    print("Users:", users)

    ## Сброс использования данных всех пользователей
    await api.reset_users_data_usage(token=token.access_token)
    print("Reset All Users Data Usage")

    ## Получение использования данных пользователя
    user_usage = await api.get_user_usage(username="new_user", token=token.access_token, start="2023-01-01", end="2023-12-31")
    print("User Usage:", user_usage)

    ## Назначение владельца для пользователя
    owner_set = await api.set_owner(username="new_user", admin_username="admin", token=token.access_token)
    print("Set Owner:", owner_set)

    ## Получение списка истекших пользователей
    expired_users = await api.get_expired_users(token=token.access_token, expired_before="2024-01-01T00:00:00Z")
    print("Expired Users:", expired_users)

    ## Удаление истекших пользователей
    deleted_expired_users = await api.delete_expired_users(token=token.access_token, expired_before="2024-01-01T00:00:00Z")
    print("Deleted Expired Users:", deleted_expired_users)

    # Работа с шаблонами пользователей
    ## Получение списка шаблонов пользователей
    user_templates = await api.get_user_templates(token=token.access_token, offset=0, limit=10)
    print("User Templates:", user_templates)

    ## Добавление нового шаблона пользователя
    new_template = UserTemplateCreate(name="template1", data_limit=1073741824, expire_duration=2592000, username_prefix="user_", username_suffix="_template")
    added_template = await api.add_user_template(template=new_template, token=token.access_token)
    print("Added User Template:", added_template)

    ## Получение шаблона пользователя по ID
    template_info = await api.get_user_template(template_id=added_template.id, token=token.access_token)
    print("User Template Info:", template_info)

    ## Изменение шаблона пользователя
    modified_template = await api.modify_user_template(template_id=added_template.id, template=UserTemplateModify(name="template1_updated"), token=token.access_token)
    print("Modified User Template:", modified_template)

    ## Удаление шаблона пользователя
    await api.remove_user_template(template_id=added_template.id, token=token.access_token)
    print("Removed User Template:", added_template.id)

    # Работа с узлами
    ## Добавление нового узла
    new_node = NodeCreate(name="Node1", address="192.168.1.1")
    added_node = await api.add_node(node=new_node, token=token.access_token)
    print("Added Node:", added_node)

    ## Получение информации об узле
    node_info = await api.get_node(node_id=added_node.id, token=token.access_token)
    print("Node Info:", node_info)

    ## Изменение данных узла
    modified_node = await api.modify_node(node_id=added_node.id, node=NodeModify(name="Node1_Updated"), token=token.access_token)
    print("Modified Node:", modified_node)

    ## Удаление узла
    await api.remove_node(node_id=added_node.id, token=token.access_token)
    print("Removed Node:", added_node.id)

    ## Повторное подключение узла
    await api.reconnect_node(node_id=added_node.id, token=token.access_token)
    print("Reconnected Node:", added_node.id)

    ## Получение списка узлов
    nodes = await api.get_nodes(token=token.access_token)
    print("Nodes:", nodes)

    ## Получение использования данных узлов
    nodes_usage = await api.get_usage(token=token.access_token, start="2023-01-01", end="2023-12-31")
    print("Nodes Usage:", nodes_usage)

    # Закрытие клиента
    await api.close()

# Запуск основного асинхронного метода
asyncio.run(main())