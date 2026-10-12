from datetime import UTC, datetime

from pydantic import AwareDatetime, BaseModel


class RateSnapshot(BaseModel):
    base: str
    date: str
    rates: dict[str, float]
    fetched_at: AwareDatetime

    def age_seconds(self, now: datetime | None = None) -> int:
        now = now or datetime.now(UTC)
        return int((now - self.fetched_at).total_seconds())
