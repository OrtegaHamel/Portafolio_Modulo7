# Integración de Django con Bases de Datos

## 1. Características Fundamentales de la Integración de Django con Bases de Datos

### a) ORM (Object-Relational Mapping)

Django incluye un ORM que actúa como intermediario entre el código
Python y la base de datos. Esto permite:

-   Definir modelos como clases de Python que se mapean a tablas en la
    base de datos.
-   Realizar consultas usando sintaxis de Python en lugar de SQL puro.
-   Manejar relaciones entre tablas (uno a muchos, muchos a muchos,
    etc.) de forma intuitiva.
-   **Portabilidad:** Cambiar de base de datos (por ejemplo, de SQLite a
    PostgreSQL) sin modificar el código de los modelos.

### b) Soporte Multi-Base de Datos

Django soporta varios motores de bases de datos:

-   **SQLite:** Ideal para desarrollo y proyectos pequeños.
-   **PostgreSQL:** Recomendado para producción.
-   **MySQL:** Popular en entornos empresariales.
-   **Oracle:** Para entornos corporativos.
-   **Otros:** Como MariaDB o SQL Server mediante backends de terceros.

### c) Migraciones

Django incluye un sistema de migraciones que permite:

-   Crear y modificar esquemas de base de datos desde los modelos.
-   Versionar cambios en la estructura.
-   Aplicar o revertir migraciones de forma controlada.

------------------------------------------------------------------------

## 2. Configuración de la Base de Datos en `settings.py`

### a) SQLite (por defecto)

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

-   **ENGINE:** Backend SQLite.
-   **NAME:** Ruta del archivo de la base de datos.

### b) PostgreSQL

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_basededatos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### c) MySQL

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_basededatos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

------------------------------------------------------------------------

## 3. Manejo de Conexiones y Operaciones con el ORM

### a) Conexiones

-   Django gestiona automáticamente las conexiones.
-   Cada solicitud abre y cierra conexiones según sea necesario.
-   En producción se puede configurar un pool de conexiones.

### b) Operaciones Básicas con el ORM

**Crear un registro:**

``` python
from myapp.models import MiModelo
objeto = MiModelo(campo1='valor1', campo2='valor2')
objeto.save()
```

**Consultar registros:**

``` python
objetos = MiModelo.objects.all()
objeto = MiModelo.objects.get(id=1)
```

**Actualizar registros:**

``` python
objeto = MiModelo.objects.get(id=1)
objeto.campo1 = 'nuevo_valor'
objeto.save()
```

**Eliminar registros:**

``` python
objeto = MiModelo.objects.get(id=1)
objeto.delete()
```

### c) Transacciones

``` python
from django.db import transaction

with transaction.atomic():
    objeto1.save()
    objeto2.save()
```

------------------------------------------------------------------------

## 4. Ejemplo Práctico: Configuración y Uso

### a) Configurar PostgreSQL en `settings.py`

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mi_proyecto',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### b) Definir un Modelo

``` python
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo
```

### c) Realizar Migraciones

``` bash
python manage.py makemigrations
python manage.py migrate
```

### d) Usar el ORM

``` python
libro = Libro(titulo="Cien años de soledad", autor="Gabriel García Márquez", fecha_publicacion="1967-05-30")
libro.save()

libros = Libro.objects.filter(autor="Gabriel García Márquez")
for libro in libros:
    print(libro.titulo)
```

------------------------------------------------------------------------

## Conclusión

Django facilita la integración con bases de datos mediante su ORM,
sistema de migraciones y soporte multi motor. La configuración es
sencilla y permite trabajar con bases de datos usando solo Python.
