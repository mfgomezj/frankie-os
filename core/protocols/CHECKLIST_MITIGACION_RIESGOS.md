# CHECKLIST DE MITIGACIÓN DE RIESGOS — JobNearMe

**Fuente:** `BITACORA_PROYECTO.md`  
**Versión:** 1.0  
**Fecha:** 2026-04-29  
**Propósito:** Seguimiento progresivo de mitigación de riesgos por fase de escalado

---

## Cómo usar este checklist

- [ ] Marcar con `[x]` cuando esté completado
- [ ] Registrar fecha de cierre en cada item
- [ ] Actualizar este documento al cerrar cada fase
- [ ] Referenciar evidencia en `BITACORA_PROYECTO.md`

---

## 🔸 FASE 0: Estabilización (0-50 páginas)

### F0.1 — Logging básico
- [x] **F0.1.1** Crear workflow n8n con nodos de logging (timestamp, user, action, result) — *2026-04-29*
- [ ] **F0.1.2** Definir formato de log estructurado (JSON)
- [ ] **F0.1.3** Configurar retención de logs (mínimo 30 días)
- [ ] **F0.1.4** Probar logging en entorno lab

### F0.2 — Higiene de contenido
- [ ] **F0.2.1** Auditar todas las URLs publicadas en busca de placeholders
- [ ] **F0.2.2** Eliminar todo contenido placeholder de producción
- [ ] **F0.2.3** Corregir slugs erróneos (incluye Illinois)
- [ ] **F0.2.4** Consolidar URLs duplicadas con canonical + 301

### F0.3 — Validación inicial
- [ ] **F0.3.1** Ejecutar Screaming Frog para detectar duplicados
- [ ] **F0.3.2** Verificar 0 duplicados indexables
- [ ] **F0.3.3** Validar consistencia de metadatos en todas las páginas

**Gate F0 — Cierre de fase:** 
- [ ] Logging activo y probando
- [ ] 0 placeholders activos
- [ ] 0 duplicados indexables
- [ ] Fecha de cierre: ________

---

## 🔸 Fase 1: Control Básico (50-200 páginas)

### F1.1 — Sanitización de input
- [ ] **F1.1.1** Crear node n8n de sanitización de input externo
- [ ] **F1.1.2** Implementar validación de caracteres especiales y scripts
- [ ] **F1.1.3** Configurar rechazo automático de input sospechoso
- [ ] **F1.1.4** Documentar política de sanitización en wiki

### F1.2 — SLO/SLA/SLI
- [ ] **F1.2.1** Definir umbrales numéricos:
  - Uptime: 99.5%
  - Tiempo de publicación: <5 min
  - Error rate: <2%
- [ ] **F1.2.2** Implementar monitoreo de uptime
- [ ] **F1.2.3** Crear alerta automática al superar threshold
- [ ] **F1.2.4** Documentar SLOs en dashboard

### F1.3 — Router n8n validado
- [ ] **F1.3.1** Implementar validación obligatoria de project_key
- [ ] **F1.3.2** Implementar validación de intent por contexto
- [ ] **F1.3.3** Crear rechazo automático si project_key inválido
- [ ] **F1.3.4** Probar flujo de rechazo en lab

**Gate F1 — Cierre de fase:**
- [ ] Sanitización activa en producción
- [ ] SLOs documentados y monitoreados
- [ ] Router validado con rechazo automático
- [ ] Fecha de cierre: ________

---

## 🔸 Fase 2: Automatización (200-500 páginas)

### F2.1 — Versionamiento de plantillas
- [ ] **F2.1.1** Crear biblioteca de plantillas de copy por canal
- [ ] **F2.1.2** Implementar versionado (v1, v2, v3...)
- [ ] **F2.1.3** Crear checklist automático de gate de calidad
- [ ] **F2.1.4** Documentar política de actualización de plantillas

### F2.2 — Métricas de baseline
- [ ] **F2.2.1** Implementar métricas: tiempo por workflow
- [ ] **F2.2.2** Implementar métricas: costo por pieza
- [ ] **F2.2.3** Implementar métricas: calidad (tasa de error post-publicación)
- [ ] **F2.2.4** Generar reporte semanal automático

### F2.3 — Anti-duplicación
- [ ] **F2.3.1** Implementar gate anti-duplicado en n8n
- [ ] **F2.3.2** Crear hash check antes de publicar
- [ ] **F2.3.3** Configurar alerta por contenido duplicado detectado
- [ ] **F2.3.4** Definir política de variación mínima (umbral %)

**Gate F2 — Cierre de fase:**
- [ ] Biblioteca versionada activa
- [ ] Dashboard con métricas semanales
- [ ] Dedupe activo y funcionando
- [ ] Fecha de cierre: ________

---

## 🔸 Fase 3: Madurez (500-1000 páginas)

### F3.1 — Evaluación de herramientas
- [ ] **F3.1.1** Aplicar marco de evaluación a cada nueva herramienta
- [ ] **F3.1.2** Documentar baseline vs resultado de piloto
- [ ] **F3.1.3** Registrar evaluación en wiki de herramientas
- [ ] **F3.1.4** Revisión táctica semanal activada

### F3.2 — Entorno controlado para modelos de riesgo
- [ ] **F3.2.1** Crear sandbox segregado para Mythos/modelos no verificados
- [ ] **F3.2.2** Implementar HITL reforzado en sandbox
- [ ] **F3.2.3** Configurar logging extendido en sandbox
- [ ] **F3.2.4** Documentar política de uso de modelos de alto riesgo

### F3.3 — Compliance
- [ ] **F3.3.1** Auditar legales y consistencia de identidad pública
- [ ] **F3.3.2** Verificar contacto consistente en todas las páginas
- [ ] **F3.3.3** Preparar documentación para auditoría Indeed/LinkedIn
- [ ] **F3.3.4** Validar consistencia de política de privacidad

**Gate F3 — Cierre de fase:**
- [ ] Evaluación de herramientas obligatoria
- [ ] Sandbox separado operativo
- [ ] Compliance auditado
- [ ] Fecha de cierre: ________

---

## 🔸 Fase 4: Escalado (1000+ páginas)

### F4.1 — Dashboard unificado
- [ ] **F4.1.1** Consolidar dashboard de seguridad + operación + negocio
- [ ] **F4.1.2** Implementar vistas por fase/métrica
- [ ] **F4.1.3** Configurar alertas ejecutivas
- [ ] **F4.1.4** Documentar acceso y permisos

### F4.2 — Pruebas adversariales
- [ ] **F4.2.1** Ejecutar ciclo de pruebas de prompt injection en lab
- [ ] **F4.2.2** Documentar resultados y vulnerabilidades encontradas
- [ ] **F4.2.3** Implementar correcciones identificadas
- [ ] **F4.2.4** Programar pruebas trimestrales

### F4.3 — Resiliencia operativa
- [ ] **F4.3.1** Crear playbook de recuperación ante fallos en cadena
- [ ] **F4.3.2** Documentar runbook de fallback por componente
- [ ] **F4.3.3** Simular escenario de fallo total
- [ ] **F4.3.4** Validar tiempo de recuperación objetivo

**Gate F4 — Cierre de fase:**
- [ ] Dashboard unificado operativo
- [ ] Pruebas adversariales completadas
- [ ] Runbook validado
- [ ] Fecha de cierre: ________

---

## 📊 Resumen de progreso

| Fase | Items | Completados | % Avance |
|---|---|---|---|
| F0 | 11 | ___ | ___% |
| F1 | 10 | ___ | ___% |
| F2 | 10 | ___ | ___% |
| F3 | 10 | ___ | ___% |
| F4 | 10 | ___ | ___% |
| **Total** | **51** | **___** | **___%** |

---

## Historial de actualizaciones

| Fecha | Fase | Cambios | Responsable |
|---|---|---|---|
| 2026-04-29 | — | Creación inicial | IA |