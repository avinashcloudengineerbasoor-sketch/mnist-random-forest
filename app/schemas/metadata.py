from pydantic import BaseModel, Field


class MetadataRequest(BaseModel):

    pen_pressure: float = Field(..., gt=0, description="Pen pressure value")

    writer_age: int = Field(..., gt=0, lt=120, description="Writer age")

    handedness: str = Field(
        ..., pattern="^(left|right)$", description="left or right handed"
    )
