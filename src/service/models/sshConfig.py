from pydantic import BaseModel, ConfigDict


class SshConfig(BaseModel):
    parameterName: str
    parameterValue: str

    model_config = ConfigDict(from_attributes=True)
