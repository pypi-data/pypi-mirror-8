from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='IPMI',
    description='Intel power management interface widgets',
    icon='dashboard',
    dependencies=[
        PluginDependency('main'),
        PluginDependency('dashboard'),
        BinaryDependency('ipmitool')
    ],
)


def init():
    import widget
    import sensor