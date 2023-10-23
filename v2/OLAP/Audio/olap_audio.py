from cubes import Workspace,PointCut,Cell

def create_olap_cube(db,model):
    workspace = Workspace()
    workspace.register_default_store("sql", url=db)
    workspace.import_model(model)
    browser = workspace.browser("Files")

    return browser