
def cp_po_editor(req):
    from apps.po_editor.admin import PoEditorAdmin
    return {"cp_po_editor":PoEditorAdmin()}