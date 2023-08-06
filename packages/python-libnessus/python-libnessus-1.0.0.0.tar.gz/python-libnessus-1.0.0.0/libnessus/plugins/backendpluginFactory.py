#!/usr/bin/env python
import sys
import inspect


class BackendPluginFactory(object):
    """
        This is a backend plugin factory a backend instance MUST be
        created via the static method create()
        ie : mybackend = BackendPluginFactory.create()
    """
    @classmethod
    def create(cls, plugin_name="mongodb", **kwargs):
        """Import the needed lib and return an object NessusBackendPlugin
           representing the backend of your desire.
           NessusBackendPlugin is an abstract class, to know what argument
           need to be given, review the code of the subclass you need
           :param plugin_name: str : name of the py file without .py
           :return: NessusBackend (abstract class on top of all plugin)
        """
        try:
            backendplugin = None
            plugin_path = "libnessus.plugins.%s" % (plugin_name)
            __import__(plugin_path)
            pluginobj = sys.modules[plugin_path]
            pluginclasses = inspect.getmembers(pluginobj, inspect.isclass)
            for classname, classobj in pluginclasses:
                if inspect.getmodule(classobj).__name__.find(plugin_path) == 0:
                    backendplugin = classobj(**kwargs)
        except Exception as error:
            print "Cannot create Backend: %s" % (error)
            raise error
        return backendplugin
