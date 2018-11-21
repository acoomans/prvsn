from prvsnlib.utils.file import add_string_if_not_present_in_file, delete_string_from_file
from ..task import Task, TaskResult
from prvsnlib.utils.run import run


class KernelModuleAction:
    ADD = 'add'
    DEL = 'delete'


class KernelModuleTask(Task):

    def __init__(self, module_name, action, secure):
        Task.__init__(self, secure)
        self._module_name = module_name
        self._action = action

    def __str__(self):
        return str(self._action).capitalize() + ' kernel module "' + self._module_name + '".'

    @staticmethod
    def check_loadable_modules():
        cmd, out, ret, err = run(['which', 'modprobe'])
        if ret or err:
            return 'Cannot find loadable linux modules.'
        return None

    def run(self):
        if self.check_loadable_modules():
            return TaskResult(error='Cannot find loadable linux modules.')

        out, err = '', ''
        if self._action == KernelModuleAction.ADD:
            out, err = add_string_if_not_present_in_file('/etc/modules', self._module_name)
        elif self._action == KernelModuleAction.ADD:
            out, err = delete_string_from_file('/etc/modules', self._module_name)
        return TaskResult(output=out, error=err)


def module(d, action=KernelModuleAction.ADD, secure=False):
    KernelModuleTask(d, action, secure)
