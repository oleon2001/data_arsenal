
Este proyecto contiene dos partes principales:

- **Backend:** API y lógica de negocio (Django)
- **Frontend:** Interfaz de usuario (React + Tailwind)

---

## Requisitos Previos

- Node.js (v16+ recomendado)
- npm o yarn
- Python 3.8+
- pip
- (Opcional) virtualenv

---

## 1. Iniciar el Backend (Django)

1. Ve al directorio del backend:
    ```bash
    cd backend
    ```

2. (Opcional) Crea y activa un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Aplica migraciones:
    ```bash
    python manage.py migrate
    ```

5. (Opcional) Crea un superusuario:
    ```bash
    python manage.py createsuperuser
    ```

6. Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

El backend estará disponible en [http://localhost:8000](http://localhost:8000)

---

## 2. Iniciar el Frontend (React)

1. Ve al directorio del frontend:
    ```bash
    cd fronted
    ```

2. Instala las dependencias:
    ```bash
    npm install
    # o
    yarn install
    ```

3. Inicia la aplicación:
    ```bash
    npm start
    # o
    yarn start
    ```

El frontend estará disponible en [http://localhost:3000](http://localhost:3000)

---

## Notas

- Asegúrate de que el backend esté corriendo antes de usar el frontend si necesitas datos reales.
- Puedes modificar la configuración de CORS en Django si accedes desde otro host o puerto.
- Para producción, consulta la documentación de Django y React sobre despliegue seguro.

---

## Scripts útiles (Frontend)


- `npm run build` — Genera una versión optimizada para producción.

---

## Recursos

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---