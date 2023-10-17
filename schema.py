from typing import Optional

import pydantic


class CreateUser(pydantic.BaseModel):
    name: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v


class PatchUser(CreateUser):
    name: Optional[str]
    password: Optional[str]


class CreateAdvertisement(pydantic.BaseModel):
    heading: str
    description: str
    owner_id: int

    @pydantic.field_validator("description")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError(f"Minimal length of description is 5")
        return v


class PatchAdvertisement(CreateAdvertisement):
    heading: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
