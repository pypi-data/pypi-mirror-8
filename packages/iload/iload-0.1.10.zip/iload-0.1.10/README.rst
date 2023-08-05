Load or reload python object
-----------------------------

import module::

    import iload

load moudule::

    mod = iload.iload('mymodule')

load function::

    func = iload.iload('mymodule.func')

load class::

    MyClass = iload.iload('mymodule.MyClass')

reload module::

    new_mod = iload.ireload(mod)

reload function::

    new_func = iload.ireload(func)

reload class::

    NewMyClass = iload.ireload(MyClass)
