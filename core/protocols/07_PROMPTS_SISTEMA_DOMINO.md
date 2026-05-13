# 🁣 07. SISTEMA DE PROMPTS EN DOMINÓ (Borrador Arquitectónico)
**Proyecto: JobNearMe.online**
*Nota: Este documento es vivo. Su propósito es definir "La Lógica de Cascada" que tomará Nano Banana para fragmentar un artículo.*

---

## 🏗️ MAPA DE LA CASCADA CONCEPTUAL

La creación de contenido no es un bloque sólido; es un río que empieza en el artículo principal y desemboca en dos océanos radicalmente diferentes: **El Embudador Largo (YouTube)** y **El Pescador de Tráfico (Redes Cortas)**.

### DOMINÓ 0: EL NUCLEO
- **Entregable:** El Artículo SEO Completo (LAx) de 2500 palabras.
- **Función:** Generar la espina dorsal semántica para Google. Es la fuente de la verdad.

### DOMINÓ 1: LA MINERÍA DE ESTRUCTURAS
- **La Acción:** El LLM traga el LAx completo y separa los componentes:
  1. Identifica y extrae estructuralmente los X "Giros Argumentales" del texto.
  2. Determina el tono demográfico al que le habla (Ej: Juniors frustrados, Managers corporativos).

---

## 🔀 LA BIFURCACIÓN DE CANALES

Una vez que tenemos los "Giros Argumentales", el río se divide en dos lógicas audiovisuales distintas que requerirán Prompts dedicados:

### A. EL MACRO-VIDEO (YouTube Medium Length)
*El YouTube no fragmenta; engulle todo el LAx. Es un formato educativo inmersivo.*
- **El Script:** El LAx mismo funge como Guion Base (A-Roll / Locutor).
- **El B-Roll (Storyboard):** Como un giro argumental puede durar 2 minutos en pantalla, no sirve tener 1 sola imagen. 
- **El Prompt Requerido:** Necesitamos que el LLM actúe como "Director de Fotografía" y nos arroje un `Shot List` (Lista de Tomas) multi-ángulo para un mismo giro. Ejemplo para hablar de trabajo remoto: Toma abierta del escritorio, Toma cerrada del café, Toma sobre el hombro del trabajador tipeando.

### B. EL MICRO-CONTENIDO (Shorts, Reels, TikTok, Pinterest)
*El pescador de tráfico tiene TDAH. Si mostrás más de una idea, deslizan para arriba.*
- **El Script:** Se toma SOLAMENTE uno de los "Giros Argumentales". El LLM lo reescribe siguiendo la curva de dopamina estricta (Gancho de 3s $\rightarrow$ Escenario visual $\rightarrow$ Call to Action).
- **El B-Roll:** Utiliza solo la imagen/video principal del "Giro Extraído" generada en la matriz "En Branding".
- **El Prompt Requerido:** Necesita moldearse a la demografía de la red. Si el prompt genera el guion para TikTok, debe ser enérgico y polémico. Si lo moldea a LinkedIn, debe ser reflexivo y corporativo.

---

## 📝 RESERVORIOS DE PROMPTS (Por definir)

*[Pendiente de construcción: Aquí iremos volcando el código "crudo" de nuestras instrucciones exactas para Nano Banana o Frankie a medida que modelemos el comportamiento de las redes].*

1. **[PROMPT] Redactor Core LAx**
   * **Instrucción Vital de Estructura:** 
     "Toda la entrega del artículo debe comenzar con un bloque YAML Frontmatter estricto. Es obligatorio que el campo `featured_image` termine en extensión `.webp` (No `.png` ni `.jpg`), ya que nuestro pipeline de Python convierte todos los RAWs a WebP automáticamente antes de entregar a n8n."
     ```yaml
     ---
     title: "Título SEO 2026"
     slug: "titulo-seo-2026"
     seo_title: "Título SEO (2026) | JobNearMe"
     meta_description: "160 caracteres."
     focus_keyword: "titulo seo 2026"
     status: "draft"
     canonical_url: "https://jobnearme.online/titulo-seo-2026/"
     category_ids: [X]
     tag_ids: [Y,Z]
     featured_image: "./titulo-seo-2026.webp"
     ---
     ```
2. **[PROMPT] Extractor de Storyboard (YouTube)**
3. **[PROMPT] Creador de Ganchos y Guiones 9:16 (TikToK/IG/FB)**
4. **[PROMPT] Copywriter de Hilos Corporativos y Emocionales (X / LinkedIn)**
5. **[PROMPT] Conversor de Pinterest (Pins de retención visual)**
