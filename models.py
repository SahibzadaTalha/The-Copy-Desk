from pydantic import BaseModel, Field, field_validator

class MarketingCopy(BaseModel):
    product_name: str
    platform: str
    tone: str
    headline: str
    body: str
    call_to_action: str
    hashtags: list[str] = Field(default_factory=list)

    @property
    def full_text(self) -> str:
        tag_line = (" " + " ".join(self.hashtags)) if self.hashtags else ""
        return f"{self.headline}\n\n{self.body}\n\n{self.call_to_action}{tag_line}"

    @property
    def character_count(self) -> int:
        return len(self.full_text)

    def compliance_check(self, max_characters: int) -> bool:
        return self.character_count <= max_characters


class BatchJobRow(BaseModel):
    product_name: str
    platform: str
    tone: str

    @field_validator("platform")
    @classmethod
    def lower_platform(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("tone")
    @classmethod
    def lower_tone(cls, v: str) -> str:
        return v.strip().lower()