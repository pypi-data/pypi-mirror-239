import os.path
import sys
from logging import getLogger
from typing import List, Optional

# make sure turAI folder is in sys.path (relevant in dev)
turAI_container = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if turAI_container not in sys.path:
    sys.path.insert(0, turAI_container)

import turAI
from turAI.common import PROCESS_ACK
from turAI.plugins.micropython.os_mp_backend import SshUnixMicroPythonBackend

logger = getLogger("turAI.plugins.ev3.ev3_back")


class EV3MicroPythonBackend(SshUnixMicroPythonBackend):
    def _get_sys_path_for_analysis(self) -> Optional[List[str]]:
        return [
            os.path.join(os.path.dirname(__file__), "api_stubs"),
        ] + super()._get_sys_path_for_analysis()


if __name__ == "__main__":
    turAI_USER_DIR = os.environ["turAI_USER_DIR"]
    turAI.configure_backend_logging()
    print(PROCESS_ACK)

    import ast

    args = ast.literal_eval(sys.argv[1])

    EV3MicroPythonBackend(args)
