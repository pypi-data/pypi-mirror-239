from sqlmodel import Field
from typing import Optional
from .base import BaseMixin
from pydantic import validator


class Naf(BaseMixin, table=True):
    """This table hosts the Naf labels

    Attributes:
        id:
        naf:
        label:
    """

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    naf: str
    label: str

    @validator("naf", pre=True)
    def is_naf(cls, v):
        """Validator for `naf`

        Rules:
            - should be 5 characters long
            - the first 4 values should be numeric
            - The last value should be a letter

        Raises:
            ValueError:

        """
        # A valid NAF is composed 4 numbers and a letter (could be a regex ^\d{4}\D{1}$)
        error = "a NAF should be made up of 4 numbers and a letter"
        if len(v) != 5:
            raise ValueError(error)

        if not v[:4].isdigit():
            raise ValueError(error)

        if v[-1].isdigit():
            raise ValueError(error)
        return v
