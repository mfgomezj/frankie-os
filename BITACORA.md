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
