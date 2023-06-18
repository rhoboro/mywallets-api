from datetime import datetime, timezone

def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)

def to_iso8601(utc_or_native: datetime) -> str:
    utc_datetime = utc_or_native.replace(
        tzinfo=timezone.utc
    )
    return utc_datetime.isoformat()
