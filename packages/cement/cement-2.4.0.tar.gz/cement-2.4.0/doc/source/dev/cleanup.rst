Application Cleanup
===================

The concept of 'cleanup' after application run time is nothing new.  What
happens during 'cleanup' all depends on the application.  This might mean
cleaning up temporary files, removing session data, or removing a PID
(Process ID) file.

To allow for application cleanup not only within your program, but also
external plugins and extensions, there is the ``app.close()`` function that
must be called after ``app.run()`` regardless of any exceptions or runtime
errors.

For example:

.. code-block:: python

    from cement.core import foundation

    app = foundation.CementApp('helloworld')

    try:
        app.setup()
        app.run()
    finally:
        app.close()


You will note that we put ``app.run()`` within a ``try`` block, and
``app.close()`` in a ``finally`` block.  The important thing to note is that
regardless of whether an exception is encountered or not, we always run
``app.close()``.  This is where the ``pre_close`` and ``post_close`` hooks are
run, allowing extensions/plugins/etc to cleanup after the program runs.

Also note that you can optionally pass an exit code to ``app.close()`` to tell
Cement to exit the app here as well:

.. code-block:: python

    # non-error exit status is generally 0
    app.close(0)

    # or exit with an error
    app.close(1)


Running Cleanup Code
--------------------

Any extension, or plugin, or even the application itself that has 'cleanup'
code should do so within the ``pre_close`` or ``post_close`` hooks to ensure
that it gets run.  For example:

.. code-block:: python

    from cement.core import hook

    def my_cleanup(app):
        # do something when app.close() is called
        pass

    hook.register('pre_close', my_cleanup)
