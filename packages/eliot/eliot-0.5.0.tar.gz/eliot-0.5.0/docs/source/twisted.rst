Using Eliot with Twisted
========================

Eliot provides a variety of APIs to support integration with the `Twisted`_ networking framework.

.. _Twisted: https://twistedmatrix.com


.. _ThreadedFileWriter:

Destinations
------------

``eliot.logwriter.ThreadedFileWriter`` is a logging destination that writes to a file-like object in a thread.
This is useful because it keeps the Twisted thread from blocking if writing to the log file is slow.
``ThreadedFileWriter`` is a Twisted ``Service`` and starting it will call ``add_destination`` for you and stopping it will call ``remove_destination``; there is no need to call those directly.

.. literalinclude:: ../../examples/logfile.py

If you want log rotation you can pass in one of the classes from `twisted.python.logfile`_ as the destination file.

.. _twisted.python.logfile: https://twistedmatrix.com/documents/current/api/twisted.python.logfile.html

If you're using Twisted's ``trial`` program to run your tests you can redirect your Eliot logs to Twisted's logs by calling ``eliot.twisted.redirectLogsForTrial()``.
This function will automatically detect whether or not it is running under ``trial``.
If it is then you will be able to read your Eliot logs in ``_trial_temp/test.log``, where ``trial`` writes out logs by default.
If it is not running under ``trial`` it will not do anything.
In addition calling it multiple times has the same effect as calling it once.
As a result you can simply call it in your package's ``__init__.py`` and rely on it doing the right thing.
Take care if you are separately redirecting Twisted logs to Eliot; you should make sure not to call ``redirectLogsForTrial`` in that case so as to prevent infinite loops.


Logging Failures
----------------

``eliot.writeFailure`` is the equivalent of ``eliot.write_traceback``, only for ``Failure`` instances:

.. code-block:: python

    from eliot import Logger, writeFailure

    class YourClass(object):
        logger = Logger()

        def run(self):
            d = dosomething()
            d.addErrback(writeFailure, self.logger, u"yourapp:yourclass")


Actions and Deferreds
---------------------

An additional set of APIs is available to help log actions when using Deferreds.
To understand why, consider the following example:

.. code-block:: python

     from eliot import startAction, Logger

     logger = Logger()


     def go():
         action = startAction(logger, u"yourapp:subsystem:frob")
         with action:
             d = Deferred()
             d.addCallback(gotResult, x=1)
             return d

This has two problems.
First, ``gotResult`` is not going to run in the context of the action.
Second, the action finishes once the ``with`` block finishes, i.e. before ``gotResult`` runs.
If we want ``gotResult`` to be run in the context of the action and to delay the action finish we need to do some extra work, and manually wrapping all callbacks would be tedious.

To solve this problem you can use the ``eliot.twisted.DeferredContext`` class.
It grabs the action context when it is first created and provides the same API as ``Deferred`` (``addCallbacks`` and friends), with the difference that added callbacks run in the context of the action.
When all callbacks have been added you can indicate that the action should finish after those callbacks have run by calling ``DeferredContext.addActionFinish``.
As you would expect, if the ``Deferred`` fires with a regular result that will result in success message.
If the ``Deferred`` fires with an errback that will result in failure message.
Finally, you can unwrap the ``DeferredContext`` and access the wrapped ``Deferred`` by accessing its ``result`` attribute.

.. code-block:: python

     from eliot import startAction, Logger
     from eliot.twisted import DeferredContext

     logger = Logger()


     def go():
         action = startAction(logger, u"yourapp:subsystem:frob")
         with action.context():
             d = DeferredContext(Deferred())
             # gotResult(result, x=1) will be called in the context of the action:
             d.addCallback(gotResult, x=1)
             # After gotResult finishes, finish the action:
             d.addActionFinish()
             # Return the underlying Deferred:
             return d.result
