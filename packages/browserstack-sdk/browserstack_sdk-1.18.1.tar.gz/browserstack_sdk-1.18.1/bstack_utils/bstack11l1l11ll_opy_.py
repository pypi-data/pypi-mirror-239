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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1ll111111l_opy_, bstack1ll1l1l11l_opy_, get_host_info, bstack1l1lllll11_opy_, bstack1l1llll1ll_opy_, bstack1l1l1ll111_opy_, \
    bstack1l1l1l1lll_opy_, bstack1l1ll1111l_opy_, bstack1ll111l11_opy_, bstack1l1l11l1ll_opy_, bstack1l1l1ll1ll_opy_, bstack1l1ll1l11l_opy_
from bstack_utils.bstack11ll1llll1_opy_ import bstack11lll1111l_opy_
from bstack_utils.bstack11ll1111ll_opy_ import bstack11ll11l1ll_opy_
bstack11l1l1ll1l_opy_ = [
    bstack1llllll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ቗"), bstack1llllll1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪቘ"), bstack1llllll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ቙"), bstack1llllll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩቚ"),
    bstack1llllll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫቛ"), bstack1llllll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫቜ"), bstack1llllll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬቝ")
]
bstack11l1l11111_opy_ = bstack1llllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ቞")
logger = logging.getLogger(__name__)
class bstack1111l111l_opy_:
    bstack11ll1llll1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def launch(cls, bs_config, bstack11l1ll11ll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack11l11lllll_opy_():
            return
        cls.bstack11l1l1l111_opy_()
        bstack1l1lllllll_opy_ = bstack1l1lllll11_opy_(bs_config)
        bstack1l1lllll1l_opy_ = bstack1l1llll1ll_opy_(bs_config)
        data = {
            bstack1llllll1_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭቟"): bstack1llllll1_opy_ (u"ࠧ࡫ࡵࡲࡲࠬበ"),
            bstack1llllll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧቡ"): bs_config.get(bstack1llllll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧቢ"), bstack1llllll1_opy_ (u"ࠪࠫባ")),
            bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩቤ"): bs_config.get(bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨብ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩቦ"): bs_config.get(bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩቧ")),
            bstack1llllll1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ቨ"): bs_config.get(bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬቩ"), bstack1llllll1_opy_ (u"ࠪࠫቪ")),
            bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡢࡸ࡮ࡳࡥࠨቫ"): datetime.datetime.now().isoformat(),
            bstack1llllll1_opy_ (u"ࠬࡺࡡࡨࡵࠪቬ"): bstack1l1l1ll111_opy_(bs_config),
            bstack1llllll1_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩቭ"): get_host_info(),
            bstack1llllll1_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨቮ"): bstack1ll1l1l11l_opy_(),
            bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨቯ"): os.environ.get(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨተ")),
            bstack1llllll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨቱ"): os.environ.get(bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩቲ"), False),
            bstack1llllll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧታ"): bstack1ll111111l_opy_(),
            bstack1llllll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧቴ"): {
                bstack1llllll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧት"): bstack11l1ll11ll_opy_.get(bstack1llllll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩቶ"), bstack1llllll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩቷ")),
                bstack1llllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ቸ"): bstack11l1ll11ll_opy_.get(bstack1llllll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨቹ")),
                bstack1llllll1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩቺ"): bstack11l1ll11ll_opy_.get(bstack1llllll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫቻ"))
            }
        }
        config = {
            bstack1llllll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬቼ"): (bstack1l1lllllll_opy_, bstack1l1lllll1l_opy_),
            bstack1llllll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩች"): cls.default_headers()
        }
        response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧቾ"), cls.request_url(bstack1llllll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪቿ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1llllll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪኀ")] = bstack1llllll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫኁ")
            os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧኂ")] = bstack1llllll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬኃ")
            os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧኄ")] = bstack1llllll1_opy_ (u"ࠤࡱࡹࡱࡲࠢኅ")
            os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫኆ")] = bstack1llllll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤኇ")
            bstack11l1l1lll1_opy_ = response.json()
            if bstack11l1l1lll1_opy_ and bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ኈ")]:
                error_message = bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ኉")]
                if bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪኊ")] == bstack1llllll1_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡊࡐ࡙ࡅࡑࡏࡄࡠࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘ࠭ኋ"):
                    logger.error(error_message)
                elif bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬኌ")] == bstack1llllll1_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠩኍ"):
                    logger.info(error_message)
                elif bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧ኎")] == bstack1llllll1_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡘࡊࡋࡠࡆࡈࡔࡗࡋࡃࡂࡖࡈࡈࠬ኏"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1llllll1_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣነ"))
            return [None, None, None]
        logger.debug(bstack1llllll1_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫኑ"))
        os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧኒ")] = bstack1llllll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧና")
        bstack11l1l1lll1_opy_ = response.json()
        if bstack11l1l1lll1_opy_.get(bstack1llllll1_opy_ (u"ࠪ࡮ࡼࡺࠧኔ")):
            os.environ[bstack1llllll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬን")] = bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠬࡰࡷࡵࠩኖ")]
            os.environ[bstack1llllll1_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪኗ")] = json.dumps({
                bstack1llllll1_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩኘ"): bstack1l1lllllll_opy_,
                bstack1llllll1_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪኙ"): bstack1l1lllll1l_opy_
            })
        if bstack11l1l1lll1_opy_.get(bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫኚ")):
            os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩኛ")] = bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ኜ")]
        if bstack11l1l1lll1_opy_.get(bstack1llllll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩኝ")):
            os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧኞ")] = str(bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫኟ")])
        return [bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠨ࡬ࡺࡸࠬአ")], bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫኡ")], bstack11l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧኢ")]]
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1llllll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬኣ")] == bstack1llllll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥኤ") or os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬእ")] == bstack1llllll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧኦ"):
            print(bstack1llllll1_opy_ (u"ࠨࡇ࡛ࡇࡊࡖࡔࡊࡑࡑࠤࡎࡔࠠࡴࡶࡲࡴࡇࡻࡩ࡭ࡦࡘࡴࡸࡺࡲࡦࡣࡰࠤࡗࡋࡑࡖࡇࡖࡘ࡚ࠥࡏࠡࡖࡈࡗ࡙ࠦࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞ࠦ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩኧ"))
            return {
                bstack1llllll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩከ"): bstack1llllll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩኩ"),
                bstack1llllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬኪ"): bstack1llllll1_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪካ")
            }
        else:
            cls.bstack11ll1llll1_opy_.shutdown()
            data = {
                bstack1llllll1_opy_ (u"࠭ࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࠩኬ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1llllll1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨክ"): cls.default_headers()
            }
            bstack1l1l11ll1l_opy_ = bstack1llllll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩኮ").format(os.environ[bstack1llllll1_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣኯ")])
            bstack11l1ll1ll1_opy_ = cls.request_url(bstack1l1l11ll1l_opy_)
            response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠪࡔ࡚࡚ࠧኰ"), bstack11l1ll1ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1llllll1_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ኱"))
    @classmethod
    def bstack11l11llll1_opy_(cls):
        if cls.bstack11ll1llll1_opy_ is None:
            return
        cls.bstack11ll1llll1_opy_.shutdown()
    @classmethod
    def bstack111111l11_opy_(cls):
        if cls.on():
            print(
                bstack1llllll1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨኲ").format(os.environ[bstack1llllll1_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧኳ")]))
    @classmethod
    def bstack11l1l1l111_opy_(cls):
        if cls.bstack11ll1llll1_opy_ is not None:
            return
        cls.bstack11ll1llll1_opy_ = bstack11lll1111l_opy_(cls.bstack11l11lll1l_opy_)
        cls.bstack11ll1llll1_opy_.start()
    @classmethod
    def bstack11l1l111l1_opy_(cls, bstack11l1ll1l1l_opy_, bstack11l1l1ll11_opy_=bstack1llllll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ኴ")):
        if not cls.on():
            return
        bstack1ll111lll_opy_ = bstack11l1ll1l1l_opy_[bstack1llllll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬኵ")]
        bstack11l1l1111l_opy_ = {
            bstack1llllll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ኶"): bstack1llllll1_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧ኷"),
            bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ኸ"): bstack1llllll1_opy_ (u"࡚ࠬࡥࡴࡶࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧኹ"),
            bstack1llllll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧኺ"): bstack1llllll1_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙࡫ࡪࡲࡳࡩࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ኻ"),
            bstack1llllll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬኼ"): bstack1llllll1_opy_ (u"ࠩࡏࡳ࡬ࡥࡕࡱ࡮ࡲࡥࡩ࠭ኽ"),
            bstack1llllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫኾ"): bstack1llllll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨ኿"),
            bstack1llllll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧዀ"): bstack1llllll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨ዁"),
            bstack1llllll1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫዂ"): bstack1llllll1_opy_ (u"ࠨࡅࡅࡘࡤ࡛ࡰ࡭ࡱࡤࡨࠬዃ")
        }.get(bstack1ll111lll_opy_)
        if bstack11l1l1ll11_opy_ == bstack1llllll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨዄ"):
            cls.bstack11l1l1l111_opy_()
            cls.bstack11ll1llll1_opy_.add(bstack11l1ll1l1l_opy_)
        elif bstack11l1l1ll11_opy_ == bstack1llllll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨዅ"):
            cls.bstack11l11lll1l_opy_([bstack11l1ll1l1l_opy_], bstack11l1l1ll11_opy_)
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def bstack11l11lll1l_opy_(cls, bstack11l1ll1l1l_opy_, bstack11l1l1ll11_opy_=bstack1llllll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ዆")):
        config = {
            bstack1llllll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭዇"): cls.default_headers()
        }
        response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"࠭ࡐࡐࡕࡗࠫወ"), cls.request_url(bstack11l1l1ll11_opy_), bstack11l1ll1l1l_opy_, config)
        bstack1ll1111lll_opy_ = response.json()
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def bstack11l1ll1lll_opy_(cls, bstack11l11ll1l1_opy_):
        bstack11l1l11lll_opy_ = []
        for log in bstack11l11ll1l1_opy_:
            bstack11l1l111ll_opy_ = {
                bstack1llllll1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬዉ"): bstack1llllll1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪዊ"),
                bstack1llllll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨዋ"): log[bstack1llllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩዌ")],
                bstack1llllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧው"): log[bstack1llllll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨዎ")],
                bstack1llllll1_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ዏ"): {},
                bstack1llllll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨዐ"): log[bstack1llllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩዑ")],
            }
            if bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩዒ") in log:
                bstack11l1l111ll_opy_[bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪዓ")] = log[bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫዔ")]
            elif bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዕ") in log:
                bstack11l1l111ll_opy_[bstack1llllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ዖ")] = log[bstack1llllll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ዗")]
            bstack11l1l11lll_opy_.append(bstack11l1l111ll_opy_)
        cls.bstack11l1l111l1_opy_({
            bstack1llllll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬዘ"): bstack1llllll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ዙ"),
            bstack1llllll1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨዚ"): bstack11l1l11lll_opy_
        })
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def bstack11l1l1l1l1_opy_(cls, steps):
        bstack11l1l11l11_opy_ = []
        for step in steps:
            bstack11l11lll11_opy_ = {
                bstack1llllll1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩዛ"): bstack1llllll1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨዜ"),
                bstack1llllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬዝ"): step[bstack1llllll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ዞ")],
                bstack1llllll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫዟ"): step[bstack1llllll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬዠ")],
                bstack1llllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫዡ"): step[bstack1llllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬዢ")],
                bstack1llllll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧዣ"): step[bstack1llllll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨዤ")]
            }
            if bstack1llllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧዥ") in step:
                bstack11l11lll11_opy_[bstack1llllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨዦ")] = step[bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩዧ")]
            elif bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪየ") in step:
                bstack11l11lll11_opy_[bstack1llllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫዩ")] = step[bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዪ")]
            bstack11l1l11l11_opy_.append(bstack11l11lll11_opy_)
        cls.bstack11l1l111l1_opy_({
            bstack1llllll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪያ"): bstack1llllll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫዬ"),
            bstack1llllll1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ይ"): bstack11l1l11l11_opy_
        })
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def bstack11l1l1l11l_opy_(cls, screenshot):
        cls.bstack11l1l111l1_opy_({
            bstack1llllll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ዮ"): bstack1llllll1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧዯ"),
            bstack1llllll1_opy_ (u"ࠫࡱࡵࡧࡴࠩደ"): [{
                bstack1llllll1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪዱ"): bstack1llllll1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨዲ"),
                bstack1llllll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪዳ"): datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"ࠨ࡜ࠪዴ"),
                bstack1llllll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪድ"): screenshot[bstack1llllll1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩዶ")],
                bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫዷ"): screenshot[bstack1llllll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዸ")]
            }]
        }, bstack11l1l1ll11_opy_=bstack1llllll1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫዹ"))
    @classmethod
    @bstack1l1ll1l11l_opy_(class_method=True)
    def bstack111ll11ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1l111l1_opy_({
            bstack1llllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫዺ"): bstack1llllll1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬዻ"),
            bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫዼ"): {
                bstack1llllll1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣዽ"): cls.current_test_uuid(),
                bstack1llllll1_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥዾ"): cls.bstack11l1l11ll1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1llllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ዿ"), None) is None or os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧጀ")] == bstack1llllll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧጁ"):
            return False
        return True
    @classmethod
    def bstack11l11lllll_opy_(cls):
        return bstack1l1l1ll1ll_opy_(cls.bs_config.get(bstack1llllll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬጂ"), False))
    @staticmethod
    def request_url(url):
        return bstack1llllll1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨጃ").format(bstack11l1l11111_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1llllll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩጄ"): bstack1llllll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧጅ"),
            bstack1llllll1_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨጆ"): bstack1llllll1_opy_ (u"࠭ࡴࡳࡷࡨࠫጇ")
        }
        if os.environ.get(bstack1llllll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨገ"), None):
            headers[bstack1llllll1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨጉ")] = bstack1llllll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬጊ").format(os.environ[bstack1llllll1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦጋ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1llllll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨጌ"), None)
    @staticmethod
    def bstack11l1l11ll1_opy_(driver):
        return {
            bstack1l1ll1111l_opy_(): bstack1l1l1l1lll_opy_(driver)
        }
    @staticmethod
    def bstack11l11ll1ll_opy_(exception_info, report):
        return [{bstack1llllll1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨግ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1l1lll1l_opy_(typename):
        if bstack1llllll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤጎ") in typename:
            return bstack1llllll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣጏ")
        return bstack1llllll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤጐ")
    @staticmethod
    def bstack11l1ll1l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1111l111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1l1l1ll_opy_(test, hook_name=None):
        bstack11l1ll1111_opy_ = test.parent
        if hook_name in [bstack1llllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ጑"), bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫጒ"), bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪጓ"), bstack1llllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧጔ")]:
            bstack11l1ll1111_opy_ = test
        scope = []
        while bstack11l1ll1111_opy_ is not None:
            scope.append(bstack11l1ll1111_opy_.name)
            bstack11l1ll1111_opy_ = bstack11l1ll1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11l1ll11l1_opy_(hook_type):
        if hook_type == bstack1llllll1_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦጕ"):
            return bstack1llllll1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ጖")
        elif hook_type == bstack1llllll1_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ጗"):
            return bstack1llllll1_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤጘ")
    @staticmethod
    def bstack11l1l11l1l_opy_(bstack1l1ll11ll_opy_):
        try:
            if not bstack1111l111l_opy_.on():
                return bstack1l1ll11ll_opy_
            if os.environ.get(bstack1llllll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣጙ"), None) == bstack1llllll1_opy_ (u"ࠦࡹࡸࡵࡦࠤጚ"):
                tests = os.environ.get(bstack1llllll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤጛ"), None)
                if tests is None or tests == bstack1llllll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦጜ"):
                    return bstack1l1ll11ll_opy_
                bstack1l1ll11ll_opy_ = tests.split(bstack1llllll1_opy_ (u"ࠧ࠭ࠩጝ"))
                return bstack1l1ll11ll_opy_
        except Exception as exc:
            print(bstack1llllll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤጞ"), str(exc))
        return bstack1l1ll11ll_opy_
    @classmethod
    def bstack11l1l1llll_opy_(cls, event: str, bstack11l1ll1l1l_opy_: bstack11ll11l1ll_opy_):
        bstack11l1ll111l_opy_ = {
            bstack1llllll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ጟ"): event,
            bstack11l1ll1l1l_opy_.bstack11ll11ll11_opy_(): bstack11l1ll1l1l_opy_.bstack11ll11llll_opy_(event)
        }
        bstack1111l111l_opy_.bstack11l1l111l1_opy_(bstack11l1ll111l_opy_)