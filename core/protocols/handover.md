# Protocolo de Handover y Snapshot Automático

## 1. Propósito
Garantizar la continuidad de la conciencia operativa entre diferentes instancias de Frankie (Cloud, PC, Arquitecto) y sesiones de trabajo, eliminando la dependencia de la memoria volátil o la intervención humana para el traspaso de contexto.

## 2. Definición de Snapshot
Un snapshot es una entrada estructurada en **Engram** que captura el estado exacto del trabajo en un momento dado.

### Contenido Obligatorio:
- **Change ID**: El identificador de la tarea/cambio en curso (ej: `frankie-trilobular`).
- **Phase**: Fase actual de SDD (Explore, Propose, Spec, Design, Tasks, Apply, Verify).
- **Progress**: Lista de tareas completadas y pendientes en el bloque actual.
- **Context Bits**: Descubrimientos críticos, errores encontrados o decisiones tomadas en la sesión.
- **Next Action**: La instrucción exacta para el siguiente agente que retome el hilo.

## 3. Disparadores (Triggers) Automáticos
Todo agente operando bajo el protocolo `AGENTS.md` DEBE realizar un `mem_save` en los siguientes eventos:

1. **Cierre de Fase SDD**: Al finalizar la redacción de una spec, diseño o checklist de tareas.
2. **Hito Técnico**: Al completar la migración de un bloque de archivos o una refactorización exitosa.
3. **Cierre de Sesión**: Antes de despedirse del usuario o entrar en estado de reposo.
4. **Error de Bloqueo**: Si el agente se detiene por la "Regla de 2 Fallos", debe dejar un snapshot detallado del problema.

## 4. Implementación en Engram
Se utilizará la siguiente convención de `topic_key`:

- **General**: `sdd/{change-name}/state`
- **Progreso**: `sdd/{change-name}/apply-progress`

### Ejemplo de Snapshot:
```json
{
  "title": "Snapshot: frankie-trilobular - Phase: Spec",
  "topic_key": "sdd/frankie-trilobular/state",
  "content": "**What**: Specs actualizadas con Ley de Propiedad de Milton\n**Why**: Asegurar soberanía de IP antes de migración\n**Where**: openspec/changes/frankie-trilobular/specs/spec.md\n**Next**: Implementar protocolos de seguridad y handover en frankie-os"
}
```

## 5. Recuperación (The Handover)
Al iniciar una nueva sesión, el agente debe:
1. Consultar `mem_search(query: "sdd/{change-name}/state")`.
2. Leer el último snapshot con `mem_get_observation`.
3. Validar el estado contra el filesystem.
4. Continuar desde el punto exacto de la última "Next Action".

---
*Este protocolo es la garantía de que Frankie nunca olvida. Es así de fácil.*
