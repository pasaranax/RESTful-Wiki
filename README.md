# RESTful-Wiki
REST API для доступа к статьям википедии, хранящимся в elasticsearch. Обмен данными идет в формате json. Используется веб-фреймворк Flask.

##Реализованы методы
* GET для поиска статей:
  * `curl -i http://localhost:5000/wiki/?query=python` - поиск статей с текстом python
  * `curl -i http://localhost:5000/wiki/id/9999` - статья с id 9999
  * `curl -i http://localhost:5000/wiki/author/pasaranax` - статьи автора pasaranax
* POST для создания статьи:
  * `curl -i -H "Content-Type: application/json" -X POST -d '{"title": "title", "author": "pasaranax", "text": "text"}' http://localhost:5000/wiki/` - создает статью с заголовком title, текстом text от автора pasaranax
* PUT для редактирования статьи:
  * `curl -i -H "Content-Type: application/json" -X PUT -d '{"title": "title", "author": "pasaranax", "text": "edited"}' http://localhost:5000/wiki/id/9999` - редактирует статью с id 9999
* DELETE для удаления статьи:
  * `curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/wiki/id/9999` - удалить статью с id 9999
