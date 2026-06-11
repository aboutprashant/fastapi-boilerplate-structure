from typing import Annotated

import jwt
from contracts import ScopeObject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from kb.core.config import Settings, get_settings
from kb.core.errors import ForbiddenError

bearer = HTTPBearer(auto_error=False)


async def get_current_scope(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ScopeObject:
    if credentials is None:
        raise ForbiddenError("Missing bearer token")
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise ForbiddenError("Invalid bearer token") from exc
    return ScopeObject(**payload)


ScopeDep = Annotated[ScopeObject, Depends(get_current_scope)]
