import requests

url_user = "http://127.0.0.1:5000/user"
url_ad = "http://127.0.0.1:5000/advertisement"

# REST для пользователей
# # POST - создать пользователя
# response = requests.post(
#     url_user,
#     json={"name": "user_2авыавыаы", "password": "gsegewget#4%$5J"},
#     headers={"Authorization": "some_token"},
# )

# # GET - получить пользователя
# response = requests.get(
#     url_user + "/1",
#     headers={"Authorization": "some_token"},
# )
#
# # PATCH - изменить пользователя
# response = requests.patch(
#     url_user + "/1",
#     json={"name": "user_1", "password": "gsegewget#4%$5J"},
#     headers={"Authorization": "some_token"},
# )
#
# # DELETE - удалить пользователя
# response = requests.delete(
#     url_user + "/1",
#     headers={"Authorization": "some_token"},
# )


# # REST для объявлений
# POST - создать объявление
# response = requests.post(
#     url_ad,
#     json={"heading": "Заголовок 1", "description": "Описание 1", "owner_id": 1},
#     headers={"Authorization": "some_token"},
# )
#
# GET - получить объявление
# response = requests.get(
#     url_ad + "/1",
#     headers={"Authorization": "some_token"},
# )
#
# # PATCH - изменить объявление
# response = requests.patch(
#     url_ad + "/1",
#     json={"heading": "Заголовок 1-1", "owner_id": 1},
#     headers={"Authorization": "some_token"},
# )
#
# # DELETE - удалить объявление
# response = requests.delete(
#     url_ad + "/1",
#     headers={"Authorization": "some_token"},
# )

print(response.status_code)
print(response.text)
