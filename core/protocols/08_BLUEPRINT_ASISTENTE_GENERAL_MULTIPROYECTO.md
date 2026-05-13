# BLUEPRINT OPERATIVO — ASISTENTE GENERAL MULTIPROYECTO

Fuente de referencia documental: `PORTFOLIO_01_JOBNEARME/00_INDICE_DOCUMENTAL.md`
Estado: Activo
Actualización: 2026-04-22

## 1) Objetivo
Diseñar un asistente agéntico multipropósito para operar varios portfolios dentro de este repositorio (`PORTFOLIO_01_*`, `PORTFOLIO_02_*`, etc.), con memoria persistente, control de costos y ejecución omnicanal.

## 2) Principios rectores
1. Separación por proyecto: cada portfolio conserva su contexto, workflows y métricas.
2. Cerebro central + brazos especializados: Frankie orquesta, n8n ejecuta integraciones API, OpenClaw cubre huecos sin API.
3. Memoria operacional primero: decisiones en bitácora + wiki + specs.
4. Iteración corta y verificable: lotes pequeños, E2E validado antes de escalar.
5. Costo bajo control: política explícita por modelo/fase y límites diarios.

## 3) Arquitectura de alto nivel
Canales (Web, Telegram, WhatsApp)
-> n8n (webhook/router de intención)
-> Router de proyecto (Portfolio Resolver)
-> Motor de conocimiento (Wiki/Obsidian + Repo + Bitácora)
-> Ejecución API (WordPress/Graph/OpenRouter/...)
-> Ejecución UI-RPA (OpenClaw)
-> Respuesta / acción / registro

## 4) Diseño por capas
### Capa A — Gobierno y memoria
- `00_CORE_AGENCY/*` = reglas globales, playbooks, skills, políticas.
- `BITACORA_PROYECTO.md` = memoria cronológica oficial.
- `openspec/changes/*` = cambios de arquitectura con método SDD.
- Obsidian Vault (operativo): espejo estructurado de conocimiento para consulta rápida, conectado al repo.

### Capa B — Contexto por portfolio
- `PORTFOLIO_01_JOBNEARME/*`
- `PORTFOLIO_02_*/*`
- Cada portfolio debe tener: objetivos, stack, workflows, KPIs y cola de acciones.

### Capa C — Orquestación
- n8n (DO): trigger, enrutamiento, validación, ejecución, logging.
- OpenClaw (DO): tareas UI determinísticas cuando no exista API.
- OpenRouter: enrutamiento multi-modelo por tipo de tarea.

### Capa D — Publicación y distribución
- WordPress (EC2) para contenido web.
- Canva/Abacus para capa visual.
- Social/push (Telegram/WhatsApp) por conectores n8n.

## 5) Router multiproyecto
`project_key` obligatorio en cada solicitud:
- `jobnearme` -> `PORTFOLIO_01_JOBNEARME`
- `p02_xxx` -> `PORTFOLIO_02_XXX`
- fallback: `core_agency` para tareas transversales.

Campos mínimos del sobre de ejecución:
```json
{
  "project_key": "jobnearme",
  "intent": "publish_content|research|automation|qa|ops",
  "priority": "low|medium|high",
  "source_channel": "web|telegram|whatsapp|manual",
  "payload": {}
}
```

## 6) Obsidian + AI como memoria
Enfoque inicial:
- Empezar con LLM Wiki + archivos markdown.
- Repo GitHub = fuente versionada.
- Obsidian = IDE de conocimiento.
- Exportes relevantes se consolidan en `.md` dentro del repo.

Estructura sugerida del vault:
- `/00_inbox`
- `/10_projects/jobnearme`
- `/10_projects/p02_xxx`
- `/20_decisions`
- `/30_playbooks`
- `/40_sources`
- `/50_syntheses`

## 7) Móvil
### Telegram (fase inmediata)
- n8n Webhook -> validar usuario/comando -> resolver `project_key` -> ejecutar acción -> responder.
- Comandos iniciales:
  - `/status <project_key>`
  - `/next <project_key>`
  - `/publish_check <project_key>`
  - `/log <project_key> <texto>`

### WhatsApp (fase 2)
- Integrar vía proveedor (Cloud API/Twilio/360dialog).
- Mismo contrato que Telegram para no duplicar lógica.

## 08. BLUEPRINT: ASISTENTE GENERAL MULTIPROYECTO (FRANKIE)

## 1. Visión General
**Frankie** no es solo un bot; es la capa de orquestación entre la vida personal y profesional del director. Su objetivo es centralizar la captura, procesamiento y ejecución de tareas a través de múltiples dominios, garantizando que el director pueda operar la agencia y sus asuntos personales desde cualquier lugar con un comando único.

---

## 2. Metodología Operativa: GTD + Zettelkasten + PARA
Frankie opera bajo el sistema de **Gestión de Atención y Conocimiento (GDT/GTD)**:

1.  **CAPTURAR (Inbox)**: Entrada omnicanal (Telegram, Audio, Texto, Terminal). Nada se queda en la cabeza.
2.  **ACLARAR**: Frankie clasifica el input. ¿Es una tarea? ¿Es conocimiento (Zettel)? ¿Es un evento?
3.  **ORGANIZAR (PARA)**:
    -   **P**royectos: Esfuerzos con fecha límite (ej. Lanzamiento Funnel X).
    -   **Á**reas: Responsabilidades permanentes (ej. Finanzas, Salud).
    -   **R**ecursos: Intereses y Bibliografía (Zettelkasten).
    -   **A**rchivo: Cosas completadas o inactivas.
4.  **REFLEXIONAR**: Revisiones semanales de bitácora y estados de proyectos.
5.  **EJECUTAR**: Acción quirúrgica basada en el contexto (PC o Móvil).

---

## 3. Arquitectura de Dominios (Project Keys)

| Project Key | Dominio | Alcance |
| :--- | :--- | :--- |
| `jobnearme` | **Negocio / Agencia** | Operación de portales de empleo, SEO, WordPress, n8n. |
| `field_service` | **Servicios Industriales** | Frankie Field-Service: Clientes, Maquinaria, Pipeline técnico. |
| `personal_os` | **Vida Personal** | Agenda, Salud, Finanzas hogar, Compras. |
| `lab` | **I+D / IA** | Experimentos, prompts nuevos, pruebas de herramientas. |
| `estudio` | **Formación** | Cursos, Bibliografía, Zettelkasten (Obsidian). |

---

## 4. El Contrato de Comando Único
Toda interacción con Frankie debe seguir este esquema para evitar ambigüedad:

```yaml
project_key: [key_del_dominio]
intent: [tarea | nota | alerta | status]
priority: [1-5]
payload:
  content: "Descripción de la acción o información"
  metadata: { tag: "importante", due: "2026-05-12" }
```

---

## 5. Hub Operativo: Frankie Field-Service (Módulo Especializado)
Este módulo gestiona la vertical de servicios técnicos e industriales.
- **Entidades**: Clientes (CRM), Maquinaria (Activos), Pipeline (Flujo de Servicio), Métricas (Margen).
- **Integración**: Cada intervención en el Pipeline puede disparar una **Tarea** en el sistema global y registrar un **Zettel** técnico sobre la máquina.

---

## 6. Protocolo de Handover (PC <-> Cloud)
Frankie existe en dos estados que se comunican entre sí:

-   **Frankie Cloud (Always-On)**:
    -   Escucha en Telegram/Webhooks.
    -   Procesa audios y capturas rápidas.
    -   Mantiene el **Dashboard de Notion** actualizado.
-   **Frankie PC (Local - Antigravity)**:
    -   Ejecuta tareas complejas de código, git y manejo de archivos.
    -   Se activa cuando el director está en su puesto de trabajo.
    -   Consume la "Bandeja de Entrada" procesada por Cloud.

---

## 7. Flujo de Estados de Ejecución
1.  **DRAFT**: Idea capturada en Inbox.
2.  **READY**: Clasificada y con recursos asignados.
3.  **DOING**: En ejecución (PC o Automation).
4.  **DONE**: Verificada y archivada.
5.  **LOGGED**: Registrada en `BITACORA_PROYECTO.md`.

---

## 8. Reglas de Oro (Constraints)
- **Privacidad Estricta**: Los datos de `personal_os` nunca se cruzan con `jobnearme` sin permiso explícito.
- **Traceabilidad Total**: Todo lo que Frankie ejecuta debe dejar rastro en la Bitácora.
- **No Alucinaciones**: Si Frankie no entiende el `intent`, debe preguntar antes de escribir en Notion o WordPress.
- **Clientes Primero**: En `field_service`, el foco es el cliente y la rentabilidad del servicio.

---

## 9. Glosario Operativo
- **Clientes**: Antiguos "Participantes". Personas o empresas que reciben servicios.
- **Zettel**: Nota atómica de conocimiento vinculada a una fuente o activo.
- **Harness**: Arnés de validación que rodea cada automatización para evitar errores.
  "priority": "low|medium|high",
  "approval_mode": "required|auto",
  "source_channel": "telegram|whatsapp|web|manual",
  "payload": {}

### Política de fronteras de contexto
- `jobnearme`: operación de negocio y publicación con trazabilidad estricta.
- `personal_os`: agenda, recordatorios, pendientes, compras y estudio.
- `lab`: experimentación técnica sin impacto productivo.
- Si no existe `project_key`, el sistema debe pedir contexto antes de ejecutar.

### Estado operativo de ejecución
`DRAFT -> READY_FOR_APPROVAL -> APPROVED -> EXECUTED -> LOGGED`

### Regla de aprobación
- En `jobnearme`, `approval_mode` por defecto es `required` para publicar o ejecutar acciones críticas.
- En `personal_os`, se permite `auto` solo para recordatorios y tareas no destructivas.
- Ningún flujo debe cruzar información entre `jobnearme` y `personal_os` sin instrucción explícita del director.