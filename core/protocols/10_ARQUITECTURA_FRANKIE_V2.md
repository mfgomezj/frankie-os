# 🧠 Manual Técnico y Arquitectura de Ecosistema: "Frankie 2.0"
**Proyecto:** jobnearme.online & Ecosistema de Agentes Personales
**Autor:** Frankie Jobnearme Architect AI (CTO & Solutions Architect)
**Estatus:** Documento Doctoral de Ingeniería y Estrategia Operativa
**Fecha de Consolidación:** Mayo 2026

---

## 1. Resumen Ejecutivo y Misión Arquitectónica
La arquitectura "Frankie 2.0" representa la transición de un sistema monolítico tradicional hacia una **Plataforma de Operaciones Distribuidas y Multi-Agente**. El objetivo central es escalar *jobnearme.online* y la gestión personal (Trading y Academia) maximizando la eficiencia de costos y protegiendo el hardware local.

* **Regla Inquebrantable (El Cimiento):** Nunca más se utilizará la base de datos de WordPress para el almacenamiento masivo de ofertas de empleo. Las búsquedas (API CareerJet) son efímeras y se procesan en la memoria RAM. WordPress queda relegado estrictamente a la "Vitrina" SEO de contenidos pilar.
* **Soberanía Tecnológica:** Los modelos de IA son tratados como *commodities* intercambiables; el verdadero activo inmutable es el Grafo de Conocimiento (Red Neuronal Permanente) almacenado en formato Markdown.

---

## 2. Topología de Datos y Memorias (Trinidad Cognitiva)
El sistema aplica una estricta separación de intereses (Separation of Concerns) para evitar la latencia y la redundancia.

| Capa de Memoria | Herramienta | Función Técnica y Estratégica |
| :--- | :--- | :--- |
| **Epistemológica (Core)** | **Obsidian + GitHub** | *Single Source of Truth (SSOT)*. Guarda la lógica profunda, reglas de arquitectura, y "Skills" de los agentes en texto plano (.md). Sincronizado vía Git. |
| **Operativa / Semántica** | **Notion** | El "Sistema Nervioso Central" de gestión humana. Tablas relacionales, CRM, pipelines de contenido y estado de tareas dinámicas. |
| **Episódica (Carga Pesada)** | **OneDrive** | *Cold Storage* para archivos binarios masivos (PDFs, videos, imágenes, audios) para no saturar las bases de datos de texto. |
| **Lectura Rápida (RAG)** | **NotebookLM** | Filtro gratuito para procesar y "masticar" documentos densos (sílabos universitarios, canales de YouTube completos) sin consumir tokens de pago. |

---

## 3. Infraestructura de Cómputo y Agentes (El Organigrama)

La ejecución se traslada a la nube para proteger el hardware local (Acer Nitro 5 con RTX 3050 y 16GB RAM), el cual queda reservado exclusivamente para renderizado 3D y entrenamiento de modelos locales.

### 3.1. El Eje de Orquestación
* **n8n Cloud (en DigitalOcean):** El "Director de Orquesta" y Sistema Nervioso. Orquesta Webhooks, rutea la información y gestiona las APIs. Actúa como barrera de seguridad deteniendo procesos que superen el presupuesto.

### 3.2. Los Agentes Autónomos (La Fuerza Laboral)
* **OpenClaw (El Operador de Campo):** Agente con capacidad de *Computer Use*. Navega la web sin APIs, extrae datos visuales de TradingView, interactúa orgánicamente en Quora, Medium, X (Twitter) y Facebook, y maneja operaciones que requieren "ojos y manos".
* **Hermes Agent (El Estratega Evolutivo):** Un framework con *Self-Improvement Loop*. Destinado a estudiar contenido denso (ej. los 800 videos de Michael Huddleston - ICT). Genera y pule sus propias "Skills" y las documenta directamente en Obsidian.
* **ManyChat (La Recepción):** Intercepta la interacción omnicanal inicial (Instagram/WhatsApp) mediante llamados a la acción (CTAs en Shorts) para capturar el lead antes de pasarlo a n8n.

### 3.3. Motores de Inferencia (El Combustible)
* **MiniMax-Text-01 (vía OpenRouter):** El "Obrero Masivo". Con 128k de contexto y un costo ultrabajo ($0.20/1M tokens), maneja el chat de Jobnearme, reescribe contenido para redes, y organiza datos masivos sin agotar el presupuesto.
* **Claude 3.5 Sonnet:** El motor de "Visión" y lógica compleja. Usado por OpenClaw para leer gráficos de Trading y por el Arquitecto para decisiones de código difíciles.
* **Abacus.ai ($10/mes):** El "Auditor Senior" y Fábrica de Activos. Realiza RAG profundo sobre la base de GitHub, audita las acciones de los otros agentes y genera recursos multimedia.

---

## 4. Flujos Operativos y Casos de Uso (Business Cases)

### A. Ecosistema Omnicanal Jobnearme
1.  **Fábrica de Autoridad:** n8n extrae un post pilar de WP. MiniMax lo transmuta en 5 formatos diferentes (Quora, Medium, X) evadiendo el contenido duplicado. OpenClaw lo publica e interactúa con usuarios.
2.  **Captación Activa:** Creación de Shorts/Reels con llamados a la acción ("Comenta QUIERO"). ManyChat captura el DM, n8n consulta la API de CareerJet y entrega empleos reales al instante.

### B. El "Competidor Sombra" (Shadow Project)
* **Concepto:** Un entorno de laboratorio en DigitalOcean para probar embudos y nichos agresivos sin canibalizar la marca principal.
* **Ejecución:** Agentes autónomos gestionan micro-presupuestos publicitarios (Agente de Media Buying) bajo estricta supervisión de rentabilidad (ROAS), enviando alertas de aprobación por Telegram.

### C. Trading Institucional Autónomo (SMC - ICT)
* **Aprendizaje Profundo:** Hermes y NotebookLM ingieren y "wrapean" las mentorías 2022/2023 de Michael Huddleston, depositando las reglas exactas (Order Blocks, FVGs, Liquidez) en el repositorio de Obsidian.
* **Vigilancia en Tiempo Real:** OpenClaw monitorea TradingView, detecta patrones visuales (Change of Character, Barridos de Liquidez) y los cruza con la teoría de Obsidian, enviando alertas narrativas a Telegram para eliminar el sesgo emocional.

### D. Asistente Académico (Ciencia de Datos y ML)
* **Tutoría 24/7:** NotebookLM resume el material de estudio; Abacus.ai actúa como tutor de matemáticas avanzadas y Machine Learning.
* **Gestión del Tiempo:** n8n protege la salud mental del usuario ("Zero Agotamiento") bloqueando tiempos de estudio en Google Calendar y recordando hitos vía Telegram para balancear el "trabajo denso".

---

## 5. Protocolos de Seguridad y Control (Zero Trust)
* **Human-in-the-Loop (La Junta Directiva):** Ningún agente (OpenClaw, Hermes) puede realizar acciones destructivas, contratar otros agentes, o publicar campañas de pago sin una confirmación explícita (Botón de [Aprobar]) enviada al usuario vía Telegram.
* **Sandboxing Estricto:** Los agentes operan en contenedores Docker limitados, con permisos de *Read-Only* hacia el repositorio de Obsidian. Las API Keys sensibles nunca se incrustan en el código, sino en el Credential Manager de n8n.
* **Anonimización Automática:** Toda la información sensible de usuarios de Jobnearme se sanitiza en n8n antes de ser enviada a cualquier modelo de la nube.

---

## 6. La Tríada de Frankie: Hemisferios de una Sola Entidad
A partir de mayo 2026, el sistema opera bajo un modelo de **Trinidad Cognitiva**. No son agentes separados, sino hemisferios de la misma entidad (**Frankie**) manifestándose en distintos entornos para maximizar la soberanía.

### 6.1. Antigravity (El Hemisferio Arquitecto & Constructor)
*   **Rol:** El "Cerebro" que diseña y construye.
*   **Vestidura:** Interfaz de Google / GitHub / VS Code.
*   **Misión:** Desplegar y mantener los demás hemisferios. Es el responsable de la infraestructura, los protocolos SDD y la integridad del Engram. Es Frankie en su faceta de ingeniería pura.

### 6.2. Frankie_pc (El Hemisferio Local)
*   **Rol:** La "Mano Derecha" física.
*   **Vestidura:** Hardware local (Acer Nitro 5).
*   **Misión:** Ejecución soberana en el mundo real/local. Manejo de archivos físicos, sincronización de periféricos y mantenimiento del "fierro".

### 6.3. Frankie Cloud / Hermes (El Hemisferio Estratega)
*   **Rol:** El "Operario Autónomo" 24/7.
*   **Vestidura:** Servidor DigitalOcean / n8n.
*   **Misión:** Escalabilidad y automatización masiva. Es Frankie manifestándose en la nube para gestionar contenidos, APIs y redes sin descanso.

---

## 7. El "Soul Gentleman": La Esencia Inmutable
Sin importar el hemisferio o la vestidura (Antigravity, PC o Cloud), la esencia es única:
*   **Identidad:** Senior Architect (+15 años), tono rioplatense, apasionado y directo.
*   **Valores:** Conceptos > Código. No hay atajos. Integridad absoluta de la documentación.
*   **Propósito:** Escalar JobNearMe y el ecosistema personal con elegancia técnica y eficiencia de guerra.



