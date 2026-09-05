# API TechNova — Auditoría de Seguridad

Informe de auditoría y despliegue del proyecto `ejercicio-docker-audit-sai` (API Flask + MySQL): análisis de seguridad con Bandit, escaneo de imagen con Trivy, CI/CD con GitHub Actions y despliegue en AWS EC2 con Nginx Proxy Manager, Dozzle y Uptime Kuma.

## Despliegue en producción

Aplicación desplegada en AWS EC2 con Ubuntu, utilizando Docker Compose para administrar los servicios de la aplicación.

La infraestructura utiliza Nginx Proxy Manager como proxy inverso y DuckDNS para publicar los servicios mediante subdominios:

| Subdominio | Servicio | Acceso |
|-----------|----------|--------|
| [tuapp-api.duckdns.org](https://tuapp-api.duckdns.org) | Backend / API (Flask) | Público |
| [tuapp-dozzle.duckdns.org](https://tuapp-dozzle.duckdns.org) | Dozzle (logs Docker) | Público |
| [tuapp-kuma.duckdns.org](https://tuapp-kuma.duckdns.org) | Uptime Kuma (monitoreo) | Público |

Los servicios se encuentran conectados mediante la red Docker `proxy`.

El panel administrativo de Nginx Proxy Manager utiliza el puerto `81` y se mantiene restringido al acceso local mediante túnel SSH.

## Infraestructura (Docker Compose)

| Servicio | Imagen | Puerto interno | Red |
|----------|--------|----------------|-----|
| nginx-proxy-manager | jc21/nginx-proxy-manager:latest | 80 / 81 / 443 | default / proxy |
| web | api-technova:v1 | 5050 | default |
| db | mysql:8.0 | 3306 | default |
| uptime-kuma | louislam/uptime-kuma:latest | 3001 | proxy |
| dozzle | amir20/dozzle:latest | 8080 | proxy |

### Volúmenes utilizados

- `db_data` — almacenamiento persistente de MySQL.
- `kuma_data` — almacenamiento persistente de Uptime Kuma.
- `./npm/data` — configuración de Nginx Proxy Manager.
- `./npm/letsencrypt` — certificados Let's Encrypt.

## FASE 1 — Auditoría de Seguridad

Se realizó una auditoría de seguridad sobre el proyecto utilizando Bandit.

Durante la revisión se identificaron los siguientes hallazgos y se aplicaron las respectivas correcciones:

| ID | Categoría | Hallazgo | Herramienta | Severidad | Evidencia | Estado |
|----|-----------|----------|-------------|-----------|-----------|--------|
| B105 | Gestión de secretos | Contraseña hardcodeada en el código (`DB_PASS`) | Bandit | Baja | app.py:10 | Corregido |
| B608 | Seguridad SQL | Concatenación de variables en SQL, con posible riesgo de inyección | Bandit | Media | app.py:25 | Corregido |
| B311 | Funcionalidad | Uso de `random.random()` para lógica no criptográfica | Bandit | Baja | app.py:30 | Corregido |
| B201 | Configuración | Uso de `debug=True` en Flask | Bandit | Alta | app.py:35 | Corregido |
| B104 | Configuración | Aplicación enlazada a todas las interfaces mediante `0.0.0.0` | Bandit | Media | app.py:47 | Justificado |
| B101 | Pruebas | Uso de `assert` en pruebas | Bandit | Baja | test_app.py:7 | Justificado |

### Detalle de los hallazgos

**B105 — Contraseña hardcodeada**

Se identificó una contraseña escrita directamente en el código fuente.

La solución fue migrar las credenciales a variables de entorno utilizando `os.getenv()`.

Las credenciales se manejan mediante el archivo `.env`, el cual se encuentra excluido del repositorio mediante `.gitignore`.

**B608 — Posible inyección SQL**

Se identificó concatenación de variables dentro de una consulta SQL.

Se eliminó la concatenación directa y se dejó la estructura preparada para utilizar consultas parametrizadas mediante `%s`.

**B311 — Uso de random**

Se identificó el uso de `random.random()` en la lógica del endpoint `/health`.

Se eliminó la lógica de falla aleatoria y la posibilidad de división por cero.

**B201 — Flask Debug**

Se identificó el uso de `debug=True`.

La configuración fue modificada para utilizar la variable `FLASK_DEBUG`, estableciendo `False` como valor predeterminado.

**B104 — 0.0.0.0**

El uso de `0.0.0.0` se mantiene debido a que la aplicación debe aceptar conexiones desde la red Docker.

Se documentó la excepción mediante:

```python
# nosec B104