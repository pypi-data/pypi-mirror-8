
import pyblish.backend.lib
import pyblish.backend.plugin


@pyblish.backend.lib.log
class SelectDuplicateInstance(pyblish.backend.plugin.Selector):
    hosts = ['python']
    version = (0, 1, 0)
