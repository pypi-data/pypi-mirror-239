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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _1l1l111111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1l11lll111_opy_:
    def __init__(self, handler):
        self._1l1l1111l1_opy_ = {}
        self._1l11llllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._1l1l1111l1_opy_[bstack1llllll1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭მ")] = Module._inject_setup_function_fixture
        self._1l1l1111l1_opy_[bstack1llllll1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬნ")] = Module._inject_setup_module_fixture
        self._1l1l1111l1_opy_[bstack1llllll1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬო")] = Class._inject_setup_class_fixture
        self._1l1l1111l1_opy_[bstack1llllll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧპ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack1l1l111l11_opy_(bstack1llllll1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪჟ"))
        Module._inject_setup_module_fixture = self.bstack1l1l111l11_opy_(bstack1llllll1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩრ"))
        Class._inject_setup_class_fixture = self.bstack1l1l111l11_opy_(bstack1llllll1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩს"))
        Class._inject_setup_method_fixture = self.bstack1l1l111l11_opy_(bstack1llllll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫტ"))
    def bstack1l11llll1l_opy_(self, bstack1l11lll1ll_opy_, hook_type):
        meth = getattr(bstack1l11lll1ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l11llllll_opy_[hook_type] = meth
            setattr(bstack1l11lll1ll_opy_, hook_type, self.bstack1l11llll11_opy_(hook_type))
    def bstack1l1l1111ll_opy_(self, instance, bstack1l11lll11l_opy_):
        if bstack1l11lll11l_opy_ == bstack1llllll1_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢუ"):
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨფ"))
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥქ"))
        if bstack1l11lll11l_opy_ == bstack1llllll1_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣღ"):
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢყ"))
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦშ"))
        if bstack1l11lll11l_opy_ == bstack1llllll1_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥჩ"):
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤც"))
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨძ"))
        if bstack1l11lll11l_opy_ == bstack1llllll1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢწ"):
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨჭ"))
            self.bstack1l11llll1l_opy_(instance.obj, bstack1llllll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥხ"))
    @staticmethod
    def bstack1l1l11111l_opy_(hook_type, func, args):
        if hook_type in [bstack1llllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨჯ"), bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬჰ")]:
            _1l1l111111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l11llll11_opy_(self, hook_type):
        def bstack1l1l111l1l_opy_(arg=None):
            self.handler(hook_type, bstack1llllll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫჱ"))
            result = None
            exception = None
            try:
                self.bstack1l1l11111l_opy_(hook_type, self._1l11llllll_opy_[hook_type], (arg,))
                result = Result(result=bstack1llllll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬჲ"))
            except Exception as e:
                result = Result(result=bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ჳ"), exception=e)
                self.handler(hook_type, bstack1llllll1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ჴ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llllll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧჵ"), result)
        def bstack1l11ll1lll_opy_(this, arg=None):
            self.handler(hook_type, bstack1llllll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩჶ"))
            result = None
            exception = None
            try:
                self.bstack1l1l11111l_opy_(hook_type, self._1l11llllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪჷ"))
            except Exception as e:
                result = Result(result=bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫჸ"), exception=e)
                self.handler(hook_type, bstack1llllll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫჹ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llllll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬჺ"), result)
        if hook_type in [bstack1llllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭჻"), bstack1llllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪჼ")]:
            return bstack1l11ll1lll_opy_
        return bstack1l1l111l1l_opy_
    def bstack1l1l111l11_opy_(self, bstack1l11lll11l_opy_):
        def bstack1l11lll1l1_opy_(this, *args, **kwargs):
            self.bstack1l1l1111ll_opy_(this, bstack1l11lll11l_opy_)
            self._1l1l1111l1_opy_[bstack1l11lll11l_opy_](this, *args, **kwargs)
        return bstack1l11lll1l1_opy_