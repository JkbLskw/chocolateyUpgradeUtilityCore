import re

from executable.abstract_executable import AbstractExecutable


class Plain(AbstractExecutable):
    """ Plain Executable - Version in Link """

    def __init__(self):
        AbstractExecutable.__init__(self)

    def version(self, path):
        version_pattern = re.compile(r"(\d+\.)+")
        version_match = re.search(version_pattern, path)
        if version_match is not None:
            version_string = version_match.group()
            if version_string.endswith('.'):
                version_string = version_string.strip('.')
            return [int(x) for x in version_string.split(".")]
        else:
            return None
