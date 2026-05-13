# ⚖️ Matriz de Convergencia: Frankie V1 vs. Ecosistema Hermes/Antigravity (V2)
**Estatus:** Análisis Estratégico 90/10
**Fecha:** Mayo 2026

Este documento mapea la estructura de trabajo previa de *JobNearMe* y *Funnels Foundry* contra el nuevo paradigma de **Hermes (Kanban Swarms) + Antigravity (MCP)**, definiendo dónde coinciden, dónde chocan y qué decisiones debemos tomar.

---

## 1. Paralelismos y Convergencias (Donde encaja perfecto)

| Concepto Previo (Frankie V1) | Equivalente Nuevo (Hermes V2) | Análisis de Convergencia |
| :--- | :--- | :--- |
| **Content Waterfall (Cascada)** | **Kanban Swarms (SEO Clusters)** | Es exactamente la misma filosofía. Nuestro plan de crear un artículo pilar (LAx) y derivar satélites se ejecuta nativamente mediante el "Dispatcher" de Hermes levantando múltiples perfiles en paralelo para generar clusters de 50 páginas. |
| **Integración n8n** | **n8n Gateway / Webhooks** | n8n sigue siendo fundamental. Hermes no debe tener credenciales de WordPress directas por seguridad. Hermes escribe el contenido y lanza un webhook a n8n para que este lo publique y distribuya. |
| **Notion como Memoria** | **Notion MCP (Antigravity)** | Antes usábamos la API de Notion manual o n8n. Ahora, mediante el protocolo MCP, Antigravity puede leer/escribir en Notion de forma nativa como si fuera una base de datos local. |
| **Regla de Cobre (Revisión Humana)** | **Modo "Planning" y Tablero Kanban** | Nuestra regla inquebrantable de "nunca publicar sin revisión" se alinea con el flujo de Hermes: genera un `strategy.md`, se detiene, y solo avanza cuando le comentamos "Aprobado" en el Kanban. |

---

## 2. Resoluciones Arquitectónicas (Tras Feedback)

### A. La Fuente de Verdad del Estado (Task Tracking vs Outputs)
*   **Decisión:** **No habrá duplicación de bases de datos.** Hermes usará exclusivamente su `kanban.db` interno para operar y tomar decisiones. 
*   **El Rol de Notion:** Notion no será un tablero Kanban de tareas. Actuará como **Repositorio Semántico Estructurado**. Cuando un agente genere derivados (ej. libretos cortos para shorts, prompts de imágenes basados en giros argumentales), los guardará de forma organizada en bases de datos de Notion para su futuro uso.

### B. El Orquestador y las Vías de Integración
*   **Decisión:** Frankie (tanto en su versión Local/Desktop como Cloud) es el cerebro.
*   **Ejecución:** Frankie utilizará integraciones nativas cuando sea óptimo (ej. Notion MCP, OneDrive), pero delegará en **n8n** las tareas de interconexión compleja (ej. tomar una carpeta de OneDrive con un artículo LA3 y su imagen optimizada, y publicarlo en WordPress).

### C. Local vs. Nube (La Estrategia de Ahorro)
*   **Decisión Crítica:** El grueso del trabajo (el músculo generativo pesado, los enjambres masivos) se ejecutará en **Local (Frankie Desktop / Antigravity)** para minimizar costos operativos de servidor y aprovechar la máquina local.
*   **Uso de la Nube:** El VPS (Frankie Cloud / Hermes) se reservará para tareas automatizadas más ligeras, rutinas de bajo consumo, o enjambres en la nube estrictamente cuando sea necesario. Ambas instancias (Desktop y Cloud) compartirán la misma memoria persistente (Engram).

---

## 3. Ventajas del Nuevo Stack Consolidado

### Ventajas (Pros)
*   **Costo-Eficiencia Extrema:** Al derivar el "Heavy Lifting" a la terminal local con Antigravity, protegemos el presupuesto, usando la nube solo como nodo permanente.
*   **Ecosistema Interconectado (Content Waterfall):** Un solo comando local puede generar un LA3, depositarlo en OneDrive junto a sus imágenes, y estructurar decenas de prompts de distribución en Notion, dejando que n8n se encargue solo del tráfico final.
*   **Memoria Compartida:** Al sincronizar el Engram entre Local y Cloud, Frankie no pierde el hilo sin importar desde dónde esté operando.

---

## 4. Puntos que Necesitan Análisis (Para Feedback)
1.  **Sincronización Notion vs. Kanban DB:** ¿Querés que armemos un puente para ver el Kanban de Hermes reflejado en Notion, o te sentís cómodo gestionando las misiones de los agentes directamente vía comandos de Telegram?
2.  **Topología de n8n:** ¿n8n vivirá en el mismo VPS que Hermes (Docker) o usaremos n8n Cloud / otro servidor?
3.  **Límites de Seguridad (Circuit Breakers):** ¿Qué presupuesto máximo diario (tokens/dólares) le configuramos al agente antes de que se autobloquee y te pida permiso por Telegram?
