# SendFlow MCP Server

Servidor MCP em Python que expõe a **SendAPI** da SendFlow como ferramentas
nativas do Claude (Claude Code no VS Code, Claude Desktop, etc.).

Com isso você pode, dentro do Claude, pedir coisas como:

> "Liste minhas campanhas", "Mande a mensagem X para a campanha Y", "Qual o analytics da campanha Z?", "Bloqueie o número 5511..." — e o Claude chama a SendAPI diretamente.

## 1. Requisitos

- Python 3.10 ou superior (`python3 --version` para checar)
- Uma API Key da SendFlow. Se não tiver, siga: https://dubble.so/guides/sendia-criando-o-token-api-vgujvjqox8vatfjhhemw

## 2. Instalação

```bash
# entre na pasta
cd sendflow-mcp

# crie o ambiente virtual
python3 -m venv .venv

# ative o venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

# instale as dependências
pip install -r requirements.txt

# configure a API key
cp .env.example .env
# depois abra .env e coloque sua SENDFLOW_API_KEY
```

Para testar se o servidor sobe sem erro:

```bash
python server.py
```

Se não imprimir nada e ficar "parado", está correto — servidores MCP ficam
aguardando stdio. Encerre com `Ctrl+C`.

## 3. Registrar o MCP no Claude Code (VS Code)

O Claude Code lê configurações de MCP em dois lugares:

- `~/.claude/mcp.json` (global, vale para todos os projetos)
- `.mcp.json` dentro do projeto (vale só para aquele projeto)

Use o arquivo `.mcp.example.json` como base. Copie para `.mcp.json` e edite
o caminho absoluto do Python e do `server.py`:

```json
{
  "mcpServers": {
    "sendflow": {
      "command": "/CAMINHO/ABSOLUTO/sendflow-mcp/.venv/bin/python",
      "args": ["/CAMINHO/ABSOLUTO/sendflow-mcp/server.py"],
      "env": {
        "SENDFLOW_API_KEY": "send_api-coloque_sua_chave_aqui"
      }
    }
  }
}
```

Dica: descubra o caminho absoluto rodando `pwd` dentro da pasta. No Windows,
use `where python` com o venv ativo para achar o Python.

Depois de salvar, abra o Claude Code no VS Code e você deve ver o servidor
`sendflow` na lista de MCPs. O próprio Claude Code pede aprovação para habilitar
cada ferramenta nova.

Alternativa via CLI (sem editar JSON manualmente):

```bash
claude mcp add sendflow \
  /CAMINHO/ABSOLUTO/sendflow-mcp/.venv/bin/python \
  /CAMINHO/ABSOLUTO/sendflow-mcp/server.py \
  --env SENDFLOW_API_KEY=send_api-coloque_sua_chave_aqui
```

## 4. Registrar no Claude Desktop

Edite o arquivo de config do Claude Desktop:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Use `claude_desktop_config.example.json` como base — mesmo formato do
`.mcp.json`. Reinicie o Claude Desktop depois de salvar.

## 5. Ferramentas disponíveis

### Campanhas (releases)
- `list_campaigns`, `create_campaign`, `get_campaign`, `update_campaign`, `delete_campaign`
- `update_campaign_redirect_slug`, `get_campaign_groups`, `get_campaign_analytics`
- `generate_campaign_leadscoring`, `download_campaign_leadscoring`

### Grupos de campanhas
- `add_release_group`, `get_release_group`, `update_release_group`, `delete_release_group`

### Envio em grupos (ações)
- `send_text_to_campaign`, `send_image_to_campaign`, `send_video_to_campaign`, `send_audio_to_campaign`
- `send_universal_message`
- `create_group_action`, `make_group_admin`, `analyze_groups`, `find_participant`

### Envio direto a número
- `send_direct_text`, `send_direct_image`, `send_direct_video`, `send_direct_audio`

### Templates
- `list_message_templates`, `create_message_template`, `update_message_template`, `delete_message_template`

### Contas
- `list_accounts`, `create_account`, `update_account`, `delete_account`
- `connect_account`, `disconnect_account`, `get_account_qrcode`

### Números bloqueados e verificação
- `list_blocked_numbers`, `block_number`, `verify_number`

## 6. Teste rápido depois de registrado

Abra o Claude Code/Desktop e peça:

> "Usando a ferramenta sendflow, liste minhas contas de WhatsApp."

O Claude vai chamar `list_accounts` e mostrar o resultado da SendAPI.

Se você já usava o cenário do Make, o `releaseId = vD4pBj9V3BfoblAgo197` e o
`accountId = hgMQJEPpIQk9ZZh9UNQ2` continuam válidos para testar envios em
grupo com `send_text_to_campaign`.

## 7. Troubleshooting

**`SENDFLOW_API_KEY não está definida`** — confira se o `.env` existe na pasta
ou se você colocou a chave no campo `env` do `.mcp.json`. A key no `.mcp.json`
tem precedência.

**`401 Unauthorized`** — API key inválida ou expirada. Gere uma nova no
SendFlow e atualize.

**Claude Code não lista as ferramentas** — verifique se o caminho do Python
e do `server.py` no `.mcp.json` são absolutos e existem. Rode `python server.py`
na mão para conferir que sobe sem erro.

**Socket error / network** — a SendAPI pode ter limites de rate; tente com
timeout maior (`SENDFLOW_TIMEOUT=120` no `.env`).

## 8. Segurança

- Nunca commite `.env` — o `.gitignore` já está configurado.
- Se sua API key vazar, gere uma nova no SendFlow e atualize tanto o `.env`
  quanto qualquer lugar onde ela esteja (Make, outros scripts).
