import uuid
from typing import Tuple

from django.conf import settings
from twilio.base.exceptions import TwilioException
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client


class TwilioVideoError(Exception):
    """Erro generico para falhas de video."""


class TwilioNotConfigured(TwilioVideoError):
    """Indica que o Twilio nao esta habilitado/ajustado."""


def _client() -> Client:
    if not is_configured():
        raise TwilioNotConfigured("Twilio nao configurado.")
    if settings.TWILIO_AUTH_TOKEN:
        return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return Client(settings.TWILIO_API_KEY_SID, settings.TWILIO_API_KEY_SECRET, settings.TWILIO_ACCOUNT_SID)


def is_configured() -> bool:
    return bool(
        getattr(settings, "TWILIO_ENABLED", False)
        and settings.TWILIO_ACCOUNT_SID
        and settings.TWILIO_API_KEY_SID
        and settings.TWILIO_API_KEY_SECRET
    )


def create_room_and_token(identity: str) -> Tuple[str, str]:
    """
    Cria uma sala de video e retorna (room_name, jwt_token).
    Lanca TwilioVideoError caso algo falhe.
    """
    try:
        client = _client()
        room_name = f"room-{uuid.uuid4().hex[:12]}"
        room = client.video.v1.rooms.create(
            unique_name=room_name,
            type=getattr(settings, "TWILIO_ROOM_TYPE", "go"),
        )
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY_SID,
            settings.TWILIO_API_KEY_SECRET,
            identity=identity,
        )
        token.add_grant(VideoGrant(room=room.unique_name))
        jwt_bytes = token.to_jwt()
        jwt_str = jwt_bytes.decode("utf-8") if hasattr(jwt_bytes, "decode") else jwt_bytes
        return room.unique_name, jwt_str
    except TwilioNotConfigured as exc:
        raise exc
    except TwilioException as exc:
        raise TwilioVideoError(str(exc)) from exc
