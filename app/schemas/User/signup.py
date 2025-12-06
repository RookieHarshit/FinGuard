from pydantic import BaseModel, Field

class SignupRequestOTP(BaseModel):
    phone: str = Field(
        ...,
        pattern=r"^(?:\+91)?[6-9]\d{9}$",
        description="User's mobile number with optional +91"
    )
