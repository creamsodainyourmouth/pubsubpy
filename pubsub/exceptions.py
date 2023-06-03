class ListenerDecoratorIsNotApplied(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    def __str__(self):
        return "To register events handlers by `channel.listen(event_type: T)` decorator " \
               "need to decorate `__init__` of handlers class"
