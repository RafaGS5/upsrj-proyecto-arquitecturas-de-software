import os
from dataclasses import dataclass
from typing import Tuple

ROOT_DIR        = "upsrj-proyecto-arquitecturas-de-software"
SRC_DIR         = os.path.join(ROOT_DIR, "src")
TEMPLATES_DIR   = os.path.join(SRC_DIR, "templates")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class Hosts:
    """
    Configuration for host and port settings.

    Attributes:
        main (Tuple[str, int]): IP address and port for the main host.
    """
    main: Tuple[str, int] = ('0.0.0.0', 5000)