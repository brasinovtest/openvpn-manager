# from typing import Callable, Any
#
#
# def parse_output(func):
#     def wrapper(*args, **kwargs):
#         method = args[1]
#         output = func(*args, **kwargs)
#         return f"{method}: {output}"
#     return wrapper
#
#
#
# class ApiObject:
#     def __init__(self, attr: str, parent: Callable):
#         self.attr = attr
#         self.parent = parent
#
#     def __getattr__(self, method: str) -> Callable:
#         def func(*args, **kwargs) -> Any:
#             if method != 'execute':
#                 raise AttributeError(f"'{self.parent}' object has no attribute '{method}'")
#             aaa = self.attr.replace('_', '-')
#             return self.parent._execute(method, aaa, *args, **kwargs)
#         return func
#
#
#
# class Novo:
#
#     def __repr__(self):
#         return f"{self.__class__.__name__}"
#
#     def __getattr__(self, attr: str):
#         return ApiObject(attr, self)
#
#     @parse_output
#     def _execute(self, *args, **kwargs):
#         return args
#
#
# um = Novo()
# print(um.aaa.execute())


valor = ['nome', 'sobrenome', 'darci', 'ferreira']

print(valor.index('sobrenome'))