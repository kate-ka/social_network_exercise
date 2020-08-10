### Social Network Exercise

What is done:

* Create, retrieve, update operations for Post
* Like/Unlike Post
* Like analytics by day, example usage:

     "/api/posts/analytics/?created_after=2020-08-09&created_before=2020-08-10"
* Sign-in using JWT Sign-up
* Automated bot that creates and likes post randomly
* Browsable Swagger API is available by http://127.0.0.1:8000/api/swagger/

 
#### Installation and run

Project requires python3.8

`make install` - install requirements & run migrations

`make test` - run tests

`make install-bot` - install bot requirements 

`python manage.py runserver`

#### Installation and run via Docker

`docker-compose up`

`make test-docker`

#### Run bot:
`python bot/automated_bot.py` or 
`python bot/fast_automated_bot.py` (using threads and postgresql)
