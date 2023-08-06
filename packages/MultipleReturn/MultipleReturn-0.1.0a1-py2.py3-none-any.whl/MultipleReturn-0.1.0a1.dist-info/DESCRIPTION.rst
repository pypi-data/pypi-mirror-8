Unlike Lisp's "values" function, Python lacks a way of creating a function that return multiple values where the caller by default only sees the first one. Simply add the @multiplereturn decorator to any function or method that return a tuple, and it will now return only the first item in that tuple to its callers. Wrap the call to a @multiplereturn decorated function with thevalues() function and the caller gets the original tuple.


