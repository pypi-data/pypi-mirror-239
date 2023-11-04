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
import re
from bstack_utils.bstack11lll1ll1l_opy_ import bstack11lll1llll_opy_
def bstack11lll1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1llllll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇆ")):
        return bstack1llllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᇇ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇈ")):
        return bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᇉ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇊ")):
        return bstack1llllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᇋ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᇌ")):
        return bstack1llllll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᇍ")
def bstack11lll1ll11_opy_(fixture_name):
    return bool(re.match(bstack1llllll1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᇎ"), fixture_name))
def bstack11lll1l111_opy_(fixture_name):
    return bool(re.match(bstack1llllll1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᇏ"), fixture_name))
def bstack11llll11l1_opy_(fixture_name):
    return bool(re.match(bstack1llllll1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᇐ"), fixture_name))
def bstack11llll11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1llllll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᇑ")):
        return bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᇒ"), bstack1llllll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᇓ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᇔ")):
        return bstack1llllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᇕ"), bstack1llllll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᇖ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᇗ")):
        return bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᇘ"), bstack1llllll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᇙ")
    elif fixture_name.startswith(bstack1llllll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇚ")):
        return bstack1llllll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᇛ"), bstack1llllll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᇜ")
    return None, None
def bstack11lll1l1ll_opy_(hook_name):
    if hook_name in [bstack1llllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᇝ"), bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᇞ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11llll1111_opy_(hook_name):
    if hook_name in [bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᇟ"), bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᇠ")]:
        return bstack1llllll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᇡ")
    elif hook_name in [bstack1llllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᇢ"), bstack1llllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᇣ")]:
        return bstack1llllll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᇤ")
    elif hook_name in [bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᇥ"), bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᇦ")]:
        return bstack1llllll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᇧ")
    elif hook_name in [bstack1llllll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᇨ"), bstack1llllll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᇩ")]:
        return bstack1llllll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᇪ")
    return hook_name
def bstack11lll11lll_opy_(node, scenario):
    if hasattr(node, bstack1llllll1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᇫ")):
        parts = node.nodeid.rsplit(bstack1llllll1_opy_ (u"ࠥ࡟ࠧᇬ"))
        params = parts[-1]
        return bstack1llllll1_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᇭ").format(scenario.name, params)
    return scenario.name
def bstack11lll1lll1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1llllll1_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᇮ")):
            examples = list(node.callspec.params[bstack1llllll1_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᇯ")].values())
        return examples
    except:
        return []
def bstack11lll1l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11llll1l11_opy_(report):
    try:
        status = bstack1llllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᇰ")
        if report.passed or (report.failed and hasattr(report, bstack1llllll1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᇱ"))):
            status = bstack1llllll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᇲ")
        elif report.skipped:
            status = bstack1llllll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᇳ")
        bstack11lll1llll_opy_(status)
    except:
        pass
def bstack1lllllll1_opy_(status):
    try:
        bstack11llll1l1l_opy_ = bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᇴ")
        if status == bstack1llllll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᇵ"):
            bstack11llll1l1l_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᇶ")
        elif status == bstack1llllll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᇷ"):
            bstack11llll1l1l_opy_ = bstack1llllll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᇸ")
        bstack11lll1llll_opy_(bstack11llll1l1l_opy_)
    except:
        pass
def bstack11llll111l_opy_(item=None, report=None, summary=None, extra=None):
    return