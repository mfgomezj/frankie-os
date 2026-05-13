# Handover Skill 🤝

Protocolo de sincronización de estado entre sesiones de IA (Local <-> Cloud).

## Contexto
Este proyecto utiliza un modelo híbrido:
- **Antigravity (PC Local)**: Desarrollo intensivo, refactorización y ejecución local.
- **Hermes (DigitalOcean Cloud)**: Automatización, Trafficker y publicación 24/7.

Para evitar desincronización, cada cambio relevante debe ser "entregado" mediante este protocolo.

## Reglas de Oro
1. **Nunca cerrar sesión sin snapshot**: Si hiciste cambios en `openspec` o en la bitácora, debés correr el handover.
2. **Engram es la Verdad**: El topic `comm/handover` en Engram es el puente oficial.
3. **Validación Humana**: El handover requiere aprobación (vía Frankie/Telegram) antes de considerarse exitoso.

## Cómo ejecutar el Handover

### 1. Preparar el Snapshot
Usa el script `GLOBAL_SCRIPTS/handover_manager.py` para generar el mensaje de entrega.

### 2. Publicar en Engram
Asegurate de incluir:
- **Change**: El nombre del cambio SDD actual.
- **Phase**: En qué fase te quedaste.
- **Context**: Tareas completadas y qué sigue.

### 3. Registro en Notion
El script registrará automáticamente el evento en la base de datos **Handover Logs 🤝**.

## Flujo de Trabajo
1. Finalizar lote de trabajo.
2. Ejecutar `python GLOBAL_SCRIPTS/handover_manager.py`.
3. Notificar al usuario que el estado está "en el aire" esperando a Hermes.
4. Esperar confirmación de que Hermes recibió la posta.

## Anti-patrones
- Hacer handover sin haber actualizado la `BITACORA_PROYECTO.md`.
- No mencionar bloqueos o riesgos en el snapshot.
- Asumir que el otro agente "ya sabe" qué hacer sin leer el snapshot.
