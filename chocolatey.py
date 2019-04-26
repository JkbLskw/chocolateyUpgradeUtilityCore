import subprocess


class Chocolatey(object):

    def __init__(self):
        self.command = "chocolatey"
        self.args = ["pack"]

    def pack(self, nuspec_path, output_path):
        self.args += [nuspec_path, "--out", output_path]
        self.args.insert(0, self.command)
        result = subprocess.Popen(self.args, stdout=subprocess.PIPE).communicate()[0]
        if "success" in result:
            return True
        return False
