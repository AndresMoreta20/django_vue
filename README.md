https://www.canva.com/design/DAF5W-v9y_g/mBTXdgz7a4-x5TXShJw2pQ/edit?utm_content=DAF5W-v9y_g&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Lecturespaces

# Documentación de la API del Proyecto MVC

## Resumen

Este documento proporciona una visión general completa de la API para el Proyecto MVC, diseñado para facilitar sesiones de estudio a través de una plataforma educativa. La API soporta operaciones sobre `lecturespaces`, `flashcards` y `tags`, permitiendo a los usuarios gestionar materiales de estudio de manera eficiente. Esta guía está destinada para desarrolladores que integran con la API o contribuyen a su desarrollo.

## Empezando

### Prerrequisitos

- Node.js (v12.x o posterior)
- npm (v6.x o posterior)
- Python (v3.8 o posterior)
- Django (v3.2 o posterior)
- Django REST Framework (v3.12 o posterior)

### Instalación

#### Clona el Repositorio

```bash
git clone https://github.com/yourusername/mvcproject-api.git
cd mvcproject-api
```

#### Configura un Entorno Virtual

```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
```

#### Instala Dependencias

```bash
pip install -r requirements.txt
```

#### Migra la Base de Datos

```bash
python manage.py migrate
```

#### Ejecuta el Servidor

```bash
python manage.py runserver
```

### Configuración

Las variables de entorno se pueden configurar en un archivo `.env` en la raíz del proyecto.

Ejemplo de configuración de `.env`:

```makefile
DEBUG=on
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
```

## Endpoints de la API

### Lecturespaces

- Listar Lecturespaces: `GET /api/lecturespaces/`
- Crear Lecturespace: `POST /api/lecturespaces/`
- Recuperar Lecturespace: `GET /api/lecturespaces/{id}/`
- Actualizar Lecturespace: `PUT /api/lecturespaces/{id}/`
- Eliminar Lecturespace: `DELETE /api/lecturespaces/{id}/`

### Flashcards

- Listar Flashcards: `GET /api/flashcards/`
- Crear Flashcard: `POST /api/flashcards/`
- Recuperar Flashcard: `GET /api/flashcards/{id}/`
- Actualizar Flashcard: `PUT /api/flashcards/{id}/`
- Eliminar Flashcard: `DELETE /api/flashcards/{id}/`

### Tags

- Listar Tags: `GET /api/tags/`
- Crear Tag: `POST /api/tags/`
- Recuperar Tag: `GET /api/tags/{name}/`
- Eliminar Tag: `DELETE /api/tags/{name}/`

### Sesiones de Estudio

- Iniciar Sesión de Estudio: `POST /api/study_sessions/start/`
- Finalizar Sesión de Estudio: `POST /api/study_sessions/{session_id}/end/`
- Obtener la Siguiente Flashcard: `GET /api/study_sessions/{session_id}/next/`

![image](https://github.com/AndresMoreta20/django_vue/assets/61909582/5df009f2-f589-4bb6-9eef-e1b78987a95d)
