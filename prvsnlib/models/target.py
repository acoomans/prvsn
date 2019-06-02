from prvsnlib.singleton import Singleton

class Target:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

    def __str__(self):
        return 'target %s' % self.name

    def run(self, runbook):
        raise NotImplementedError

    def apply(self, package):
        raise NotImplementedError

    @property
    def is_valid(self):
        raise NotImplementedError

class LocalTarget(Singleton('SingletonMeta', (object,), {})):

    def __init__(self):
        # super().__init__('local')
        self.name = 'local target'

    @property
    def is_valid(self):
        return True


class RemoteTarget(Target):

    @property
    def is_valid(self):
        return len(self.name)
