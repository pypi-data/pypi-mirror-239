from logzero import logger

from chaosreliably.controls.vendors.honeycomb import HoneycombVendorHandler

__all__ = ["apply_vendors", "register_vendors"]
VENDORS = []


def register_vendors() -> None:
    if HoneycombVendorHandler.is_on():
        VENDORS.append(HoneycombVendorHandler())


def apply_vendors(method: str, **kwargs) -> None:  # type: ignore
    for v in VENDORS:
        if method == "started":
            try:
                v.started(**kwargs)
            except Exception:
                logger.debug(
                    "failed to apply 'started' method on vendor "
                    f"class {v.__class__.__name__}",
                    exc_info=True,
                )
        elif method == "finished":
            try:
                v.finished(**kwargs)
            except Exception:
                logger.debug(
                    "failed to apply 'finished' method on vendor "
                    f"class {v.__class__.__name__}",
                    exc_info=True,
                )
