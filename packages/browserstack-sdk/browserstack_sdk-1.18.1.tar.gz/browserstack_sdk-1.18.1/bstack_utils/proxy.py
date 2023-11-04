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
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l11ll11ll_opy_
def bstack11lllll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11lllll1ll_opy_(bstack11llllll11_opy_, bstack11llll1lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11llllll11_opy_):
        with open(bstack11llllll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11lllll111_opy_(bstack11llllll11_opy_):
        pac = get_pac(url=bstack11llllll11_opy_)
    else:
        raise Exception(bstack1llllll1_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᆡ").format(bstack11llllll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1llllll1_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᆢ"), 80))
        bstack11llll1ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11llll1ll1_opy_ = bstack1llllll1_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᆣ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11llll1lll_opy_, bstack11llll1ll1_opy_)
    return proxy_url
def bstack1ll11ll1l_opy_(config):
    return bstack1llllll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᆤ") in config or bstack1llllll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᆥ") in config
def bstack1llll1llll_opy_(config):
    if not bstack1ll11ll1l_opy_(config):
        return
    if config.get(bstack1llllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᆦ")):
        return config.get(bstack1llllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᆧ"))
    if config.get(bstack1llllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᆨ")):
        return config.get(bstack1llllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᆩ"))
def bstack1ll11lll1l_opy_(config, bstack11llll1lll_opy_):
    proxy = bstack1llll1llll_opy_(config)
    proxies = {}
    if config.get(bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᆪ")) or config.get(bstack1llllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᆫ")):
        if proxy.endswith(bstack1llllll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᆬ")):
            proxies = bstack1lll11ll_opy_(proxy, bstack11llll1lll_opy_)
        else:
            proxies = {
                bstack1llllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᆭ"): proxy
            }
    return proxies
def bstack1lll11ll_opy_(bstack11llllll11_opy_, bstack11llll1lll_opy_):
    proxies = {}
    global bstack11lllll1l1_opy_
    if bstack1llllll1_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧᆮ") in globals():
        return bstack11lllll1l1_opy_
    try:
        proxy = bstack11lllll1ll_opy_(bstack11llllll11_opy_, bstack11llll1lll_opy_)
        if bstack1llllll1_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧᆯ") in proxy:
            proxies = {}
        elif bstack1llllll1_opy_ (u"ࠨࡈࡕࡖࡓࠦᆰ") in proxy or bstack1llllll1_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨᆱ") in proxy or bstack1llllll1_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢᆲ") in proxy:
            bstack11lllll11l_opy_ = proxy.split(bstack1llllll1_opy_ (u"ࠤࠣࠦᆳ"))
            if bstack1llllll1_opy_ (u"ࠥ࠾࠴࠵ࠢᆴ") in bstack1llllll1_opy_ (u"ࠦࠧᆵ").join(bstack11lllll11l_opy_[1:]):
                proxies = {
                    bstack1llllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᆶ"): bstack1llllll1_opy_ (u"ࠨࠢᆷ").join(bstack11lllll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᆸ"): str(bstack11lllll11l_opy_[0]).lower() + bstack1llllll1_opy_ (u"ࠣ࠼࠲࠳ࠧᆹ") + bstack1llllll1_opy_ (u"ࠤࠥᆺ").join(bstack11lllll11l_opy_[1:])
                }
        elif bstack1llllll1_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤᆻ") in proxy:
            bstack11lllll11l_opy_ = proxy.split(bstack1llllll1_opy_ (u"ࠦࠥࠨᆼ"))
            if bstack1llllll1_opy_ (u"ࠧࡀ࠯࠰ࠤᆽ") in bstack1llllll1_opy_ (u"ࠨࠢᆾ").join(bstack11lllll11l_opy_[1:]):
                proxies = {
                    bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᆿ"): bstack1llllll1_opy_ (u"ࠣࠤᇀ").join(bstack11lllll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llllll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᇁ"): bstack1llllll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᇂ") + bstack1llllll1_opy_ (u"ࠦࠧᇃ").join(bstack11lllll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1llllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᇄ"): proxy
            }
    except Exception as e:
        print(bstack1llllll1_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᇅ"), bstack1l11ll11ll_opy_.format(bstack11llllll11_opy_, str(e)))
    bstack11lllll1l1_opy_ = proxies
    return proxies