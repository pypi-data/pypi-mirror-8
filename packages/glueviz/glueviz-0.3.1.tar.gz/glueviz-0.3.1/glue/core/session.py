from . import DataCollection, CommandStack


class Session(object):

    def __init__(self, application=None, data_collection=None,
                 command_stack=None, hub=None):

        # applications can be added after instantiation
        self.application = application

        self.data_collection = data_collection or DataCollection()
        self.hub = self.data_collection.hub
        self.command_stack = command_stack or CommandStack()
        self.command_stack.session = self
