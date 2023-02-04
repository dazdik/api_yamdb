# API для Yatube
Yandex educational project.Python Developer course workshop(backend).
### Description
- create personal pages
- subscribe to the authors of the article and comment them
- community publications
- records changes and user blocking
### Technologies
Python 3.7
Django 3.2.16
Django Rest FrameWork 3.12.4
Pillow 9.3.0
### Launching a project in developer mode
- Install and activate the virtual environment
- Install dependencies from the file requirements.txt
```
pip install -r requirements.txt
``` 
- In the file folder manage.py run the commands:
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
```
python3 manage.py runserver
```
### Documentation
После запуска dev-сервера документация к API доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```
### Request examples
##### Publishing and receiving posts
- Request: [GET] http://127.0.0.1:8000/api/v1/posts/?limit=2&offset=1
    > Response: 
    ``` 
    {
        "count": 5,
        "next": "http://127.0.0.1:8000/api/v1/posts/?limit=2&offset=3",
        "previous": "http://127.0.0.1:8000/api/v1/posts/?limit=2",
        "results": [
            {
                "id": 2,
                "author": "string",
                "text": "string",
                "pub_date": "2022-08-06T10:01:17.273956Z",
                "image": "string",
                "group": 0
            },
            {
                "id": 3,
                "author": "string",
                "text": "string",
                "pub_date": "2022-08-06T10:42:39.095878Z",
                "image": "string",
                "group": 0
            }
        ]
    }
    ```
- Request: [POST] http://127.0.0.1:8000/api/v1/posts/
    > Request body:
    ```
    {
        "text": "string",
        "image": "string",
        "group": 0
    }
    ```
    > Response:
    ```
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2022-08-06T10:59:31.721673Z",
        "image": "string",
        "group": 0
    }
    ```
- Request: [GET] http://127.0.0.1:8000/api/v1/posts/{id}/
    >  Response:
    
    ```
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2019-08-24T14:15:22Z",
        "image": "string",
        "group": 0
    }
    ```

- Request: [POST] http://127.0.0.1:8000/api/v1/posts/{id}/
    > Response:
    ```
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2022-08-06T10:59:31.721673Z",
        "image": "string",
        "group": 0
    }
    ```

### Authors
Mironov Denis
