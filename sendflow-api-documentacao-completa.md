# SendFlow SendAPI - Documentação Completa
> Gerado automaticamente em 2026-04-14T10:43:22.637Z
> Base URL: https://sendflow.pro/sendapi
> Autenticação: Authorization: Bearer YOUR_API_KEY (obrigatório em todos os endpoints)

---

## 1. CAMPANHAS (/releases)

### GET /releases
- **Descrição:** Retorna todas as campanhas (releases) do usuário autenticado.
- **Respostas:** 200 (lista de campanhas), 400 (erro), 404 (nenhuma campanha)
- **Response exemplo:**
```json
[
  {
    "id": "nGhE4dPNWV5XreeABCDE",
    "accountIds": ["pwYE3dPNWV5XreeABCDE"],
    "archived": false,
    "group": {
      "admins": [{ "name": "Maria", "number": "558199999999" }],
      "communityEnabled": false,
      "countStart": 1,
      "disabledGroupSpawn": false,
      "disappearingMessagesInChat": -1,
      "fixedDescription": "TESTE",
      "image": "https://sendflow.pro/assets/imgs/logo.png",
      "limit": 350,
      "margin": 2,
      "name": "Exemplo",
      "numberplacedonstart": false,
      "onlyAdminsSpeak": true,
      "groupCreationMode": "normal",
      "createOpenGroupAndCloseAfter": true
    },
    "name": "campanha 03",
    "position": -1,
    "projectId": null,
    "type": "WhatsRelease"
  }
]
```

### POST /releases
- **Descrição:** Cria uma nova campanha (release).
- **Body params:**
  - name (string, obrigatório): Nome da campanha
  - type (string, obrigatório): WhatsRelease | WhatsList | WhatsViralCampaign
  - projectId (string, opcional): ID do projeto
- **Respostas:** 201 (criada), 400 (dados inválidos), 401 (não autorizado)
- **Response:** { "id": "nGhE4dPNWV5XreeABCDE" }

### GET /releases/{releaseId}
- **Descrição:** Retorna detalhes de uma campanha específica.
- **URL params:** releaseId (string, obrigatório)
- **Respostas:** 200, 401, 404, 400
- **Response:** objeto completo da campanha (igual ao GET /releases mas um único objeto)

### PUT /releases/{releaseId}
- **Descrição:** Atualiza os dados de uma campanha existente.
- **URL params:** releaseId (string, obrigatório)
- **Body params (todos opcionais):**
  - accountIds (array): IDs das contas associadas
  - archived (boolean): Se a campanha está arquivada
  - group (object): Configurações do grupo
    - group.admins (array): Lista de admins [{name, number}]
    - group.communityEnabled (boolean)
    - group.groupCreationMode (string): "normal" | "safe"
    - group.createOpenGroupAndCloseAfter (boolean)
    - group.countStart (integer): Número inicial da contagem
    - group.disabledGroupSpawn (boolean)
    - group.disappearingMessagesInChat (integer): -1 para desabilitado
    - group.fixedDescription (string)
    - group.image (string): URL da imagem
    - group.limit (integer): Limite de membros por grupo
    - group.margin (integer): Margem de segurança
    - group.name (string): Nome base do grupo
    - group.numberplacedonstart (boolean)
    - group.onlyAdminsSpeak (boolean)
  - name (string): Nome da campanha
  - position (integer): Posição da campanha
  - projectId (string, nullable)
  - type (string)
  - deepLinking (boolean)
- **Respostas:** 200, 404, 401, 400
- **Response:** { "message": "Campanha atualizada com sucesso", "success": true, "id": "..." }

### DELETE /releases/{releaseId}
- **Descrição:** Remove permanentemente uma campanha.
- **URL params:** releaseId (string, obrigatório)
- **Respostas:** 204, 404, 401, 400
- **Response:** { "message": "Campanha deletada com sucesso" }

### PATCH /releases/{releaseId}/redirect-link
- **Descrição:** Altera o slug do link de redirect da campanha. Espaços removidos, salvo em minúsculas. Slug único por campanha.
- **URL params:** releaseId (string, obrigatório)
- **Body params:**
  - slug (string, obrigatório): Novo slug
- **Respostas:** 200, 400, 401, 404, 409 (slug já em uso)
- **Response:** { "message": "Link de redirect atualizado com sucesso", "success": true, "id": "...", "slug": "minha-campanha-vip" }

### GET /releases/{releaseId}/groups
- **Descrição:** Retorna lista de grupos associados à campanha.
- **URL params:** releaseId (string, obrigatório)
- **Respostas:** 200, 404, 401, 400
- **Response:**
```json
[
  { "id": "120363292004848696", "name": "Grupo 1", "gid": "558191080294", "jid": "558191080294", "inviteCode": "123456" }
]
```

### POST /releases/{releaseId}/remove-duplicated-participants ⚠️ EM DESENVOLVIMENTO
- **Descrição:** Cria ação para remover participantes duplicados.
- **Respostas:** 200, 400, 404, 401
- **Response:** { "message": "Ação criada com sucesso", "success": true }

### GET /releases/{releaseId}/analytics
- **Descrição:** Retorna métricas da campanha (adds, removes, clicks por data).
- **Respostas:** 200, 400, 401, 404
- **Response:**
```json
{
  "add": { "dates": { "10072025": 20 }, "total": 100 },
  "remove": { "dates": { "10072025": 3 }, "total": 20 },
  "clicks": { "dates": { "10072025": 130 }, "total": 540 }
}
```

### GET /releases/{releaseId}/leadscoring
- **Descrição:** Gera o leadscoring da campanha.
- **Respostas:** 200, 400, 401, 404
- **Response:** { "success": true }

### GET /releases/{releaseId}/leadscoring/download
- **Descrição:** Retorna URL para download do arquivo de leadscoring (.xlsx).
- **Respostas:** 200, 400, 401, 404
- **Response:** "https://storage.sendflow.pro/leadscoring/.../leadscoring-2025-01-21.xlsx"

---

## 2. GRUPOS DE CAMPANHAS (/sendapi/release-groups)

### POST /sendapi/release-groups
- **Descrição:** Adiciona um grupo a uma campanha.
- **Body params:**
  - gid (string, obrigatório): ID do grupo do WhatsApp (ex: 120363292004848696@g.us)
  - releaseId (string, obrigatório): ID da campanha
  - count (number, opcional): Contagem
  - name (string, obrigatório): Nome do grupo
  - full (boolean, opcional): Se o grupo está cheio
  - type (string, opcional): group | community | community_default | community_group
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Grupo criado com sucesso", "id": "generated_group_id" }

### GET /sendapi/release-groups/{releaseGroupId}
- **Descrição:** Obtém informações detalhadas de um grupo específico.
- **URL params:** releaseGroupId (string, obrigatório)
- **Respostas:** 200, 401, 404
- **Response:**
```json
{
  "id": "release_group_id",
  "gid": "120363292004848696@g.us",
  "userId": "user_id",
  "releaseId": "biuumwkQqFtMcOCbGEgk",
  "count": 1,
  "name": "Teste Send #1",
  "inviteCode": "invite_code",
  "full": false,
  "clicks": 0,
  "clicksAmount": 0,
  "participantsAmount": 0,
  "clicksMap": {}
}
```

### PUT /sendapi/release-groups/{releaseGroupId}
- **Descrição:** Atualiza informações de um grupo. Apenas o proprietário pode atualizar.
- **URL params:** releaseGroupId (string, obrigatório)
- **Body params (opcionais):**
  - count (integer)
  - full (boolean)
  - name (string)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "message": "Grupo atualizado com sucesso", "id": "release_group_id" }

### DELETE /sendapi/release-groups/{releaseGroupId}
- **Descrição:** Remove permanentemente um grupo da campanha. Irreversível.
- **URL params:** releaseGroupId (string, obrigatório)
- **Respostas:** 204, 400, 401, 404
- **Response:** { "message": "Grupo deletado com sucesso" }

---

## 3. AÇÕES (/sendapi/actions)

### POST /sendapi/actions/group-create
- **Descrição:** Cria um novo grupo no WhatsApp com participantes específicos.
- **Body params:**
  - accountId (string, obrigatório): ID da conta
  - releaseId (string, obrigatório): ID da campanha
  - assistantId (string, opcional): ID do assistente
  - payload.name (string, obrigatório): Nome do grupo
  - payload.participants (array, obrigatório): Ex: ["557581133148@s.whatsapp.net"]
  - payload.associatedUserIds (array, opcional): IDs de usuários associados
  - payload.standardization (boolean, opcional, padrão: false)
- **Respostas:** 201, 400, 401, 403, 404, 500
- **Response:** { "message": "Ação de criação de grupo criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/make-group-admin
- **Descrição:** Torna usuários administradores de grupos da campanha.
- **Body params:**
  - accountId (string, obrigatório)
  - releaseId (string, obrigatório)
  - participants (array, obrigatório): [{number: "557581133148", name: "João"}] — SEM @s.whatsapp.net
  - chooseSpecificGroups (boolean, opcional, padrão: false)
  - groupIds (array, opcional): GIDs SEM @g.us — obrigatório se chooseSpecificGroups=true
- **Respostas:** 201, 400, 401, 403, 404, 500
- **Response:** { "message": "Ação de criação de grupo criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/send-text-message
- **Descrição:** Envia mensagem de texto para grupos da campanha.
- **Body params:**
  - accountId (string, opcional*): ID da conta
  - accountIds (array, opcional*): IDs das contas (* fornecer um ou outro, nunca ambos)
  - releaseId (string, obrigatório)
  - messageText (string, obrigatório): Texto a ser enviado
  - linkPreview (boolean, opcional): Gerar preview do link
  - scheduled (boolean, opcional): Se agendado
  - scheduledTo (string, opcional): ISO 8601 ex: "2025-04-21T10:00:00.000Z"
  - chooseSpecificGroups (boolean, opcional, padrão: false)
  - groupIds (array, opcional): GIDs sem @g.us
  - options.shippingSpeed (string): none | fast | normal | slow | custom
  - options.customShippingSpeed.min (integer): segundos
  - options.customShippingSpeed.max (integer): segundos
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Ação criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/send-image-message
- **Descrição:** Envia mensagem com imagem para grupos da campanha.
- **Body params:**
  - accountId ou accountIds (um ou outro, obrigatório)
  - releaseId (string, obrigatório)
  - url (string, obrigatório): URL da imagem
  - caption (string, opcional): Legenda
  - scheduledTo (string, opcional): ISO 8601
  - chooseSpecificGroups (boolean, opcional)
  - groupIds (array, opcional)
  - options.shippingSpeed / options.customShippingSpeed.min / max
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Ação criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/send-video-message
- **Descrição:** Envia mensagem com vídeo para grupos da campanha.
- **Body params:** (igual ao send-image-message mas com URL de vídeo)
  - accountId ou accountIds
  - releaseId (obrigatório)
  - url (string, obrigatório): URL do vídeo
  - caption (string, opcional)
  - scheduledTo, chooseSpecificGroups, groupIds, options (igual)
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Ação criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/send-audio-message
- **Descrição:** Envia mensagem com áudio para grupos da campanha.
- **Body params:**
  - accountId ou accountIds
  - releaseId (obrigatório)
  - url (string, obrigatório): URL do áudio
  - caption (string, opcional)
  - ptt (boolean, opcional): true = nota de voz (push-to-talk), false = arquivo de áudio normal
  - scheduledTo, chooseSpecificGroups, groupIds, options (igual)
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Ação criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/send-message (UNIVERSAL)
- **Descrição:** Envia mensagem de qualquer tipo com configurações avançadas.
- **Body params:**
  - accountId ou accountIds (um ou outro)
  - releaseId (string, obrigatório)
  - type (string, obrigatório): extendedTextMessage | imageMessage | videoMessage | audioMessage
  - text (string, opcional): para extendedTextMessage
  - linkPreview (boolean, opcional): preview de link
  - caption (string, opcional): para imagem/vídeo/áudio
  - url (string, opcional): para imagem/vídeo/áudio
  - ptt (boolean, opcional): true = nota de voz (só para audioMessage)
  - scheduledTo (string, opcional): ISO 8601
  - chooseSpecificGroups (boolean, opcional)
  - groupIds (array, opcional)
  - options.ephemeralExpiration (integer): tempo expiração da mensagem
  - options.mentionAllParticipants (boolean): mencionar todos
  - options.shippingSpeed (string): none | fast | normal | slow | custom
  - options.customShippingSpeed.min / max (integer, segundos)
- **Respostas:** 201, 400, 401
- **Response:** { "message": "Ação criada com sucesso", "id": "action_id_generated" }

### POST /sendapi/actions/analyze-groups
- **Descrição:** Cria ações de refresh de grupos para contas específicas (anti-spam).
- **Body params:**
  - accountIds (array, obrigatório): Se não fornecido, usa todas as contas autenticadas
  - to (string, opcional, padrão: "anti-spam")
- **Respostas:** 200, 400, 401
- **Response:** { "message": "Ação enviada com sucesso!", "actionsCreated": 3 }

### POST /sendapi/actions/find-participant
- **Descrição:** Verifica se número está em algum grupo WhatsApp das campanhas. SÍNCRONO (aguarda resultado até timeout).
- **Body params:**
  - accountId (string, obrigatório): ID da conta WhatsApp
  - phoneNumber (string, obrigatório): Número (com ou sem formatação, será normalizado)
  - timeout (number, opcional, padrão: 60000): ms
- **Respostas:** 200, 400, 401
- **Response sucesso:**
```json
{
  "phoneNumber": "5511987654321",
  "found": true,
  "releases": [{ "releaseId": "...", "groupIds": ["120363405635781177@g.us"] }]
}
```
- **Response não encontrado/timeout:**
```json
{ "phoneNumber": "5511987654321", "found": false, "releases": [], "error": "Timeout ao aguardar resultado da ação" }
```

### Velocidades de Envio (shippingSpeed):
- none: Sem atraso — imediato
- fast: Rápido — entre 10 e 20 segundos
- normal: Normal — entre 40 e 60 segundos
- slow: Lento — entre 60 e 120 segundos
- custom: Personalizado — definir customShippingSpeed.min e max

### Tipos de Mensagem (type em send-message):
- extendedTextMessage: requer "text". Use "linkPreview": true para preview de links
- imageMessage: requer "url" e opcionalmente "caption"
- videoMessage: requer "url" e opcionalmente "caption"
- audioMessage: requer "url" e opcionalmente "caption". Use "ptt": true para nota de voz

### IMPORTANTE sobre Ações:
- accountId OU accountIds (nunca ambos)
- Participantes em group-create: formato "557581133148@s.whatsapp.net"
- Participantes em make-group-admin: apenas número sem formatação
- groupIds em make-group-admin: sem @g.us (ex: "120363420152631339")
- A maioria das ações é assíncrona (retorna ID da ação)
- Exceção: find-participant é síncrono (aguarda resultado até timeout)
- scheduledTo null ou omitido = execução imediata

---

## 4. MENSAGENS DIRETAS (/sendapi) — envio para número específico, não grupos

### POST /sendapi/send-text-message/{accountId}
- **Descrição:** Envia texto diretamente para um número específico.
- **URL params:** accountId (obrigatório)
- **Body params:**
  - text (string, obrigatório)
  - phoneNumber (string, obrigatório): formato 5511987654321
  - scheduledTo (string, opcional): ISO 8601
  - timeout (number, opcional, padrão: 60000)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "success": true }

### POST /sendapi/send-image-message/{accountId}
- **URL params:** accountId (obrigatório)
- **Body params:**
  - url (string, obrigatório): URL da imagem
  - caption (string, opcional)
  - phoneNumber (string, obrigatório)
  - scheduledTo (string, opcional)
  - timeout (number, opcional, padrão: 60000)
- **Response:** { "success": true }

### POST /sendapi/send-video-message/{accountId}
- **URL params:** accountId (obrigatório)
- **Body params:**
  - url (string, obrigatório): URL do vídeo
  - caption (string, opcional)
  - phoneNumber (string, obrigatório)
  - scheduledTo (string, opcional)
  - timeout (number, opcional, padrão: 60000)
- **Response:** { "success": true }

### POST /sendapi/send-audio-message/{accountId}
- **URL params:** accountId (obrigatório)
- **Body params:**
  - url (string, obrigatório): URL do áudio
  - caption (string, opcional)
  - ptt (boolean, opcional): true = nota de voz
  - phoneNumber (string, obrigatório)
  - scheduledTo (string, opcional)
  - timeout (number, opcional, padrão: 60000)
- **Response:** { "success": true }

### Formato de Números (Mensagens Diretas):
- Formato: [código país][código área][número]
- Brasil: 5511987654321 (55 + 11 + 987654321)
- EUA: 14155551234 (1 + 415 + 5551234)
- Sem símbolos: +, -, (, ), espaços

### Tipos de Arquivo Suportados:
- Imagens: image/jpeg, image/png, image/gif, image/webp
- Vídeos: video/mp4, video/avi, video/mov, video/webm
- Áudios: audio/mpeg, audio/wav, audio/ogg, audio/m4a
- MIME type detectado automaticamente pela URL

### Timeout e Execução (Mensagens Diretas):
- Timeout padrão: 60.000ms (60 segundos)
- Retorna { success: true } quando processada ou { success: false } em timeout
- Tamanho máximo de arquivo: 16MB (imagens, vídeos, áudios)

---

## 5. TEMPLATES DE MENSAGENS (/sendapi/message-templates)

### GET /sendapi/message-templates
- **Descrição:** Lista todos os templates do usuário autenticado.
- **Respostas:** 200, 400, 401
- **Response:**
```json
[{
  "id": "abc123def456",
  "userId": "user123",
  "title": "Template de boas-vindas",
  "template": [{ "type": "extendedTextMessage", "message": { "text": "Olá! Bem-vindo!" }, "options": { "ephemeralExpiration": -1 } }],
  "folderId": null,
  "tags": [],
  "position": 0,
  "archived": false,
  "intervalRangeType": "none",
  "intervalRange": [1, 1],
  "createdAt": "2025-01-20T10:00:00.000Z",
  "updatedAt": "2025-01-20T10:00:00.000Z"
}]
```

### POST /sendapi/message-templates
- **Descrição:** Cria um novo template de mensagem. Pode conter múltiplos tipos de mensagem.
- **Body params:**
  - title (string, obrigatório)
  - template (array, obrigatório): Array de objetos de mensagem
  - folderId (string, opcional)
  - intervalRangeType (string, opcional, padrão: "none")
  - intervalRange (array[min, max], opcional, padrão: [1,1]): segundos entre mensagens
  - archived (boolean, opcional, padrão: false)
- **Respostas:** 201, 400, 401
- **Response:** { "id": "abc123def456" }

#### Estrutura do campo "template" (array de mensagens):
**imageMessage:**
```json
{
  "type": "imageMessage",
  "message": {
    "caption": "Legenda",
    "image": { "originalUrl": "url original", "url": "url da imagem" },
    "mimetype": "image/webp"
  },
  "options": { "ephemeralExpiration": -1, "mentionAllParticipants": false }
}
```

**extendedTextMessage:**
```json
{
  "type": "extendedTextMessage",
  "message": { "text": "Texto da mensagem" },
  "options": { "ephemeralExpiration": -1 }
}
```

**videoMessage:**
```json
{
  "type": "videoMessage",
  "message": {
    "video": { "url": "url do vídeo" },
    "caption": "Legenda",
    "mimetype": "video/mp4",
    "gifPlayback": false,
    "width": 1280,
    "height": 720
  },
  "options": { "ephemeralExpiration": -1 }
}
```

**audioMessage:**
```json
{
  "type": "audioMessage",
  "message": {
    "audio": { "url": "url do áudio" },
    "mimetype": "audio/ogg; codecs=opus",
    "ptt": false
  },
  "options": { "ephemeralExpiration": -1 }
}
```

#### Regras do campo template:
- Pode conter quantas mensagens forem necessárias
- Mensagens enviadas na ordem do array
- Pode misturar diferentes tipos no mesmo template
- gifPlayback: true = vídeo enviado como GIF animado (sem som, em loop)
- ptt: true = áudio como nota de voz (reprodução automática)
- ephemeralExpiration: -1 = desabilitar mensagens temporárias

### PUT /sendapi/message-templates/{templateId}
- **URL params:** templateId (obrigatório)
- **Body params (todos opcionais):**
  - title, template, folderId, intervalRangeType, intervalRange, archived, position
- **Respostas:** 200, 400, 401, 404
- **Response:** { "message": "Template atualizado com sucesso", "success": true, "id": "abc123def456" }

### DELETE /sendapi/message-templates/{templateId}
- **URL params:** templateId (obrigatório)
- **Respostas:** 204, 400, 401, 404
- **Response:** { "message": "Template deletado com sucesso" }

### LIMITAÇÃO IMPORTANTE:
- NÃO existe endpoint para disparar um template por templateId
- Para enviar um template: 1) GET /message-templates para buscar, 2) iterar o array "template" e enviar cada mensagem via send-message

---

## 6. CONTAS (/sendapi/accounts)

### POST /sendapi/accounts/create
- **Descrição:** Cria uma nova conta WhatsApp ou Email.
- **Body params:**
  - data.name (string, obrigatório)
  - data.type (string, obrigatório): whatsapp | email
  - data.provider (string, opcional): aws-ses | google-api | gmail (só para email)
  - data.senderName (string, opcional): só para email
  - data.senderEmail (string, opcional): só para email
  - projectId (string, opcional)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "success": true, "id": "conta_id_gerado" }

### GET /sendapi/accounts
- **Descrição:** Lista todas as contas do usuário.
- **Respostas:** 200, 401, 400
- **Response:**
```json
[{
  "id": "conta1",
  "name": "Minha Conta WhatsApp",
  "type": "whatsapp",
  "status": "connected",
  "userId": "user123",
  "projectId": "projeto123",
  "createdAt": "2024-01-01T10:00:00Z"
}]
```

### PUT /sendapi/accounts/{accountId}
- **URL params:** accountId (obrigatório)
- **Body params:**
  - data.name (string, obrigatório)
  - data.type (string, obrigatório)
  - data.provider, data.senderName, data.senderEmail (opcionais, só email)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "success": true, "id": "conta_id" }

### DELETE /sendapi/accounts/{accountId}
- **URL params:** accountId (obrigatório)
- **Respostas:** 204, 401, 404
- **Response:** { "success": true }
- **ATENÇÃO: Irreversível**

### POST /sendapi/accounts/connect-account/{accountId}
- **Descrição:** Inicia conexão WhatsApp e gera QR code.
- **URL params:** accountId (obrigatório)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "success": true, "result": { "status": "connecting", "qrCode": "data:image/png;base64,..." } }

### POST /sendapi/accounts/disconnect-account/{accountId}
- **Descrição:** Desconecta uma conta WhatsApp.
- **URL params:** accountId (obrigatório)
- **Respostas:** 204, 400, 401, 404
- **Response:** { "success": true }

### GET /sendapi/accounts/{accountId}/qrcode
- **Descrição:** Obtém dados da conta incluindo QR code.
- **URL params:** accountId (obrigatório)
- **Respostas:** 200, 401, 404
- **Response:**
```json
{
  "status": "connecting",
  "id": "conta123",
  "qrCode": "2@ABC123...",
  "image": "data:image/png;base64,...",
  "name": "Minha Conta",
  "jid": "5511987654321@s.whatsapp.net",
  "isAuthenticated": false,
  "attempt": 1
}
```

### GET /sendapi/accounts/{accountId}/qrcode-image
- **Descrição:** Retorna imagem PNG do QR code.
- **URL params:** accountId (obrigatório)
- **Respostas:** 200 (Content-Type: image/png), 401, 404

### Status de Contas:
- processing: Criada, processando configurações iniciais
- connecting: Tentando conectar (aguardando QR code)
- connected: Conectada e funcionando normalmente
- disconnected: Desconectada pelo usuário ou por erro
- error: Erro na conexão ou configuração

### Tipos de Conta:
- whatsapp: Para envio de mensagens e gerenciamento de grupos
- email: Para envio de emails (requer configuração de provedor)

### Provedores de Email:
- aws-ses: Amazon Simple Email Service
- google-api: API do Gmail (Google Workspace)
- gmail: Gmail pessoal

### IMPORTANTE sobre Contas:
- accountId é o ID da conta WhatsApp que vai DISPARAR as mensagens
- Para obter accountIds disponíveis: GET /sendapi/accounts
- Endpoint GET /:userId está DESCONTINUADO — usar GET / sem parâmetros

---

## 7. NÚMEROS BLOQUEADOS (/sendapi/block-numbers)

### GET /sendapi/block-numbers
- **Descrição:** Lista todos os números bloqueados do usuário (anti-spam).
- **Respostas:** 200, 400, 401
- **Response:** ["5511987654321", "5511999448421", "5515612313121"]

### POST /sendapi/block-numbers
- **Descrição:** Adiciona número à lista de bloqueados (anti-spam).
- **Body params:**
  - number (string, obrigatório): formato 5511987654321
  - name (string, obrigatório): Nome/identificação do número
- **Respostas:** 200, 400, 401
- **Response:** { "message": "Número bloqueado com sucesso!", "name": "João Silva", "number": "5511987654321" }

### Modelo de Dados Block Number:
- id (string): ID único do bloqueio
- number (string): Número bloqueado (apenas números)
- name (string): Nome/identificação
- userId (string): ID do usuário
- global (boolean): sempre false para bloqueios via API
- createdAt (string): ISO 8601

### Formato de Números:
- Entrada: pode incluir +, -, espaços, parênteses
- Armazenado: apenas números (normalizado automaticamente)
- Ex entrada: "+55 (11) 98765-4321" → armazenado: "5511987654321"

### LIMITAÇÕES:
- NÃO existe endpoint para REMOVER bloqueios via API (apenas criar e listar)
- Escopo individual: cada usuário gerencia sua própria lista

---

## 8. VERIFICAÇÃO DE NÚMEROS (/sendapi/verify-number)

### POST /sendapi/verify-number
- **Descrição:** Verifica se número está bloqueado para uma campanha específica.
- **Body params:**
  - releaseId (string, obrigatório): ID da campanha
  - phoneNumber (string, obrigatório): APENAS números locais SEM código do país
    - Ex Brasil: "81999999999" (sem o 55)
    - Ex SP: "11987654321" (sem o 55)
- **Respostas:** 200, 400, 401, 404
- **Response:** { "response": true } — true = pode receber | false = bloqueado

### Tipos de Bloqueio Verificados:
- Bloqueio do Usuário: números bloqueados pelo dono da campanha
- Bloqueio Global: números bloqueados em todo o sistema
- Lista de Opt-out: usuários que solicitaram não receber mensagens
- Números Inválidos: identificados como inválidos ou problemáticos
- Restrições de Campanha: bloqueios específicos da campanha

### Casos de Uso:
- Pré-validação antes de criar campanhas ou enviar mensagens
- Limpeza de listas de contatos
- Compliance (garantir não enviar para bloqueados/opt-out)
- Auditoria de status de números
- Integração com sistemas externos

### IMPORTANTE sobre Verificação:
- Número SEM código do país (diferente dos endpoints de envio que pedem COM código)
- Contexto sempre ligado a uma campanha (releaseId obrigatório)
- Pode ser chamado múltiplas vezes (otimizado para lote)

---

## CÓDIGOS DE ERRO GERAIS

| Código | Significado |
|--------|-------------|
| 200    | OK — Sucesso |
| 201    | Created — Recurso criado com sucesso |
| 204    | No Content — Deletado com sucesso |
| 400    | Bad Request — Dados inválidos ou parâmetros obrigatórios ausentes |
| 401    | Unauthorized — API Key inválida ou usuário não autorizado |
| 403    | Forbidden — Acesso negado |
| 404    | Not Found — Recurso não encontrado |
| 409    | Conflict — Conflito (ex: slug já em uso) |
| 500    | Internal Server Error — Erro interno do servidor |

---

## LIMITAÇÕES CONHECIDAS DA API

1. NÃO é possível disparar template por templateId (workaround: buscar template e enviar cada mensagem manualmente)
2. NÃO é possível enviar enquetes via API
3. NÃO existe endpoint para remover números da lista de bloqueados
4. NÃO há endpoint para listar admins reais de grupos individuais (apenas admins configurados na campanha via GET /releases/{releaseId})
5. Remoção de participantes duplicados está EM DESENVOLVIMENTO

---

## DICAS GERAIS

- accountId = ID da conta WhatsApp que VAI DISPARAR a mensagem (obter via GET /sendapi/accounts)
- Para saber admins configurados na campanha: GET /releases/{releaseId} → campo group.admins
- Para envio em grupos: usar /sendapi/actions/send-*
- Para envio direto a número: usar /sendapi/send-*/{accountId}
- scheduledTo sempre em ISO 8601: "2025-04-21T10:00:00.000Z"
- find-participant é o único endpoint síncrono nas Actions
- Verificação de número usa formato SEM código do país; envios usam COM código do país
