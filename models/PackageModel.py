from pydantic import BaseModel, Field, AliasPath
from typing import Annotated, Optional


class VersionResponse(BaseModel):
	name: Annotated[str, Field(validation_alias=AliasPath('info', 'name'))]
	current: Optional[str] = None
	latest: Annotated[str, Field(validation_alias=AliasPath('info', 'version'))]
