class Version(object):
    def __init__(self, new, last, delimiter='.'):
        self.new = new
        self.last = last
        self.delimiter = delimiter

    def is_new(self):
        if self.new is None:
            return False
        if len(self.new) == len(self.last):
            for i in range(len(self.new)):
                if self.new[i] > self.last[i]:
                    return True
        else:
            if self.new == self.last:
                return False
            else:
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
