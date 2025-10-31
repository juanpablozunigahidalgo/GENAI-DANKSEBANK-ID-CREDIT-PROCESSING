# backend/utils/tools.py

from typing import Dict, Any
from langchain.tools import Tool

from backend.utils.langchain_setup import load_vectorstore
# if you want to use the separate engine instead of the inline mock, you can also:
# from backend.services.id_verification import verify_identity

# ----------------------------------------------------------
# Shared in-memory store for uploaded IDs
# ----------------------------------------------------------
# Every time /upload-id is called, we store the parsed ID here
# so that the agent can later read it with GetUploadedId.
UPLOADED_IDS: Dict[str, Dict[str, Any]] = {}

# ----------------------------------------------------------
# 1) Fake “GetVerifiedUser” tool
# ----------------------------------------------------------
def fetch_user_info() -> str:
    """
    Mock tool. In real life it would read from your customer DB.
    We keep it so the agent has something to call when it wants to
    “retrieve the verified customer”.
    """
    return "User: John Doe, CPR: 123456-7890, verified for Denmark."

get_user_data_tool = Tool(
    name="GetVerifiedUser",
    func=fetch_user_info,
    description="Use this only AFTER the user has uploaded their ID to retrieve their verified data.",
)

# ----------------------------------------------------------
# 2) Search in business procedures (PDF → FAISS)
# ----------------------------------------------------------
def search_procedure(query: str) -> str:
    try:
        vs = load_vectorstore()
    except Exception:
        return "Knowledge base not ready. Please ingest the PDF documents first."
    docs = vs.similarity_search(query, k=4)
    return "\n\n".join([d.page_content for d in docs])

search_docs_tool = Tool(
    name="SearchBusinessProcedures",
    func=search_procedure,
    description=(
        "Use this to answer questions about required documents, branches, "
        "or country-specific onboarding rules (Denmark, Sweden, Norway, Finland)."
    ),
)

# ----------------------------------------------------------
# 3) GetUploadedId tool
# ----------------------------------------------------------
def get_uploaded_id_for_user(user_id: str) -> str:
    """
    Return the parsed/verified ID for a given user_id.
    The agent must pass the SAME user_id the frontend used in /upload-id.
    """
    data = UPLOADED_IDS.get(user_id)
    if not data:
        return "No ID uploaded yet for this user."
    return str(data)

get_uploaded_id_tool = Tool(
    name="GetUploadedId",
    func=get_uploaded_id_for_user,
    description=(
        "Use this to retrieve the parsed/verified ID data for the current user. "
        "You MUST pass the correct user_id. The response can include a "
        "`verification` field if the backend has already checked the ID "
        "against the national registry."
    ),
)

# ----------------------------------------------------------
# 4) (Optional) Inline mock national registry verifier
#     — you can keep it OR delete it now that we moved the real
#       verification to backend/services/id_verification
# ----------------------------------------------------------
def verify_national_registry(national_id: str, country: str | None) -> Dict[str, Any]:
    """
    Mock verification: simple deterministic rule for POC.
    - if national_id ends with even digit -> approved
    - if national_id ends with odd digit  -> rejected
    """
    resp: Dict[str, Any] = {"status": "rejected", "reason": "Could not match national registry."}
    if not national_id:
        return resp

    last_char = national_id.strip()[-1]
    if last_char.isdigit():
        if int(last_char) % 2 == 0:
            resp = {"status": "approved", "reason": "Matched national registry (POC)."}
        else:
            resp = {"status": "rejected", "reason": "Registry mismatch (POC)."}

    if resp["status"] == "approved":
        resp["registry_record"] = {
            "firstName": "John",
            "lastName": "Doe",
            "dateOfBirth": "1975-01-01",
            "address": "POC Street 1, Copenhagen",
            "citizenship": [country or "Denmark"],
        }
    return resp


def _verify_national_registry_tool_impl(args: str):
    """
    Tool adapter: expects a JSON string or a plain national id.
    Examples:
      - "123456-7890"
      - '{"national_id":"123456-7890","country":"Denmark"}'
    """
    import json as _json
    try:
        parsed = _json.loads(args)
        national_id = parsed.get("national_id") or parsed.get("id") or parsed.get("cpr")
        country = parsed.get("country")
    except Exception:
        national_id = args
        country = None

    result = verify_national_registry(str(national_id or ""), country)
    return result


VerifyNationalRegistryTool = Tool(
    name="VerifyNationalRegistry",
    func=_verify_national_registry_tool_impl,
    description=(
        "Verify a national id (CPR or national number) against the national registry. "
        "Input: national id string or JSON with {national_id, country}. "
        "Returns: dict with status ('approved' or 'rejected') and optional details."
    ),
)
