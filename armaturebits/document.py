import c4d

from typing import Optional


def create_layer(
    name: str,
    color: Optional[c4d.Vector] = None,
    doc: Optional[c4d.documents.BaseDocument] = None,
):
    if doc is None:
        doc = c4d.documents.GetActiveDocument()

    # get existing root layers
    layers: List[c4d.documents.LayerObject] = doc.GetLayerObjectRoot().GetChildren()  # type: ignore

    root_layer_names = [x.GetName() for x in layers]

    if name in root_layer_names:
        # return existing layer
        # if layer exists in root layers
        return layers[root_layer_names.index(name)]
    else:
        # create new layer
        layer: c4d.documents.LayerObject = c4d.documents.LayerObject()
        layer.SetName(name)
        layer.InsertUnder(doc.GetLayerObjectRoot())

        if color:
            layer[c4d.ID_LAYER_COLOR] = color

    return layer
