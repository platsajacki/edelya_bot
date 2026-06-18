from importlib import import_module


def register_handlers() -> None:
    import_module('bot.handlers.start')
    import_module('bot.handlers.how_it_works')
    import_module('bot.handlers.help')
