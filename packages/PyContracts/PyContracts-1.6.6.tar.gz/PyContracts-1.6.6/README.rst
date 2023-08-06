PyContracts is a Python package that allows to declare constraints on function parameters and
return values. It supports a basic type system, variables binding, arithmetic constraints, and
has several specialized contracts (notably for Numpy arrays). 

.. container:: brief_summary
  
    A brief summary follows. See the full documentation at: <http://andreacensi.github.com/contracts/>

**Why**: The purpose of PyContracts is **not** to turn Python into a statically-typed language
(albeit you can be as strict as you wish), but, rather, to avoid the time-consuming and
obfuscating checking of various preconditions. In fact, more than the type constraints, I found
useful the ability to impose value and size constraints. For example, "I need a list of at least
3 positive numbers" can be expressed as ``list[>=3](number, >0))``. If you find that
PyContracts is overkill for you, you might want to try a simpler alternative, such as
typecheck_. If you find that PyContracts is not *enough* for you, you probably want to be
using Haskell_ instead of Python.

**Specifying contracts**: Contracts can be specified in three ways:

1. **Using the ``@contract`` decorator:** ::
   
      @contract(a='int,>0', b='list[N],N>0', returns='list[N]')
      def my_function(a, b):
          ...

2. **Using annotations** (for Python 3): :: 
  
      @contract
      def my_function(a : 'int,>0', b : 'list[N],N>0') -> 'list[N]': 
           # Requires b to be a nonempty list, and the return 
           # value to have the same length.
           ...
      
3. **Using docstrings**, with the ``:type:`` and ``:rtype:`` tags: ::
   
      @contract
      def my_function(a, b): 
          """ Function description.
              :type a: int,>0
              :type b: list[N],N>0
              :rtype: list[N]
          """
          ...
          
..
   In any case, PyContracts will include the spec in the ``__doc__`` attribute.

**Deployment**: In production, all checks can be disabled using the function ``contracts.disable_all()``, so the performance hit is 0.

**Extensions:** You can extend PyContracts with new contracts types: ::

    new_contract('valid_name', lambda s: isinstance(s, str) and len(s)>0)
    @contract(names='dict(int: (valid_name, int))')
    def process_accounting(records):
        ...

Any Python type is a contract: ::

    @contract(a=int, # simple contract
              b='int,>0' # more complicated
              )
    def f(a, b):
        ...

**Enforcing interfaces**:  ``ContractsMeta`` is a metaclass like ABCMeta that propagates contracts to the subclasses: ::

    from contracts import contract, ContractsMeta
    
    class Base(object):
        __metaclass__ = ContractsMeta

        @abstractmethod
        @contract(probability='float,>=0,<=1')
        def sample(self, probability):
            pass

    class Derived(Base):
        # The contract above is automatically enforced, 
        # without this class having to know about PyContracts at all!
        def sample(self, probability):
            ....

**Numpy**: There is special support for Numpy: ::

    @contract(image='array[HxWx3](uint8),H>10,W>10')
    def recolor(image):
        ...

**Status:** PyContracts is very well tested and documented. The syntax is stable and it won't be changed.

.. _typecheck: http://oakwinter.com/code/typecheck/
.. _Haskell: http://www.haskell.org/


