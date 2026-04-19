/**
 * Proxy para `ng serve`: reenvía `/api` al backend Django.
 *
 * Por defecto usa el puerto publicado en `docker-compose.yml` (8001 → 8000 en el contenedor).
 * Si ejecutas `python manage.py runserver` en el puerto clásico 8000, arranca Angular así:
 *   PowerShell:  $env:DT_API_URL="http://127.0.0.1:8000"; npm start
 *   cmd:         set DT_API_URL=http://127.0.0.1:8000&& npm start
 */
const target = process.env.DT_API_URL || 'http://127.0.0.1:8001';

module.exports = {
  '/api': {
    target,
    secure: false,
    changeOrigin: true,
    logLevel: 'silent',
  },
};
