# aspectp
Aspect Oriented Programming in Python.

Aspect-Oriented Programming (`AOP`) is a programming paradigm that separates cross-cutting concerns, like logging or security, from the main code to improve modularity and code organization, making it easier to manage and maintain complex software systems.

## Intallation

`pip install aspectp`

## Example

```python
import aspectp
import math

def add_one(result):
    return result + 1

print(math.pow(2, 2)) # 4.0
aspectp.after(math.pow, add_one)
print(math.pow(2, 2)) # 5.0
```

## Background

### Aspect
An `aspect` is a modular unit that encapsulates a specific cross-cutting concern. Cross-cutting concerns are features or behaviors that span across multiple parts of a program, such as logging, error handling, or transaction management. Aspects allow these concerns to be added to existing code without modifying the code itself.

### Joinpoint
A `joinpoint` is a point in the execution of the program, such as a function/method call, or an exception being thrown. A `joinpoint` is the place where an `advice` is attached. The following joinpoints are supported:
- `function`
- `method`
- `object`: the `advice` is attached to all methods of the object
- `class`: the `advice` is attached to all methods of the class
- `module`: the `advice` is attached to all functions in the module

### Advice
An `advice` is the action taken by an `aspect` at a specific `joinpoint`. There are 4 kinds of advices:
- `before`: executed before a `joinpoint`
- `after`: exectuted after a `joinpoint`
- `around`: executed before and after a `joinpoint`
- `error`: executed when a `joinpoint` raises an `error`

## Usage

### Before
To attach before a `joinpoint` execution use:
```python
aspectp.before(joinpoint, before_advice)
```
Where `before_advice` is a function with the following signature:
```python
def before_advice(args, kwargs):
    # Do stuff
    return args, kwargs
```
`before_advice` can read and modify the arguments that will be passed to `joinpoint`. `before_advice` can also throw an exception to prevent `joinpoint` from being executed.

Here is an example of `aspectp.before`:
```Python
import aspectp
import math

def increase_exponenet(args, kwargs):
    return (args[0], args[1] + 1), kwargs

print(math.pow(2, 2)) # 4.0
aspectp.before(math.pow, increase_exponenet)
print(math.pow(2, 2)) # 8.0
```

### After
To attach after a `joinpoint` execution use:
```python
aspectp.after(joinpoint, after_advice)
```
Where `after_advice` is a function with the following signature:
```python
def after_advice(result):
    # Do stuff
    return result
```
`after_advice` can read and modify the result returned by `joinpoint`. `after_advice` can also throw an exception to prevent `result` from being returned.

Here is an example of `aspectp.after`:
```Python
import aspectp
import math

def increase_result(result):
    return result + 1

print(math.pow(2, 2)) # 4.0
aspectp.after(math.pow, increase_result)
print(math.pow(2, 2)) # 5.0
```

### Around
Attaching around a `joinpoint` is similar to attaching before and after a `joinpoint`. To attach around a `joinpoint` execution use:
```python
aspectp.around(joinpoint, around_advice)
```
Where `around_advice` is a function with the following signature:
```python
def around_advice(func, args, kwargs):
    # Do stuff
    result = func(args, kwargs)
    # Do stuff
    return result
```
`around_advice` can read and modify the arguments that will be passed to `joinpoint`. `around_advice` can also prevent `joinpoint` from being executed and it can read and modify the result returned by `joinpoint`.

Here is an example of `aspectp.around`:
```Python
import aspectp
import math

def increase_exponent_and_result(func, args, kwargs):
    result = func((args[0], args[1] + 1), kwargs)
    return result + 1

print(math.pow(2, 2)) # 4.0
aspectp.around(math.pow, increase_exponent_and_result)
print(math.pow(2, 2)) # 9.0
```

### Error
To attach after a `joinpoint` raises an `error` use:
```python
aspectp.error(joinpoint, error_advice)
```
Where `error_advice` is a function with the following signature:
```python
def error_advice(error):
    # Do stuff
    return error
```
`error_advice` can handle the error raised by `joinpoint`. `error_advice` does not need to return `error`.

Here is an example of `aspectp.error`:
```Python
import aspectp
import math

def return_zero_on_error(error):
    return 0.0
try:
    math.sqrt(-1)
except ValueError as e:
    print(e) # math domain error
aspectp.error(math.sqrt, return_zero_on_error)
print(math.sqrt(-1)) # 0.0
```

### Remove
To remove all advices from a `joinpoint` use:
```python
aspectp.remove(joinpoint)
```
To remove a single advice from a `joinpoint` use:
```python
id = aspectp.before(joinpoint, before_advice)
# Do stuff
aspectp.remove(joinpoint, id)
```
