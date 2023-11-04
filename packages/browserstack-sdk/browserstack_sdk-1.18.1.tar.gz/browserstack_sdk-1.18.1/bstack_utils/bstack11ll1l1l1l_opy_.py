# coding: UTF-8
import sys
bstack1l1l111_opy_ = sys.version_info [0] == 2
bstack11l1lll_opy_ = 2048
bstack11l_opy_ = 7
def bstack1llllll1_opy_ (bstack11111ll_opy_):
    global bstack111ll_opy_
    bstack1l11_opy_ = ord (bstack11111ll_opy_ [-1])
    bstack111l1_opy_ = bstack11111ll_opy_ [:-1]
    bstack1111ll1_opy_ = bstack1l11_opy_ % len (bstack111l1_opy_)
    bstack1lll_opy_ = bstack111l1_opy_ [:bstack1111ll1_opy_] + bstack111l1_opy_ [bstack1111ll1_opy_:]
    if bstack1l1l111_opy_:
        bstack1l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1lll_opy_ - (bstack1l1l1ll_opy_ + bstack1l11_opy_) % bstack11l_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lll_opy_)])
    else:
        bstack1l1111_opy_ = str () .join ([chr (ord (char) - bstack11l1lll_opy_ - (bstack1l1l1ll_opy_ + bstack1l11_opy_) % bstack11l_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lll_opy_)])
    return eval (bstack1l1111_opy_)
class bstack11ll1ll111_opy_:
    def __init__(self, handler):
        self._11ll1l1ll1_opy_ = None
        self.handler = handler
        self._11ll1ll11l_opy_ = self.bstack11ll1l1lll_opy_()
        self.patch()
    def patch(self):
        self._11ll1l1ll1_opy_ = self._11ll1ll11l_opy_.execute
        self._11ll1ll11l_opy_.execute = self.bstack11ll1ll1l1_opy_()
    def bstack11ll1ll1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._11ll1l1ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._11ll1ll11l_opy_.execute = self._11ll1l1ll1_opy_
    @staticmethod
    def bstack11ll1l1lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver