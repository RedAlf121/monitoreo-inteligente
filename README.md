# Monitoreo Inteligente de Préstamos Bibliotecarios

Este proyecto es una plataforma de monitoreo inteligente para la gestión de préstamos en bibliotecas, utilizando FastAPI, MCP y agentes LLM para consultas avanzadas.

## Características principales

- **API REST** construida con FastAPI para exponer servicios de monitoreo y notificación.
- **Agente LLM** (Large Language Model) capaz de generar y ejecutar consultas complejas sobre la base de datos MongoDB.
- **Notificaciones automáticas** por email a usuarios con préstamos vencidos o próximos a vencer.
- **Soporte para reglas personalizadas** de negocio extraídas desde archivos de texto.
- **Capa de post-procesamiento** para asegurar que las respuestas del LLM sean JSON válidos.
- **CORS habilitado** para facilitar la integración con frontends modernos.

## Estructura del proyecto

```
├── main.py                        # Punto de entrada principal (FastAPI)
├── requirements.txt               # Dependencias del proyecto
├── env_utils.py                   # Utilidades para variables de entorno
├── controllers/                   # Rutas y lógica de API REST
│   ├── document_controller.py
│   └── notification_controller.py
├── models/                        # Modelos de datos y agentes
│   ├── user.py
│   ├── book.py
│   └── ...
├── services/                      # Lógica de negocio y utilidades
│   ├── scanner/
│   │   └── borrow_scan.py         # Lógica de escaneo y consulta de préstamos
│   └── ...
├── agent/                         # Implementación de agentes y tools
│   └── local/
│       └── mongodb_tools.py       # Tools de solo lectura para MongoDB
├── cached_documents/              # Documentos y reglas cacheadas
│   └── rules/
│       └── rules.txt
└── ...
```

## Instalación y configuración

1. **Clona el repositorio**
2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura las variables de entorno:**
   - Crea un archivo `.env` con las variables necesarias para la conexión a MongoDB y otros servicios.
4. **Configura el archivo `mcp.json`** para los endpoints de MCP si usas agentes remotos. https://github.com/punkpeye/awesome-mcp-servers

## Ejecución

- **Modo desarrollo:**
  ```bash
  python main.py
  ```
  Esto iniciará el servidor FastAPI y el watcher de notificaciones.

## Endpoints principales

- `GET /` — Mensaje de bienvenida
- Otros endpoints definidos en `controllers/`

## Agentes y consultas inteligentes

- El agente LLM puede recibir instrucciones en lenguaje natural y convertirlas en consultas MongoDB.
- El sistema incluye un post-procesador para asegurar que las respuestas sean JSON válidos.
- Si la consulta no arroja resultados, el agente puede devolver el filtro usado para depuración.

## Notificaciones

- El sistema envía emails automáticos a los usuarios con préstamos vencidos o próximos a vencer.
- El estado de notificación se guarda en `notified_status.json`.

## Personalización de reglas

- Las reglas de negocio pueden editarse en `cached_documents/rules/rules.txt`.
- El sistema puede extraer y filtrar reglas relevantes usando prompts y LLM.

## Desarrollo y pruebas

- Puedes usar funciones mock para probar el flujo sin acceder a la base real.
- El sistema soporta recarga automática (`reload=True`) en desarrollo.

## Licencia

MIT

---

**Autor:** Alfredo Hernandez Rodriguez
