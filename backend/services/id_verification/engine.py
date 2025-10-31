# backend/services/id_verification/engine.py
from typing import Dict, Any, Optional

from .denmark import verify_denmark_cpr
from .sweden import verify_sweden_spar
from .norway import verify_norway_registry
from .finland import verify_finland_registry


def normalize_country(country: Optional[str]) -> str:
    if not country:
        return "denmark"
    c = country.lower()
    if c in ("dk", "danmark", "denmark"):
        return "denmark"
    if c in ("se", "sweden", "sverige"):
        return "sweden"
    if c in ("no", "norway", "norge"):
        return "norway"
    if c in ("fi", "finland", "suomi"):
        return "finland"
    return "denmark"  # default for POC


def verify_identity(national_id: str, country: str) -> Dict[str, Any]:
    """
    Central, reusable verification entrypoint.
    Everything (upload endpoint, agent tool, future services) should call THIS.

    Returns dict:
    {
      "status": "approved" | "rejected",
      "reason": "...",
      "registry_record": { ... } | None,
      "source": "denmark" | "sweden" | ...
    }
    """
    c = normalize_country(country)

    if c == "denmark":
        return verify_denmark_cpr(national_id)
    elif c == "sweden":
        return verify_sweden_spar(national_id)
    elif c == "norway":
        return verify_norway_registry(national_id)
    elif c == "finland":
        return verify_finland_registry(national_id)

    # fallback
    return {
        "status": "rejected",
        "reason": f"Unsupported country: {country}",
        "registry_record": None,
        "source": "unknown",
    }
