import subprocess
import re

class Chocolatey(object):

    def __init__(self):
        self.success_pattern = "Successfully created package .%s.nupkg."
        self.command = "choco"
        self.args = [self.command, "pack"]

    def pack(self, nuspec_path, output_path, joined_version):
        pattern = self.success_pattern % (output_path.replace('\\', '\\\\') + ".*" + joined_version.replace('.', '\\.'))
        args = self.args + [nuspec_path, "--out", output_path]
        result = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()
        if re.compile(pattern).search(result[0].decode('utf-8')):
            return True
        return False
