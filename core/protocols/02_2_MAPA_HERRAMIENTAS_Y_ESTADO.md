{# MAPA DE HERRAMIENTAS Y ESTADO DE INTEGRACIÓN
Fuente de referencia documental: `00_INDICE_DOCUMENTAL.md`
Actualización: 2026-04-19

## 1. Mapeo de Infraestructura Activa

| Herramienta / Servicio | Rol & Integración | Ubicación | Estado Actual |
|------------------------|--------------------|-----------|---------------|
| **WordPress** | La Vitrina (CMS). Sirve como frontend para el usuario y Google. Recibe contenido inyectado por n8n. | AWS EC2 (Recursos básicos) | **🟢 Activo**. SSL listo, `jobnearme.online` enrutado por Cloudflare CDN. |
| **Cloudflare** | CDN y DNS. Protege y cachea WordPress para acelerar el load time global. | Cloudflare Cloud | **🟢 Activo**. |
| **n8n (Orquestador)** | El Sistema Nervioso. Maneja las automatizaciones y lanza webhooks a WP. | DigitalOcean (Droplet independiente) | **🟢 Activo**. Automatización n8n $\rightarrow$ WordPress probada y lista. |
| **OpenClaw (Agente)** | Brazo Ejecuctor (RPA). Navega webs sin API. Operado vía triggers. | DigitalOcean (Droplet de $25/mes. Promo $200) | **🟢 Activo**. Cuentas separadas de n8n. |
| **Antigravity / Frankie** | Cerebro Local (Arquitecto). Audita SEO, crea Prompts, define base de datos y mantiene memoria (Engram). | Entorno Local (Workspace) | **🟢 Activo y Operando**. |

## 2. Componentes Pendientes o En Proceso

| Herramienta / Servicio | Rol & Integración | Ubicación | Estado Actual |
|------------------------|--------------------|-----------|---------------|
| **ZohoMail** | Correo corporativo transaccional básico (Temporal hasta SES). | Zoho Cloud | **🟢 Activo**. Listo para usarse como SMTP en WP. |
| **Amazon SES & Mautic**| Suite avanzada de Marketing y envío masivo. | AWS / Nube | **🔴 Bloqueado**. Requiere que el sitio tenga contenido y "Autoridad" primero. |
| **CareerJet API** | Fuente origen de las vacantes. Inyecta datos crudos a WP. | Nube | **🔴 Bloqueado (Fase 1)**. Requiere que el sitio tenga autoridad y contenido para aprobar la cuenta. |
| **Abacus.ai** | Generación de activos multimedia (Imágenes HD/Video) con multi-modelo. | Interfaz Web | **🟢 Activo (Manual/RPA)**. Se usa vía Web UI porque no hay acceso CLI fácil a multi-modelo. Genera archivos muy pesados. |
| **Canva Pro** | Planta de ensamblaje visual final. Añade branding (logotipos, fuentes) y adapta piezas para redes sociales y pines de Pinterest masivos. | Canva Cloud | **🟢 Activo**. Cuenta Pro disponible. Potencial integración con n8n u OpenClaw para plantillado. |
| **Microsoft OneDrive** | Eje de Sincronización y Almacenamiento (Reemplaza a Google Drive/S3 inicial). | Local / Nube | **🟢 Activo**. Sincroniza la computadora física con la nube. |

## 3. Notas de Integridad
Para mantener la continuidad, toda modificación de instancias EC2/Droplets o vencimiento de créditos promo en OpenClaw ($200) debe ajustarse aquí para tener el panorama comercial y técnico alineado.
