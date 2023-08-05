from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

from reconfigure.configs import ResolvConfig
from reconfigure.items.resolv import ItemData

from api import RAIDManager


@plugin
class RAID (SectionPlugin):
    def init(self):
        self.title = _('RAID')
        self.icon = 'hdd'
        self.category = _('System')

        self.append(self.ui.inflate('raid:main'))

        def post_array_bind(o, c, i, u):
            u.find('recovery').visible = i.recovery

        self.find('arrays').post_item_bind = post_array_bind

        self.mgr = RAIDManager.get()
        self.binder = Binder(None, self)

    def on_page_load(self):
        self.refresh()

    def refresh(self):
        self.mgr.refresh()
        self.binder.setup(self.mgr).populate()
