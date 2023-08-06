Command Line Client
-------------------

The ``pds`` command line client provides commands for interacting with the You Technology
Personal Data Store.  The overall command structure is fairly simple,
with command groups for each major resource in the PDS (types, scopes,
etc...). All inputs and outputs are in the form of JSON documents.

Command Line Tutorial
~~~~~~~~~~~~~~~~~~~~~

We have created a simple sample which includes the definition of 2 types
(CompilerTest and ActivityScore), data for CompilerTest and an answer
module which updates one type and generates new data for the other. The
files for this are in the ``pdscli/examples`` directory.

Setup
^^^^^

First we need to configure the PDS client and get logged into our PDS.
These commands only need to be done once on a given developer's PDS
(though you'll need to repeat them if you completely wipe the data from
your PDS installation).

-  **pds config set host *<pds host>***

   Sets the host to which to connect. If you don't specify one we will
   assume ``pds.you.tc``. You can override the host on any command using the 
   ``--host`` argument. The configuration is stored persistently in 
   ``~/.youtech/config``.

-  **pds login**

   The first time this is run it will prompt you for your user name and
   password. If you don't exist yet as a user it will register you and
   then also prompt for your full name. Once authenticated you will be
   given an OAuth token which permits developer access and we will store
   the user and token in your ``.netrc`` file (or ``_netrc`` on Windows)
   for later use. This command will need to be repeated when the generated
   OAuth token expires or is revoked for some reason.

-  **pds config set namespace tc.you.demo**

   This configures the namespace which is bound to your PDS. In order to
   create new PDS meta-data (types, scopes, answer modules, etc...) your
   PDS must be bound to an existing namespace.

Create new PDS artifacts
^^^^^^^^^^^^^^^^^^^^^^^^

Now that we've configured our PDS (and client) for development we can
start loading new meta-data into the PDS.

-  **pds types load pdscli/examples/types.json**
-  **pds data load tc.you.CompilerTest
   pdscli/examples/compilerTest.json**
-  **pds data fetch tc.you.CompilerTest**

   The first 2 commands load the type definitions and then some data for
   the ``tc.you.CompilerTest`` type. You can do ``pds types help`` to
   find out about more type commands. The last command will show us the
   data we added.

-  **pds modules load pdscli/examples/compilerActivityModule.py**

   This will load the given module into the PDS.

Promoting artifacts to the System PDS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All of the things we've created to this point reside in our own local
PDS. In order for them to be used by users or other developers we need
to promote them to the system PDS. This is also currently necessary in
order to run any answer module (since the scheduler sees only the
contents of the system PDS). So let's do that now.

-  **pds types promote all**
-  **pds modules promote all**

   This will promote all of the types that we've defined and all of the
   answer modules that we've defined. This is all we need to do since
   these are the only things we've created to this point (if/when we
   create other artifacts we'd need to promote them as well).

Promoting the module will also create a job for it which will be
scheduled every hour by default. This job will be scheduled immediately
and process the data that we previously added to our PDS. We can see the
results of this execution by looking at the data in our PDS.

-  **pds data fetch tc.you.CompilerTest**
-  **pds data fetch tc.you.ActivityScore**

   This lets us see the data in our PDS. We should see that
   ``tc.you.CompilerTest`` has been updated and a new object was added
   to ``tc.you.ActivityScore``. Woot -- we ran our first answer module.