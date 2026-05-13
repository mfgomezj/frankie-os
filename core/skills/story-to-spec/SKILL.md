---
name: story-to-spec
description: >
  Generates a specification from a user story, listing non-technical assumptions, and interactively refining rejected assumptions one by one with a progress bar and multiple-choice options.
  Trigger: Cuando el usuario diga "vamos a definir una spec", "crear spec desde historia", "story to spec", o entregue una historia de usuario para rellenar espacios en blanco.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Cuando el usuario entrega una historia de usuario de alto nivel y requiere una especificación detallada.
- Cuando hay ambigüedad y el agente necesita asumir variables funcionales o de negocio, pero debe validarlas con el usuario.
- Cuando se requiere un proceso interactivo de preguntas y respuestas para refinar requerimientos.

## Critical Patterns

### Fase 1: Generación de la Spec Inicial y Asunciones
1. Lee la historia de usuario entregada.
2. Genera una propuesta de especificación preliminar, llenando los espacios en blanco con lógica de negocio y sentido común.
3. **OBLIGATORIO**: Debajo de la especificación, crea un listado numerado con TODAS las asunciones no técnicas o funcionales que tomaste (ej: "1. Asumí que...", "2. Asumí que...").
4. Pídele al usuario que te indique los números de las asunciones que **no** le gustaron o con las que no está de acuerdo.
5. **DETENTE** y espera la respuesta del usuario.

### Fase 2: Refinamiento Interactivo (Paso a Paso)
1. Cuando el usuario indique los números rechazados, debes hacer preguntas para corregirlas **UNA POR UNA**. ¡No hagas todas las preguntas juntas!
2. En cada pregunta, muestra una **Barra de Progreso** visual e indicadora (ej: `[Pregunta 1 de 3] ▓░░░░`).
3. Para la asunción que estás consultando, propón 4 alternativas lógicas y distintas.
4. Siempre añade una **5ta opción** exactamente como: `"5. Otra (por favor especifica)"`.
5. **DETENTE** y espera a que el usuario responda la pregunta actual antes de avanzar a la siguiente asunción rechazada.

### Fase 3: Cierre
1. Una vez que el usuario haya respondido a la última pregunta del ciclo, **no generes la spec de inmediato**.
2. Dile explícitamente: "Ya me encuentro listo para crear la especificación final."
3. Espera la confirmación del usuario para proceder.

## Code Examples

**IA (Fase 1):**
Aquí está la especificación basada en tu historia...
Mis asunciones funcionales fueron:
1. El registro requiere validación por email.
2. El dashboard principal muestra métricas de 30 días.
¿Qué números de estas asunciones no te gustan?

**Usuario:**
La 2.

**IA (Fase 2):**
Perfecto, vamos a refinar esa asunción.

**[Pregunta 1 de 1]** ▓▓▓▓▓▓▓▓▓▓
Sobre las métricas del dashboard principal:
1. Mostrar métricas de los últimos 7 días.
2. Mostrar métricas desde el inicio del mes actual (MTD).
3. Mostrar un selector de fechas personalizado sin métrica por defecto.
4. Ocultar métricas y mostrar solo acciones rápidas.
5. Otra (por favor especifica).

¿Cuál opción prefieres?

## Commands

No se requieren comandos bash. Este es un flujo conversacional y analítico.

## Resources
- No requiere templates externos. Sigue estrictamente la estructura interactiva de preguntas.
