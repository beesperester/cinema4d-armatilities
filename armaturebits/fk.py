import c4d

from typing import Any, Generator, List, Optional, Dict

from armature import dag

from armaturebits import doodle


def create_ctrl(
    dag_base_object: dag.DagBaseObject,
    parent: Optional[dag.DagBaseObject] = None,
    layer: Optional[c4d.documents.LayerObject] = None,
) -> Generator[dag.DagAtom, None, None]:
    matrix: c4d.Matrix = dag_base_object.GetMg()
    name: str = dag_base_object.GetName()

    # create off group
    Off = dag.create_dagbaseobject(
        name.replace("_Joint", "_Off"), c4d.Onull, layer=layer
    )

    # create sdk group
    Sdk = dag.create_dagbaseobject(
        name.replace("_Joint", "_Sdk"), c4d.Onull, parent=Off, layer=layer
    )

    # create ctrl group
    Ctrl = dag.create_dagbaseobject(
        name.replace("_Joint", "_Ctrl"), c4d.Onull, parent=Sdk, layer=layer
    )

    # derive tag name
    tag_name = name.replace("_Joint", "_FK_Constraint")

    op_tags: dag.DagBaseTagList = dag_base_object.GetTags()
    tag_names: List[str] = [x.GetName() for x in op_tags]

    if tag_name not in tag_names:
        # add new constraint with tag name
        # if no tag with tag name exists
        constraint = dag.create_dagbasetag(
            tag_name, 1019364, dag_base_object, layer=layer
        )

        # enable PSR
        constraint[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True
        # set Ctrl object reference
        constraint[10001] = Ctrl.item
        # enable P
        constraint[10005] = True
        # enable S
        constraint[10006] = True
        # enable R
        constraint[10007] = True

        yield constraint

    if parent:
        Off.InsertUnder(parent)
        Off.SetMg(matrix)

    # expose off adapter
    yield Off

    # expose sdk adapter
    yield Sdk

    # expose ctrl adapter
    yield Ctrl


def create_ctrl_shape(
    name: str, children: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    if children is None:
        children = []

    ctrl_shape = doodle.create_shape(f"{name}_Ctrl", c4d.Onull, children)

    sdk_shape = doodle.create_shape(f"{name}_Sdk", c4d.Onull, [ctrl_shape])

    off_shape = doodle.create_shape(f"{name}_Off", c4d.Onull, [sdk_shape])

    return off_shape
