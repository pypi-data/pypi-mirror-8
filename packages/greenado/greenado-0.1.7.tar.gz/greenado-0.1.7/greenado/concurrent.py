#
# Copyright 2014 Dustin Spicuzza
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from functools import partial, wraps
import sys
import types

import greenlet

from tornado import concurrent, gen
from tornado.ioloop import IOLoop


def gcall(f, *args, **kwargs):
    '''
        Calls a function, makes it asynchronous, and returns the result of
        the function as a tornado.concurrent.Future. The wrapped function
        may use gyield to pseudo-synchronously wait for a future to resolve.
        
        This is the same code that groutine uses to wrap functions.
    '''
    
    # When this function gets updated, update groutine.wrapper also!
    
    future = concurrent.TracebackFuture()

    def greenlet_base():    
        try:
            future.set_result(f(*args, **kwargs))
        except:
            future.set_exc_info(sys.exc_info())
    
    gr = greenlet.greenlet(greenlet_base)        
    gr.switch()
    
    return future


def generator(f):
    '''
        A decorator that allows you to use the 'yield' keyword in a function,
        without requiring callers to also yield this function.
        
        The yield keyword can be used inside a decorated function on any
        function call that returns a future object, such as functions
        decorated by gen.coroutine, and most of the tornado API as of
        tornado 4.0.
        
        Similar to `tornado.gen.coroutine`, in versions of Python before 3.3
        you must raise tornado.gen.Return to return a value from this
        function.
        
        This function must only be used by functions that either have a
        greenlet_coroutine decorator, or functions that are children of
        functions that have the decorator applied.
        
        .. versionadded:: 0.1.7
    '''
    
    # Note: this code is vaguely similar to tornado's gen.coroutine/Runner,
    #       which is licensed under the Apache 2.0 license.
    
    @wraps(f)
    def wrapper(*args, **kwargs):
    
        assert greenlet.getcurrent().parent is not None, "functions decorated with generator() can only be called from functions that have the @greenado.groutine decorator in the call stack."
        
        try:
            result = f(*args, **kwargs)
        except (gen.Return, StopIteration) as e:
            result = getattr(e, 'value', None)
        else:
            if isinstance(result, types.GeneratorType):
                try:
                    future = next(result)
                    
                    while True:       
                        try:
                            value = gyield(future)
                        except Exception:
                            result.throw(*sys.exc_info()) 
                        else:
                            future = result.send(value)
                
                except (gen.Return, StopIteration) as e:
                    return getattr(e, 'value', None)
        
        return result
        
    
    return wrapper


def groutine(f):
    '''
        A decorator that makes a function asynchronous and returns the result
        of the function as a tornado.concurrent.Future. The wrapped function
        may use gyield to pseudo-synchronously wait for a future to resolve.  
        
        The primary advantage to using this decorator is that it allows
        *all* called functions and their children to use gyield, and doesn't
        require the use of generators.
        
        If you are calling a groutine-wrapped function from a function with
        a groutine wrapper, you will need to use gyield to wait for the 
        returned future to resolve.
        
        From a caller's perspective, this decorator is functionally
        equivalent to the tornado.gen.coroutine decorator. You should not use
        this decorator and the tornado.gen.coroutine decorator on the same
        function.
    '''

    @wraps(f)
    def wrapper(*args, **kwargs):
        
        # When this function gets updated, update gcall also!
        
        future = concurrent.TracebackFuture()

        def greenlet_base():    
            try:
                future.set_result(f(*args, **kwargs))
            except:
                future.set_exc_info(sys.exc_info())
        
        gr = greenlet.greenlet(greenlet_base)        
        gr.switch()
        
        return future
    
    return wrapper


def gyield(future):
    '''
        This is functionally equivalent to the 'yield' statements used in a
        tornado coroutine, but doesn't require turning all your functions
        into generators -- so you can use the return statement normally, and
        exceptions won't be accidentally discarded.
        
        This can be used on any function that returns a future object, such
        as functions decorated by gen.coroutine, and most of the tornado API
        as of tornado 4.0.
        
        This function must only be used by functions that either have a
        greenado.groutine decorator, or functions that are children of
        functions that have the decorator applied.
        
        :param future: A `tornado.concurrent.Future` object
        :returns: The result yielded from the future object
    '''
    
    gr = greenlet.getcurrent()
    assert gr.parent is not None, "gyield() can only be called from functions that have the @greenado.groutine decorator in the call stack."
    
    # don't switch/wait if the future is already ready to go
    if not future.done():
        
        def on_complete(result):
            gr.switch()
        
        IOLoop.current().add_future(future, on_complete)
        gr.parent.switch()
        
        while not future.done():
            gr.parent.switch()
    
    return future.result()
    
