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
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll1lll1l_opy_, bstack1l1ll11l1l_opy_
from bstack_utils.bstack1111l11l1_opy_ import bstack11lll1lll1_opy_
class bstack11ll11l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11ll11l11l_opy_=None, framework=None, tags=[], scope=[], bstack11ll1111l1_opy_=None, bstack11ll11l111_opy_=True, bstack11ll11ll1l_opy_=None, bstack1ll111lll_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11ll11l111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11ll11l11l_opy_ = bstack11ll11l11l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11ll1111l1_opy_ = bstack11ll1111l1_opy_
        self.bstack11ll11ll1l_opy_ = bstack11ll11ll1l_opy_
        self.bstack1ll111lll_opy_ = bstack1ll111lll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l1llll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1llllll_opy_(self):
        bstack11l1lllll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1llllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪሡ"): bstack11l1lllll1_opy_,
            bstack1llllll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪሢ"): bstack11l1lllll1_opy_,
            bstack1llllll1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧሣ"): bstack11l1lllll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1llllll1_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦሤ") + key)
            setattr(self, key, val)
    def bstack11ll111111_opy_(self):
        return {
            bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩሥ"): self.name,
            bstack1llllll1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪሦ"): {
                bstack1llllll1_opy_ (u"࠭࡬ࡢࡰࡪࠫሧ"): bstack1llllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧረ"),
                bstack1llllll1_opy_ (u"ࠨࡥࡲࡨࡪ࠭ሩ"): self.code
            },
            bstack1llllll1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩሪ"): self.scope,
            bstack1llllll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨራ"): self.tags,
            bstack1llllll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧሬ"): self.framework,
            bstack1llllll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩር"): self.bstack11ll11l11l_opy_
        }
    def bstack11l1lll11l_opy_(self):
        return {
         bstack1llllll1_opy_ (u"࠭࡭ࡦࡶࡤࠫሮ"): self.meta
        }
    def bstack11ll111ll1_opy_(self):
        return {
            bstack1llllll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪሯ"): {
                bstack1llllll1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬሰ"): self.bstack11ll1111l1_opy_
            }
        }
    def bstack11ll111lll_opy_(self, bstack11ll11111l_opy_, details):
        step = next(filter(lambda st: st[bstack1llllll1_opy_ (u"ࠩ࡬ࡨࠬሱ")] == bstack11ll11111l_opy_, self.meta[bstack1llllll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩሲ")]), None)
        step.update(details)
    def bstack11ll11l1l1_opy_(self, bstack11ll11111l_opy_):
        step = next(filter(lambda st: st[bstack1llllll1_opy_ (u"ࠫ࡮ࡪࠧሳ")] == bstack11ll11111l_opy_, self.meta[bstack1llllll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫሴ")]), None)
        step.update({
            bstack1llllll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪስ"): bstack1ll1lll1l_opy_()
        })
    def bstack11l1lll1l1_opy_(self, bstack11ll11111l_opy_, result):
        bstack11ll11ll1l_opy_ = bstack1ll1lll1l_opy_()
        step = next(filter(lambda st: st[bstack1llllll1_opy_ (u"ࠧࡪࡦࠪሶ")] == bstack11ll11111l_opy_, self.meta[bstack1llllll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧሷ")]), None)
        step.update({
            bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧሸ"): bstack11ll11ll1l_opy_,
            bstack1llllll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬሹ"): bstack1l1ll11l1l_opy_(step[bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨሺ")], bstack11ll11ll1l_opy_),
            bstack1llllll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬሻ"): result.result,
            bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧሼ"): str(result.exception) if result.exception else None
        })
    def bstack11ll11lll1_opy_(self):
        return {
            bstack1llllll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬሽ"): self.bstack11l1llll11_opy_(),
            **self.bstack11ll111111_opy_(),
            **self.bstack11l1llllll_opy_(),
            **self.bstack11l1lll11l_opy_()
        }
    def bstack11l1lll111_opy_(self):
        data = {
            bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ሾ"): self.bstack11ll11ll1l_opy_,
            bstack1llllll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪሿ"): self.duration,
            bstack1llllll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪቀ"): self.result.result
        }
        if data[bstack1llllll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫቁ")] == bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቂ"):
            data[bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬቃ")] = self.result.bstack1l1l1lll1l_opy_()
            data[bstack1llllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨቄ")] = [{bstack1llllll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫቅ"): self.result.bstack1l1ll11ll1_opy_()}]
        return data
    def bstack11ll111l11_opy_(self):
        return {
            bstack1llllll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧቆ"): self.bstack11l1llll11_opy_(),
            **self.bstack11ll111111_opy_(),
            **self.bstack11l1llllll_opy_(),
            **self.bstack11l1lll111_opy_(),
            **self.bstack11l1lll11l_opy_()
        }
    def bstack11ll11llll_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack1llllll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫቇ"):
            return self.bstack11ll11lll1_opy_()
        elif event == bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ቈ"):
            return self.bstack11ll111l11_opy_()
    def bstack11ll11ll11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11ll11ll1l_opy_ = time if time else bstack1ll1lll1l_opy_()
        self.duration = duration if duration else bstack1l1ll11l1l_opy_(self.bstack11ll11l11l_opy_, self.bstack11ll11ll1l_opy_)
        if result:
            self.result = result
class bstack11ll111l1l_opy_(bstack11ll11l1ll_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack1ll111lll_opy_=bstack1llllll1_opy_ (u"ࠬࡺࡥࡴࡶࠪ቉"))
    @classmethod
    def bstack11l1lll1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1llllll1_opy_ (u"࠭ࡩࡥࠩቊ"): id(step),
                bstack1llllll1_opy_ (u"ࠧࡵࡧࡻࡸࠬቋ"): step.name,
                bstack1llllll1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩቌ"): step.keyword,
            })
        return bstack11ll111l1l_opy_(
            **kwargs,
            meta={
                bstack1llllll1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪቍ"): {
                    bstack1llllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ቎"): feature.name,
                    bstack1llllll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ቏"): feature.filename,
                    bstack1llllll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪቐ"): feature.description
                },
                bstack1llllll1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨቑ"): {
                    bstack1llllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬቒ"): scenario.name
                },
                bstack1llllll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧቓ"): steps,
                bstack1llllll1_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫቔ"): bstack11lll1lll1_opy_(test)
            }
        )
    def bstack11l1llll1l_opy_(self):
        return {
            bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩቕ"): self.hooks
        }
    def bstack11ll111l11_opy_(self):
        return {
            **super().bstack11ll111l11_opy_(),
            **self.bstack11l1llll1l_opy_()
        }
    def bstack11ll11ll11_opy_(self):
        return bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ቖ")