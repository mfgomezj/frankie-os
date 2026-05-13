# ESTRATEGIA DE CONTENIDO AUTOMATIZADO V1 (Fase: Authority Building)
Fuente de referencia documental: `00_INDICE_DOCUMENTAL.md`

## Objetivo
Establecer la Autoridad Semántica del sitio (Fake-it-till-you-make-it) publicando páginas pilares masivas (LA2/LA3) que logren la aprobación humana y algorítmica de los proveedores de API (CareerJet / Amazon SES).

## Fases de la Línea de Ensamble Visual y Semántica

### Paso 1: El Minero (OpenClaw + Abacus.ai)
- **Acción:** OpenClaw automatiza la Web UI de Abacus.ai mediante un prompt cerrado.
- **Salida:** Descarga de imagen hiper-realista/creativa en muy alta resolución (>200MB).
- **Destino:** Carpeta vigilada en Microsoft OneDrive.

### Paso 2: El Compactador (Python Watchdog Local)
- **Acción:** Un script Python corriendo en el entorno local (OpenCode) detecta el archivo crudo en OneDrive. Lo comprime de forma agresiva y sin pérdidas visibles.
- **Salida:** Imagen en formato `.webp` de aprox. 80KB-120KB.
- **Destino:** Carpeta `OneDrive/WebP_Ready`. El original pesado se borra o se archiva.

### Paso 3: La Fábrica de Branding (Canva Pro)
- **Acción:** Integración automatizada inyecta la imagen WebP dentro de la Plantilla Maestra de Canva Pro. 
- **Salida:** Se le añade el logo de JobNearMe, una capa oscura para contraste, y tipografía en dos formatos (16:9 para Web, 2:3 para Pinterest).
- **Destino:** URL publicable o retorno a ecosistema de n8n.

### Paso 4: El Generador Semántico y Repartidor (n8n + Gemini)
- **Acción:** n8n lee del *Content Scheduler* (la lista de 87KB) que hoy toca "Plumber jobs in Texas". Le pide a Gemini un borrador con datos económicos. Recoge la imagen final de Canva.
- **Salida:** Creación mediante REST API de un Custom Post en WordPress que incluye la foto optimizada y la data dura.
- **Destino Final:** Post Estático en WordPress (Borrador/Publicado) esperando la Fase 2 (donde incluiremos la inyección JS de CareerJet).

---

## Checklist Operativo (Dónde estamos y qué sigue)

- [x] **Arquitectura y Bases:** Mapas de servidores y documentación maestra consolidada.
- [x] **Flujo Teórico Validado:** Mapeo de la línea de ensamble aprobado.
- [x] **1. Content Scheduler:** `local_scheduler.py` genera el calendario y metadatos extendidos.
- [x] **2. Script Compactador Local:** `process_raw_image.py` organiza el banco y sincroniza con Notion.
- [ ] **3. Prompts de OpenClaw:** Definir las instrucciones hiper-rígidas para que extraiga asertivamente de Abacus.
- [ ] **4. Plantillas Canva Pro:** Crear diseño fijo en Canva para automatizar branding.
- [x] **5. Conector n8n:** `notion_trafficker_sync.py` y workflows de n8n integrados con Notion.

---

## 📝 CONTRATO DE METADATOS "TRAFFICKER" (Notion Core)

Para asegurar la consistencia omnicanal, todo contenido debe cumplir con este esquema de metadatos en el YAML del archivo `.md` origen:

```yaml
slug: "nombre-del-post"
focus_keyword: "keyword principal"
visual_triad:
  hero: { prompt: "Contexto visual del post (16:9)", purpose: "WP Featured" }
  twist_a: { prompt: "Giro narrativo A (9:16)", purpose: "Short A / Scene 1" }
  twist_b: { prompt: "Giro narrativo B (9:16)", purpose: "Short B / Scene 2" }
derivatives:
  short_a: { script: "Guion de 15-30s para Short A" }
  short_b: { script: "Guion de 15-30s para Short B" }
  youtube: { script_long: "Guion extendido para video de YouTube" }
status: "ideation | writing | visuals_pending | ready | published"
```

**Flujo de Verdad:**
1. **Source of Truth:** Archivo `.md` en `OneDrive/Inbox`.
2. **Cerebro Operativo:** Registro en Notion (actualizado por `notion_trafficker_sync.py`).
3. **Asset Bank:** `D:/BANK/{Project}/{Category}/{Slug}/processed/` (actualizado por `process_raw_image.py`).
