
ParselTongue Magic
==================

This python module adds ipython magic for the ParselTongue language that
is part of the `online programming languages
class <http://cs.brown.edu/courses/csci1730/2012/OnLine/>`__ run at
Brown.

You can install this module using ``pip`` as follows pip install
pslmagic

Notes for Windows Users
-----------------------

If you intend to use this module on Windows, you will need the do the
following

1) install and have ``bash`` on your PATH. An acceptable version of bash
   is included in the Git for Windows installer, make sure to select
   **Use Git and optional Unix tools for the Windows Command Prompt**

2) Use relative addresses when registering the executable and specifying
   the test file base (see below).

Using ``pslmagic``
------------------

The first step when using ``pslmagic`` is to start the ipython notebook,
preferably from the command line in the test folder.

::

    ipython notebook

Load the magic
~~~~~~~~~~~~~~

Start a new notebook and run the following command to load ``palmagic``

.. code:: python

    %load_ext pslmagic

.. parsed-literal::

    WARNING:Please register the address of the ParselTongue executable            using %psl_exe <address>


Register the ParselTongue interpreter(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to download the parseltongue interpreter from the `Brown CS1730
page <http://cs.brown.edu/courses/csci1730/2012/Assignments/ParselTest/Software/>`__

Then, call the ``psl_exe`` to register the address for the execuable
(*Use a relative address for Windows*)

.. code:: python

    %psl_exe ../../../win32-dist/win32-dist/assignment1-win32.exe

Line magic to evaluate short commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can evaluate a single line of ParselTongue using the ``psl`` magic.
A single % indicates *line* magic

.. code:: python

    %psl +(40, 2)

.. parsed-literal::

    42
    


Errors are thrown as python exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    %psl 5;7

::


      File "<string>", line unknown
    SyntaxError: Encountered error while parsing, near: "" [line=#f, column=#f, position=#f]
    



Use cell magic to evaluate longer programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can type a whole cell of ParselTongue using the ``%%psl`` cell
magic. The double % are used to indicate cell magic, and the remainder
of the current cell will be considered ParselTongue.

.. code:: python

    %%psl
    # deffun defines a recursive function
    deffun fib(n)
      # operators like + and == are prefix
      if <(n, 1) then 0 else
      if ==(n, 1) then 1 else
      +(fib(-(n, 1)), fib(-(n, 2)))
    # The in ends the function body in a deffun, which can be followed by
    # another deffun, a defvar, or a braced expression
    in
    # defvar creates a new variable with an initial value, bound inside the
    # body of the defvar
    defvar x = 0 in {
      # For loops have an initialization, a test, an update, and a body
      for(x = 0; <(x,10); x++) {
        # print takes any value and displays it
        print(fib(x));
        print(" ");
      };
      # The result of the program is the value of the last expression
      # evaluated.  It is printed, so we avoid printing it by terminating the
      # program with a ""
      "";
    }

.. parsed-literal::

    0 1 1 2 3 5 8 13 21 34 
    


Create tests for the test suite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a test for your test suite using the
``%%psl_create_test`` magic. The first argument (on the
``%%psl_create_test line``) is the base file name. Three files will be
created

1) base.psl - contains the code in the cell

2) base.psl.expected - creates the output when running the code vs. the
   correct interpreter.

3) base.psl.error - contains any errors generated when running vs. the
   correct interpreter



.. code:: python

    %%psl_create_test test_case
    # deffun defines a recursive function
    deffun fib(n)
      # operators like + and == are prefix
      if <(n, 1) then 0 else
      if ==(n, 1) then 1 else
      +(fib(-(n, 1)), fib(-(n, 2)))
    # The in ends the function body in a deffun, which can be followed by
    # another deffun, a defvar, or a braced expression
    in
    # defvar creates a new variable with an initial value, bound inside the
    # body of the defvar
    defvar x = 0 in {
      # For loops have an initialization, a test, an update, and a body
      for(x = 0; <(x,10); x++) {
        # print takes any value and displays it
        print(fib(x));
        print(" ");
      };
      # The result of the program is the value of the last expression
      # evaluated.  It is printed, so we avoid printing it by terminating the
      # program with a ""
      "";
    }


To inspect the resulting files, run the following commands

.. code:: python

    %%bash
    echo "*******PSL FILE*******"
    less test_case.psl
    echo "*******EXPECTED RESULTS FILE*******"
    less test_case.psl.expected
    echo "*******ERROR FILE*******"
    less test_case.psl.error

.. parsed-literal::

    *******PSL FILE*******
    # deffun defines a recursive function
    deffun fib(n)
      # operators like + and == are prefix
      if <(n, 1) then 0 else
      if ==(n, 1) then 1 else
      +(fib(-(n, 1)), fib(-(n, 2)))
    # The in ends the function body in a deffun, which can be followed by
    # another deffun, a defvar, or a braced expression
    in
    # defvar creates a new variable with an initial value, bound inside the
    # body of the defvar
    defvar x = 0 in {
      # For loops have an initialization, a test, an update, and a body
      for(x = 0; <(x,10); x++) {
        # print takes any value and displays it
        print(fib(x));
        print(" ");
      };
      # The result of the program is the value of the last expression
      # evaluated.  It is printed, so we avoid printing it by terminating the
      # program with a ""
      "";
    }*******EXPECTED RESULTS FILE*******
    0 1 1 2 3 5 8 13 21 34 
    *******ERROR FILE*******


Run the test suite versus the 25 incorrect interpreters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can run your test suite versus the 25 incorrect interpreters using
the ``%psl_run_tests`` magic. The first argument is the address of the
execuable (again using relative addresses on Windows)

.. code:: python

    %psl_run_tests ../../../sample-test-suite/

.. parsed-literal::

    bindings1:
    Bug not found!
    bindings2:
    Bug not found!
    bindings3:
    Differences in:
    c:\Users\tiverson.SMUMN\Desktop\sample-tests\sample-test-suite\pslmagic\../../../sample-test-suite/functions\func5.psl
    
    bindings4:
    Bug not found!
    functions1:
    Differences in:
    c:\Users\tiverson.SMUMN\Desktop\sample-tests\sample-test-suite\pslmagic\../../../sample-test-suite/functions\func5.psl
    
    functions2:
    Bug not found!
    functions3:
    Bug not found!
    if-then-else1:
    Bug not found!
    if-then-else2:
    Bug not found!
    if-then-else3:
    Differences in:
    c:\Users\tiverson.SMUMN\Desktop\sample-tests\sample-test-suite\pslmagic\../../../sample-test-suite/if1.psl
    
    loops1:
    Bug not found!
    loops2:
    Bug not found!
    loops3:
    Bug not found!
    loops4:
    Bug not found!
    loops5:
    Bug not found!
    objects1:
    Bug not found!
    objects2:
    Bug not found!
    objects3:
    Bug not found!
    objects4:
    Bug not found!
    operators1:
    Bug not found!
    operators2:
    Bug not found!
    operators2:
    Bug not found!
    operators3:
    Bug not found!
    sequence1:
    Bug not found!
    sequence2:
    Bug not found!
    You found bugs in 3/25 interpreters.
    
    

