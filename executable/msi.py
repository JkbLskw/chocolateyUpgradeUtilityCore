from executable.abstract_executable import AbstractExecutable
from msilib import *


class Msi(AbstractExecutable):
    """ msi executable """

    def __init__(self):
        AbstractExecutable.__init__(self)

    def version(self, path):
        property_query = "SELECT Value FROM Property WHERE Property='" + self.fileinfo_versionstring + "'"
        db = OpenDatabase(path, MSIDBOPEN_READONLY)
        view = db.OpenView(property_query)
        view.Execute(None)
        result = view.Fetch()
        return [int(x) for x in result.GetString(1).split(".")]
