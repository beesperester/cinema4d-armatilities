from typing import Any, Dict, List, Optional


def create_shape(
    name: str, type: int, children: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    if children is None:
        children = []

    return {"name": name, "type": type, "children": children}
