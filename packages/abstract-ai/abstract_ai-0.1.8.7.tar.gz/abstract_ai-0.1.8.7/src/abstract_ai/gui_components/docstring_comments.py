import inspect
import abstract_ai
def get_docstrings(module):
    docstrings = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            docstrings[name] = inspect.getdoc(obj)
    return docstrings

docstrings = get_docstrings(abstract_ai)
input(docstrings)
