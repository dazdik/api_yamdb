<<<<<<< develop

# api_final

## Authors:

[dazdik](https://github.com/dazdik)

[FedOK007](https://github.com/FedOK007)

[kvazymir1199](https://github.com/kvazymir1199)

## Discription:

### REST API для YaMDb

Created on the basis of the framework [Django REST Framework (DRF)](https://github.com/ilyachch/django-rest-framework-rusdoc)

> The YaMDb project collects user reviews of works. The works are divided into categories: "Books", "Films", "Music".
>
> The works themselves are not stored in YaMDb, you can't watch a movie or listen to music here.
>
> In each category there are works: books, movies or music.
>
> A work can be assigned a genre from the preset list (for example, "Fairy Tale", "Rock" or "Arthouse").
>
> Grateful or outraged users leave text reviews for the works and rate the work, an average rating of the work is formed from user ratings.

## Technologies

Python 3.7

Django 3.2.15

## Start Project

Clone the repository and go to it on the command line:

```
git@github.com:kvazymir1199/api_yamdb.git
```

Пo to the project directory

```go
cd api_yamdb
```

Create and activate a virtual environment:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Install dependencies from requirements.txt:

```
pip install -r requirements.txt
```

Perform migrations:

~~~
python manage.py makemigrations
~~~

```
python manage.py migrate
```

Upload information to the database:

```
python manage.py fill_database
```

Run project:

```
python manage.py runserver
```

> When you launch the project, at http://127.0.0.1:8000/redoc / documentation for the Yandex API will be available. The documentation describes how the API works. The documentation is presented in Doc format.

## Request examples

> Get (http://127.0.0.1:8000/api/v1/categories/1):

```
{
  "name": "Film",
  "slug": "Movie"
}
```

## Requirements:

```
asgiref==3.5.2
atomicwrites==1.4.1
attrs==22.1.0
certifi==2022.9.24
charset-normalizer==2.0.12
colorama==0.4.5
Django==2.2.16
django-filter==21.1
djangorestframework==3.12.4
djangorestframework-simplejwt==5.2.1
idna==3.4
importlib-metadata==4.13.0
iniconfig==1.1.1
packaging==21.3
pluggy==0.13.1
py==1.11.0
PyJWT==2.1.0
pyparsing==3.0.9
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
pytz==2022.4
requests==2.26.0
sqlparse==0.4.3
toml==0.10.2
typing_extensions==4.3.0
urllib3==1.26.12
zipp==3.8.1
```

=======

Mironov Denis

Дарья Андреевна
