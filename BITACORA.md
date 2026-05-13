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
