# Calidad-Ambiente — Guía para exposición del proyecto

Documento orientado a explicar **arquitectura**, **carpetas**, **archivos clave** y **flujo de datos** del repositorio *Calidad-Ambiente* (tienda demo: Angular + Django + PostgreSQL + Docker).

---

## 1. Resumen ejecutivo (30 segundos)

El proyecto es una **aplicación web full-stack** que simula una tienda de tecnología:

- **Frontend:** Angular (SPA, rutas, servicios HTTP, carrito en cliente).
- **Backend:** Django con **Django REST Framework** (API JSON de solo lectura).
- **Base de datos:** PostgreSQL.
- **Despliegue local:** **Docker Compose** levanta base de datos, API y sitio estático servido por **Nginx** (Angular compilado), con **proxy** de `/api/` hacia Django.

El usuario accede por el **puerto 8080**; las peticiones a `/api/...` las reenvía Nginx al contenedor del backend.

---

## 2. Arquitectura lógica

```
Navegador
    │
    ▼
┌─────────────────────────────────────┐
│  Contenedor `frontend` (Nginx)      │
│  - Sirve Angular (HTML/JS/CSS)     │
│  - location /api/ → proxy          │
└──────────────┬──────────────────────┘
               │ HTTP interno Docker
               ▼
┌─────────────────────────────────────┐
│  Contenedor `backend` (Gunicorn)    │
│  - Django + DRF                    │
│  - Rutas /api/productos/           │
└──────────────┬──────────────────────┘
               │ SQL (red interna)
               ▼
┌─────────────────────────────────────┐
│  Contenedor `db` (PostgreSQL)       │
│  - Base `tienda`, usuario `tienda`  │
└─────────────────────────────────────┘
```

**Puertos habituales (host):**

| Puerto | Servicio |
|--------|----------|
| **8080** | Sitio web (Nginx + Angular) |
| **8001** | API Django (mapeo típico `8001:8000`; revisar `docker-compose.yml`) |
| **5432** | Postgres **no** expuesto por defecto al host (solo red Docker), para evitar conflictos con otro Postgres local |

---

## 3. Raíz del repositorio

| Ruta / archivo | Descripción |
|----------------|-------------|
| **`docker-compose.yml`** | Orquesta servicios `db`, `backend`, `frontend`; variables de entorno, volúmenes, healthcheck de Postgres, mapeo de puertos. |
| **`CARPETA.txt`** | Notas rápidas en español (cómo ejecutar, URLs). |
| **`EXPOSICION-PROYECTO.md`** | Este documento (guía de exposición). |
| **`im/`** | Recursos de marca (p. ej. logo fuente SVG); el sitio usa assets bajo `frontend/public/assets/`. |

**Comando típico para demostrar:**

```bash
docker compose up --build
```

- Web: `http://localhost:8080`
- API (si está publicada): `http://localhost:8001/api/productos/`

---

## 4. Backend — carpeta `backend/`

### 4.1 Rol general

Django define el **modelo de datos**, la **API REST** y el **panel de administración**. Los datos persisten en PostgreSQL.

### 4.2 `backend/config/` — proyecto Django

| Archivo | Función |
|---------|---------|
| **`settings.py`** | `INSTALLED_APPS`, base de datos (host `db`, credenciales por env), `REST_FRAMEWORK`, idioma, `DEBUG`, etc. |
| **`urls.py`** | Rutas globales: `/admin/` y prefijo `/api/` → incluye `catalog.urls`. |
| **`wsgi.py`** | Entrada WSGI (usada por Gunicorn en producción). |
| **`asgi.py`** | Entrada ASGI (extensiones async / futuros). |

### 4.3 `backend/catalog/` — aplicación “catálogo”

| Archivo | Función |
|---------|---------|
| **`models.py`** | Modelo **`Producto`**: campos como `nombre`, `marca`, `categoria`, `precio`, `moneda`, `descripcion`, `imagen_url`, timestamps, etc. |
| **`serializers.py`** | **`ProductoSerializer`**: serializa el modelo a JSON para la API. |
| **`views.py`** | **`ProductoViewSet`**: `list` + `retrieve`; filtro opcional `?categoria=` en el queryset. |
| **`urls.py`** | Router DRF (`DefaultRouter`) registra `productos` → URLs tipo `/api/productos/` y `/api/productos/{id}/`. |
| **`admin.py`** | Registro del modelo en `/admin/` para gestión manual. |
| **`migrations/`** | Evolución del esquema y datos. Cada `000X_*.py` es un paso ejecutado con `python manage.py migrate`. |

**Idea del historial de migraciones (para narrar la evolución):**

1. Creación de tabla y datos iniciales.
2. Añadidos de campos (`marca`, `moneda`).
3. Expansión del catálogo y URLs de imagen.
4. Correcciones de URLs (p. ej. imágenes confiables).
5. Actualización por modelo con enlaces verificados a Wikimedia Commons (donde aplique).

### 4.4 Otros archivos relevantes en `backend/`

| Archivo | Función |
|---------|---------|
| **`manage.py`** | Interfaz de línea de comandos Django. |
| **`requirements.txt`** | Dependencias Python (Django, djangorestframework, psycopg2, gunicorn, etc.). |
| **`Dockerfile`** | Construye la imagen del API. |
| **`entrypoint.sh`** | Al iniciar el contenedor: ejecuta migraciones y arranca Gunicorn. |
| **`scripts/build_wikimedia_urls.py`** | Script **opcional** para consultar Commons y ayudar a definir URLs de imágenes (no sustituye al flujo de `migrate` por sí solo). |

---

## 5. Frontend — carpeta `frontend/`

### 5.1 Rol general

Angular genera una **SPA**: una sola carga de `index.html` y navegación por **rutas del lado cliente**. Los datos del catálogo vienen del **HTTP** contra `/api/`.

### 5.2 Configuración y despliegue

| Archivo | Función |
|---------|---------|
| **`angular.json`** | Build, assets, estilos globales, opciones del proyecto. |
| **`package.json`** | Dependencias y scripts (`ng serve`, `ng build`). |
| **`Dockerfile`** | `ng build --configuration=production` (o la usada) y copia a imagen Nginx. |
| **`nginx.conf`** | Sirve archivos estáticos; **`location /api/`** hace `proxy_pass` al servicio `backend`; **`try_files`** para rutas Angular. |
| **`proxy.conf.js`** | En desarrollo con `ng serve`, proxy de `/api` hacia el backend. Por defecto **`http://127.0.0.1:8001`** (mismo puerto que publica Docker en el host). Para `runserver` en 8000: variable de entorno **`DT_API_URL`**. |

### 5.3 `frontend/src/` — entrada de la app

| Archivo | Función |
|---------|---------|
| **`main.ts`** | Arranque: `bootstrapApplication(App, appConfig)`. |
| **`index.html`** | Documento HTML base; carga el bundle. |
| **`styles.scss`** | Estilos globales y **variables CSS** de marca (`--dt-primary`, `--dt-accent`, `--dt-gradient`, etc.). |

### 5.4 `frontend/src/app/` — módulo principal

| Archivo | Función |
|---------|---------|
| **`app.ts`**, **`app.html`**, **`app.scss`** | Componente raíz: layout (cabecera, `router-outlet`, pie, FAB WhatsApp), **splash** de bienvenida con animación del logo. |
| **`app.config.ts`** | `provideRouter`, `provideHttpClient`, listeners de error. |
| **`app.routes.ts`** | Rutas con **lazy loading** (`loadComponent`): inicio, catálogo, detalle `producto/:id`, carrito, tienda, contacto; comodín `**` → inicio. |

#### `pages/` — pantallas (componentes standalone)

| Ruta (URL) | Componente típico | Qué hace |
|------------|-------------------|----------|
| `/` | `inicio.page` | Home: categorías, productos destacados (API), CTAs, WhatsApp. |
| `/catalogo` | `catalogo.page` | Lista productos; filtros `?categoria=` y búsqueda `?q=` (filtrado en cliente sobre la lista cargada). |
| `/producto/:id` | `producto-detalle.page` | `GET /api/productos/{id}/`; ficha y **Añadir al carrito**. |
| `/carrito` | `carrito.page` | Resumen del carrito demo; quitar líneas; vaciar. |
| `/tienda` | `tienda.page` | Información de la tienda. |
| `/contacto` | `contacto.page` | Contacto / formulario según implementación. |

Cada página suele tener **`.ts` (lógica + signals)**, **`.html` (plantilla)** y **`.scss` (estilos)**.

#### `layout/` — piezas repetidas

| Componente | Función |
|------------|---------|
| **`app-header`** | Logo, búsqueda, utilidades, barra de categorías, enlace al carrito con totales. |
| **`app-footer`** | Pie con enlaces e información. |
| **`whatsapp-fab`** | Botón flotante; usa `whatsapp.config.ts` y `whatsapp.util.ts`. |

#### `core/` — servicios y configuración compartida

| Archivo | Función |
|---------|---------|
| **`producto.service.ts`** | Métodos `listar(categoria?)` y `obtener(id)` contra `/api/productos/`. |
| **`carrito.service.ts`** | Estado del carrito (signals), agregar/quitar/vaciar, persistencia en `localStorage`. |
| **`whatsapp.config.ts`** | Número E.164 para WhatsApp. |
| **`whatsapp.util.ts`** | Construcción de URL `wa.me` y apertura en nueva pestaña. |

#### `models/` — tipos TypeScript

| Archivo | Función |
|---------|---------|
| **`producto.ts`** | Interfaz **`Producto`** alineada con el JSON del backend (`precio` como string por Decimal). |
| **`linea-carrito.ts`** | **`LineaCarrito`**: `producto` + `cantidad`. |

### 5.5 `frontend/public/assets/`

Archivos estáticos del build (logos SVG, etc.) referenciados desde plantillas como `assets/logo-dt-technology.svg`.

---

## 6. Flujo de datos (para explicar en voz)

1. El usuario abre `http://localhost:8080`.
2. Angular carga la ruta activa (p. ej. inicio o catálogo).
3. **`ProductoService`** hace `GET /api/productos/` (y opcionalmente con query de categoría en el backend).
4. **Nginx** reenvía esa petición al contenedor **backend**.
5. **Django** ejecuta la vista, consulta **PostgreSQL**, devuelve **JSON**.
6. Angular actualiza **signals** o estado y la **plantilla** renderiza tarjetas, precios e imágenes.
7. En **detalle de producto**, se usa `GET /api/productos/{id}/`.
8. **“Añadir al carrito”** en esta demo es **solo frontend**: `CarritoService` guarda en memoria y en `localStorage` (no hay endpoint de pedido todavía).

---

## 7. Ideas para “mejoras futuras” (cierre de exposición)

- Autenticación de usuarios y carrito/pedidos en **servidor**.
- Pasarela de pago y stock real.
- Paginación y búsqueda full-text en backend (Elasticsearch o Postgres `tsvector`).
- CI/CD y despliegue en la nube (contenedores o PaaS).
- Pruebas automatizadas (Jest/Karma en Angular, pytest en Django).

---

## 8. Glosario breve

| Término | Significado breve |
|---------|-------------------|
| **SPA** | Single Page Application: una sola página cargada y el resto son rutas JS. |
| **REST / JSON** | API basada en recursos y respuestas en formato JSON. |
| **DRF** | Django REST Framework: vistas, serializers y routers para APIs. |
| **Migración** | Script versionado que altera esquema o datos en la base. |
| **Lazy loading** | Cargar código de una ruta solo cuando el usuario entra en ella. |
| **Proxy inverso** | Nginx recibe peticiones y las delega a otro servicio (aquí, `/api/` → Django). |

---

*Generado como apoyo para exposición oral o escrita. Para PDF: abre este archivo en VS Code / Cursor, Markdown PDF, o Pandoc (`pandoc EXPOSICION-PROYECTO.md -o exposicion.pdf`).*
