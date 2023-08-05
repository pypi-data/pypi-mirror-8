# -*- test-case-name: automat._test.test_methodical -*-

from functools import wraps
from itertools import count

from characteristic import attributes

from ._core import Transitioner, Automaton
from ._introspection import preserveName

def _keywords_only(f):
    """
    Decorate a function so all its arguments must be passed by keyword.

    A useful utility for decorators that take arguments so that they don't
    accidentally get passed the thing they're decorating as their first
    argument.

    Only works for methods right now.
    """
    @wraps(f)
    def g(self, **kw):
        return f(self, **kw)
    return g



@attributes(['machine', 'method'])
class MethodicalState(object):
    """
    A state for a L{MethodicalMachine}.
    """

    def upon(self, input, enter, outputs):
        """
        Declare a state transition within the L{MethodicalMachine} associated
        with this L{MethodicalState}: upon the receipt of the input C{input},
        enter the state C{enter}, emitting each output in C{outputs}.
        """
        self.machine._oneTransition(self, input, enter, outputs)



@attributes(['automaton', 'method', 'symbol'])
class MethodicalInput(object):
    """
    An input for a L{MethodicalMachine}.
    """

    def __get__(self, oself, type=None):
        """
        Return a function that takes no arguments and returns values returned
        by output functions produced by the given L{MethodicalInput} in
        C{oself}'s current state.
        """
        # FIXME: multiple machines on one instance will stomp on each other.
        transitioner = getattr(oself, self.symbol, None)
        if transitioner is None:
            transitioner = Transitioner(
                self.automaton,
                # FIXME: public API on Automaton for getting the initial state.
                list(self.automaton._initialStates)[0],
            )
            setattr(oself, self.symbol, transitioner)
        @preserveName(self.method)
        @wraps(self.method)
        def doInput():
            return [output(oself) for output in transitioner.transition(self)]
        return doInput



@attributes(['machine', 'method'])
class MethodicalOutput(object):
    """
    An output for a L{MethodicalMachine}.
    """

    def __get__(self, oself, type=None):
        """
        Outputs are private, so raise an exception when we attempt to get one.
        """
        raise AttributeError(
            "{cls}.{method} is a state-machine output method; "
            "to produce this output, call an input method instead.".format(
                cls=type.__name__,
                method=self.method.__name__
            )
        )


    def __call__(self, oself):
        """
        Call the underlying method.
        """
        return self.method(oself)



counter = count()
def gensym():
    """
    Create a unique Python identifier.
    """
    return "_symbol_" + str(next(counter))



class MethodicalMachine(object):
    """
    A L{MethodicalMachine} is an interface to an L{Automaton} that uses methods
    on a class.
    """

    def __init__(self):
        self._automaton = Automaton()
        self._symbol = gensym()


    def __get__(self, oself, type=None):
        """
        L{MethodicalMachine} is an implementation detail for setting up
        class-level state; applications should never need to access it on an
        instance.
        """
        raise AttributeError("MethodicalMachine is an implementation detail.")


    @_keywords_only
    def state(self, initial=False, terminal=False):
        """
        Declare a state, possibly an initial state or a terminal state.

        This is a decorator for methods, but it will modify the method so as
        not to be callable any more.
        """
        def decorator(stateMethod):
            state = MethodicalState(machine=self,
                                    method=stateMethod)
            if initial:
                self._automaton.addInitialState(state)
            return state
        return decorator


    @_keywords_only
    def input(self):
        """
        Declare an input.

        This is a decorator for methods.
        """
        def decorator(inputMethod):
            return MethodicalInput(automaton=self._automaton,
                                   method=inputMethod,
                                   symbol=self._symbol)
        return decorator


    @_keywords_only
    def output(self):
        """
        Declare an output.

        This is a decorator for methods.

        This method will be called when the state machine transitions to this
        state as specified in the L{MethodicalMachine.output} method.
        """
        def decorator(outputMethod):
            return MethodicalOutput(machine=self, method=outputMethod)
        return decorator


    def transitions(self, transitions):
        """
        Declare a set of transitions.

        @param transitions: a L{list} of 4-tuples of (startState - a method
            decorated with C{@state()}, inputToken - a method decorated with
            C{@input()}, endState - a method decorated with C{@state()},
            outputTokens - a method decorated with C{@output()}).
        @type transitions: L{list} of 4-L{tuples} of (L{MethodicalState},
            L{MethodicalInput}, L{MethodicalState}, L{list} of
            L{types.FunctionType}).
        """
        for startState, inputToken, endState, outputTokens in transitions:
            self._oneTransition(startState, inputToken, endState, outputTokens)


    def _oneTransition(self, startState, inputToken, endState, outputTokens):
        """
        See L{transitions}.
        """
        # FIXME: tests for all of this (some of it is wrong)
        # if not isinstance(startState, MethodicalState):
        #     raise NotImplementedError("start state {} isn't a state"
        #                               .format(startState))
        # if not isinstance(inputToken, MethodicalInput):
        #     raise NotImplementedError("start state {} isn't an input"
        #                               .format(inputToken))
        # if not isinstance(endState, MethodicalState):
        #     raise NotImplementedError("end state {} isn't a state"
        #                               .format(startState))
        # for output in outputTokens:
        #     if not isinstance(endState, MethodicalState):
        #         raise NotImplementedError("output state {} isn't a state"
        #                                   .format(endState))
        self._automaton.addTransition(startState, inputToken, endState,
                                      tuple(outputTokens))
