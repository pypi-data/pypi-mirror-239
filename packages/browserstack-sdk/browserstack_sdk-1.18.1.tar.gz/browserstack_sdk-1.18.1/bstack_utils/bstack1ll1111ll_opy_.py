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
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1ll1111l1l_opy_ as bstack1ll1111l11_opy_
from bstack_utils.helper import bstack1ll1lll1l_opy_, bstack11111lll_opy_, bstack1l1lllll11_opy_, bstack1l1llll1ll_opy_, bstack1ll1l1l11l_opy_, get_host_info, bstack1ll111111l_opy_, bstack1ll111l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
def bstack1llll111_opy_(config):
  try:
    if not bstack11111lll_opy_(config):
      return False
    bstack1l1llllll1_opy_ = os.getenv(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥ࡙ࡎࡎࠪಹ")) == bstack1llllll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ಺") or os.getenv(bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪ಻")) == bstack1llllll1_opy_ (u"ࠧࡺࡲࡶࡧ಼ࠥ")
    bstack1ll11111l1_opy_ = os.getenv(bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫಽ")) is not None and len(os.getenv(bstack1llllll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬಾ"))) > 0 and os.getenv(bstack1llllll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ಿ")) != bstack1llllll1_opy_ (u"ࠩࡱࡹࡱࡲࠧೀ")
    return bstack1l1llllll1_opy_ and bstack1ll11111l1_opy_
  except Exception as error:
    logger.debug(bstack1llllll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪು") + str(error))
  return False
def bstack1lll1l1ll_opy_(config, bstack1l1llll11l_opy_, bstack1ll1111ll1_opy_):
  bstack1l1lllllll_opy_ = bstack1l1lllll11_opy_(config)
  bstack1l1lllll1l_opy_ = bstack1l1llll1ll_opy_(config)
  if bstack1l1lllllll_opy_ is None or bstack1l1lllll1l_opy_ is None:
    logger.error(bstack1llllll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬೂ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ೃ"), bstack1llllll1_opy_ (u"࠭ࡻࡾࠩೄ")))
    data = {
        bstack1llllll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ೅"): config[bstack1llllll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ೆ")],
        bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೇ"): config.get(bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೈ"), os.path.basename(os.getcwd())),
        bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧ೉"): bstack1ll1lll1l_opy_(),
        bstack1llllll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪೊ"): config.get(bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩೋ"), bstack1llllll1_opy_ (u"ࠧࠨೌ")),
        bstack1llllll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ್"): {
            bstack1llllll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ೎"): bstack1l1llll11l_opy_,
            bstack1llllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೏"): bstack1ll1111ll1_opy_,
            bstack1llllll1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ೐"): __version__
        },
        bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ೑"): settings,
        bstack1llllll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧ೒"): bstack1ll111111l_opy_(),
        bstack1llllll1_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧ೓"): bstack1ll1l1l11l_opy_(),
        bstack1llllll1_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪ೔"): get_host_info(),
        bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫೕ"): bstack11111lll_opy_(config)
    }
    headers = {
        bstack1llllll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩೖ"): bstack1llllll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ೗"),
    }
    config = {
        bstack1llllll1_opy_ (u"ࠬࡧࡵࡵࡪࠪ೘"): (bstack1l1lllllll_opy_, bstack1l1lllll1l_opy_),
        bstack1llllll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ೙"): headers
    }
    response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ೚"), bstack1ll1111l11_opy_ + bstack1llllll1_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬ೛"), data, config)
    try:
      bstack1ll1111lll_opy_ = response.json()
      parsed = json.loads(os.getenv(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ೜"), bstack1llllll1_opy_ (u"ࠪࡿࢂ࠭ೝ")))
      parsed[bstack1llllll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬೞ")] = bstack1ll1111lll_opy_[bstack1llllll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ೟")][bstack1llllll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧೠ")]
      os.environ[bstack1llllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨೡ")] = json.dumps(parsed)
      return bstack1ll1111lll_opy_[bstack1llllll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ೢ")][bstack1llllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧೣ")], bstack1ll1111lll_opy_[bstack1llllll1_opy_ (u"ࠪࡨࡦࡺࡡࠨ೤")][bstack1llllll1_opy_ (u"ࠫ࡮ࡪࠧ೥")]
    except Exception as e:
      raise Exception(e)
  except Exception as error:
    logger.error(bstack1llllll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨ೦") +  str(error))
    return None, None
def bstack1l11ll1l_opy_():
  if os.getenv(bstack1llllll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ೧")) is None:
    return {
        bstack1llllll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ೨"): bstack1llllll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೩"),
        bstack1llllll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ೪"): bstack1llllll1_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩ೫")
    }
  data = {bstack1llllll1_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬ೬"): bstack1ll1lll1l_opy_()}
  headers = {
      bstack1llllll1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ೭"): bstack1llllll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧ೮") + os.getenv(bstack1llllll1_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧ೯")),
      bstack1llllll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ೰"): bstack1llllll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬೱ")
  }
  response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠪࡔ࡚࡚ࠧೲ"), bstack1ll1111l11_opy_ + bstack1llllll1_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ೳ"), data, { bstack1llllll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭೴"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1llllll1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢ೵") + datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"࡛ࠧࠩ೶"))
      return {bstack1llllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೷"): bstack1llllll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ೸"), bstack1llllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೹"): bstack1llllll1_opy_ (u"ࠫࠬ೺")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1llllll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣ೻") + str(error))
    return {
        bstack1llllll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭೼"): bstack1llllll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭೽"),
        bstack1llllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ೾"): str(error)
    }
def bstack1l1llll1l1_opy_(caps):
  try:
    bstack1l1llll111_opy_ = caps.get(bstack1llllll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ೿"), {}).get(bstack1llllll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧഀ"), caps.get(bstack1llllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫഁ"), bstack1llllll1_opy_ (u"ࠬ࠭ം")))
    if bstack1l1llll111_opy_:
      logger.error(bstack1llllll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥഃ"))
      return False
    browser = caps.get(bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬഄ"), bstack1llllll1_opy_ (u"ࠨࠩഅ")).lower()
    if browser != bstack1llllll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩആ"):
      logger.error(bstack1llllll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨഇ"))
      return False
    browser_version = caps.get(bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬഈ"), caps.get(bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧഉ")))
    if browser_version and browser_version != bstack1llllll1_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ഊ") and int(browser_version) <= 94:
      logger.error(bstack1llllll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧഋ"))
      return False
    chrome_options = webdriver.ChromeOptions()
    if bstack1llllll1_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬഌ") in chrome_options.arguments:
      logger.error(bstack1llllll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦ഍"))
      return False
    return True
  except Exception as error:
    logger.debug(bstack1llllll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢࡈࡶࡷࡵࡲ࠻ࠤഎ") + str(error))
    return False
def bstack1lll1ll1_opy_(caps, config):
  try:
    if bstack1llllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫഏ") in config and config[bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬഐ")] == True:
      bstack1ll11111ll_opy_ = config.get(bstack1llllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭഑"), {})
      bstack1ll11111ll_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪഒ")] = os.getenv(bstack1llllll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ഓ"))
      bstack1ll1111111_opy_ = json.loads(os.getenv(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪഔ"), bstack1llllll1_opy_ (u"ࠪࡿࢂ࠭ക"))).get(bstack1llllll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬഖ"))
      if bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ഗ") in caps:
        caps[bstack1llllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧഘ")][bstack1llllll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧങ")] = bstack1ll11111ll_opy_
        caps[bstack1llllll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩച")][bstack1llllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩഛ")][bstack1llllll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫജ")] = bstack1ll1111111_opy_
      else:
        bstack1ll11111ll_opy_[bstack1llllll1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧഝ")] = os.getenv(bstack1llllll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪഞ"))
        caps[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬട")] = bstack1ll11111ll_opy_
        caps[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ഠ")][bstack1llllll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩഡ")] = bstack1ll1111111_opy_
  except Exception as error:
    logger.debug(bstack1llllll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲࠣഢ") + str(error))