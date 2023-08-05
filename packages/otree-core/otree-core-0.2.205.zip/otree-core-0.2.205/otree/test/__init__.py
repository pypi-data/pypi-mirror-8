from importlib import import_module
client = import_module('otree.test.client')

# public API

class Bot(client.PlayerBot):

    def play(self):
        return super(Bot, self).play()

    def submit(self, ViewClass, param_dict=None):
        return super(Bot, self).submit(ViewClass, param_dict)

    def submit_with_invalid_input(self, ViewClass, param_dict=None):
        return super(Bot, self).submit_with_invalid_input(ViewClass, param_dict)

class ExperimenterBot(client.ExperimenterBot):

    def play(self):
        return super(ExperimenterBot, self).play()

    def submit(self, ViewClass, param_dict=None):
        return super(ExperimenterBot, self).submit(ViewClass, param_dict)

    def submit_with_invalid_input(self, ViewClass, param_dict=None):
        return super(ExperimenterBot, self).submit_with_invalid_input(ViewClass, param_dict)
