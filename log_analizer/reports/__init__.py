from typing import Callable, Optional
from .handlers import generate_handler_report

REPORTS: dict[str, Callable] = {
    "handlers": generate_handler_report,
}

def get_report(name: str) -> Optional[Callable]:
    return REPORTS.get(name)