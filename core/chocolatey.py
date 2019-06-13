import subprocess
import re


class Chocolatey(object):

    def __init__(self):
        # not really beautiful :-(
        self.success_pattern = "Successfully created package"
        self.command = "chocolatey"
        self.args = [self.command, "pack"]

    def pack(self, nuspec_path, output_path):
        args = self.args + [nuspec_path, "--out", output_path]
        result = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()
        if re.compile(self.success_pattern).search(result[0].decode('utf-8')):
            return True
        return False
