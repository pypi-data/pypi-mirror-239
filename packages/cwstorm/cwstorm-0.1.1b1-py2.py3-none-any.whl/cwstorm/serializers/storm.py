def serialize(node, parent=None):
    result = {"name": node.name()}

    if node.is_reference(parent):
        result.update({"reference": True})
        return result

    result.update(dict(node))
    result["reference"] = False
    result["tasks"] = []
    for c in node.children:
        
        result["tasks"].append(serialize(c, node))
    return result
