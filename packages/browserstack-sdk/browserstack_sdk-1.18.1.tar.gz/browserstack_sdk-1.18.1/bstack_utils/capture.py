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
import sys
class bstack1l1lll1lll_opy_:
    def __init__(self, handler):
        self._1l1lll1ll1_opy_ = sys.stdout.write
        self._1l1lll1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1l1lll1l11_opy_
        sys.stdout.error = self.bstack1l1lll11ll_opy_
    def bstack1l1lll1l11_opy_(self, _str):
        self._1l1lll1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack1llllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩണ"): bstack1llllll1_opy_ (u"ࠫࡎࡔࡆࡐࠩത"), bstack1llllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഥ"): _str})
    def bstack1l1lll11ll_opy_(self, _str):
        self._1l1lll1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1llllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬദ"): bstack1llllll1_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ധ"), bstack1llllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩന"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1l1lll1ll1_opy_
        sys.stderr.write = self._1l1lll1l1l_opy_