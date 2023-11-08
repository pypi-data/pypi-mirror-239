import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Shape:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        
        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SHAPE")
        script.append("df_shape = pd.DataFrame([df.shape], columns=['num_rows', 'num_columns'])")
        df = pd.DataFrame([df.shape], columns=["num_rows", "num_columns"])

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
