class Version(object):
    def __init__(self, new, number, delimiter='.'):
        self.new = new
        self.number = number
        self.delimiter = delimiter

    def is_new(self):
        return self.new

    def get_number(self):
        if isinstance(self.number, list):
            return self.delimiter.join([str(x) for x in self.number])
        else:
            return self.number
