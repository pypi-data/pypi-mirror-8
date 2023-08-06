Logging Actions and Tasks
=========================

Actions: A Start and a Finish
-----------------------------

A higher-level construct than messages is the concept of an action.
An action can be started, and then finishes either successfully or with some sort of an exception.
Success in this case simply means no exception was thrown; the result of an action may be a successful response saying "this did not work".
Log messages are emitted for action start and finish.

Actions are also nested; one action can be the parent of another.
An action's parent is deduced from the Python call stack and context managers like ``Action.context()``.
Log messages will also note the action they are part of if they can deduce it from the call stack.
The result of all this is that you can trace the operation of your code as it logs various actions, and see a narrative of what happened and what caused it to happen.

Tasks: Top-level Actions
------------------------

A top-level action with no parent is called a task, the root cause of all its child actions.
E.g. a web server receiving a new HTTP request would create a task for that new request.
Log messages emitted from Eliot are therefore logically structured as a forest: trees of actions with tasks at the root.

While the logical structure of log messages is a forest, the actual output is effectively a list of dictionaries (e.g. a series of JSON messages written to a file).
To bridge the gap between the two structures each output message contains enough information to recreate the logical relationship between it and other messages:

1. The task, identified using a UUID.
2. The specific action within that task's action tree.
3. A per-action counter that is incremented for each new output message directly within that action.

See the :doc:`Fields <fields>` documentation for more details about the way these fields define a tree structure.

Logging Actions
---------------

Here's a basic example of logging an action:

.. code-block:: python

     from eliot import start_action, Logger

     logger = Logger()

     with start_action(logger, u"yourapp:subsystem:frob"):
         x = _beep()
         frobinate(x)

This will log an action start message and if the block finishes successfully an action success message.
If an exception is thrown by the block then an action failure message will be logged along with the exception type and reason as additional fields.
Each action thus results in two messages being logged: at the start and finish of the action.
No traceback will be logged so if you want a traceback you will need to do so explicitly.
Notice that the action has a name, with a subsystem prefix.
Again, this should be a logical name.

Note that all code called within this block is within the context of this action.
While running the block of code within the ``with`` statement new actions created with ``start_action`` will get the top-level ``start_action`` as their parent.
If there is no parent the action will be considered a task.
If you want to ignore the context and create a top-level task you can use the ``eliot.start_task`` API.


Non-Finishing Contexts
----------------------

Sometimes you want to have the action be the context for other messages but not finish automatically when the block finishes.
You can do so with ``Action.context()``.
You can explicitly finish an action by calling ``eliot.Action.finish``.
If called with an exception it indicates the action finished unsuccessfully.
If called with no arguments it indicates that the action finished successfully.
Keep in mind that code within the context block that is run after the action is finished will still be in that action's context.

.. code-block:: python

     from eliot import start_action, Logger

     logger = Logger()

     action = start_action(logger, u"yourapp:subsystem:frob"):
     try:
         with action.context():
             x = _beep()
         with action.context():
             frobinate(x)
         # Action still isn't finished, need to so explicitly.
     except FrobError as e:
         action.finish(e)
     else:
         action.finish()

You can also explicitly run a function within the action context:

.. code-block:: python

     from eliot import start_action, Logger

     logger = Logger()

     action = start_action(logger, u"yourapp:subsystem:frob")
     # Call do_something(x=1) in context of action, return its result:
     result = action.run(do_something, x=1)


Action Fields
^^^^^^^^^^^^^

You can add fields to both the start message and the success message of an action.

.. code-block:: python

     from eliot import start_action, Logger

     logger = Logger()

     with start_action(logger, u"yourapp:subsystem:frob",
                      # Fields added to start message only:
                      key=123, foo=u"bar") as action:
         x = _beep(123)
         result = frobinate(x)
         # Fields added to success message only:
         action.add_success_fields(result=result)

If you want to include some extra information in case of failures beyond the exception you can always log a regular message with that information.
Since the message will be recorded inside the context of the action its information will be clearly tied to the result of the action by the person (or code!) reading the logs later on.
