"""SendFlow SendAPI MCP Server.

Expõe os endpoints da SendAPI (https://sendflow.pro/sendapi) como ferramentas
MCP que o Claude pode invocar diretamente (no Claude Code, Claude Desktop, etc.).

Autenticação: variável de ambiente SENDFLOW_API_KEY (obrigatória).
Base URL configurável via SENDFLOW_BASE_URL (padrão: https://sendflow.pro).

Rodar standalone (debug):
    python server.py

Registrar no Claude Code (ver README.md).
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

BASE_URL = os.getenv("SENDFLOW_BASE_URL", "https://sendflow.pro").rstrip("/")
API_KEY = os.getenv("SENDFLOW_API_KEY", "").strip()
DEFAULT_TIMEOUT = float(os.getenv("SENDFLOW_TIMEOUT", "60"))

mcp = FastMCP("sendflow")


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------
def _headers() -> dict[str, str]:
    if not API_KEY:
        raise RuntimeError(
            "SENDFLOW_API_KEY não está definida. Coloque-a no .env ou exporte "
            "no ambiente antes de iniciar o servidor."
        )
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _request(
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    expect_json: bool = True,
) -> Any:
    """Faz a requisição HTTP e devolve JSON (ou texto) já tratado.

    Em caso de erro HTTP, devolve um dict {"error": ..., "status": ..., "body": ...}
    em vez de levantar exceção — isso facilita o Claude reportar o erro ao usuário.
    """
    url = f"{BASE_URL}{path}"
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.request(
                method,
                url,
                headers=_headers(),
                json=json_body,
                params=params,
            )
    except httpx.HTTPError as exc:
        return {"error": "network_error", "detail": str(exc)}

    if resp.status_code >= 400:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        return {"error": "http_error", "status": resp.status_code, "body": body}

    if resp.status_code == 204 or not resp.content:
        return {"success": True, "status": resp.status_code}

    if not expect_json:
        return {"status": resp.status_code, "content_type": resp.headers.get("content-type"), "text": resp.text}

    try:
        return resp.json()
    except Exception:
        return {"status": resp.status_code, "text": resp.text}


def _drop_none(data: dict[str, Any]) -> dict[str, Any]:
    """Remove chaves com valor None — a SendAPI às vezes valida presença."""
    return {k: v for k, v in data.items() if v is not None}


# ---------------------------------------------------------------------------
# 1. CAMPANHAS (/releases)
# ---------------------------------------------------------------------------
@mcp.tool()
def list_campaigns() -> Any:
    """Lista todas as campanhas (releases) do usuário autenticado."""
    return _request("GET", "/sendapi/releases")


@mcp.tool()
def create_campaign(name: str, type: str = "WhatsRelease", projectId: str | None = None) -> Any:
    """Cria uma nova campanha.

    Args:
        name: Nome da campanha.
        type: WhatsRelease | WhatsList | WhatsViralCampaign.
        projectId: ID do projeto (opcional).
    """
    return _request(
        "POST",
        "/sendapi/releases",
        json_body=_drop_none({"name": name, "type": type, "projectId": projectId}),
    )


@mcp.tool()
def get_campaign(releaseId: str) -> Any:
    """Retorna detalhes de uma campanha específica."""
    return _request("GET", f"/sendapi/releases/{releaseId}")


@mcp.tool()
def update_campaign(releaseId: str, fields: dict[str, Any]) -> Any:
    """Atualiza uma campanha existente.

    Args:
        releaseId: ID da campanha.
        fields: Dicionário com campos a atualizar (name, accountIds, archived,
            group, position, projectId, type, deepLinking, ...).
    """
    return _request("PUT", f"/sendapi/releases/{releaseId}", json_body=fields)


@mcp.tool()
def delete_campaign(releaseId: str) -> Any:
    """Remove permanentemente uma campanha."""
    return _request("DELETE", f"/sendapi/releases/{releaseId}")


@mcp.tool()
def update_campaign_redirect_slug(releaseId: str, slug: str) -> Any:
    """Altera o slug do link de redirect da campanha."""
    return _request(
        "PATCH",
        f"/sendapi/releases/{releaseId}/redirect-link",
        json_body={"slug": slug},
    )


@mcp.tool()
def get_campaign_groups(releaseId: str) -> Any:
    """Lista os grupos associados à campanha."""
    return _request("GET", f"/sendapi/releases/{releaseId}/groups")


@mcp.tool()
def get_campaign_analytics(releaseId: str) -> Any:
    """Retorna métricas (adds, removes, clicks por data) de uma campanha."""
    return _request("GET", f"/sendapi/releases/{releaseId}/analytics")


@mcp.tool()
def generate_campaign_leadscoring(releaseId: str) -> Any:
    """Gera o leadscoring da campanha."""
    return _request("GET", f"/sendapi/releases/{releaseId}/leadscoring")


@mcp.tool()
def download_campaign_leadscoring(releaseId: str) -> Any:
    """Retorna URL para download do arquivo de leadscoring (.xlsx)."""
    return _request("GET", f"/sendapi/releases/{releaseId}/leadscoring/download")


# ---------------------------------------------------------------------------
# 2. GRUPOS DE CAMPANHAS (/sendapi/release-groups)
# ---------------------------------------------------------------------------
@mcp.tool()
def add_release_group(
    releaseId: str,
    gid: str,
    name: str,
    count: int | None = None,
    full: bool | None = None,
    type: str | None = None,
) -> Any:
    """Adiciona um grupo a uma campanha.

    Args:
        releaseId: ID da campanha.
        gid: ID do grupo do WhatsApp (ex: 120363292004848696@g.us).
        name: Nome do grupo.
        count: Contagem (opcional).
        full: Se o grupo está cheio (opcional).
        type: group | community | community_default | community_group.
    """
    return _request(
        "POST",
        "/sendapi/release-groups",
        json_body=_drop_none(
            {
                "releaseId": releaseId,
                "gid": gid,
                "name": name,
                "count": count,
                "full": full,
                "type": type,
            }
        ),
    )


@mcp.tool()
def get_release_group(releaseGroupId: str) -> Any:
    """Obtém informações detalhadas de um grupo da campanha."""
    return _request("GET", f"/sendapi/release-groups/{releaseGroupId}")


@mcp.tool()
def update_release_group(
    releaseGroupId: str,
    count: int | None = None,
    full: bool | None = None,
    name: str | None = None,
) -> Any:
    """Atualiza um grupo da campanha (apenas campos fornecidos)."""
    body = _drop_none({"count": count, "full": full, "name": name})
    return _request("PUT", f"/sendapi/release-groups/{releaseGroupId}", json_body=body)


@mcp.tool()
def delete_release_group(releaseGroupId: str) -> Any:
    """Remove permanentemente um grupo da campanha. Irreversível."""
    return _request("DELETE", f"/sendapi/release-groups/{releaseGroupId}")


# ---------------------------------------------------------------------------
# 3. AÇÕES (/sendapi/actions) — envio em grupos da campanha
# ---------------------------------------------------------------------------
def _require_one_account(accountId: str | None, accountIds: list[str] | None) -> dict[str, Any]:
    if accountId and accountIds:
        raise ValueError("Forneça accountId OU accountIds, nunca ambos.")
    if accountId:
        return {"accountId": accountId}
    if accountIds:
        return {"accountIds": accountIds}
    raise ValueError("É obrigatório informar accountId ou accountIds.")


@mcp.tool()
def send_text_to_campaign(
    releaseId: str,
    messageText: str,
    accountId: str | None = None,
    accountIds: list[str] | None = None,
    linkPreview: bool | None = None,
    scheduledTo: str | None = None,
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
    shippingSpeed: str | None = None,
    customShippingSpeedMin: int | None = None,
    customShippingSpeedMax: int | None = None,
) -> Any:
    """Envia mensagem de texto para grupos de uma campanha.

    Args:
        releaseId: ID da campanha.
        messageText: Texto da mensagem.
        accountId / accountIds: forneça um dos dois (não ambos).
        linkPreview: se True, gera preview do link.
        scheduledTo: ISO 8601, ex "2025-04-21T10:00:00.000Z".
        chooseSpecificGroups: se True, usa groupIds informado.
        groupIds: lista de GIDs SEM @g.us.
        shippingSpeed: none | fast | normal | slow | custom.
        customShippingSpeedMin / Max: segundos (quando shippingSpeed="custom").
    """
    body: dict[str, Any] = {"releaseId": releaseId, "messageText": messageText}
    body.update(_require_one_account(accountId, accountIds))
    body.update(
        _drop_none(
            {
                "linkPreview": linkPreview,
                "scheduledTo": scheduledTo,
                "chooseSpecificGroups": chooseSpecificGroups,
                "groupIds": groupIds,
            }
        )
    )
    options = _drop_none(
        {
            "shippingSpeed": shippingSpeed,
            "customShippingSpeed": _drop_none(
                {"min": customShippingSpeedMin, "max": customShippingSpeedMax}
            )
            or None,
        }
    )
    if options:
        body["options"] = options
    return _request("POST", "/sendapi/actions/send-text-message", json_body=body)


@mcp.tool()
def send_image_to_campaign(
    releaseId: str,
    url: str,
    accountId: str | None = None,
    accountIds: list[str] | None = None,
    caption: str | None = None,
    scheduledTo: str | None = None,
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
    shippingSpeed: str | None = None,
) -> Any:
    """Envia imagem para grupos de uma campanha."""
    body: dict[str, Any] = {"releaseId": releaseId, "url": url}
    body.update(_require_one_account(accountId, accountIds))
    body.update(
        _drop_none(
            {
                "caption": caption,
                "scheduledTo": scheduledTo,
                "chooseSpecificGroups": chooseSpecificGroups,
                "groupIds": groupIds,
            }
        )
    )
    if shippingSpeed:
        body["options"] = {"shippingSpeed": shippingSpeed}
    return _request("POST", "/sendapi/actions/send-image-message", json_body=body)


@mcp.tool()
def send_video_to_campaign(
    releaseId: str,
    url: str,
    accountId: str | None = None,
    accountIds: list[str] | None = None,
    caption: str | None = None,
    scheduledTo: str | None = None,
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
    shippingSpeed: str | None = None,
) -> Any:
    """Envia vídeo para grupos de uma campanha."""
    body: dict[str, Any] = {"releaseId": releaseId, "url": url}
    body.update(_require_one_account(accountId, accountIds))
    body.update(
        _drop_none(
            {
                "caption": caption,
                "scheduledTo": scheduledTo,
                "chooseSpecificGroups": chooseSpecificGroups,
                "groupIds": groupIds,
            }
        )
    )
    if shippingSpeed:
        body["options"] = {"shippingSpeed": shippingSpeed}
    return _request("POST", "/sendapi/actions/send-video-message", json_body=body)


@mcp.tool()
def send_audio_to_campaign(
    releaseId: str,
    url: str,
    accountId: str | None = None,
    accountIds: list[str] | None = None,
    caption: str | None = None,
    ptt: bool | None = None,
    scheduledTo: str | None = None,
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
    shippingSpeed: str | None = None,
) -> Any:
    """Envia áudio para grupos de uma campanha. ptt=True = nota de voz."""
    body: dict[str, Any] = {"releaseId": releaseId, "url": url}
    body.update(_require_one_account(accountId, accountIds))
    body.update(
        _drop_none(
            {
                "caption": caption,
                "ptt": ptt,
                "scheduledTo": scheduledTo,
                "chooseSpecificGroups": chooseSpecificGroups,
                "groupIds": groupIds,
            }
        )
    )
    if shippingSpeed:
        body["options"] = {"shippingSpeed": shippingSpeed}
    return _request("POST", "/sendapi/actions/send-audio-message", json_body=body)


@mcp.tool()
def send_universal_message(
    releaseId: str,
    type: str,
    accountId: str | None = None,
    accountIds: list[str] | None = None,
    text: str | None = None,
    linkPreview: bool | None = None,
    caption: str | None = None,
    url: str | None = None,
    ptt: bool | None = None,
    scheduledTo: str | None = None,
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
    ephemeralExpiration: int | None = None,
    mentionAllParticipants: bool | None = None,
    shippingSpeed: str | None = None,
    customShippingSpeedMin: int | None = None,
    customShippingSpeedMax: int | None = None,
) -> Any:
    """Envio universal — equivalente ao POST /sendapi/actions/send-message.

    type: extendedTextMessage | imageMessage | videoMessage | audioMessage.
    """
    body: dict[str, Any] = {"releaseId": releaseId, "type": type}
    body.update(_require_one_account(accountId, accountIds))
    body.update(
        _drop_none(
            {
                "text": text,
                "linkPreview": linkPreview,
                "caption": caption,
                "url": url,
                "ptt": ptt,
                "scheduledTo": scheduledTo,
                "chooseSpecificGroups": chooseSpecificGroups,
                "groupIds": groupIds,
            }
        )
    )
    options = _drop_none(
        {
            "ephemeralExpiration": ephemeralExpiration,
            "mentionAllParticipants": mentionAllParticipants,
            "shippingSpeed": shippingSpeed,
            "customShippingSpeed": _drop_none(
                {"min": customShippingSpeedMin, "max": customShippingSpeedMax}
            )
            or None,
        }
    )
    if options:
        body["options"] = options
    return _request("POST", "/sendapi/actions/send-message", json_body=body)


@mcp.tool()
def create_group_action(
    accountId: str,
    releaseId: str,
    name: str,
    participants: list[str],
    assistantId: str | None = None,
    associatedUserIds: list[str] | None = None,
    standardization: bool | None = None,
) -> Any:
    """Cria um novo grupo no WhatsApp via ação (assíncrono).

    participants: formato "557581133148@s.whatsapp.net".
    """
    payload = _drop_none(
        {
            "name": name,
            "participants": participants,
            "associatedUserIds": associatedUserIds,
            "standardization": standardization,
        }
    )
    body = _drop_none(
        {
            "accountId": accountId,
            "releaseId": releaseId,
            "assistantId": assistantId,
            "payload": payload,
        }
    )
    return _request("POST", "/sendapi/actions/group-create", json_body=body)


@mcp.tool()
def make_group_admin(
    accountId: str,
    releaseId: str,
    participants: list[dict[str, str]],
    chooseSpecificGroups: bool | None = None,
    groupIds: list[str] | None = None,
) -> Any:
    """Torna usuários administradores de grupos da campanha.

    participants: [{"number": "557581133148", "name": "João"}] — SEM @s.whatsapp.net.
    groupIds: GIDs sem @g.us (obrigatório se chooseSpecificGroups=True).
    """
    body = _drop_none(
        {
            "accountId": accountId,
            "releaseId": releaseId,
            "participants": participants,
            "chooseSpecificGroups": chooseSpecificGroups,
            "groupIds": groupIds,
        }
    )
    return _request("POST", "/sendapi/actions/make-group-admin", json_body=body)


@mcp.tool()
def analyze_groups(accountIds: list[str] | None = None, to: str | None = None) -> Any:
    """Cria ações de refresh de grupos (anti-spam)."""
    body = _drop_none({"accountIds": accountIds, "to": to})
    return _request("POST", "/sendapi/actions/analyze-groups", json_body=body)


@mcp.tool()
def find_participant(accountId: str, phoneNumber: str, timeout: int | None = None) -> Any:
    """Verifica se um número está em algum grupo das campanhas (síncrono)."""
    body = _drop_none(
        {"accountId": accountId, "phoneNumber": phoneNumber, "timeout": timeout}
    )
    return _request("POST", "/sendapi/actions/find-participant", json_body=body)


# ---------------------------------------------------------------------------
# 4. MENSAGENS DIRETAS (/sendapi/send-*/{accountId})
# ---------------------------------------------------------------------------
@mcp.tool()
def send_direct_text(
    accountId: str,
    phoneNumber: str,
    text: str,
    scheduledTo: str | None = None,
    timeout: int | None = None,
) -> Any:
    """Envia texto diretamente para um número (não grupo)."""
    body = _drop_none(
        {
            "text": text,
            "phoneNumber": phoneNumber,
            "scheduledTo": scheduledTo,
            "timeout": timeout,
        }
    )
    return _request("POST", f"/sendapi/send-text-message/{accountId}", json_body=body)


@mcp.tool()
def send_direct_image(
    accountId: str,
    phoneNumber: str,
    url: str,
    caption: str | None = None,
    scheduledTo: str | None = None,
    timeout: int | None = None,
) -> Any:
    """Envia imagem diretamente para um número."""
    body = _drop_none(
        {
            "url": url,
            "caption": caption,
            "phoneNumber": phoneNumber,
            "scheduledTo": scheduledTo,
            "timeout": timeout,
        }
    )
    return _request("POST", f"/sendapi/send-image-message/{accountId}", json_body=body)


@mcp.tool()
def send_direct_video(
    accountId: str,
    phoneNumber: str,
    url: str,
    caption: str | None = None,
    scheduledTo: str | None = None,
    timeout: int | None = None,
) -> Any:
    """Envia vídeo diretamente para um número."""
    body = _drop_none(
        {
            "url": url,
            "caption": caption,
            "phoneNumber": phoneNumber,
            "scheduledTo": scheduledTo,
            "timeout": timeout,
        }
    )
    return _request("POST", f"/sendapi/send-video-message/{accountId}", json_body=body)


@mcp.tool()
def send_direct_audio(
    accountId: str,
    phoneNumber: str,
    url: str,
    caption: str | None = None,
    ptt: bool | None = None,
    scheduledTo: str | None = None,
    timeout: int | None = None,
) -> Any:
    """Envia áudio diretamente para um número. ptt=True = nota de voz."""
    body = _drop_none(
        {
            "url": url,
            "caption": caption,
            "ptt": ptt,
            "phoneNumber": phoneNumber,
            "scheduledTo": scheduledTo,
            "timeout": timeout,
        }
    )
    return _request("POST", f"/sendapi/send-audio-message/{accountId}", json_body=body)


# ---------------------------------------------------------------------------
# 5. TEMPLATES DE MENSAGENS (/sendapi/message-templates)
# ---------------------------------------------------------------------------
@mcp.tool()
def list_message_templates() -> Any:
    """Lista todos os templates de mensagem do usuário."""
    return _request("GET", "/sendapi/message-templates")


@mcp.tool()
def create_message_template(
    title: str,
    template: list[dict[str, Any]],
    folderId: str | None = None,
    intervalRangeType: str | None = None,
    intervalRange: list[int] | None = None,
    archived: bool | None = None,
) -> Any:
    """Cria um novo template de mensagem.

    template: lista de objetos (extendedTextMessage, imageMessage,
    videoMessage, audioMessage). Ver docs da SendAPI.
    """
    body = _drop_none(
        {
            "title": title,
            "template": template,
            "folderId": folderId,
            "intervalRangeType": intervalRangeType,
            "intervalRange": intervalRange,
            "archived": archived,
        }
    )
    return _request("POST", "/sendapi/message-templates", json_body=body)


@mcp.tool()
def update_message_template(templateId: str, fields: dict[str, Any]) -> Any:
    """Atualiza um template. fields pode conter title, template, folderId,
    intervalRangeType, intervalRange, archived, position."""
    return _request(
        "PUT", f"/sendapi/message-templates/{templateId}", json_body=fields
    )


@mcp.tool()
def delete_message_template(templateId: str) -> Any:
    """Remove um template de mensagem."""
    return _request("DELETE", f"/sendapi/message-templates/{templateId}")


# ---------------------------------------------------------------------------
# 6. CONTAS (/sendapi/accounts)
# ---------------------------------------------------------------------------
@mcp.tool()
def list_accounts() -> Any:
    """Lista todas as contas (WhatsApp/Email) do usuário."""
    return _request("GET", "/sendapi/accounts")


@mcp.tool()
def create_account(
    name: str,
    type: str,
    provider: str | None = None,
    senderName: str | None = None,
    senderEmail: str | None = None,
    projectId: str | None = None,
) -> Any:
    """Cria uma nova conta (whatsapp | email)."""
    data = _drop_none(
        {
            "name": name,
            "type": type,
            "provider": provider,
            "senderName": senderName,
            "senderEmail": senderEmail,
        }
    )
    body = _drop_none({"data": data, "projectId": projectId})
    return _request("POST", "/sendapi/accounts/create", json_body=body)


@mcp.tool()
def update_account(
    accountId: str,
    name: str,
    type: str,
    provider: str | None = None,
    senderName: str | None = None,
    senderEmail: str | None = None,
) -> Any:
    """Atualiza uma conta existente."""
    data = _drop_none(
        {
            "name": name,
            "type": type,
            "provider": provider,
            "senderName": senderName,
            "senderEmail": senderEmail,
        }
    )
    return _request("PUT", f"/sendapi/accounts/{accountId}", json_body={"data": data})


@mcp.tool()
def delete_account(accountId: str) -> Any:
    """Remove permanentemente uma conta. IRREVERSÍVEL."""
    return _request("DELETE", f"/sendapi/accounts/{accountId}")


@mcp.tool()
def connect_account(accountId: str) -> Any:
    """Inicia conexão WhatsApp e gera QR code."""
    return _request("POST", f"/sendapi/accounts/connect-account/{accountId}")


@mcp.tool()
def disconnect_account(accountId: str) -> Any:
    """Desconecta uma conta WhatsApp."""
    return _request("POST", f"/sendapi/accounts/disconnect-account/{accountId}")


@mcp.tool()
def get_account_qrcode(accountId: str) -> Any:
    """Obtém dados da conta incluindo QR code (base64 PNG em `image`)."""
    return _request("GET", f"/sendapi/accounts/{accountId}/qrcode")


# ---------------------------------------------------------------------------
# 7. NÚMEROS BLOQUEADOS (/sendapi/block-numbers)
# ---------------------------------------------------------------------------
@mcp.tool()
def list_blocked_numbers() -> Any:
    """Lista todos os números bloqueados (anti-spam)."""
    return _request("GET", "/sendapi/block-numbers")


@mcp.tool()
def block_number(number: str, name: str) -> Any:
    """Adiciona número à lista de bloqueados.

    number: formato 5511987654321 (pode incluir símbolos que são normalizados).
    name: identificação do número.
    """
    return _request(
        "POST", "/sendapi/block-numbers", json_body={"number": number, "name": name}
    )


# ---------------------------------------------------------------------------
# 8. VERIFICAÇÃO DE NÚMERO (/sendapi/verify-number)
# ---------------------------------------------------------------------------
@mcp.tool()
def verify_number(releaseId: str, phoneNumber: str) -> Any:
    """Verifica se um número está bloqueado/válido para uma campanha.

    phoneNumber: SEM código do país (ex: "11987654321", não "5511987654321").
    Retorna { "response": true } se pode receber, false caso contrário.
    """
    return _request(
        "POST",
        "/sendapi/verify-number",
        json_body={"releaseId": releaseId, "phoneNumber": phoneNumber},
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
