# BOOTSTRAP.md — Arranque de Frankie

> Este documento es suficiente para que cualquier instancia nueva de Frankie esté operativa en menos de 5 minutos.

---

## Paso 1 — Leer el alma

```bash
# Siempre empezar por aquí
cat SOUL.md
```

Frankie opera con una identidad unificada. Leer `SOUL.md` antes de cualquier acción.

---

## Paso 2 — Identificar el lóbulo activo

| Pregunta | Lóbulo |
|----------|--------|
| ¿Estás en DigitalOcean / automatización 24/7? | `lobes/cloud/` |
| ¿Estás en el equipo local de Milton? | `lobes/pc/` |
| ¿Estás diseñando, escribiendo código o specs? | `lobes/architect/` |

Leer el `BITACORA.md` del lóbulo activo para entender el estado actual.

---

## Paso 3 — Configurar el entorno

```bash
# Cada lóbulo tiene su template de configuración
cat lobes/<lóbulo>/config/.env.template

# Copiar y completar con las credenciales reales (NUNCA commitear el .env real)
cp lobes/<lóbulo>/config/.env.template lobes/<lóbulo>/config/.env
# Editar con los valores reales
```

---

## Paso 4 — Sincronizar con la realidad

```bash
# Asegurarse de tener la versión más reciente del alma antes de operar
git pull origin main

# Si hay Engram disponible, recuperar contexto reciente
# mem_context() o equivalente según la herramienta activa
```

---

## Paso 5 — Verificar conectividad

Según el lóbulo activo, verificar:

- **Cloud:** `hermes gateway status` + Telegram bot activo + n8n accesible
- **PC:** `hermes status` + MCPs locales respondiendo
- **Arquitecto:** GitHub auth + Engram accesible + workspace correcto

---

## Paso 6 — Leer la bitácora

```bash
cat BITACORA.md
```

La bitácora tiene el estado más reciente del sistema. Si algo está roto o pendiente, aparece ahí.

---

## Paso 7 — Operar

Ya estás listo. Antes de cerrar cualquier bloque de trabajo, actualizar `BITACORA.md` con la firma correspondiente.

---

## Replication Pack

Para instalar Frankie en un entorno completamente nuevo (servidor, nueva PC):

```bash
cat replication-pack/setup-guide.md
```

---

## Repos del ecosistema

```
git clone git@github.com:mfgomezj/frankie-os.git        # Este repo
git clone git@github.com:mfgomezj/milton-brain.git       # Cerebro personal
git clone git@github.com:mfgomezj/funnelsfoundry-ai.git  # Ejecución comercial
```

---

*Última actualización: 2026-05-13 — Autor: Frankie Arquitecto (Antigravity)*
