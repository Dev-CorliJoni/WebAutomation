class BaseStep:

    def __call__(self, *args, **kwargs):
        automation = args[0]
        session = args[1]
        return automation, session
