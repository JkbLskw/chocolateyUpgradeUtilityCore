from msilib import *


def GetMsiProperty(path, property):
    property_query = "SELECT Value FROM Property WHERE Property='" + property + "'"
    db = OpenDatabase(path, MSIDBOPEN_READONLY)
    view = db.OpenView(property_query)
    view.Execute(None)
    result = view.Fetch()
    return result.GetString(1)
