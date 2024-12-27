from openvpn_manager.parser import parser_factory


def parser(func):
    def wrapper(*args, **kwargs):
        result = parser_factory(args[1], func(*args, **kwargs))
        return result.parse()
    return wrapper