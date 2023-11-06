import inspect

def my_func():
    print("Hello, world!")

source = inspect.getsource(my_func)
print(source)
