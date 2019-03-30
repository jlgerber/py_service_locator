
class Logger(object):
    def __init__(self, name):
        self.name = name

    def debug(self, *args):
        print "DEBUG: {}:".format(self.name)," ".join(args)

    def info(self, *args):
        print "INFO: {}:".format(self.name)," ".join(args)

    def warn(self, *args):
        print "WARN: {}:".format(self.name)," ".join(args)

class Dioculator(object):
    def __init__(self, frombulator):
        self.frombulator = frombulator

    def dioculate(self):
        print "Dioculating with frombulator: '{}'".format(self.frombulator)
