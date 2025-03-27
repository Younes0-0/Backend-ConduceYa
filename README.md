# Proyecto: Sistema de Gestión de Autoescuela

Este proyecto tiene como objetivo **gestionar la agenda de los profesores de una autoescuela**, permitir a los alumnos **reservar y pagar clases**, y facilitar la administración a las recepcionistas. Se utiliza **Python** y **Django** como tecnologías principales en el **backend**.


## Tecnologías y librerías utilizadas

### Lenguaje y framework principal

- **Python 5.1.7**  
  Lenguaje de programación principal.

- **Django 4.x**  
  Framework web de alto nivel para desarrollar aplicaciones web rápidas, seguras y escalables.

### Librerías de Django y complementos

- **Django REST Framework (DRF)**  
  Para la creación de APIs RESTful, facilitando la serialización de datos, la gestión de endpoints y la autenticación.

- **django-cors-headers**  
  Para configurar y controlar el acceso de dominios externos (CORS), permitiendo la comunicación segura entre el frontend y la API.

- **psycopg2** (o `psycopg2-binary`) / **mysqlclient** / **sqlite3**  
  Dependiendo del motor de base de datos elegido (PostgreSQL, MySQL o SQLite), se empleará la librería correspondiente.

- **django-environ** (opcional, pero recomendado)  
  Para manejar variables de entorno (credenciales, configuración, etc.) de manera segura y modular.

### Autenticación y seguridad

- **djangorestframework-simplejwt**  
  Soporte para autenticación basada en **JSON Web Tokens (JWT)**, permitiendo un control robusto de la sesión y el acceso a la API.

- **bcrypt** / **argon2** (opcional)  
  Opciones de hashing seguro para contraseñas, si se prefiere un método distinto al predeterminado de Django.

### Gestión de pagos (opcional)

- **stripe** / **paypalrestsdk** / etc.  
  Integración con pasarelas de pago como Stripe, PayPal, etc., para permitir a los alumnos comprar paquetes de clases o realizar pagos puntuales.

### Envío de notificaciones (WhatsApp / SMS)

- **requests** o **httpx**  
  Para realizar peticiones HTTP a servicios externos (por ejemplo, APIs de WhatsApp Business o Twilio).

- **twilio** (opcional)  
  Integración con la API de Twilio para el envío automatizado de notificaciones vía SMS o WhatsApp.

### Testing

- **pytest** y **pytest-django** (opcional)  
  Herramientas para la creación y ejecución de pruebas unitarias y de integración de manera más flexible.

- **coverage** (opcional)  
  Para calcular el porcentaje de cobertura de las pruebas y asegurar la calidad del código.

### Otros complementos útiles

- **Celery** (opcional)  
  Para manejar tareas asíncronas, como el envío programado de recordatorios a los alumnos.

- **flower** (opcional)  
  Panel web para monitorear y gestionar el estado de las tareas ejecutadas por Celery.

- **drf-yasg** o **drf-spectacular**  
  Para generar documentación automática de la API en formatos Swagger o OpenAPI.


## Estructura básica del proyecto

```bash
proyecto_autoescuela/
├── manage.py
├── requirements.txt       # Librerías y dependencias
├── .env                   # Variables de entorno (no subir a repositorio público)
├── config/                # Configuraciones globales (settings, wsgi, urls)
├── apps/
│   ├── users/             # Gestión de usuarios (alumnos, profesores, recepcionistas)
│   ├── reservas/          # Módulo de reservas y calendario
│   ├── pagos/             # Módulo de pagos e integración con pasarela
│   └── ...                # Otros módulos que se requieran
└── ...
```


## Requisitos y configuración

1. **Instalación de dependencias**  
    Asegurarse de tener `pip` y `virtualenv` (o algún manejador de entornos virtuales como `pipenv`) instalado:
    ```shell
    python -m venv venv
  	source venv/bin/activate   # En Linux/Mac
  	# o en Windows: venv\Scripts\activate
  	pip install -r requirements.txt
	  ```
	
    
2. **Variables de entorno (`.env`)**  
    Ejemplo de contenido:
    
    ```ini
    DEBUG=True
  	SECRET_KEY=YOUR_SECRET_KEY
  	DATABASE_URL=postgres://usuario:password@localhost:5432/nombre_bd
  	ALLOWED_HOSTS=localhost,127.0.0.1
	  ``````
    
    - **SECRET_KEY**: clave secreta de Django para ambientes de producción.
        
    - **DATABASE_URL**: indica qué motor y credenciales usar para la base de datos.

3. **Migraciones y ejecución**
    
    ```shell
    python manage.py migrate
  	python manage.py runserver
  	```

## Cómo contribuir o extender

- Crear un _fork_ o rama nueva en el repositorio.
    
- Añadir los cambios o funcionalidades deseadas (nuevos endpoints, mejoras en la UI, etc.).
    
- Realizar los tests correspondientes (`pytest` o `python manage.py test`).
    
- Enviar un Pull Request para su revisión.
  

## Licencia

**Todos los derechos reservados.**  
No se permite la copia, distribución, modificación ni uso comercial de este software o de cualquier parte de su contenido sin el consentimiento expreso y por escrito del titular de los derechos. Para cualquier duda o consulta sobre el uso de este software, póngase en contacto con el autor o propietario.



