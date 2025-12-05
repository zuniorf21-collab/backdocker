import re
from django.core.exceptions import ValidationError

CPF_REGEX = re.compile(r"^\d{11}$")


def validate_cpf(value: str) -> str:
    """
    Basic CPF validator (only length/digits). Real CPF checksum should be added for production.
    """
    if not value:
        raise ValidationError("CPF obrigatório")
    digits = re.sub(r"\D", "", value)
    if not CPF_REGEX.match(digits):
        raise ValidationError("CPF inválido")
    return digits


def mask_payload(payload: dict) -> dict:
    """
    Recursively mask sensitive fields and token-looking strings.
    """
    if not isinstance(payload, dict):
        if isinstance(payload, str) and len(payload.split(".")) == 3:
            return "***"
        return payload

    masked = {}
    for key, value in payload.items():
        if key.lower() in ["password", "senha", "token", "authorization", "jwt"]:
            masked[key] = "***"
        elif isinstance(value, dict):
            masked[key] = mask_payload(value)
        elif isinstance(value, list):
            masked[key] = [mask_payload(v) for v in value]
        else:
            masked[key] = value
    return masked
