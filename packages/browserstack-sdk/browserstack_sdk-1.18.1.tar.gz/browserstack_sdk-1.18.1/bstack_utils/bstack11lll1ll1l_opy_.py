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
import json
import os
import threading
from bstack_utils.helper import bstack1l1l1lll11_opy_, bstack1l1l11ll1_opy_, bstack1lll1l1lll_opy_, bstack111lll11_opy_, \
    bstack1l1l11l111_opy_
def bstack1lll1ll1l_opy_(bstack11ll1l11ll_opy_):
    for driver in bstack11ll1l11ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1lll111_opy_(type, name, status, reason, bstack111l1l111_opy_, bstack111llll1_opy_):
    bstack1l1l11lll_opy_ = {
        bstack1llllll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩᇹ"): type,
        bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᇺ"): {}
    }
    if type == bstack1llllll1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ᇻ"):
        bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᇼ")][bstack1llllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᇽ")] = bstack111l1l111_opy_
        bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᇾ")][bstack1llllll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᇿ")] = json.dumps(str(bstack111llll1_opy_))
    if type == bstack1llllll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪሀ"):
        bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ሁ")][bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩሂ")] = name
    if type == bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨሃ"):
        bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩሄ")][bstack1llllll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧህ")] = status
        if status == bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨሆ") and str(reason) != bstack1llllll1_opy_ (u"ࠤࠥሇ"):
            bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ለ")][bstack1llllll1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫሉ")] = json.dumps(str(reason))
    bstack111l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪሊ").format(json.dumps(bstack1l1l11lll_opy_))
    return bstack111l1l1ll_opy_
def bstack1l11l1ll_opy_(url, config, logger, bstack1111lll1l_opy_=False):
    hostname = bstack1l1l11ll1_opy_(url)
    is_private = bstack111lll11_opy_(hostname)
    try:
        if is_private or bstack1111lll1l_opy_:
            file_path = bstack1l1l1lll11_opy_(bstack1llllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ላ"), bstack1llllll1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ሌ"), logger)
            if os.environ.get(bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ል")) and eval(
                    os.environ.get(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧሎ"))):
                return
            if (bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧሏ") in config and not config[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨሐ")]):
                os.environ[bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪሑ")] = str(True)
                bstack11ll1l11l1_opy_ = {bstack1llllll1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨሒ"): hostname}
                bstack1l1l11l111_opy_(bstack1llllll1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ሓ"), bstack1llllll1_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ሔ"), bstack11ll1l11l1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1llll1l_opy_(caps, bstack11ll1l1l11_opy_):
    if bstack1llllll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪሕ") in caps:
        caps[bstack1llllll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫሖ")][bstack1llllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪሗ")] = True
        if bstack11ll1l1l11_opy_:
            caps[bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭መ")][bstack1llllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨሙ")] = bstack11ll1l1l11_opy_
    else:
        caps[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬሚ")] = True
        if bstack11ll1l1l11_opy_:
            caps[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩማ")] = bstack11ll1l1l11_opy_
def bstack11lll1llll_opy_(bstack11ll1l1111_opy_):
    bstack11ll1l111l_opy_ = bstack1lll1l1lll_opy_(threading.current_thread(), bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ሜ"), bstack1llllll1_opy_ (u"ࠪࠫም"))
    if bstack11ll1l111l_opy_ == bstack1llllll1_opy_ (u"ࠫࠬሞ") or bstack11ll1l111l_opy_ == bstack1llllll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ሟ"):
        threading.current_thread().testStatus = bstack11ll1l1111_opy_
    else:
        if bstack11ll1l1111_opy_ == bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሠ"):
            threading.current_thread().testStatus = bstack11ll1l1111_opy_