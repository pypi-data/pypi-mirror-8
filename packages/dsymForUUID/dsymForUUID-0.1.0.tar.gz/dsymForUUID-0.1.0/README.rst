The `LLDB debugger`_ has `built-in support for symbolication`_, and in
particular on Mac OS X, for symbolicating OS X and iOS crash logs.
Unfortunately, for some reason best known to Apple, in order to function, the
``lldb.macosx.crashlog`` module requires an external script to locate ``dSYM``
files from the UUIDs listed in the crash log.  Quite why there couldn’t be a
default implementation of this is beyond me.

Anyway, this package really just contains a single script, named
``dsymForUUID`` (the name that the ``crashlog`` module expects).  The approach
taken by the script is to use Spotlight to locate the ``dSYM`` file; if it
finds, rather than a single ``dSYM``, an ``.xcarchive``, it will scan the
``dSYM`` files in the archive to locate the correct one, and will also search
for the executable.

The expectation here is that you will have Xcode archives of your releases,
in which case it should Just Work.

To use ``lldb.macosx.crashlog`` after installing this script, you can do the
following::

  (lldb) command script import lldb.macosx.crashlog
  "crashlog" and "save_crashlog" command installed, use the "--help" option for detailed help
  "malloc_info", "ptr_refs", "cstr_refs", and "objc_refs" commands have been installed, use the "--help" options on these commands for detailed help.
  (lldb) crashlog /tmp/crash.log

While I haven’t tested this, you may also be able to use the ``dsymForUUID``
script with the DebugSymbols framework (part of Mac OS X) by doing something
like::

  defaults write com.apple.DebugSymbols DBGShellCommands -string /usr/local/bin/dsymForUUID

See the `LLDB page about debug symbols on Mac OS X`_ for more on this.

.. _`LLDB debugger`: http://lldb.llvm.org
.. _`built-in support for symbolication`: http://lldb.llvm.org/symbolication.html
.. _`LLDB page about debug symbols on Mac OS X`: http://lldb.llvm.org/symbols.html
