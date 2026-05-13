# 🛠️ 09. METODOLOGÍAS Y BUENAS PRÁCTICAS DE INGENIERÍA
**Funnels Foundry.ai — JobNearMe**

Este documento centraliza las metodologías de desarrollo, arquitectura y buenas prácticas que rigen el proyecto. Sirve como el "contrato de calidad" para cualquier agente de IA (Antigravity/Frankie) o desarrollador humano que toque el código o los flujos.

---

## 1. SDD (Spec-Driven Development)
El Desarrollo Guiado por Especificaciones (SDD) es nuestro estándar innegociable para cualquier cambio de arquitectura o feature nuevo.

**El Problema:** La IA conversacional (y los humanos) tienden a escribir código al vuelo, perdiendo el panorama general y generando deuda técnica.
**La Solución (SDD):**
1. **Explore (`/sdd-explore`):** Se investiga el código actual y se analizan enfoques. No se escribe código.
2. **Propose (`/sdd-propose`):** Se redacta una propuesta de arquitectura.
3. **Spec & Design (`/sdd-spec`, `/sdd-design`):** Se escriben los requisitos exactos y el diseño técnico.
4. **Tasks (`/sdd-tasks`):** Se divide en tareas atómicas.
5. **Apply (`/sdd-apply`):** Se ejecuta el código de forma quirúrgica siguiendo la especificación al pie de la letra.
6. **Verify (`/sdd-verify`):** Se valida contra los specs originales.

*Dónde viven los specs:* En la carpeta `openspec/changes/`. Todo cambio grande deja un rastro documental antes de existir en código.

---

## 2. Harness Engineering (Ingeniería de Arneses)
Basado en las mejores prácticas de software, el **Harness Engineering** es la construcción de un "arnés de seguridad" alrededor del código y de los prompts de IA para garantizar que las salidas sean deterministas, seguras y probadas.

**Cómo lo aplicamos en el Ecosistema (Antigravity / n8n / Hermes):**

### A. Arneses de Prompt (Prompt Harness)
En lugar de enviar un prompt a un LLM y esperar que devuelva algo útil, envolvemos la llamada en un arnés que fuerza la salida estructurada.
- **Ejemplo:** En n8n, no le pedimos a la IA "Escribe un artículo". Le pedimos que devuelva un **JSON estricto** con validación de esquema (JSON Schema). Si el JSON viene roto, el arnés lo rechaza y pide reintento antes de enviarlo a WordPress.

### B. Arneses de Flujo de Trabajo (Workflow Harness en n8n)
Ningún flujo de n8n va directo de A a B sin validación.
- **Nodos IF / Switch de Validación:** Antes del nodo HTTP Request a WordPress, existe un nodo que verifica: `¿Existe el título? ¿El SEO Meta está completo? ¿La imagen tiene URL absoluta?`. Si algo falla, el arnés desvía el flujo a la carpeta `error` de OneDrive.

### C. Arneses de Código (Test Harness)
Para los scripts locales (ej. `local_scheduler.py`), implementaremos pruebas controladas.
- En lugar de ejecutar el script masivamente contra 100 archivos, el arnés ejecuta 1 solo archivo (modo `Dry-Run`) y verifica los logs antes de permitir la ejecución en lote.

---

## 3. Integración SDD + Harness Engineering
Estas dos metodologías se retroalimentan:
1. Con **SDD**, planeamos QUÉ vamos a construir y establecemos los límites técnicos.
2. Con **Harness Engineering**, construimos las barreras de contención (pruebas, validaciones JSON, error handling) DURANTE la fase de `/sdd-apply`, asegurando que el código implementado no pueda romper la aplicación si falla una API o si la IA alucina.

**Regla de Oro:** Si vas a crear un workflow en n8n o un script en Python, el primer paso no es la lógica central; el primer paso es construir el arnés (validación de entrada y manejo de salida de errores).
