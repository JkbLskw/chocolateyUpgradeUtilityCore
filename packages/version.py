class Version(object):
    def __init__(self, new, last, delimiter='.'):
        self.new = new
        self.last = last
        self.delimiter = delimiter

    def is_new(self):
        if self.new is None:  # none new version
            return False
        if self.last is None:
            return True
        for i in range(len(self.new) if len(self.new) >= len(self.last) else len(self.last)):
            if i < len(self.new) and i < len(self.last) and self.new[i] > self.last[i]:  # number at position higher
                return True
        return False

    def get(self, last=False):
        value = None
        if last:
            value = self.last
        else:
            value = self.new
        if isinstance(value, list):
            return self.delimiter.join([str(x) for x in value])
        else:
            return value
