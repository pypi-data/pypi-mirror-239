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
import multiprocessing
import os
from browserstack_sdk.bstack11l111l1l_opy_ import *
from bstack_utils.helper import bstack1l1ll1l11_opy_
from bstack_utils.messages import bstack11ll1ll11_opy_
from bstack_utils.constants import bstack1llllll1ll_opy_
class bstack11l11l1ll_opy_:
    def __init__(self, args, logger, bstack1ll111l11l_opy_, bstack1ll111l1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll111l11l_opy_ = bstack1ll111l11l_opy_
        self.bstack1ll111l1l1_opy_ = bstack1ll111l1l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1ll11ll_opy_ = []
        self.bstack1ll111l1ll_opy_ = None
        self.bstack11ll1ll1_opy_ = []
        self.bstack1ll111lll1_opy_ = self.bstack11lllll1_opy_()
        self.bstack1l111lll1_opy_ = -1
    def bstack1111l1l1l_opy_(self, bstack1ll111llll_opy_):
        self.parse_args()
        self.bstack1ll11l111l_opy_()
        self.bstack1ll111l111_opy_(bstack1ll111llll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1ll11l1111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l111lll1_opy_ = -1
        if bstack1llllll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫದ") in self.bstack1ll111l11l_opy_:
            self.bstack1l111lll1_opy_ = self.bstack1ll111l11l_opy_[bstack1llllll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬಧ")]
        try:
            bstack1ll111ll1l_opy_ = [bstack1llllll1_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨನ"), bstack1llllll1_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ಩"), bstack1llllll1_opy_ (u"ࠨ࠯ࡳࠫಪ")]
            if self.bstack1l111lll1_opy_ >= 0:
                bstack1ll111ll1l_opy_.extend([bstack1llllll1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪಫ"), bstack1llllll1_opy_ (u"ࠪ࠱ࡳ࠭ಬ")])
            for arg in bstack1ll111ll1l_opy_:
                self.bstack1ll11l1111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11l111l_opy_(self):
        bstack1ll111l1ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll111l1ll_opy_ = bstack1ll111l1ll_opy_
        return bstack1ll111l1ll_opy_
    def bstack1lll1ll1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1ll11l11l1_opy_ = importlib.find_loader(bstack1llllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ಭ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11ll1ll11_opy_)
    def bstack1ll111l111_opy_(self, bstack1ll111llll_opy_):
        if bstack1ll111llll_opy_:
            self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩಮ"))
            self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"࠭ࡔࡳࡷࡨࠫಯ"))
        self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠧ࠮ࡲࠪರ"))
        self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ಱ"))
        self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫಲ"))
        self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪಳ"))
        if self.bstack1l111lll1_opy_ > 1:
            self.bstack1ll111l1ll_opy_.append(bstack1llllll1_opy_ (u"ࠫ࠲ࡴࠧ಴"))
            self.bstack1ll111l1ll_opy_.append(str(self.bstack1l111lll1_opy_))
    def bstack1ll11l11ll_opy_(self):
        bstack11ll1ll1_opy_ = []
        for spec in self.bstack1l1ll11ll_opy_:
            bstack111llllll_opy_ = [spec]
            bstack111llllll_opy_ += self.bstack1ll111l1ll_opy_
            bstack11ll1ll1_opy_.append(bstack111llllll_opy_)
        self.bstack11ll1ll1_opy_ = bstack11ll1ll1_opy_
        return bstack11ll1ll1_opy_
    def bstack11lllll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll111lll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll111lll1_opy_ = False
        return self.bstack1ll111lll1_opy_
    def bstack111ll1ll1_opy_(self, bstack1ll111ll11_opy_, bstack1111l1l1l_opy_):
        bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬವ")] = self.bstack1ll111l11l_opy_
        if bstack1llllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಶ") in self.bstack1ll111l11l_opy_:
            bstack1ll1ll1l1l_opy_ = []
            manager = multiprocessing.Manager()
            bstack111l111l1_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1ll111l11l_opy_[bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಷ")]):
                bstack1ll1ll1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1ll111ll11_opy_,
                                                           args=(self.bstack1ll111l1ll_opy_, bstack1111l1l1l_opy_)))
            i = 0
            for t in bstack1ll1ll1l1l_opy_:
                os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨಸ")] = str(i)
                i += 1
                t.start()
            for t in bstack1ll1ll1l1l_opy_:
                t.join()
            return bstack111l111l1_opy_