# 📚 06. BASE DE CONOCIMIENTO (Tech Stack)
**Funnels Foundry.ai — JobNearMe**

Fuente de referencia documental: `PORTFOLIO_01_JOBNEARME/00_INDICE_DOCUMENTAL.md`
Actualización: 2026-04-26

Este documento consolida el estado real de herramientas, intención actual del sistema y cómo integrar el stack de forma ejecutable y concisa.

---

## 🧭 1. STACK INTEGRADO ACTUAL (OPERATIVO)

| Herramienta | Estado actual | Rol dentro del sistema | Intento operativo actual |
|---|---|---|---|
| **Hermes (Frankie) (DO Droplet 1)** | 🟢 Activo | Orquestador Agentivo (Cerebro) | Gestión persistente vía `systemd` (`frankie.service`). Procesa lógica e interactúa vía Telegram. |
| **Engram (Go) (DO Droplet 1)** | 🟢 Activo | Memoria Semántica Vectorial Local | Córtex de memoria compartida entre sesiones y agentes. Integración total MCP nativa. |
| **n8n (DO Droplet 2)** | 🟢 Activo | Orquestador de APIs y Workflows | Procesamiento en tiempo real de CareerJet (patrón RAM-First) y pipeline de WP. |
| **WordPress + Gutenberg (AWS EC2)** | 🟢 Activo | CMS y frontend público de `jobnearme.online` | Frontend SEO ultraliviano. Prohibido almacenar vacantes masivas en DB SQL. |
| **Cloudflare** | 🟢 Activo | DNS/CDN | Mejorar disponibilidad y rendimiento global. |
| **OpenClaw (DO App/Worker)** | 🟢 Activo | RPA para tareas sin API | Automatizar UI web (especialmente flujos con Abacus y tareas operativas). |
| **Abacus AI / Canva Pro** | 🟢 Activo | Generación multimedia y ensamble | Crear piezas visuales pesadas y branding omnicanal. |
| **OpenRouter** | 🟡 Disponible | Router multi-modelo para inferencia | Modelos por fase (cost-control vs razonamiento técnico profundo). |
| **Notion (Trafficker Core)** | 🟢 Activo | Cerebro Central de Datos | Orquestación de metadatos, triggers de derivados y tracking de assets. |
| **OneDrive + Microsoft Graph** | 🟢 Activo | Bandeja de transferencia | Origen/destino de artefactos documentales (`inbox`, `processed`, `error`). |
| **claudeus-wp-mcp (v3.0.2)** | 🟢 Activo | Servidor MCP de WordPress | Gestión agentiva de posts, media, taxonomías y auditoría de jobnearme.online. |

---

## 🧠 2. CAPA DE ORQUESTACIÓN AGENTIVA LOCAL (ANTIGRAVITY + SDD + SKILLS)

El entorno local de desarrollo está regido por **Antigravity (Agent Teams Lite)**, un asistente orquestador que vive en el IDE y tiene acceso al sistema de archivos, terminal y contexto MCP (Engram).

1. **Antigravity (Orquestador Local)**
   - **Rol:** Ejecutor local. A diferencia de Frankie (en la nube), Antigravity opera en la PC del desarrollador para tareas de ingeniería, escritura de código y despliegue.
   - **Protocolos Activos:** MCP (context7, engram, filesystem, bash).

2. **Engram (Memoria Persistente)**
   - **Rol:** Base de datos vectorial unificada. Antigravity invoca `mem_save`, `mem_search` y `mem_session_summary` de forma proactiva para nunca perder contexto.
   - **Respaldo:** Se complementa con archivos estáticos como `BITACORA_PROYECTO.md` para lectura humana.

3. **SDD (Spec-Driven Development)**
   - **Flujo Obligatorio para Features Complejas:** `/sdd-explore` -> `/sdd-propose` -> `/sdd-spec` -> `/sdd-tasks` -> `/sdd-apply` -> `/sdd-verify`.
   - **Regla:** Ningún cambio grande se escribe "al aire". Se documenta primero en `openspec/`.

4. **Skills de Antigravity (Gemas Locales)**
   - **Qué son:** Subagentes con instrucciones específicas guardados en formato Markdown (ej. `.agent/skills/` o `~/.gemini/antigravity/skills/`).
   - **Herramienta:** `skill-creator` permite generar nuevas herramientas a demanda para evitar bucles de contexto (ej. un skill exclusivo para crear LA2 o debuggear n8n).
   - En práctica: dividir trabajo en agentes (explorar, planear, ejecutar workflows, validar publicación).

5. **Aion UI (Interfaz y Observabilidad de Hermes)**
   - **Rol:** Dashboard gráfico (Frontend) para monitorear y gestionar al agente Hermes (Frankie) en el servidor.
   - **Beneficio:** Evita tener que leer logs crudos por SSH en la terminal de Digital Ocean. Permite ver en tiempo real qué piensa el agente, qué herramientas usa y gestionar su memoria de forma visual.

6. **Multi-modelo por fase (vía OpenRouter cuando aplique)**
   - Razonamiento/propuesta: modelo fuerte de planificación.
   - Implementación: modelo orientado a tools/código.
   - Verificación: modelo fuerte en revisión y detección de fallas.

---

## ⚙️ 3. ARQUITECTURA OBJETIVO (CON LO QUE YA TIENES)

```text
Brief/keyword/source
  -> n8n (trigger manual/schedule/webhook)
  -> OpenClaw (si se requiere UI automation)
  -> Abacus AI (generación multimedia)
  -> OneDrive inbox (artefactos base)
  -> procesamiento/normalización (scripts + n8n code nodes)
  -> Canva Pro (branding + formatos)
  -> WordPress REST API (draft)
  -> QA editorial/SEO
  -> publish + distribución
```

### Flujo mínimo productivo recomendado
1. **Contenido base** entra a OneDrive con convención de slug.
2. **n8n** procesa frontmatter, renderiza HTML y crea draft en WordPress.
3. **Abacus/OpenClaw** generan activos visuales cuando no hay API directa.
4. **Canva Pro** aplica branding y saca variantes sociales.
5. **Publicación** solo después de checklist SEO y validación humana.

---

## 💸 4. ESTRATEGIA DE COSTO (ARRANQUE)

Con recursos actuales (`OpenRouter` saldo bajo + `Abacus` + infra mínima en DO/EC2):

- Priorizar en OpenRouter modelos costo-efectivos para tareas repetitivas.
- Reservar modelos premium solo para diseño/propuesta crítica o debugging complejo.
- Mantener WordPress en `draft` como política de control de calidad.
- Ejecutar lotes pequeños primero (1-3 piezas E2E) antes de escalar.

---

## 🏗️ 5. INTEGRACIÓN TÉCNICA CLAVE

### n8n
- Documentación oficial: [https://docs.n8n.io/](https://docs.n8n.io/)
- Nodos críticos actuales: Schedule Trigger, HTTP Request, Webhook, Respond to Webhook, Code, IF, Split In Batches, Write Binary File, Microsoft OneDrive (download/search/folder).
- **📋 Inventario completo de nodos nativos disponibles:** `../00_CORE_AGENCY/13_INVENTARIO_NODOS_NATIVOS_N8N.md` — consultar SIEMPRE antes de usar HTTP Request para verificar si existe nodo nativo.
- Integraciones activas del repo:
  - `N8N_WORKFLOWS/IgWTm2dUp24r8fZx_v2.json` — **Workflow activo OneDrive → WordPress SEO** (doc: `README_WORKFLOW_ONEDRIVE_WP.md`)
  - `N8N_WORKFLOWS/wp_publish_la2_pillars_seo_automation.json`
  - `PERSONAL_OS/N8N_WORKFLOWS/personal_os_telegram_inbox_capture.json`
  - `N8N_WORKFLOWS/wp_drive_inbox_to_wordpress_seo.json` — **LEGADO** (reemplazado por OneDrive)

### CLI Manager para n8n API (`n8n_manager.py`)
- **Ubicación:** `N8N_WORKFLOWS/n8n_manager.py`
- **Rol:** Permite a Antigravity (local) gestionar workflows de n8n en Digital Ocean desde la terminal.
- **Comandos:** `list`, `export <ID> <archivo>`, `push <ID> <archivo>`, `create <archivo>`
- **Credenciales:** Lee `N8N_HOST_URL` y `N8N_API_KEY` desde `.env` en la raíz del proyecto.
- **Nota técnica:** Incluye User-Agent de Chrome para evadir bloqueo de Cloudflare (Error 1010). La API PUT de n8n solo acepta `{name, nodes, connections, settings: {}}`.

### Integración n8n <-> Microsoft OneDrive
- **Autenticación (Microsoft OAuth2 API):** n8n requiere credenciales OAuth2. Se debe crear una app en Microsoft Azure / Entra ID, obtener `Client ID` y `Client Secret`.
- **Requisito Crítico de Permisos:** En Entra ID, el administrador debe habilitar la opción "User can consent to apps accessing company data on their behalf". Sin esto, n8n no podrá leer ni escribir en las bandejas `inbox/processed/error`.
- **Uso:** Funciona como bandeja de intercambio asíncrona entre generación (Abacus/PC local), procesamiento (n8n) y publicación. Evita dependencias de sincronización local.

### Integración n8n <-> WordPress REST API
- **Autenticación (Basic Auth):** Para instalaciones self-hosted (como nuestro AWS EC2), NO se usa OAuth2 ni la contraseña de admin regular. 
- **Requisito Crítico:** Se debe habilitar la Autenticación en Dos Pasos (2FA) en el perfil de WordPress, y luego generar un **Application Password** (Contraseña de Aplicación) exclusivo para n8n.
- **Endpoints base:** `/wp-json/wp/v2/posts` y `/wp-json/wp/v2/media`
- **Operación LA2:** n8n debe enviar los datos estructurados y el meta SEO al plugin activo (Yoast o RankMath) durante la creación del `draft`.
- **⚠️ GOTCHA CRÍTICO — Nodo WordPress Nativo v1:** El nodo `n8n-nodes-base.wordpress` (typeVersion 1) **SOLO soporta** los recursos `Post` y `User`. **NO tiene soporte para `Media`**. Para subir imágenes a la Media Library de WordPress, se DEBE usar un nodo **HTTP Request** haciendo POST a `/wp-json/wp/v2/media` con `contentType: binaryData`, `inputDataFieldName: data` y header `Content-Disposition: attachment; filename="archivo.ext"`. Usar el nodo nativo con `resource: "media"` genera error `"Could not get parameter"`. Ver documentación completa en `N8N_WORKFLOWS/README_WORKFLOW_ONEDRIVE_WP.md`.

### OpenClaw
- Rol operativo en este proyecto: RPA de UI cuando no exista API fiable.
- Repositorio base de despliegue observado en entorno: [https://github.com/digitalocean-labs/openclaw-appplatform.git](https://github.com/digitalocean-labs/openclaw-appplatform.git)

### Canva Pro
- Bulk Create: [https://www.canva.com/help/bulk-create/](https://www.canva.com/help/bulk-create/)
- Rol: capa final de identidad visual y exportación multiformato.

### Capa Engram/SDD/Skills (referencia metodológica)
- AI Gentle Stack: [https://github.com/Gentleman-Programming/gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)
- Engram: [https://github.com/Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)
- OpenSpec: [https://openspec.dev](https://openspec.dev)

---

## ✅ 6. QUÉ YA ESTÁ FUNCIONANDO VS QUÉ FALTA

### Funcionando
- WordPress online en EC2.
- n8n desplegado y workflows en repositorio.
- OneDrive como eje de intercambio.
- OpenClaw desplegado para automatización UI.
- Abacus y Canva Pro disponibles por suscripción.

### Falta cerrar para escalar sin fricción
- Normalizar rutas hardcodeadas en workflows y validar E2E real en entorno.
- Definir contrato único de entrada (si el scheduler empuja `.md` o `.json`).
- Cerrar política cuando falta imagen (publicar sin featured o mandar a error).
- Formalizar integración Canva en pipeline automático (hoy está disponible, no completamente acoplada).
- Definir política de uso de OpenRouter por tipo de tarea para no consumir saldo sin control.

---

## 🧩 7. MATRIZ DE INTEGRACIÓN DEL ECOSISTEMA (V1 -> V2)

| Herramienta | Rol oficial | Entra | Sale | Trigger principal | KPI operativo |
|---|---|---|---|---|---|
| **Telegram Bot** | Canal de comando y soporte en movilidad | Texto/audio de usuario | Solicitud normalizada a n8n | Mensaje entrante | Tiempo de primera respuesta |
| **WhatsApp (Fase 2)** | Canal masivo de atención y seguimiento | Texto/audio de usuario | Solicitud normalizada a n8n | Mensaje entrante | Tasa de respuesta útil por conversación |
| **n8n** | Orquestador central multiproyecto | Evento de canal/webhook/scheduler | Acciones en GitHub, Mautic, WP, correo, logs | Webhook, Trigger nodos | Éxito E2E por flujo |
| **GitHub (repo privado)** | Memoria versionada y trazabilidad | Commits de notas/logs/síntesis | Contexto consumible por IA y equipo | Push/PR/Webhook | Latencia de sincronización móvil->repo |
| **Obsidian (local)** | IDE de conocimiento y síntesis | Notas, decisiones, playbooks | Markdown sincronizable a repo | Edición local/sync | Cobertura de decisiones documentadas |
| **Mautic** | CRM + segmentación + campañas | Leads, eventos de intención, tags | Segmentos, scoring, campañas, webhooks | Form/chat webhook/evento contacto | Conversión por segmento |
| **Zoho Mail** | Correo corporativo operativo actual | Mensajes internos/operativos | Comunicación corporativa y soporte | SMTP/IMAP/API | Entregabilidad operativa |
| **AWS SES (post-sandbox)** | Capa de envío transaccional escalable | Eventos transaccionales aprobados | Emails transaccionales a escala | API/SMTP desde backend o n8n | Bounce/complaint rate |
| **Careerjet API** | Fuente de vacantes para experiencia real | Query de búsqueda (keywords/location) | Resultados de jobs para páginas/servicios | Llamada API con credenciales válidas | Cobertura de búsquedas exitosas |
| **OpenRouter / LLM Provider** | Razonamiento y generación contextual | Prompt + contexto + políticas | Respuesta/plan/acción sugerida | Llamada por intent | Costo por ítem y calidad de respuesta |
| **OpenClaw** | Automatización UI cuando no hay API | Tarea definida por workflow | Resultado de acción UI + evidencia | Disparo n8n/manual | Tasa de éxito de tareas sin API |
| **WordPress (EC2)** | Publicación web JobNearMe | Contenido validado + metadatos | Draft/publish y páginas indexables | REST API workflow | Publicaciones válidas sin retrabajo |

### Contrato de evento recomendado para todo el ecosistema
```json
{
  "project_key": "jobnearme",
  "intent": "support|lead_capture|publish_content|research|automation|qa|ops",
  "priority": "low|medium|high",
  "source_channel": "telegram|whatsapp|web|manual",
  "user_id": "string",
  "payload": {}
}
```

### Secuencia operativa por fases
1. **V1 (inmediata)**: Telegram + n8n + GitHub + Obsidian + Mautic básico + Zoho Mail.
2. **V1.5**: memoria conversacional corta, tagging de intención y campañas iniciales en Mautic.
3. **V2 (avanzada)**: vector RAG, WhatsApp, AWS SES fuera de sandbox, integración plena de Careerjet.

### Política obligatoria de documentación de herramientas
- Toda herramienta usada en el ecosistema debe estar documentada en esta wiki antes de cierre de sesión.
- Si se agrega una herramienta nueva, la actualización mínima obligatoria incluye: rol oficial, entradas, salidas, trigger principal, KPI operativo, estado y fase.
- Si se reemplaza o retira una herramienta, registrar motivo y herramienta sustituta para preservar continuidad.
- Todo cambio de herramienta debe reflejarse también en `PORTFOLIO_01_JOBNEARME/00_INDICE_DOCUMENTAL.md` y `BITACORA_PROYECTO.md` para mantener SSOT.
- Esta política existe para clonación rápida del stack en nuevos portfolios, cambios controlados e inclusión de herramientas futuras sin pérdida de contexto.

### Plantilla estándar de herramienta (alta/cambio/retiro)
```md
## Ficha de herramienta
- Nombre:
- Estado: Activa | Piloto | En evaluación | Retirada
- Fase: V1 | V1.5 | V2
- Tipo: Canal | Orquestación | CRM | Email | IA | CMS | Integración | RPA | Datos
- Proyecto(s): jobnearme | p02_xxx | core_agency

### Rol oficial
- 

### Entradas (input)
- 

### Salidas (output)
- 

### Trigger principal
- 

### KPI operativo
- 

### Dependencias
- 

### Riesgos
- 

### Reglas de operación
- 

### Historial de cambios
- Fecha UTC:
- Cambio:
- Impacto:
- Responsable:
```

### Procedimiento mínimo de uso de plantilla
1. Crear o actualizar la fila correspondiente en la matriz de integración.
2. Completar la ficha con los campos mínimos obligatorios.
3. Si hay impacto de gobierno, reflejar cambio en `PORTFOLIO_01_JOBNEARME/00_INDICE_DOCUMENTAL.md`.
4. Registrar entrada en `BITACORA_PROYECTO.md` con decisión, riesgo y siguiente paso.

### Contrato de comandos Frankie (operación diaria)
```json
{
  "project_key": "jobnearme|personal_os|lab",
  "intent": "publish_content|research|automation|agenda|reminder|ops|qa",
  "priority": "low|medium|high",
  "approval_mode": "required|auto",
  "source_channel": "telegram|whatsapp|web|manual",
  "payload": {}
}
```

### Política de ejecución y separación
- Toda solicitud debe incluir `project_key`.
- `jobnearme`: entorno negocio con aprobación obligatoria en acciones críticas.
- `personal_os`: entorno personal para agenda, hábitos y recordatorios, almacenado en `PERSONAL_OS/` fuera de `PORTFOLIO_*`.
- `lab`: entorno de pruebas y experimentación.
- Si no hay `project_key`, n8n debe solicitar aclaración y no ejecutar.

### Plantillas de comando
- `jobnearme`: "Frankie en jobnearme, investiga y prepara post sobre Top AI developer skills 2026. No publiques sin aprobación."
- `jobnearme`: "Frankie en jobnearme, apruebo draft top-ai-developer-skills-2026. Ejecuta publicación y registra bitácora."
- `personal_os`: "Frankie en personal_os, mañana 3pm cita con Doña Ana y recordarme llevar multímetro 1 hora antes."
- `personal_os`: "Frankie en personal_os, bloquea hoy 1 hora para curso de Python y recuérdame 15 minutos antes."
- `lab`: "Frankie en lab, prueba flujo de resumen de notas sin tocar producción."

## 🧬 8. ALCANCE OFICIAL DEL STACK (ACTUAL + EXPANDIBLE)

### Estado global por herramienta
| Herramienta | Rol principal | Estado | Fase |
|---|---|---|---|
| WordPress + Gutenberg + Blocksy | CMS + frontend público | Activo | V1 |
| AWS EC2 | Hosting WordPress | Activo | V1 |
| Cloudflare | DNS/CDN | Activo | V1 |
| n8n (DigitalOcean) | Orquestación central de workflows | Activo | V1 |
| OneDrive + Microsoft Graph | Bandeja de intercambio de artefactos | Activo | V1 |
| OpenClaw | RPA/automatización UI sin API | Activo | V1 |
| Abacus AI | Generación multimedia | Activo | V1 |
| Canva Pro | Branding y adaptación multiformato | Activo | V1 |
| OpenRouter | Router multi-modelo para inferencia | Disponible | V1.5 |
| Telegram Bot | Canal de comando móvil | Activo (jobnearme/personal_os) | V1 |
| WhatsApp | Canal conversacional masivo | Planificado | V2 |
| Mautic | CRM/segmentación/campañas | Parcial | V1.5 |
| Zoho Mail | Correo corporativo operativo | Activo | V1 |
| AWS SES | Correo transaccional a escala | Pendiente salida sandbox | V2 |
| Careerjet API | Vacantes en tiempo real | Pendiente aprobación | V2 |
| Obsidian + GitHub | Memoria documentada y trazabilidad | Activo | V1 |
| Hermes | Capa de coordinación de intención y ejecución agentiva | En evaluación activa | V1.5 |
| claudeus-wp-mcp | Servidor MCP para gestión profunda de WordPress | Activo | V1 |

### Alcance ampliado de Hermes y OpenClaw
- Hermes como coordinador:
  - Decide ruta de ejecución por intención (`research`, `ops`, `publish_content`, `qa`, `automation`).
  - Prioriza costo/latencia/calidad y selecciona combinación API + modelo + workflow.
  - Mantiene continuidad operativa entre canales y contextos (`jobnearme`, `personal_os`, `lab`).
- OpenClaw como ejecutor UI:
  - Resuelve pasos donde no hay API estable.
  - Ejecuta acciones repetibles sobre interfaces web y devuelve evidencia de ejecución.
  - Funciona como fallback operativo cuando API-first no cubre el caso.
- Complementariedad oficial:
  - Hermes decide y gobierna la ruta.
  - n8n orquesta nodos y contratos.
  - OpenClaw ejecuta la parte UI no cubierta por API.
  - OpenRouter/LLMs aportan razonamiento por fase.

### Principio rector de diseño del stack
- El stack se considera oficialmente abierto y recombinable.
- Se permite combinar herramientas actuales y nuevas en cualquier momento si mejoran eficiencia, calidad o resiliencia.
- Ninguna combinación queda “congelada” por preferencia histórica; toda arquitectura es revisable por evidencia operativa.

## 🔁 9. POLÍTICA OFICIAL DE OPTIMIZACIÓN CONTINUA DEL STACK

- API-first: usar integración por API como opción primaria cuando exista y sea estable.
- RPA-fallback: usar OpenClaw cuando no exista API, la API sea inestable o el costo/tiempo de integración no compense.
- Multi-modelo por intención: enrutar modelo según tipo de tarea (planificación, ejecución, verificación) y presupuesto.
- Revisión periódica: auditar stack en ciclos regulares (semanal táctico, mensual estratégico).
- Sustitución controlada: cualquier alta/cambio/retiro exige actualización de esta wiki + índice + bitácora.

## 📏 10. MARCO DE EVALUACIÓN PARA NUEVAS HERRAMIENTAS

### Criterios mínimos
- KPI de impacto: tiempo de ciclo, tasa de éxito E2E, retrabajo, calidad de salida.
- Costo total: licencias, infraestructura, mantenimiento, costo por ejecución.
- Riesgo operativo: fallos, dependencia de proveedor, lock-in, complejidad de soporte.
- Compliance y seguridad: manejo de datos, permisos, auditoría, trazabilidad.
- Interoperabilidad: compatibilidad con n8n, WordPress, OneDrive, CRM y contrato de eventos.

### Regla de adopción
- Adoptar solo si mejora neta medible frente al baseline actual.
- Si no supera baseline en piloto controlado, mantener como “en evaluación” o descartar.

## 🧪 11. INTEGRACIÓN CANVA OMNICANAL (PROCEDER CIENTÍFICO + VISIÓN AGENTIVA)

### Objetivo
Convertir Canva Pro en capa industrial de postproducción para transformar salidas de super agentes (texto, imagen, video) en activos listos para distribución multiplataforma con calidad consistente de marca.

### Arquitectura operativa recomendada
1. `Hermes` clasifica intención (`publish_content`, `omnichannel_distribution`, `qa_visual`) y define ruta.
2. `n8n` orquesta ejecución y valida contrato de entrada.
3. `Abacus/OpenClaw` generan activos base cuando no hay API directa.
4. `Canva Pro` aplica plantilla maestra y produce variantes por canal.
5. `n8n` distribuye por canal y registra métricas E2E.

### Contrato mínimo de entrada a Canva
```json
{
  "project_key": "jobnearme",
  "intent": "omnichannel_distribution",
  "asset_id": "slug-o-id-unico",
  "template_family": "jobnearme_core_v1",
  "formats": ["1200x630", "1080x1920", "1000x1500"],
  "headline": "string",
  "subheadline": "string",
  "cta": "string",
  "media_source": "onedrive|wordpress|url",
  "destination_channels": ["wordpress", "youtube_shorts", "pinterest", "telegram"],
  "approval_mode": "required|auto"
}
```

### Mapa de formatos por canal
- `1200x630`: featured image WordPress + distribución web.
- `1080x1920`: Shorts/Reels/TikTok.
- `1000x1500`: Pinterest pin.
- Regla: una misma pieza madre debe producir variantes por template sin rehacer contenido desde cero.

### Política de integración
- API-first: integrar Canva por API cuando la operación esté cubierta.
- RPA-fallback: usar OpenClaw si la acción en Canva no está expuesta por API.
- Plantillas bloqueadas: identidad visual fija; solo cambian campos dinámicos.
- Publicación condicionada: distribución automática solo tras `publish` o aprobación explícita.

### Hipótesis experimentales (ciclo 2-4 semanas)
- H1: Canva + plantillas maestras reduce tiempo de producción omnicanal >= 40%.
- H2: Reutilizar pieza madre en 3 formatos aumenta salida semanal sin perder calidad editorial.
- H3: Integrar distribución por eventos en n8n mejora tasa de publicación sin retrabajo.

### Diseño de experimentos
1. Piloto A (manual baseline): producción actual sin acople completo Canva.
2. Piloto B (semi-automático): Canva con plantillas + export por lote.
3. Piloto C (automatizado): evento `post.published` -> variantes Canva -> distribución.
4. Comparar A/B/C con misma carga de contenidos y ventana temporal homogénea.

### KPI de decisión
- Tiempo de ciclo por pieza (brief -> distribución).
- Tasa de éxito E2E por workflow.
- Retrabajo visual por pieza.
- Costo total por pieza distribuida.
- CTR/engagement por canal.
- Cumplimiento de identidad visual (checklist QA).

### Criterio de adopción
- Escalar integración solo si el piloto mejora baseline en tiempo/costo/calidad.
- Si no mejora, mantener Canva en modo parcial y ajustar plantilla/contrato antes de escalar.

## 🎯 12. INTENCIÓN OPERATIVA VIGENTE

1. Construir autoridad SEO con publicaciones estructuradas y verificables.
2. Automatizar producción omnicanal sin perder control editorial.
3. Mantener costos bajos al inicio y escalar por lotes validados.
4. Operar con memoria de proyecto entre sesiones usando bitácora + documentación fuente de verdad.

## 🌐 13. ESTRATEGIA OMNICANAL SEO + AI SEARCH (ARQUITECTURA EDITORIAL)

### Objetivo de distribución
- Maximizar descubribilidad en buscadores clásicos, motores con IA y consumo social nativo.
- Operar una pieza madre por tema y derivar versiones por plataforma sin duplicación literal.
- Mantener consistencia semántica (misma tesis) con variación estructural por canal.

### Regla de pieza madre
- Toda campaña nace como `pieza_madre` (artículo canónico en WordPress).
- Cada canal publica una `derivada` con propósito distinto: captación, autoridad, conversación o distribución.
- Cada derivada enlaza al activo canónico o a su siguiente paso de funnel.

### Política anti-duplicado Quora/Medium
- No republicar texto completo idéntico entre Quora, Medium y WordPress.
- Alternar patrón de publicación por clúster:
  - Clúster A: versión extensa en Medium + respuestas tácticas en Quora.
  - Clúster B: respuestas extensas en Quora + resumen editorial en Medium.
- Reglas de variación mínima obligatoria:
  - Cambiar apertura, estructura de subtítulos y cierre.
  - Cambiar al menos 40% del cuerpo (orden, ejemplos, framing).
  - Mantener keywords objetivo pero con intención distinta por plataforma.
- Quora debe publicarse como respuesta contextual a pregunta concreta, no como copia de artículo.
- Medium debe publicarse como artículo editorial completo con narrativa propia y enlace canónico.

## 🧭 14. MATRIZ OPERATIVA POR PLATAFORMA (API VS MANUAL)

| Plataforma | Modo recomendado | Estado API | Restricciones/compatibilidades clave | Formato principal recomendado | Rol en funnel |
|---|---|---|---|---|---|
| Quora | Manual-first | Sin API pública oficial de publicación identificada | Riesgo alto de depender de métodos no oficiales; priorizar publicación humana contextual | Respuesta educativa + imagen portada cuando aplique | TOFU/MOFU (autoridad por respuesta) |
| Medium | Manual-first + legado opcional | Medium no emite nuevos tokens ni nuevas integraciones; tokens existentes pueden seguir funcionando | Alta incertidumbre de continuidad para automatización nueva; tratar como canal editorial semi-manual | Artículo largo educativo + cover image | TOFU/MOFU (autoridad temática) |
| Pinterest | API-first | API v5 para creación de Pins | Requiere app/config OAuth; orientar piezas visuales verticales y metadata clara | Pin 1000x1500 + título + descripción + URL destino | TOFU (descubrimiento visual) |
| Facebook Page | API-first | Pages API y Graph API para feed, fotos, videos | Requiere permisos de Page y review; separar copy corto vs video/reel por objetivo | Post de texto/link + imagen 1200x630 + video/reel | TOFU/MOFU (alcance + comunidad) |
| Instagram Profesional | API-first | Instagram Content Publishing API | Solo cuentas profesionales; media en URL pública; límites de publicación por ventana móvil; validar cuota antes de publicar | Feed (imagen/carrusel) + Reels 9:16 | TOFU/MOFU (distribución visual) |
| TikTok | API-first controlado | Content Posting API (direct post/upload) | Clientes no auditados publican con restricciones de visibilidad; requiere scope y consentimiento | Video corto 9:16 + caption con hashtags | TOFU (alcance en volumen) |
| X | API-first | X API v2 creación de posts | Acceso y consumo sujetos a plan/rate limits; definir presupuesto por volumen | Post corto + enlace + media opcional | TOFU/MOFU (distribución rápida) |
| LinkedIn | API-first | Posts API / UGC API | Requiere permisos y roles por organización; límites por tipo de contenido | Post experto + documento/video nativo | MOFU/BOFU (credibilidad B2B) |
| YouTube | API-first | YouTube Data API `videos.insert` | Proyectos no verificados suben en privado hasta auditoría; costos de cuota por método | Video largo 16:9 + metadata SEO + thumbnail | TOFU/MOFU/BOFU (evergreen + autoridad) |

## 🧱 15. FORMATOS POR CANAL Y UTILIDAD (FB/IG/REELS/SHORTS/YT LARGO)

### Facebook
- Post escrito + enlace:
  - Objetivo: tráfico al canónico (WordPress).
  - Activo: copy breve + imagen 1200x630.
- Post educativo nativo (sin salir de plataforma):
  - Objetivo: engagement y señales sociales.
  - Activo: texto con microestructura (problema -> solución -> CTA).
- Reel en Facebook:
  - Objetivo: alcance incremental de video corto.
  - Activo: derivado del master 9:16.

### Instagram
- Feed (imagen/carrusel):
  - Objetivo: posicionamiento visual y guardados.
  - Activo: 1:1 o 4:5 con caption educativo.
- Reels:
  - Objetivo: alcance y descubrimiento.
  - Activo: 9:16, hook 1-3s, CTA a perfil/link.

### Reels multipropósito (FB + IG + TikTok + YouTube Shorts)
- Se define un `master_short_9x16` único por tema.
- Derivaciones mínimas por plataforma:
  - Caption y hashtags específicos por red.
  - Portada/frame adaptado por canal.
  - CTA ajustado al comportamiento de cada audiencia.
- Evitar watermark cruzado entre plataformas.

### YouTube largo
- Formato base para autoridad evergreen y SEO audiovisual.
- Estructura: problema -> contexto -> desarrollo -> síntesis -> CTA.
- Del video largo se extraen cortes para `master_short_9x16`.

## 🔗 16. INTERCONEXIONES EFICIENTES DEL STACK OMNICANAL

### Grafo operativo recomendado
1. `WordPress` recibe artículo canónico y featured image.
2. Evento `post.ready_for_distribution` dispara `n8n`.
3. `n8n` llama capa de transformación (copy variants + metadata).
4. `Canva` produce variantes visuales por formato.
5. Publicador enruta por canal:
   - API-first para Pinterest, Meta, TikTok, X, LinkedIn, YouTube.
   - Manual queue para Quora y Medium (o Medium con token legado cuando aplique).
6. `Mautic` y analítica consolidan desempeño por canal/activo.
7. `BITACORA_PROYECTO.md` registra decisiones y ajustes del ciclo.

### Contrato mínimo para despacho omnicanal
```json
{
  "project_key": "jobnearme",
  "intent": "omnichannel_distribution",
  "canonical_url": "https://jobnearme.online/...",
  "asset_slug": "string",
  "content_cluster": "string",
  "channels": ["facebook", "instagram", "tiktok", "youtube", "linkedin", "x", "pinterest", "quora", "medium"],
  "approval_mode": "required|auto",
  "dedupe_policy": "strict_quora_medium",
  "publish_mode": {
    "quora": "manual",
    "medium": "manual_or_legacy_token",
    "others": "api"
  }
}
```

## 🧪 17. MARCO DE VALIDACIÓN CONTINUA -> PRODUCCIÓN PERMANENTE

### Fase 1: Validación controlada (2-4 semanas)
- Publicar lotes semanales pequeños por clúster temático.
- Medir por canal: CTR, retención, guardados, comentarios, tráfico al canónico, tiempo de ciclo.
- Verificar cumplimiento de dedupe Quora/Medium antes de publicar.

### Fase 2: Estandarización
- Congelar plantillas ganadoras de copy y visual por tipo de pieza.
- Pasar canales estables a `approval_mode=auto` con guardas de riesgo.
- Mantener Quora/Medium en aprobación manual editorial.

### Fase 3: Producción permanente
- Operación por calendario + triggers por evento.
- Dashboard de rendimiento semanal y revisión estratégica mensual.
- Backlog continuo de optimización (nuevas herramientas, nuevos formatos, nuevos canales).

### Gate de calidad obligatorio previo a publicación
- Coherencia con tesis del canónico.
- Variación anti-duplicado en Quora/Medium validada.
- Compatibilidad técnica de formato por canal validada.
- Metadata mínima completa (título, descripción, CTA, URL canónica).
- Evidencia de ejecución registrada en bitácora/log.

## 📚 18. FUENTES OFICIALES DE CAPACIDADES (BASE DE DECISIÓN)

- Meta Instagram Content Publishing, límites y flujo: https://developers.facebook.com/docs/instagram-platform/content-publishing/
- Meta IG `content_publishing_limit`: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit/
- Facebook Pages API: https://developers.facebook.com/docs/pages-api/
- Meta Video publishing a Page: https://developers.facebook.com/docs/video-api/guides/publishing/
- Pinterest API v5: https://developers.pinterest.com/docs/api/v5/
- Pinterest Create Pin: https://developers.pinterest.com/docs/api/v5/pins-create/
- TikTok Content Posting API: https://developers.tiktok.com/products/content-posting-api/
- TikTok Direct Post reference: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- X API create post: https://docs.x.com/x-api/posts/create-post
- X API general docs: https://developer.x.com/en/docs/x-api
- LinkedIn Posts API: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2025-11
- LinkedIn UGC Post API: https://learn.microsoft.com/en-us/linkedin/compliance/integrations/shares/ugc-post-api
- YouTube `videos.insert`: https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube quota calculator: https://developers.google.com/youtube/v3/determine_quota_cost
- Medium Help Center (API/Importing): https://help.medium.com/hc/en-us/articles/213480228-API-Importing
- Referencia externa sobre ausencia de API pública en Quora: https://rollout.com/integration-guides/quora/api-essentials

## 🛡️ 19. AUDITORÍA PROFUNDA DEL MODELO AGÉNTICO/AUTÓNOMO (HITL)

### Contexto general
- La arquitectura actual tiene una base sólida: contrato de intención, separación por `project_key`, aprobación humana en acciones críticas y trazabilidad en bitácora.
- El riesgo principal no está en una sola herramienta, sino en la combinación de autonomía + acceso a herramientas + contenido externo no confiable.

### Fortalezas estructurales
- Separación explícita de contextos (`jobnearme`, `personal_os`, `lab`) para reducir mezcla accidental de dominios.
- Política de `approval_mode=required` en operaciones sensibles de negocio.
- Estrategia API-first + RPA-fallback que evita bloquear operación cuando falta API.
- Trazabilidad documental obligatoria (wiki + índice + bitácora).

### Debilidades observadas
- No existe aún una matriz de riesgo unificada por tipo de acción agentica y criticidad.
- La defensa contra prompt injection está implícita en reglas, pero requiere controles explícitos por nodo y por tool-call.
- Observabilidad parcial: falta estándar único de logging de decisiones, denegaciones y aprobaciones por ejecución.
- Riesgo de dependencia en flujos manuales para validar canales donde no hay API oficial.

### Riesgos técnicos prioritarios
- Prompt injection directa e indirecta desde web/documentos/inputs de usuario.
- Exceso de agencia (acciones de alto impacto sin suficiente fricción de control).
- Fuga de datos sensibles por tool-calls sobre-contextualizados.
- Manejo incorrecto de salida del modelo hacia sistemas ejecutables.
- Escalada de costos/consumo por tareas largas sin límites operativos.

### Resultado de auditoría (estado actual)
- Madurez operativa: **media-alta** en gobernanza documental y separación de contextos.
- Madurez de seguridad agentica: **media**; requiere endurecimiento formal en validaciones, permisos y monitoreo.
- Recomendación: avanzar a un esquema de seguridad por capas antes de ampliar autonomía de publicación/distribución.

## 🔐 20. POLÍTICA DEFENSIVA PARA MODELOS AVANZADOS (GPT-5.5, MYTHOS Y MODELOS NO VERIFICADOS)

### 20.1 GPT-5.5 (frontera generalista)
- Usar versión/snapshot fijado por entorno para estabilidad de comportamiento en producción.
- Definir `reasoning.effort` por tipo de tarea para balancear costo, latencia y riesgo de sobre-ejecución.
- Exigir salidas estructuradas en tareas de enrutamiento, ejecución o mutación de estado.
- En tareas críticas, aplicar HITL obligatorio antes de acciones irreversibles.

### 20.2 Mythos (capacidades ciber avanzadas)
- Tratar su uso como **alto riesgo operacional** incluso en contexto defensivo.
- Restringir a entornos controlados, objetivos autorizados y alcance explícitamente documentado.
- Prohibir ejecución autónoma directa sobre activos productivos sin validación humana dual.
- Registrar evidencia de propósito defensivo, autorización y resultados de cada sesión.

### 20.3 Modelos no verificados o “underground” (deep web)
- Política oficial: **no integración en producción** sin verificación legal, técnica y de cadena de suministro.
- Requerir evaluación mínima previa: procedencia, licencia, telemetría, controles de seguridad y reputación técnica.
- Si se evalúan en laboratorio, hacerlo aislado, con datos sintéticos y sin secretos.
- Criterio de descarte inmediato: opacidad de pesos/origen, claims no auditables o comportamiento inseguro recurrente.

### 20.4 Controles transversales obligatorios
- Principio de mínimo privilegio por herramienta, credencial y workflow.
- Segmentación de entornos (`lab` separado de producción) con secretos rotados.
- Confirmación humana para acciones sensibles (publicar, borrar, transferir datos, cambios masivos).
- Límites de consumo: presupuesto por flujo, rate limits y abortos automáticos por anomalía.
- Auditoría continua con pruebas adversariales periódicas (red-team de prompts y herramientas).

## 🧰 21. MATRIZ DE HERRAMIENTAS Y SKILLS CON CONTROLES DE SEGURIDAD

| Herramienta/Skill | Riesgo principal | Controles mínimos | HITL requerido |
|---|---|---|---|
| Hermes (coordinación) | Ruta incorrecta o sobre-agencia | Intents permitidos, políticas por contexto, salidas estructuradas | Sí, cuando la acción cambia estado externo |
| n8n (orquestación) | Ejecución de payload no validado | Validación de esquema, allowlist de intents, control de credenciales por workflow | Sí, para publish/delete/transfer |
| OpenClaw (RPA UI) | Automatización fuera de alcance o frágil | Runbooks cerrados, pasos determinísticos, captura de evidencia por ejecución | Sí, para acciones irreversibles |
| GPT-5.5 / OpenRouter | Prompt injection, filtración de contexto | Separar entrada confiable/no confiable, JSON schema output, límites de tokens/tiempo | Sí, en decisiones de impacto alto |
| Mythos (defensivo ciber) | Capacidad ofensiva mal utilizada | Entorno aislado, alcance autorizado, supervisión dual, logging reforzado | Sí, siempre |
| WordPress | Publicación errónea o masiva | Modo draft por defecto, roles mínimos, checklist QA previo | Sí, antes de publish |
| OneDrive/Graph | Fuga o mezcla de artefactos | Rutas por `project_key`, ACL por carpeta, escaneo de archivos entrantes | Sí, si hay datos sensibles |
| Canva | Variantes no aprobadas o fuga de marca | Plantillas bloqueadas, campos dinámicos acotados, gate de aprobación | Sí, antes de distribución automática |
| Mautic/Correo | Exposición de PII y abuso de envío | Segmentación mínima, opt-in trazable, límites de campaña y revisión legal | Sí, para envíos críticos |

### Política de skills (subagentes)
- Cada skill debe declarar: propósito, herramientas permitidas, datos permitidos, acciones prohibidas, criterio de parada.
- Ningún skill puede escalar permisos por su cuenta ni invocar herramientas fuera de su lista aprobada.
- Todo skill con acceso a web/documentos externos debe usar salida estructurada y validación previa a tool-call.
- Todo skill debe dejar huella de decisión (`qué pidió`, `qué decidió`, `qué ejecutó`, `evidencia`).

### Estándar mínimo anti prompt injection
- Tratar todo contenido externo como no confiable por defecto.
- No insertar texto no confiable dentro de instrucciones de sistema/desarrollador.
- Separar datos e instrucciones (campos dedicados y tipados).
- Validar salida con esquema estricto antes de ejecutar acciones.
- Aplicar confirmación humana en transmisiones de datos o cambios irreversibles.

### Estándar de observabilidad y auditoría
- Log obligatorio por ejecución: `trace_id`, `project_key`, `intent`, tool-calls, resultado, aprobación, duración, costo.
- Registro de denegaciones y bloqueos de seguridad con motivo explícito.
- Métricas de seguridad: tasa de bloqueo por policy, incidentes por canal, % ejecuciones con HITL, costo anómalo por flujo.
- Retención mínima de evidencias por ciclo de revisión táctica y estratégica.

## 📎 22. FUENTES TÉCNICAS DE SEGURIDAD (MODELOS Y AGENTES)

- OpenAI Safety best practices: https://developers.openai.com/api/docs/guides/safety-best-practices
- OpenAI Safety in building agents: https://platform.openai.com/docs/guides/agent-builder-safety
- OpenAI Prompt injections (research/context): https://openai.com/index/prompt-injections/
- OpenAI Designing agents to resist prompt injection: https://openai.com/index/designing-agents-to-resist-prompt-injection/
- OpenAI GPT-5.5 model docs: https://developers.openai.com/api/docs/models/gpt-5.5
- OpenAI GPT-5.5 guide: https://developers.openai.com/api/docs/guides/latest-model
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1 (GenAI Profile): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Top 10 for LLM Applications 2025: https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- Anthropic Mythos Preview technical note: https://red.anthropic.com/2026/mythos-preview/
- Amazon Bedrock model card (Claude Mythos Preview): https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-mythos-preview.html

---

## Ficha de herramienta: claudeus-wp-mcp
- **Nombre:** claudeus-wp-mcp (v3.0.2)
- **Estado:** Activa
- **Fase:** V1
- **Tipo:** Integración / CMS / MCP
- **Proyecto(s):** jobnearme | core_agency

### Rol oficial
Proporcionar una interfaz de herramientas estandarizada (MCP) para que agentes de IA (Hermes, Antigravity) puedan gestionar WordPress (posts, media, taxonomías, site health, etc.) sin necesidad de escribir código REST manual para cada acción.

### Entradas (input)
- Intenciones agentivas vía tool-call (ej. `list_posts`, `create_post`, `upload_media`).
- Configuración de sitios vía `wp-sites.json`.

### Salidas (output)
- Datos estructurados de la API de WordPress.
- Confirmaciones de creación/edición de contenido.
- Reportes de salud del sitio.

### Trigger principal
Llamada a herramientas desde el orquestador (Antigravity local o Hermes en la nube).

### KPI operativo
- Éxito en la ejecución de tools (auditado vía log de Antigravity).
- Tiempo de respuesta en auditorías de posts.

### Dependencias
- Node.js / npx.
- WordPress REST API (vía Basic Auth / Application Password).
- Archivo `wp-sites.json` configurado.

### Riesgos
- Exposición de credenciales si `wp-sites.json` no se maneja con cuidado.
- Acciones masivas accidentales (mitigado por HITL y modo draft).

### Reglas de operación
- Solo se permite el uso de **Application Passwords**.
- Todo post creado por el agente debe iniciar en estado `draft`.
- Ubicación de configuración local: `C:\Users\AIdev\AppData\Roaming\npm\node_modules\claudeus-wp-mcp\wp-sites.json`.

### Historial de cambios
- **Fecha UTC:** 2026-05-09
- **Cambio:** Instalación y configuración inicial de claudeus-wp-mcp v3.0.2.
- **Impacto:** Habilitación de 145 herramientas de WordPress para el agente. Conexión verificada con `jobnearme.online`.
- **Responsable:** Antigravity

---

## Ficha de herramienta: frankie.service (systemd)
- **Nombre:** frankie.service
- **Estado:** Activa
- **Fase:** V1.5
- **Tipo:** Orquestación / System Service
- **Proyecto(s):** jobnearme | core_agency

### Rol oficial
Mantener el agente Hermes (Frankie) en ejecución persistente y automática en el servidor DigitalOcean. Gestiona el ciclo de vida del proceso, reinicia ante fallos y redirige logs a `journalctl`.

### Reglas de operación
- Binario: `/root/.local/bin/uv`
- Directorio: `/root/hermes-agent`
- Comando: `run hermes-agent`
- Logs: `journalctl -u frankie.service -f`

---

## Ficha de herramienta: NotebookLM MCP
- **Nombre:** notebooklm-mcp
- **Estado:** Activa
- **Fase:** V1.5
- **Tipo:** IA / RAG / Investigación
- **Proyecto(s):** jobnearme | core_agency

### Rol oficial
Permite al agente realizar investigación profunda y basada en fuentes sobre cuadernos de NotebookLM. Facilita el procesamiento de grandes volúmenes de documentos sin saturar el contexto del modelo principal.

### Herramientas principales
- `ask_question`: Preguntas fundamentadas en las fuentes del notebook.
- `add_source`: Ingesta de URLs o texto para expandir la base de conocimiento.
- `generate_audio`: Creación de resúmenes en audio (podcast style).

---

## Ficha de herramienta: Context7 MCP
- **Nombre:** context7-mcp
- **Estado:** Activa
- **Fase:** V1.5
- **Tipo:** IA / Documentación / Desarrollo
- **Proyecto(s):** core_agency

### Rol oficial
Acceso en tiempo real a documentación oficial y actualizada de librerías, frameworks y APIs. Evita alucinaciones sobre sintaxis de código y configuraciones técnicas.

---

## Ficha de herramienta: Notion MCP
- **Nombre:** notion-mcp
- **Estado:** Activa
- **Fase:** V1.5
- **Tipo:** Integración / CRM / Datos
- **Proyecto(s):** jobnearme | personal_os | core_agency

### Rol oficial
Lectura y escritura agentiva en el Córtex de Notion. Permite gestionar bases de datos, páginas y bloques de forma estructurada para seguimiento de proyectos y CRM.