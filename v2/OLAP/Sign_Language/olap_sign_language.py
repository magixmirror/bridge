from cubes import Workspace, PointCut, Cell

CUBE_NAME = "Fact"

def create_olap_cube(db_string, model_path):
    workspace = Workspace()
    workspace.register_default_store("sql", url= db_string)
    workspace.import_model(model_path)
    browser = workspace.browser(CUBE_NAME)
    return browser

#cube = browser.cube
#cut = PointCut(dimension="Frame", path=[1,0,17])
#cell = Cell(browser.cube, cuts = [cut])

# Execute the query and fetch the result set
#result = browser.facts(cell)
#for record in result:
#    print (record)

