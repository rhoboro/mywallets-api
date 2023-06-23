from datetime import datetime, timezone
from pydantic import SerializerFunctionWrapHandler

def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)

def to_utc(
    utc_or_native: datetime,
    nxt: SerializerFunctionWrapHandler
) -> str:
    utc_datetime = utc_or_native.replace(
        tzinfo=timezone.utc
    )
    # 前処理をしてから元のシリアライザに渡す
    return nxt(utc_datetime)
