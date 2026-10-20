# Plan de Proyecto: Chatbot Conversacional con Búsqueda Web (Local -> Azure Cloud)

## 1. Contexto y Objetivos del Proyecto

* **Propósito:** Construir una aplicación conversacional avanzada orientada a portafolio profesional y alineada con la preparación para las certificaciones de Microsoft Azure (**AZ-204** y **AI-102**).
* **Estrategia:** Desarrollo evolutivo en fases. Se inicia con un prototipo local totalmente gratuito y privado para dominar la lógica de orquestación, e incrementalmente se migra hacia una arquitectura *Cloud-Native* en el ecosistema de Azure.

---

## 2. Arquitectura del Prototipo Inicial (Fase Local)

### Componentes Tecno-Lógicos:
* **Backend:** FastAPI (Python).
* **Cliente LLM:** SDK oficial de OpenAI (`openai-python`) apuntando a Ollama local (`http://localhost:11434/v1`).
* **Modelo LLM Local:** Llama 3, Mistral o Qwen ejecutados en Ollama.
* **Mecanismo de Búsqueda:** Pattern de **Function Calling / Tool Calling** nativo.
* **Motor de Búsqueda Web:** Librería ligera `duckduckgo_search` (sin registro ni API keys requeridas).

### Flujo de Ejecución (Function Calling Loop):
1. **Petición del usuario:** El usuario envía una consulta a FastAPI (ej. *"¿Qué noticias hay hoy sobre X?"*).
2. **Definición de Herramienta:** FastAPI envía el historial y la definición del esquema de la herramienta `web_search` a Ollama mediante el SDK de OpenAI.
3. **Decisión del Modelo:** Ollama identifica que necesita información externa y responde con un llamado de herramienta (`tool_calls`).
4. **Ejecución Local:** FastAPI captura la petición, ejecuta la búsqueda en DuckDuckGo y recupera los fragmentos con contexto.
5. **Generación Final:** FastAPI reenvía la respuesta de la herramienta a Ollama, y este genera la respuesta sintetizada final para el usuario.

---

## 3. Hoja de Ruta Evolutiva (Roadmap hacia Azure)

```
[Fase 1: Prototipo Local] ──> [Fase 2: Integración Azure AI] ──> [Fase 3: Cloud Native & IaC]
```

### Fase 1: Prototipo Local & Funcionalidad Base (Actual)
* Implementar el bucle de *Tool Calling* en FastAPI con `duckduckgo_search`.
* Diseñar endpoints limpìos y modularización del código.
* Pruebas de integración locales.

### Fase 2: Migración a Azure AI Services (Preparación AI-102)
* **Sustituir Búsqueda:** Reemplazar `duckduckgo_search` por **Bing Web Search API** o **Azure AI Search**.
* **Sustituir LLM:** Transicionar el cliente de Ollama local a **Azure OpenAI Service** (despliegue de GPT-4o / GPT-4o-mini).
* **Seguridad:** Integrar la gestión de variables y claves con **Azure Key Vault**.

### Fase 3: Despliegue, Infraestructura y DevOps (Preparación AZ-204)
* **Contenerización:** Crear el `Dockerfile` de producción para FastAPI.
* **Despliegue Cloud:** Publicar la API en **Azure Container Apps** o **Azure App Service**.
* **Infraestructura como Código (IaC):** Automatizar el aprovisionamiento de recursos en Azure con **Bicep** o **Terraform**.
* **Observabilidad:** Añadir trazabilidad con **Azure Application Insights**.

---

## 4. Próximos Pasos Inmediatos

1. Escribir la estructura del código FastAPI con el bucle de Function Calling y la integración con `duckduckgo_search`.
2. Validar la respuesta del modelo local al invocar la herramienta de búsqueda.