class CheckError(Exception):
    def __init__(self, module, msg=None):
        if msg is None:
            msg = "Check Error has occurred"
        super(CheckError, self).__init__(msg)
        self.module = module


class UnknownCheckStateError(CheckError):
    def __init__(self, module, output):
        super(UnknownCheckStateError, self).__init__(module, msg='Module returned an unknown state')
        self.output = output
