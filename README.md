# Proyecto back-end consumo
Crear entorno virtual de python

```bash
  python -m venv tutorial-env
```
```bash
  tutorial-env\Scripts\activate
```

Instalar los paquetes desde el requirements.txt

```bash
  pip install -r requirements.txt
```

iniciar la aplicacion con:
```bash
  python index.py
```


## Herramientas utlizadas
Para la creacion de API se utilizo el framework Flask y el ORM  SQLAlchemy para bases de dato en MySQL

## Variables de Entorno

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env

`MYSQL_USER`
`MYSQL_DATABASE`
`MYSQL_PASSWORD`
`MYSQL_HOST`
`MYSQL_PORT`
`SECRET_KEY`
