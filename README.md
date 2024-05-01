# Planet_Gamer_Backend

Backend Planet Gamer, e-commerce de videojuegos. Proyecto final Full Stack Course by Bottega.

<a align=center href='https://planet-gamer-backend.onrender.com/'>https://planet-gamer-backend.onrender.com/</a>

Se ha utilizado Flask, framework de Python, para construir la API, conectándose a una base de datos sqlite mediante la utilización de SQL-Alchemy, un ORM que facilita las consultas sin utilizar lenguaje SQL, tratando las consultas como si fueran clases.

Para crear las tablas utilizar los siguientes comandos:
``` 
from run import app
from src.app import db
app.app_context().push()
db.create_all()
```
