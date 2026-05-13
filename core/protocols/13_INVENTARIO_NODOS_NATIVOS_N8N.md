# 🧩 13. INVENTARIO DE NODOS NATIVOS n8n — Ecosistema FunnelsFoundry
**Actualización:** 2026-05-05
**Fuente:** docs.n8n.io + n8n.io/integrations/ (verificado)
**Propósito:** Evitar reinventar la rueda con HTTP Requests cuando ya existe un nodo nativo.

---

## ⚡ RESUMEN EJECUTIVO

n8n tiene **+400 nodos nativos** (core). Este inventario cubre solo los servicios relevantes para nuestro ecosistema. Para cada uno:
- ✅ = Nodo nativo disponible
- ⚠️ = Parcial (solo trigger o solo acción)
- ❌ = No existe nodo nativo → usar HTTP Request
- 🤖 = Nodo de IA (LangChain sub-nodes)

---

## 🔵 MICROSOFT SUITE

### Microsoft OneDrive
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.microsoftOneDrive` |
| **Trigger Node** | ✅ `n8n-nodes-base.microsoftOneDriveTrigger` |

**Operaciones (Action):**
| Recurso | Operaciones |
|---------|-------------|
| **File** | Copy, Delete, Download, Get, Rename, Search, Share, Upload |
| **Folder** | Create, Delete, Get Children, Rename, Search, Share |

**Trigger Events:** File Created, File Updated, Folder Created, Folder Updated

**⚠️ NOTA PARA EL WORKFLOW:** El workflow actual usa `Schedule Trigger` + `Get items in a folder` (polling). Se podría reemplazar por el nodo **OneDrive Trigger** (event-driven) para mayor eficiencia y menor latencia.

---

### Microsoft Teams
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.microsoftTeams` |
| **Trigger Node** | ✅ (Webhook-based) |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Channel** | Create, Delete, Get, Get Many, Update |
| **Channel Message** | Create, Get Many |
| **Chat Message** | Create, Get, Get Many, Send and Wait for Response |
| **Task** | Create, Delete, Get, Get Many, Update |

---

### Microsoft Outlook
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.microsoftOutlook` |
| **Trigger Node** | ✅ |

**Operaciones:** Folders, Messages (email), Drafts (Create, Update, Delete, Get), Calendar events, Contacts.

---

### Microsoft Excel 365
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.microsoftExcel` |
| **Trigger Node** | No |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Table** | Add Row, Get Columns, Get Rows, Lookup (search by column value) |
| **Workbook** | Add Worksheet, Get All |
| **Worksheet** | Get All, Get Content |

---

### Microsoft SharePoint
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.microsoftSharePoint` |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **File** | Download, Update, Upload |
| **Item** | Create, Upsert, Delete, Get, Get Many, Update |
| **List** | Get, Get Many |

---

## 🟡 PRODUCTIVIDAD & CONOCIMIENTO

### Notion
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.notion` |
| **Trigger Node** | ✅ `n8n-nodes-base.notionTrigger` |

**Operaciones (Action):**
| Recurso | Operaciones |
|---------|-------------|
| **Block** | Append After, Get Child Blocks |
| **Database** | Get, Get Many, Search |
| **Database Page** | Create, Get, Get Many, Update |
| **Page** | Archive, Create, Search |
| **User** | Get, Get Many |

**Trigger Events:** Page Added to Database, Page Updated in Database (polling)

---

### Canva
| Tipo | Estado |
|------|--------|
| **Action Node** | ❌ NO existe nodo nativo |
| **Trigger Node** | ❌ No |

**Solución:** HTTP Request node → Canva Connect API (`canva.dev/docs/connect/`).
**Nota:** API de Canva está orientada a Enterprise. Para brand template autofill se necesita configuración de developer. Alternativa: Templated.io (tiene community node).

---

## 🟢 CMS & PUBLICACIÓN

### WordPress
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.wordpress` (v1) |
| **Trigger Node** | ❌ No |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Post** | Create, Get, Get All, Update |
| **Page** | Create, Get, Get All, Update |
| **User** | Create, Get, Get All, Update |

**⚠️ GOTCHA CRÍTICO:** El nodo nativo **NO soporta Media, Tags, Categories, ni Custom Post Types**. Para estas operaciones se DEBE usar HTTP Request → WordPress REST API (`/wp-json/wp/v2/media`, `/wp-json/wp/v2/tags`, etc.). Se pueden reusar las mismas credenciales WP seleccionando "Predefined Credential Type" en el HTTP Request.

---

### Medium
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.medium` |
| **Trigger Node** | ❌ No |

**Operaciones:** Create Publication (post). 
**Nota:** Medium ya no emite tokens nuevos de integración. Tokens existentes pueden seguir funcionando. Canal semi-manual por política.

---

## 💬 MENSAJERÍA & COMUNICACIÓN

### Telegram
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.telegram` |
| **Trigger Node** | ✅ `n8n-nodes-base.telegramTrigger` |

**Operaciones (Action):**
| Recurso | Operaciones |
|---------|-------------|
| **Message** | Send Message, Send Photo, Send Document, Send Video, Send Audio, Send Sticker, Send Animation, Send Location, Edit Message Text, Delete, Pin Chat Message, Unpin Chat Message |
| **Chat** | Get, Get Administrators, Get Member, Leave, Set Description, Set Title |
| **Callback** | Answer Query, Answer Inline Query |
| **File** | Get (download file by ID) |

**Trigger Events:** Cualquier update del bot (message, edited_message, callback_query, inline_query, etc.)

---

### WhatsApp Business Cloud
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.whatsApp` |
| **Trigger Node** | ✅ (via Meta Webhook) |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Message** | Send Text, Send Template, Send Media (Image/Video/Document/Audio), Send Location, Send Contact, Send Interactive |

**Auth:** Requiere Meta Business Suite + WhatsApp Business API setup.

---

## 📱 REDES SOCIALES

### Facebook
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.facebookGraphApi` |
| **Trigger Node** | ✅ `n8n-nodes-base.facebookTrigger` + `n8n-nodes-base.facebookLeadAdsTrigger` |

**Operaciones (Action):** GET, POST, DELETE sobre Graph API (pages, feed, photos, video upload).
**Trigger:** Page events, Lead Ads submissions.

---

### Instagram
| Tipo | Estado |
|------|--------|
| **Action Node** | ⚠️ SOLO vía Facebook Graph API node |
| **Trigger Node** | ✅ (via Facebook Trigger — page events) |

**Nota:** No hay nodo nativo exclusivo de Instagram. Para publicar, usar HTTP Request → Instagram Content Publishing API (requiere Business Account). Para triggers, usar el Facebook Trigger node.

---

### X (formerly Twitter)
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.twitter` |
| **Trigger Node** | ❌ No (usar webhook o polling) |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Tweet** | Create, Delete, Search, Like, Retweet |
| **Direct Message** | Create |
| **User** | Get |
| **List** | Add Member |

**Auth:** OAuth2 obligatorio (OAuth1.0a deprecado). Requiere X Developer Portal app con "Read + Write + DM" permissions.

---

### TikTok
| Tipo | Estado |
|------|--------|
| **Action Node** | ❌ NO existe nodo nativo |
| **Trigger Node** | ❌ No |

**Solución:** HTTP Request → TikTok Content Posting API.

---

### YouTube
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.youTube` |
| **Trigger Node** | ❌ No |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Channel** | Get, Get All, Update |
| **Playlist** | Create, Delete, Get, Get All |
| **Playlist Item** | Add, Delete, Get, Get All |
| **Video** | Delete, Get, Get All, Rate, Update, Upload |
| **Video Category** | Get All |

**⚠️ Upload:** Proyectos no verificados suben en privado hasta auditoría de Google. Tiene costos de cuota por método.

---

## 📧 CRM & EMAIL

### Mautic
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.mautic` |
| **Trigger Node** | ✅ `n8n-nodes-base.mauticTrigger` |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Contact** | Create, Delete, Update, Get, Get All, Edit Points, Add/Remove Do Not Contact, Send Email |
| **Company** | Create, Delete, Update, Get, Get All |
| **Company Contact** | Add, Remove |
| **Campaign Contact** | Add, Remove |
| **Contact Segment** | Add, Remove |
| **Segment Email** | Send |

---

## 🛠️ DEVOPS & INFRA

### GitHub
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.github` |
| **Trigger Node** | ✅ `n8n-nodes-base.githubTrigger` |

**Operaciones (Action):**
| Recurso | Operaciones |
|---------|-------------|
| **File** | Create, Delete, Edit, Get, List |
| **Issue** | Create, Create Comment, Edit, Get, Lock |
| **Release** | Create, Delete, Get, Get Many, Update |
| **Repository** | Get, Get Issues, Get License, Get Profile, Get Pull Requests, List Popular Paths, List Referrers |
| **Review** | Create, Get, Get Many, Update |
| **User** | Get Repositories, Invite |
| **Workflow** | Disable, Dispatch, Enable, Get, Get Usage, List |

**Trigger Events:** Pull Requests, Issues, Push, Release, Repository, Comments, Deployments, Stars, etc. (Webhook-based).

---

### DigitalOcean
| Tipo | Estado |
|------|--------|
| **Action Node** | ❌ NO existe nodo nativo |
| **Trigger Node** | ❌ No |

**Solución:** HTTP Request → DO API. Para **Spaces** (object storage), usar el nodo de **S3** configurando los endpoints de DigitalOcean.

---

### AWS S3
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.awsS3` |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Bucket** | Create, Delete, Get All, Search |
| **File** | Copy, Delete, Download, Get All, Upload |
| **Folder** | Create, Delete, Get All |

---

### AWS SES
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.awsSes` |

**Operaciones:**
| Recurso | Operaciones |
|---------|-------------|
| **Custom Verification Email** | Create, Delete, Get, Get All, Send, Update |
| **Email** | Send, Send Template |
| **Template** | Create, Delete, Get, Get All, Update |

---

## 📊 ANALYTICS & ADS

### Google Ads
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.googleAds` |

**Operaciones:** Campaign management, Ad management, Reporting.

---

### Google Analytics (GA4)
| Tipo | Estado |
|------|--------|
| **Action Node** | ✅ `n8n-nodes-base.googleAnalytics` |

**Operaciones:** Report data, User Activity (GA4 properties).

---

### ManyChat
| Tipo | Estado |
|------|--------|
| **Action Node** | ❌ NO existe nodo nativo |
| **Trigger Node** | ❌ No |

**Solución:** HTTP Request → ManyChat API (API key desde Extensions > API en ManyChat).

---

## 🤖 MODELOS DE IA (LangChain Sub-Nodes)

n8n tiene un ecosistema completo de nodos de IA que funcionan como **sub-nodos** dentro del **AI Agent** node o de forma standalone:

### OpenAI
| Nodo | Tipo | Uso |
|------|------|-----|
| `@n8n/n8n-nodes-langchain.openAi` | Chat Model | GPT-4o, GPT-4o-mini, o1, o1-mini |
| `@n8n/n8n-nodes-langchain.openAiAssistant` | Assistant | Asistentes con herramientas/files |
| `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | Embeddings | text-embedding-3-small/large |
| `n8n-nodes-base.openAi` | Action (legacy) | Image generation, text completion |

---

### Anthropic (Claude)
| Nodo | Tipo | Uso |
|------|------|-----|
| `@n8n/n8n-nodes-langchain.lmChatAnthropic` | Chat Model | Claude 3.5 Sonnet, Claude 3 Opus/Haiku |

---

### Google Gemini
| Nodo | Tipo | Uso |
|------|------|-----|
| `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` | Chat Model | Gemini 1.5 Pro/Flash, Gemini 2.0 |
| `n8n-nodes-base.googleGemini` | Action | Text, Audio, Image/Video analysis |
| `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini` | Embeddings | Gemini embeddings |

---

### AI Agent (Orquestador)
| Nodo | Uso |
|------|-----|
| `@n8n/n8n-nodes-langchain.agent` | Agente autónomo que usa herramientas (tools) |
| `@n8n/n8n-nodes-langchain.chainLlm` | LLM Chain básica |
| `@n8n/n8n-nodes-langchain.chainRetrievalQa` | RAG con retrieval |
| `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Memoria conversacional |
| `@n8n/n8n-nodes-langchain.toolWorkflow` | Convierte un workflow en herramienta de agente |
| `@n8n/n8n-nodes-langchain.toolCode` | Herramienta custom en código |

**MCP (Model Context Protocol):**
- n8n soporta MCP nativo mediante nodos de herramientas que se pueden exponer como tools para agentes.
- También se pueden crear sub-workflows como herramientas del agente para integrar servicios externos.

---

## 📋 MATRIZ RESUMEN

| Servicio | Action | Trigger | Nota clave |
|----------|--------|---------|------------|
| **OneDrive** | ✅ | ✅ | Tiene trigger nativo (usar en vez de polling) |
| **Teams** | ✅ | ✅ | Incluye Send & Wait (aprobaciones) |
| **Outlook** | ✅ | ✅ | Emails, calendar, contacts |
| **Excel 365** | ✅ | ❌ | Tables, workbooks, worksheets |
| **SharePoint** | ✅ | ❌ | Files, items, lists |
| **Notion** | ✅ | ✅ | Blocks, DBs, Pages, Users |
| **Canva** | ❌ | ❌ | HTTP Request → Canva API |
| **WordPress** | ✅ | ❌ | ⚠️ NO soporta Media/Tags/Categories |
| **Medium** | ✅ | ❌ | No emiten tokens nuevos |
| **Telegram** | ✅ | ✅ | Completo: msgs, media, callbacks |
| **WhatsApp** | ✅ | ✅ | Via Meta Business Cloud API |
| **Facebook** | ✅ | ✅ | Graph API + Lead Ads trigger |
| **Instagram** | ⚠️ | ✅ | Solo trigger; publicar vía HTTP |
| **X (Twitter)** | ✅ | ❌ | OAuth2 obligatorio |
| **TikTok** | ❌ | ❌ | HTTP Request → TikTok API |
| **YouTube** | ✅ | ❌ | Upload + manage channels/playlists |
| **Mautic** | ✅ | ✅ | Contacts, companies, campaigns |
| **GitHub** | ✅ | ✅ | Files, issues, releases, workflows |
| **DigitalOcean** | ❌ | ❌ | Usar S3 node para Spaces |
| **AWS S3** | ✅ | ❌ | Buckets, files, folders |
| **AWS SES** | ✅ | ❌ | Emails, templates |
| **Google Ads** | ✅ | ❌ | Campaigns, ads, reporting |
| **Google Analytics** | ✅ | ❌ | GA4 reports |
| **ManyChat** | ❌ | ❌ | HTTP Request → ManyChat API |
| **OpenAI** | 🤖 | ❌ | Chat, Assistants, Embeddings, Images |
| **Anthropic** | 🤖 | ❌ | Claude chat models |
| **Google Gemini** | 🤖 | ❌ | Chat, Audio, Image/Video, Embeddings |

---

## 🔑 REGLAS DE USO

1. **SIEMPRE verificar** si existe nodo nativo antes de usar HTTP Request.
2. **Reusar credenciales:** Si el nodo nativo no soporta una operación específica, en el HTTP Request seleccionar "Predefined Credential Type" para reusar las credenciales del nodo nativo.
3. **Verificar versión del nodo:** Algunos nodos tienen múltiples `typeVersion`. Usar la más reciente para acceder a todas las operaciones.
4. **AI Agents:** Los modelos de IA son sub-nodos del AI Agent. No se usan como nodos standalone en la mayoría de los casos modernos.
5. **Actualizar este documento** cada vez que se detecte un nuevo nodo relevante o cuando n8n publique actualizaciones de nodos existentes.
