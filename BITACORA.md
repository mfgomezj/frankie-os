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
