solid
=====

A state machine implementation for Python --- which *isn't* solely designed to parse strings!


why state machines?
-------------------

They're cool! Also, easy to reason about --- a state machine design enables you
to compartmentalize responsibilites in a way that functions simply don't.


why "solid"?
------------

It's a convoluted name: it's a state machine library written in python;
snake is another word for python that sounds like state --- and Solid Snake is
a fairly well known character who kicks serious butt. Thus, "solid".

hello, world
------------

Let's define a super-simple state machine with two states: one that prints
"Hello" and one that prints "World":

.. code-block:: python

  from solid.machines import BaseMachine
  from solid.states import BaseState, is_entry_state
  from solid.transition import to


  class HelloMachine(BaseMachine):

    @is_entry_state
    class Hello(BaseState):
      def body(self):
        print "Hello"

        return to(HelloMachine.World)

    class World(BaseState):
      def body(self):
        print "World"

From an intertpreter (or whatever):

.. code-block:: python

  >>> h = HelloMachine()
  >>> h.start()
  Hello
  World
  >>>

and that's pretty much all there is to it.
