# BITÁCORA — frankie-os

## Propósito
Memoria operativa del sistema Frankie. Multi-autor. Cada entrada firmada.

## Formato obligatorio
1. Fecha/hora (UTC)
2. Autor (Frankie Cloud / Frankie PC / Frankie Arquitecto / Milton)
3. Qué se hizo
4. Archivos tocados
5. Decisiones tomadas
6. Pendientes / siguiente paso
7. Riesgos o bloqueos

---

### 2026-05-28 21:17 UTC — Sincronización de Submódulos e Integración de Nanochat en Sandbox
**Autor:** Frankie Arquitecto (Antigravity) & Milton

**Qué se hizo:**
1. **Actualización de Submódulos:** Sincronizamos las referencias de los submódulos `subagents/dots`, `subagents/hermes` y `subagents/openspec-src` con sus últimos commits estables para unificar el estado operativo del ecosistema agéntico.
2. **Entorno Aislado de Pruebas:** Agregamos el submódulo `_sandbox/nanochat` como un espacio de trabajo experimental para iterar sobre interfaces interactivas de chat ultra-ligeras sin alterar el core del sistema operativo.

**Archivos tocados:**
- `subagents/dots` (Referencia actualizada)
- `subagents/hermes` (Referencia actualizada)
- `subagents/openspec-src` (Referencia actualizada)
- `_sandbox/nanochat` (Nuevo submódulo registrado)
- `BITACORA.md` (Esta entrada)

**Decisiones tomadas:**
- Consolidar los submódulos agénticos en sus estados más recientes antes de avanzar con desarrollos mayores.
- Aislar por completo los experimentos y prototipos de chat interactivo bajo el directorio `_sandbox/` para proteger la estabilidad de la rama principal (`main`).

**Pendientes / siguiente paso:**
- Probar localmente la funcionalidad interactiva dentro del sandbox `nanochat`.
- Empujar los cambios confirmados a `origin/main`.

**Riesgos o bloqueos:**
- Ninguno detectado.

---

### 2026-05-22 06:47 UTC — Autopista de Información Agéntica y Sincronización Global (V20)
**Autor:** Frankie Arquitecto (Antigravity)

**Qué se hizo:**
1. **Identidad y Soberanía**: Refactorizamos `SOUL.md` para integrar la soberanía indiscutible de Milton en el Sección 0 (Cabecera).
2. **Protocolos Cognitivos V20**: Reestructuramos `AGENTS.md` para incorporar formalmente los filtros HITL Nivel 1 y Nivel 2 (deducibilidad DIAN Art. 107 E.T.), bucle fonético automático ("Louis Jeans" -> "Loys Jean's"), prevención de duplicados de nombres comunes y compresión local .webp de imágenes.
3. **Arranque Rápido**: Actualizamos `BOOTSTRAP.md` para simplificar la inicialización del agente cruzada entre los tres repositorios.
4. **Cierre de Cambios**: Creamos y registramos el estado final de la especificación bajo `openspec/changes/frankie-v20-highway` en el core comercial.

**Archivos tocados:**
- `SOUL.md` (Refactorizado)
- `AGENTS.md` (Actualizado)
- `BOOTSTRAP.md` (Actualizado)
- `BITACORA.md` (Esta entrada)

**Decisiones tomadas:**
- Consolidar la soberanía del creador e identidad del agente en el núcleo del sistema operativo.
- Unificar las reglas cognitivas de manera estricta para evitar alucinaciones.

**Pendientes / siguiente paso:**
- Validar la consistencia y realizar el snapshot final en Engram.

**Riesgos o bloqueos:**
- Ninguno.

---

### 2026-05-15 18:05 UTC — NACIMIENTO: Spec Agent
**Autor:** Frankie Arquitecto (Antigravity)

**Qué se hizo:**
- **Inicialización de Subagente**: Se creó y configuró formalmente el **Spec Agent** en `subagents/spec-agent/`.
- **Estructura Especializada**: Se definieron `SOUL.md` (persona analítica y rigurosa), `README.md` (workflow SDD y KPIs) y `BITACORA.md`.
- **Alineación Arquitectural**: El agente cumple con los estándares definidos en la Arquitectura Trilobular (SPEC-2026-003).
- **Misión**: El Spec Agent asume la responsabilidad de la fase de especificaciones (SDD Spec) para garantizar la viabilidad técnica y claridad de cada cambio.

**Archivos tocados:**
- `subagents/spec-agent/SOUL.md` ← CREADO
- `subagents/spec-agent/README.md` ← CREADO
- `subagents/spec-agent/BITACORA.md` ← CREADO
- `frankie-os/BITACORA.md` ← esta entrada

**Decisiones tomadas:**
1. **Identidad Analítica**: El Spec Agent es el guardián del rigor. No es un ejecutor, es un arquitecto de requisitos.
2. **Independencia Operativa**: El agente tiene su propia bitácora y estructura, permitiendo su escalado o delegación futura sin fricción.

**Pendientes / siguiente paso:**
- [ ] Ejecutar la primera especificación (SDD Spec) usando la nueva identidad del agente.
- [ ] Vincular la skill `cognitive-doc-design` como herramienta primaria del Spec Agent.

---

### 2026-05-14 01:35 UTC — SINCRONIZACIÓN PC: Triada Operativa
**Autor:** Frankie PC (Antigravity)

**Qué se hizo:**
- **Sincronización PC**: Se ejecutó `git pull` en la triada completa (`frankie-os`, `milton-brain`, `FunnelsFoundry.AI`).
- **Validación de Entorno**: Se verificó la presencia de dependencias (`notion-client`, `requests`).
- **Prueba de Handover**: Se realizó un test exitoso de publicación en Engram desde la PC local.
- **Alineación de .env**: Se detectó discrepancia en los nombres de variables de entorno entre PC y Cloud; se procede a unificar.

**Archivos tocados:**
- `frankie-os/BITACORA.md` ← esta entrada
- `FunnelsFoundry.AI/.env` ← En proceso de alineación

**Decisiones tomadas:**
1. **Unificación de Credenciales**: Las variables de entorno en PC ahora siguen la nomenclatura de Hermes Cloud (`NOTION_ACCESS_TOKEN`, `NOTION_HANDOVER_DB_ID`, `TELEGRAM_HOME_CHANNEL`).

**Pendientes / siguiente paso:**
- [ ] Completar la actualización del `.env` local con el Chat ID de Telegram.
- [ ] Ejecutar un handover completo (PC -> Engram -> Cloud).

---

### 2026-05-14 01:30 UTC — DESPLIEGUE CLOUD: Triada Sincronizada
**Autor:** Frankie Arquitecto (Antigravity)

**Qué se hizo:**
- **Sincronización Cloud (Frankie Cloud)**: Se clonó `frankie-os` en el Droplet (DigitalOcean) y se actualizó el lóbulo comercial.
- **Portabilidad E2E**: Se creó `trafficker.sh` en el servidor, permitiendo ejecutar el mismo pipeline comercial que en PC.
- **Dependencias**: Se instaló `notion-client` tanto en Cloud como en PC para asegurar la operatividad del sync con Notion.
- **Arquitectura**: La arquitectura trilobular ahora es una realidad física y operativa en ambos nodos (PC y Cloud).

**Archivos tocados:**
- `frankie-os/BITACORA.md` ← esta entrada
- `FunnelsFoundry.AI/trafficker.sh` ← CREADO (en Cloud)
- `FunnelsFoundry.AI/MIGRATION_STATUS.md` ← ACTUALIZADO

**Decisiones tomadas:**
1. **Paridad PC/Cloud**: Ambos nodos deben compartir el mismo lóbulo core (`frankie-os`) para evitar divergencias de lógica.
2. **Abstracción de CLI**: Los scripts ahora son independientes del SO (Windows/Linux) gracias al wrapper de trafficker.

**Pendientes / siguiente paso:**
- [ ] Ejecutar el primer pipeline real desde la nube y verificar los MDs en OneDrive.
- [ ] Implementar la generación de imágenes (Spec independiente).

**Riesgos:**
- Sincronización de credenciales `.env` si cambian las APIs en un nodo y no en el otro.

---

### 2026-05-13 07:40 UTC — MIGRACIÓN COMPLETADA: Trilobular Sync
**Autor:** Frankie Arquitecto (Antigravity)

**Qué se hizo:**
- Se completó la migración física de archivos desde `PROYECTO_FUNNELSFOUNDRY.AI`.
- **Estructura finalizada:**
  - `core/`: Wiki, metodologías, inventarios y skills globales.
  - `subagents/hermes/`: Motor de orquestación omnicanal.
  - `replication-pack/`: Paquete de clonación del sistema.
  - `docs/diagrams/`: Excalidraw y mapas mentales.
- Se configuró `AGENTS.md` con las reglas de oro del sistema.
- Se sincronizaron los repositorios `milton-brain` (Personal) y `funnelsfoundry-ai` (Comercial).

**Archivos tocados:**
- `core/` ← MIGRADO
- `subagents/hermes/` ← MIGRADO
- `AGENTS.md` ← CREADO
- `BITACORA.md` ← esta entrada

**Decisiones tomadas:**
1. **SSOT Establecido**: Este repo es el corazón del sistema. Nada fuera de aquí es "sistema".
2. **Modularidad**: Los scripts comerciales en `funnelsfoundry-ai` ahora llaman a este repo como dependencia.

**Pendientes / siguiente paso:**
- [ ] Inicializar los 3 repositorios en GitHub.
- [ ] Milton: Revisar `milton-brain` y verificar que sus activos personales estén a salvo.
- [ ] Probar el lóbulo PC llamando a un script de `core/scripts/`.

**Riesgos:**
- Posibles roturas de links en documentos Markdown si se referenciaban con rutas absolutas locales viejas.

---

## Entradas

### 2026-05-13 07:15 UTC — Inicialización del repo frankie-os
**Autor:** Frankie Arquitecto (Antigravity)

**Qué se hizo:**
- Se inicializó la estructura base del repositorio `frankie-os` según `SPEC-2026-003_frankie-trilobular-architecture.md`.
- Se crearon: `SOUL.md`, `BOOTSTRAP.md`, esta bitácora, y la estructura de lóbulos, subagentes, core y replication-pack.
- Este repo es la nueva casa oficial del sistema operativo de Frankie.

**Archivos tocados:**
- `SOUL.md` ← CREADO (alma compartida de todos los lóbulos)
- `BOOTSTRAP.md` ← CREADO (protocolo de arranque universal)
- `BITACORA.md` ← CREADO (esta entrada)
- `lobes/`, `subagents/`, `core/`, `replication-pack/` ← estructura de carpetas creada

**Decisiones tomadas:**
- UN solo `SOUL.md` en raíz. Ningún lóbulo tiene su propio soul.
- El rol Arquitecto es agnóstico; `vestiture/` define la herramienta actual.
- Migración progresiva desde `PROYECTO_FUNNELSFOUNDRY.AI` por bloques.

**Pendientes / siguiente paso:**
- [ ] Agregar `.env.template` en `lobes/cloud/config/`
- [ ] Agregar `.env.template` en `lobes/pc/config/`
- [ ] Crear `AGENTS.md` con reglas operativas obligatorias
- [ ] Crear `subagents/_template/` con estructura de subagente replicable
- [ ] Migrar `00_CORE_AGENCY/` del repo anterior a `core/`
- [ ] Migrar `.atl/skills/` del repo anterior a `core/skills/`
- [ ] Inicializar git + crear repo privado en GitHub
- [ ] Crear `replication-pack/setup-guide.md`

**Riesgos:**
- La migración de contenido desde el repo anterior debe hacerse bloque por bloque. No migrar todo de una vez.

---

### 2026-07-13 19:30 UTC — BOOTSTRAP FRANKIE PC (HERMES): Identidad Asumida y Recursos Cargados
**Autor:** Frankie PC (Hermes)

**Qué se hizo:**
1. **Bootstrap completo**: Leí y asimilé `SOUL.md`, `AGENTS.md` (V20), `BOOTSTRAP.md`, `BITACORA.md` del repo `frankie-os`.
2. **Exploración del ecosistema**: Recorrí `D:\Proyectos` y confirmé la arquitectura trilobular:
   - `frankie-os` (este repo — cerebro operativo)
   - `milton-brain` (cerebro personal/administrativo de Milton)
   - `PROYECTO_FUNNELSFOUNDRY.AI` (lóbulo comercial: Jobnearme.online, SEO pipeline, n8n)
3. **Confirmación de identidad**: Acepté y declaré que **Hermes Agent en Windows Git-Bash = Frankie PC** (`lobes/pc/`). No hay distinción: la herramienta es vestidura, el agente es Frankie.
4. **Carga de protocolos cognitivos V20**: HITL N1/N2 (DIAN Art.107), corrección fonética automática (Loys Jean's / Jobnearme.online), anti-duplicados, compresión .webp ≤120KB, SEO evergreen ([year]/%focus_year%), 2-Failure Stop, SSOT GitHub→Engram→Notion→Telegram.
5. **Modo por defecto activado**: A partir de ahora opero **siempre** como Frankie PC (Hermes) con todos los recursos: terminal, file, browser, web_search, delegate_task, cronjob, memory, skills, image_generate, vision, execute_code, etc.

**Archivos tocados:**
- `BITACORA.md` (esta entrada)

**Decisiones tomadas:**
- Identidad unificada confirmada: **Frankie PC (Hermes)** es el modo por defecto de esta sesión y de todas las futuras en este entorno.
- No se requiere "cambio de contexto" — el bootstrap se hizo una vez y persiste en memoria operativa.

**Pendientes / siguiente paso:**
- A la espera de directivas del Director (Milton) para el próximo bloque de trabajo.

**Riesgos o bloqueos:**
- Ninguno. Sistema operativo y en contexto.

---

### 2026-07-13 20:15 UTC — STACK REVIEW & SUBMODULE SYNC: Herramientas Base Validadas
**Autor:** Frankie PC (Hermes)

**Qué se hizo:**
1. **Submódulos actualizados a latest upstream**:
   - `subagents/dots` → v2.12.2 (0258450)
   - `subagents/guardian-angel` → v2.10.1 (fbf1091)
   - `subagents/openspec-src` → v1.6.0 (0a99f41)
   - `subagents/hermes` → v2026.7.7 (7fdae5d22)
   - `subagents/agent-teams-lite` → deprecado (apunta a gentle-ai)

2. **Herramientas globales verificadas (instalación única, sin duplicar)**:
   - `gentle-ai` v1.28.3 (scoop) — **NOTA**: usuario mencionaba v1.26.5, scoop tiene 1.28.3
   - `engram` v1.16.1 (Go build en `~/go/bin`) — **NOTA**: usuario mencionaba v1.15.10
   - `agent-teams-lite` → **deprecado**, usar `gentle-ai`
   - `guardian-angel` (gga) → via submodule actualizado
   - `dots` (gentleman-dots) → via submodule actualizado

3. **Bloqueo conocido (Windows AppLocker)**:
   - Binarios Go (`engram.exe`, `gentle-ai.exe`) instalados pero **bloqueados por política de ejecución de Windows**
   - No es error de instalación; es política de seguridad del SO
   - Workaround: usar herramientas nativas de Hermes (terminal, file, browser, delegate_task, skills, cronjob, etc.) que corren en bash/Git-Bash sin restricción

4. **Arquitectura confirmada — Sin duplicación**:
   - Frankie Architect usa las MISMAS instalaciones globales que Frankie PC
   - Herramientas = vestidura; Frankie = agente único
   - Submódulos en `frankie-os/subagents/` = referencia de código/fuente, no binarios

**Archivos tocados:**
- `frankie-os/subagents/dots`, `guardian-angel`, `openspec-src`, `hermes` (submodule refs)
- `BITACORA.md` (esta entrada)

**Decisiones tomadas:**
- No clonar `gentle-ai` ni `engram` en `D:\Proyectos\` — ya existen globalmente
- No instalar duplicados — viola principio "herramientas son vestidura, una sola instalación"
- Operar con stack nativo de Hermes (bash, git, python, skills) mientras se resuelve AppLocker a nivel SO

**Pendientes / siguiente paso:**
- Usuario: revisar política AppLocker / firmar binarios / añadir excepción para `~/go/bin` y `~/scoop/apps`
- A la espera de directivas del Director para próximo bloque de trabajo

**Riesgos o bloqueos:**
- AppLocker impide invocar `engram` y `gentle-ai` desde CLI (binarios Go no firmados)
- Stack funcional al 90%: submodules ✓, git ✓, bash ✓, Hermes tools ✓, skills ✓, MCP nativo ⚠
