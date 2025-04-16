import json
import requests
from jsonschema import validate

url = 'https://reqres.in'
endpoint = '/api/users'

payload = {
    "name": "morpheus",
    "job": "leader"
}


def test_get_list_of_users():
    response = requests.get(url + endpoint, params={"page": 2, "per_page": 3})
    users = response.json()['data']
    assert response.status_code == 200
    assert users[0]["first_name"] == 'Eve'  # Проверка имени
    assert users[0]['last_name'] == 'Holt'  # Проверка фамилии
    assert len(users) == 3

    # Валидация ответа от сервера
    with open('../../schemas/users_list.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_get_single_user():
    endpoint_single_user = "/api/users/3"
    response = requests.get(url + endpoint_single_user)
    users = response.json()['data']
    assert response.status_code == 200  # Проверка статуса ответа
    assert users['first_name'] == 'Emma'
    assert users['last_name'] == 'Wong'

    # Валидация ответа от сервера
    with open('../../schemas/get_single_user.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_create_user():
    response = requests.post(url + endpoint, data=payload)
    assert response.status_code == 201
    assert response.json()['name'] == 'morpheus'  # Проверка имени
    assert response.json()['job'] == 'leader'  # Проверка должности

    # Валидация ответа от сервера
    with open('../../schemas/post_users.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_single_user_not_found():
    endpoint_single_user = "/api/users/23"
    response = requests.get(url + endpoint_single_user)
    assert response.status_code == 404  # Проверка статуса ответа


def test_list_resource():
    endpoint = "/api/unknown"
    response = requests.get(url + endpoint, params={"per_page": 3})
    assert response.status_code == 200

    resource_list = response.json()['data']
    assert resource_list[0]['id'] == 1
    assert resource_list[0]['name'] == 'cerulean'
    assert len(resource_list) == 3

    # Валидация ответа от сервера
    with open('../../schemas/list_resource.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_update_users_by_put():
    endpoint = "/api/users/2"
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.put(url + endpoint, data=payload)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['name'] == "morpheus"
    assert updated_user['job'] == "zion resident"

    # Валидация ответа от сервера
    with open('../../schemas/update_users.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_update_users_by_patch():
    endpoint = "/api/users/2"
    payload = {
        "name": "morpheus jr.",
        "job": "assistant"
    }

    response = requests.patch(url + endpoint, data=payload)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['name'] == "morpheus jr."
    assert updated_user['job'] == "assistant"

    # Валидация ответа от сервера
    with open('../../schemas/update_user_by_patch.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_delete_user():
    endpoint = "/api/users/2"

    response = requests.delete(url + endpoint)
    assert response.status_code == 204


def test_register_successful():
    endpoint = '/api/register'
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    response = requests.post(url + endpoint, data=payload)
    assert response.status_code == 200

    assert response.json()['id'] == 4  # Проверка id из ответа
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'  # Проверка токена

    # Валидация ответа от сервера
    with open('../../schemas/successful_register.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


def test_register_unsuccessful():
    endpoint = '/api/register'
    payload = {
        "email": "eve.holted@reqres.in",
    }

    response = requests.post(url + endpoint, data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'

    # Валидация ответа от сервера
    with open('../../schemas/unsuccessful_register.json') as file:
        schema = json.load(file)
    validate(response.json(), schema)  # Валидация ответа от сервера


# Пример с заголовками (headers) - авторизацией (для себя чтобы не забыть)

# import requests
#
# url = 'https://reqres.in'
# endpoint = '/api/users'
#
# headers = {
#     'Content-Type': 'application/json'
#     'Authorization': 'Bearer token'
# }
#
# def test_create_user():
#     response = requests.get(url + endpoint, headers=headers)
#     assert response.status_code == 200
