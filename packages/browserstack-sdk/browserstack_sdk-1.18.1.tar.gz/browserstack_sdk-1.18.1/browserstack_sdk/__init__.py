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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack11111ll1l_opy_():
  global CONFIG
  headers = {
        bstack1llllll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack1llllll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack1ll11lll1l_opy_(CONFIG, bstack1111l1111_opy_)
  try:
    response = requests.get(bstack1111l1111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l111111_opy_ = response.json()[bstack1llllll1_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack1111ll11_opy_.format(response.json()))
      return bstack11l111111_opy_
    else:
      logger.debug(bstack1l11l111l_opy_.format(bstack1llllll1_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack1l11l111l_opy_.format(e))
def bstack1l111l1l_opy_(hub_url):
  global CONFIG
  url = bstack1llllll1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack1llllll1_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack1llllll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack1llllll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack1ll11lll1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll11111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l1111_opy_.format(hub_url, e))
def bstack1l1ll11l_opy_():
  try:
    global bstack1llll1l1l1_opy_
    bstack11l111111_opy_ = bstack11111ll1l_opy_()
    bstack11ll111l1_opy_ = []
    results = []
    for bstack11111111_opy_ in bstack11l111111_opy_:
      bstack11ll111l1_opy_.append(bstack1l11l1l1_opy_(target=bstack1l111l1l_opy_,args=(bstack11111111_opy_,)))
    for t in bstack11ll111l1_opy_:
      t.start()
    for t in bstack11ll111l1_opy_:
      results.append(t.join())
    bstack111l1ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1llllll1_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack1llllll1_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack111l1ll1_opy_[hub_url] = latency
    bstack1ll1l11ll1_opy_ = min(bstack111l1ll1_opy_, key= lambda x: bstack111l1ll1_opy_[x])
    bstack1llll1l1l1_opy_ = bstack1ll1l11ll1_opy_
    logger.debug(bstack11lll1l1_opy_.format(bstack1ll1l11ll1_opy_))
  except Exception as e:
    logger.debug(bstack1l1l1l1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1ll111l11_opy_, bstack1l1ll1111_opy_, bstack1lll1l1lll_opy_, bstack11111lll_opy_, Notset, bstack111l1ll11_opy_, \
  bstack1llll1lll1_opy_, bstack11111111l_opy_, bstack1111l1lll_opy_, bstack1ll1l1l11l_opy_, bstack1l1lll11l_opy_
from bstack_utils.bstack11l1l11ll_opy_ import bstack1111l111l_opy_
from bstack_utils.proxy import bstack1lll11ll_opy_, bstack1ll11lll1l_opy_, bstack1llll1llll_opy_, bstack1ll11ll1l_opy_
from bstack_utils.bstack1ll1111ll_opy_ import bstack1lll1l1ll_opy_, bstack1l11ll1l_opy_, bstack1lll1ll1_opy_, bstack1llll111_opy_
from browserstack_sdk.bstack1llllll11_opy_ import *
from browserstack_sdk.bstack11l111l1l_opy_ import *
from bstack_utils.bstack1111l11l1_opy_ import bstack1lllllll1_opy_
bstack1lll111ll_opy_ = bstack1llllll1_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack1l1llll1l_opy_ = bstack1llllll1_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack111111l1_opy_ = None
CONFIG = {}
bstack11l111l1_opy_ = {}
bstack11l11ll11_opy_ = {}
bstack11l1lll11_opy_ = None
bstack111lllll_opy_ = None
bstack1ll1llll11_opy_ = None
bstack11l11111l_opy_ = -1
bstack11l1l1l1l_opy_ = bstack11ll11l1l_opy_
bstack1lll11lll_opy_ = 1
bstack1l111llll_opy_ = False
bstack1lll1l1111_opy_ = False
bstack1ll1l1l1l_opy_ = bstack1llllll1_opy_ (u"ࠧࠨࢁ")
bstack1l11lllll_opy_ = bstack1llllll1_opy_ (u"ࠨࠩࢂ")
bstack1l1l11l1l_opy_ = False
bstack1ll11llll_opy_ = True
bstack1l1l111l1_opy_ = bstack1llllll1_opy_ (u"ࠩࠪࢃ")
bstack1ll1lllll_opy_ = []
bstack1llll1l1l1_opy_ = bstack1llllll1_opy_ (u"ࠪࠫࢄ")
bstack1ll1l111ll_opy_ = False
bstack1l11lll1_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack11lll111_opy_ = -1
bstack111l1111_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠫࢃ࠭ࢅ")), bstack1llllll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack1llllll1_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack1ll1l1l1l1_opy_ = []
bstack1l1ll1l1l_opy_ = []
bstack11llll11l_opy_ = False
bstack11l1111l_opy_ = False
bstack1lll11l11l_opy_ = None
bstack1llll1l11l_opy_ = None
bstack111111ll1_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1lll1ll11l_opy_ = None
bstack111llll1l_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack1lll11l111_opy_ = None
bstack11l11ll1l_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1lll1lll_opy_ = None
bstack1ll1lll11_opy_ = None
bstack11ll11lll_opy_ = None
bstack11l1ll1l_opy_ = None
bstack11111ll11_opy_ = None
bstack11lll11l_opy_ = None
bstack1l11l1l1l_opy_ = None
bstack11lll1lll_opy_ = None
bstack1l1111l11_opy_ = bstack1llllll1_opy_ (u"ࠢࠣ࢈")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l1l1l1l_opy_,
                    format=bstack1llllll1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ࢉ"),
                    datefmt=bstack1llllll1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫࢊ"),
                    stream=sys.stdout)
bstack1l11l11l1_opy_ = Config.get_instance()
percy = bstack1lllll11ll_opy_()
def bstack1ll1ll1l_opy_():
  global CONFIG
  global bstack11l1l1l1l_opy_
  if bstack1llllll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢋ") in CONFIG:
    bstack11l1l1l1l_opy_ = bstack1lllll11l_opy_[CONFIG[bstack1llllll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࢌ")]]
    logging.getLogger().setLevel(bstack11l1l1l1l_opy_)
def bstack111ll1l11_opy_():
  global CONFIG
  global bstack11llll11l_opy_
  bstack1l1ll1lll_opy_ = bstack11l1llll1_opy_(CONFIG)
  if (bstack1llllll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ") in bstack1l1ll1lll_opy_ and str(bstack1l1ll1lll_opy_[bstack1llllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢎ")]).lower() == bstack1llllll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࢏")):
    bstack11llll11l_opy_ = True
def bstack1lll111lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l111ll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1111ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1llllll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1llllll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l111l1_opy_
      bstack1l1l111l1_opy_ += bstack1llllll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1llll11l1l_opy_ = re.compile(bstack1llllll1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll111ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll11l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1llllll1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1llllll1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack11ll1l11l_opy_():
  bstack1l1l1l11l_opy_ = bstack1l1111ll1_opy_()
  if bstack1l1l1l11l_opy_ and os.path.exists(os.path.abspath(bstack1l1l1l11l_opy_)):
    fileName = bstack1l1l1l11l_opy_
  if bstack1llllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1llllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1lll1ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lll1ll_opy_ = bstack1llllll1_opy_ (u"࢛ࠬ࠭")
  bstack1l1lll11_opy_ = os.getcwd()
  bstack11l1lll1l_opy_ = bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l111ll1_opy_ = bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1lll1ll_opy_)) and bstack1l1lll11_opy_ != bstack1llllll1_opy_ (u"ࠣࠤ࢞"):
    bstack1lll1ll_opy_ = os.path.join(bstack1l1lll11_opy_, bstack11l1lll1l_opy_)
    if not os.path.exists(bstack1lll1ll_opy_):
      bstack1lll1ll_opy_ = os.path.join(bstack1l1lll11_opy_, bstack1l111ll1_opy_)
    if bstack1l1lll11_opy_ != os.path.dirname(bstack1l1lll11_opy_):
      bstack1l1lll11_opy_ = os.path.dirname(bstack1l1lll11_opy_)
    else:
      bstack1l1lll11_opy_ = bstack1llllll1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1lll1ll_opy_):
    bstack11ll1l11_opy_(
      bstack1ll1l111_opy_.format(os.getcwd()))
  try:
    with open(bstack1lll1ll_opy_, bstack1llllll1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1llllll1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1llll11l1l_opy_)
      yaml.add_constructor(bstack1llllll1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll111ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lll1ll_opy_, bstack1llllll1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11ll1l11_opy_(bstack1llll1l111_opy_.format(str(exc)))
def bstack1ll111l1l_opy_(config):
  bstack1ll1lll1_opy_ = bstack111111lll_opy_(config)
  for option in list(bstack1ll1lll1_opy_):
    if option.lower() in bstack1ll1l11111_opy_ and option != bstack1ll1l11111_opy_[option.lower()]:
      bstack1ll1lll1_opy_[bstack1ll1l11111_opy_[option.lower()]] = bstack1ll1lll1_opy_[option]
      del bstack1ll1lll1_opy_[option]
  return config
def bstack1ll1l1111l_opy_():
  global bstack11l11ll11_opy_
  for key, bstack1ll11ll1ll_opy_ in bstack11ll1l1ll_opy_.items():
    if isinstance(bstack1ll11ll1ll_opy_, list):
      for var in bstack1ll11ll1ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l11ll11_opy_[key] = os.environ[var]
          break
    elif bstack1ll11ll1ll_opy_ in os.environ and os.environ[bstack1ll11ll1ll_opy_] and str(os.environ[bstack1ll11ll1ll_opy_]).strip():
      bstack11l11ll11_opy_[key] = os.environ[bstack1ll11ll1ll_opy_]
  if bstack1llllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack11l11ll11_opy_[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack11l11ll11_opy_[bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1llllll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack11ll1l111_opy_():
  global bstack11l111l1_opy_
  global bstack1l1l111l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1llllll1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack11l111l1_opy_[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack11l111l1_opy_[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1llllll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack111ll111l_opy_ in bstack1lll1l11ll_opy_.items():
    if isinstance(bstack111ll111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111ll111l_opy_:
          if idx < len(sys.argv) and bstack1llllll1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack11l111l1_opy_:
            bstack11l111l1_opy_[key] = sys.argv[idx + 1]
            bstack1l1l111l1_opy_ += bstack1llllll1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1llllll1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1llllll1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack111ll111l_opy_.lower() == val.lower() and not key in bstack11l111l1_opy_:
          bstack11l111l1_opy_[key] = sys.argv[idx + 1]
          bstack1l1l111l1_opy_ += bstack1llllll1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack111ll111l_opy_ + bstack1llllll1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack111lll1l_opy_(config):
  bstack1l1l111l_opy_ = config.keys()
  for bstack1lll11lll1_opy_, bstack11llll1l_opy_ in bstack1l1l1llll_opy_.items():
    if bstack11llll1l_opy_ in bstack1l1l111l_opy_:
      config[bstack1lll11lll1_opy_] = config[bstack11llll1l_opy_]
      del config[bstack11llll1l_opy_]
  for bstack1lll11lll1_opy_, bstack11llll1l_opy_ in bstack11l1l1ll_opy_.items():
    if isinstance(bstack11llll1l_opy_, list):
      for bstack1l111111_opy_ in bstack11llll1l_opy_:
        if bstack1l111111_opy_ in bstack1l1l111l_opy_:
          config[bstack1lll11lll1_opy_] = config[bstack1l111111_opy_]
          del config[bstack1l111111_opy_]
          break
    elif bstack11llll1l_opy_ in bstack1l1l111l_opy_:
      config[bstack1lll11lll1_opy_] = config[bstack11llll1l_opy_]
      del config[bstack11llll1l_opy_]
  for bstack1l111111_opy_ in list(config):
    for bstack1ll1l1111_opy_ in bstack1l11l11ll_opy_:
      if bstack1l111111_opy_.lower() == bstack1ll1l1111_opy_.lower() and bstack1l111111_opy_ != bstack1ll1l1111_opy_:
        config[bstack1ll1l1111_opy_] = config[bstack1l111111_opy_]
        del config[bstack1l111111_opy_]
  bstack1lll11l1_opy_ = []
  if bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1lll11l1_opy_ = config[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1lll11l1_opy_:
    for bstack1l111111_opy_ in list(platform):
      for bstack1ll1l1111_opy_ in bstack1l11l11ll_opy_:
        if bstack1l111111_opy_.lower() == bstack1ll1l1111_opy_.lower() and bstack1l111111_opy_ != bstack1ll1l1111_opy_:
          platform[bstack1ll1l1111_opy_] = platform[bstack1l111111_opy_]
          del platform[bstack1l111111_opy_]
  for bstack1lll11lll1_opy_, bstack11llll1l_opy_ in bstack11l1l1ll_opy_.items():
    for platform in bstack1lll11l1_opy_:
      if isinstance(bstack11llll1l_opy_, list):
        for bstack1l111111_opy_ in bstack11llll1l_opy_:
          if bstack1l111111_opy_ in platform:
            platform[bstack1lll11lll1_opy_] = platform[bstack1l111111_opy_]
            del platform[bstack1l111111_opy_]
            break
      elif bstack11llll1l_opy_ in platform:
        platform[bstack1lll11lll1_opy_] = platform[bstack11llll1l_opy_]
        del platform[bstack11llll1l_opy_]
  for bstack1llll1111_opy_ in bstack1ll1llllll_opy_:
    if bstack1llll1111_opy_ in config:
      if not bstack1ll1llllll_opy_[bstack1llll1111_opy_] in config:
        config[bstack1ll1llllll_opy_[bstack1llll1111_opy_]] = {}
      config[bstack1ll1llllll_opy_[bstack1llll1111_opy_]].update(config[bstack1llll1111_opy_])
      del config[bstack1llll1111_opy_]
  for platform in bstack1lll11l1_opy_:
    for bstack1llll1111_opy_ in bstack1ll1llllll_opy_:
      if bstack1llll1111_opy_ in list(platform):
        if not bstack1ll1llllll_opy_[bstack1llll1111_opy_] in platform:
          platform[bstack1ll1llllll_opy_[bstack1llll1111_opy_]] = {}
        platform[bstack1ll1llllll_opy_[bstack1llll1111_opy_]].update(platform[bstack1llll1111_opy_])
        del platform[bstack1llll1111_opy_]
  config = bstack1ll111l1l_opy_(config)
  return config
def bstack1l111l1ll_opy_(config):
  global bstack1l11lllll_opy_
  if bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack1llllll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack1llllll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack1ll1lll1l_opy_ = datetime.datetime.now()
      bstack1llll1ll1l_opy_ = bstack1ll1lll1l_opy_.strftime(bstack1llllll1_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1ll1l11l1l_opy_ = bstack1llllll1_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1llllll1_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1llll1ll1l_opy_, hostname, bstack1ll1l11l1l_opy_)
      config[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack1llllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack1l11lllll_opy_ = config[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1llllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1lllll1l1l_opy_():
  bstack11lll1l1l_opy_ =  bstack1ll1l1l11l_opy_()[bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack11lll1l1l_opy_ if bstack11lll1l1l_opy_ else -1
def bstack1ll11llll1_opy_(bstack11lll1l1l_opy_):
  global CONFIG
  if not bstack1llllll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack1llllll1_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack11lll1l1l_opy_)
  )
def bstack1l11lll11_opy_():
  global CONFIG
  if not bstack1llllll1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack1ll1lll1l_opy_ = datetime.datetime.now()
  bstack1llll1ll1l_opy_ = bstack1ll1lll1l_opy_.strftime(bstack1llllll1_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack1llllll1_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1llll1ll1l_opy_
  )
def bstack1ll11l1ll1_opy_():
  global CONFIG
  if bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack1llllll1_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack1llllll1_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1l11lll11_opy_()
    os.environ[bstack1llllll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack1llllll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack11lll1l1l_opy_ = bstack1llllll1_opy_ (u"࠭ࠧࣛ")
  bstack1l1111l1l_opy_ = bstack1lllll1l1l_opy_()
  if bstack1l1111l1l_opy_ != -1:
    bstack11lll1l1l_opy_ = bstack1llllll1_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack1l1111l1l_opy_)
  if bstack11lll1l1l_opy_ == bstack1llllll1_opy_ (u"ࠨࠩࣝ"):
    bstack1l1l1ll1l_opy_ = bstack11ll111ll_opy_(CONFIG[bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack1l1l1ll1l_opy_ != -1:
      bstack11lll1l1l_opy_ = str(bstack1l1l1ll1l_opy_)
  if bstack11lll1l1l_opy_:
    bstack1ll11llll1_opy_(bstack11lll1l1l_opy_)
    os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack11l11111_opy_(bstack11ll111l_opy_, bstack1111111ll_opy_, path):
  bstack1lllll1111_opy_ = {
    bstack1llllll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack1111111ll_opy_
  }
  if os.path.exists(path):
    bstack11llllll1_opy_ = json.load(open(path, bstack1llllll1_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack11llllll1_opy_ = {}
  bstack11llllll1_opy_[bstack11ll111l_opy_] = bstack1lllll1111_opy_
  with open(path, bstack1llllll1_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack11llllll1_opy_, outfile)
def bstack11ll111ll_opy_(bstack11ll111l_opy_):
  bstack11ll111l_opy_ = str(bstack11ll111l_opy_)
  bstack111l1l11_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠨࢀࠪࣤ")), bstack1llllll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack111l1l11_opy_):
      os.makedirs(bstack111l1l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠪࢂࣦࠬ")), bstack1llllll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack1llllll1_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1llllll1_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack1llllll1_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1llllll1_opy_ (u"ࠨࡴࠪ࣫")) as bstack1ll1lll1l1_opy_:
      bstack1llll11lll_opy_ = json.load(bstack1ll1lll1l1_opy_)
    if bstack11ll111l_opy_ in bstack1llll11lll_opy_:
      bstack1l1lll1l1_opy_ = bstack1llll11lll_opy_[bstack11ll111l_opy_][bstack1llllll1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack1l1ll1ll_opy_ = int(bstack1l1lll1l1_opy_) + 1
      bstack11l11111_opy_(bstack11ll111l_opy_, bstack1l1ll1ll_opy_, file_path)
      return bstack1l1ll1ll_opy_
    else:
      bstack11l11111_opy_(bstack11ll111l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111l1ll_opy_.format(str(e)))
    return -1
def bstack11ll11ll1_opy_(config):
  if not config[bstack1llllll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack1llllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack1lll111l_opy_(config, index=0):
  global bstack1l1l11l1l_opy_
  bstack111ll1lll_opy_ = {}
  caps = bstack111ll1111_opy_ + bstack1llll1ll11_opy_
  if bstack1l1l11l1l_opy_:
    caps += bstack1llll111l1_opy_
  for key in config:
    if key in caps + [bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack111ll1lll_opy_[key] = config[key]
  if bstack1llllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1lll1l1l_opy_ in config[bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1lll1l1l_opy_ in caps + [bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack111ll1lll_opy_[bstack1lll1l1l_opy_] = config[bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1lll1l1l_opy_]
  bstack111ll1lll_opy_[bstack1llllll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack1llllll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack111ll1lll_opy_:
    del (bstack111ll1lll_opy_[bstack1llllll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack111ll1lll_opy_
def bstack1lll111l1l_opy_(config):
  global bstack1l1l11l1l_opy_
  bstack1lll111l11_opy_ = {}
  caps = bstack1llll1ll11_opy_
  if bstack1l1l11l1l_opy_:
    caps += bstack1llll111l1_opy_
  for key in caps:
    if key in config:
      bstack1lll111l11_opy_[key] = config[key]
  return bstack1lll111l11_opy_
def bstack11l11l1l1_opy_(bstack111ll1lll_opy_, bstack1lll111l11_opy_):
  bstack1ll11lll11_opy_ = {}
  for key in bstack111ll1lll_opy_.keys():
    if key in bstack1l1l1llll_opy_:
      bstack1ll11lll11_opy_[bstack1l1l1llll_opy_[key]] = bstack111ll1lll_opy_[key]
    else:
      bstack1ll11lll11_opy_[key] = bstack111ll1lll_opy_[key]
  for key in bstack1lll111l11_opy_:
    if key in bstack1l1l1llll_opy_:
      bstack1ll11lll11_opy_[bstack1l1l1llll_opy_[key]] = bstack1lll111l11_opy_[key]
    else:
      bstack1ll11lll11_opy_[key] = bstack1lll111l11_opy_[key]
  return bstack1ll11lll11_opy_
def bstack1l1ll111l_opy_(config, index=0):
  global bstack1l1l11l1l_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lll111l11_opy_ = bstack1lll111l1l_opy_(config)
  bstack1lllll11_opy_ = bstack1llll1ll11_opy_
  bstack1lllll11_opy_ += bstack1llll1l1ll_opy_
  if bstack1l1l11l1l_opy_:
    bstack1lllll11_opy_ += bstack1llll111l1_opy_
  if bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack1l11llll_opy_ = {}
    for bstack11111l1l_opy_ in bstack1lllll11_opy_:
      if bstack11111l1l_opy_ in config[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
        if bstack11111l1l_opy_ == bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧऄ"):
          try:
            bstack1l11llll_opy_[bstack11111l1l_opy_] = str(config[bstack1llllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack11111l1l_opy_] * 1.0)
          except:
            bstack1l11llll_opy_[bstack11111l1l_opy_] = str(config[bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack11111l1l_opy_])
        else:
          bstack1l11llll_opy_[bstack11111l1l_opy_] = config[bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack11111l1l_opy_]
        del (config[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack11111l1l_opy_])
    bstack1lll111l11_opy_ = update(bstack1lll111l11_opy_, bstack1l11llll_opy_)
  bstack111ll1lll_opy_ = bstack1lll111l_opy_(config, index)
  for bstack1l111111_opy_ in bstack1llll1ll11_opy_ + [bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨउ"), bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬऊ")]:
    if bstack1l111111_opy_ in bstack111ll1lll_opy_:
      bstack1lll111l11_opy_[bstack1l111111_opy_] = bstack111ll1lll_opy_[bstack1l111111_opy_]
      del (bstack111ll1lll_opy_[bstack1l111111_opy_])
  if bstack111l1ll11_opy_(config):
    bstack111ll1lll_opy_[bstack1llllll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1lll111l11_opy_)
    caps[bstack1llllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack111ll1lll_opy_
  else:
    bstack111ll1lll_opy_[bstack1llllll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack11l11l1l1_opy_(bstack111ll1lll_opy_, bstack1lll111l11_opy_))
    if bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1l11ll11_opy_():
  global bstack1llll1l1l1_opy_
  if bstack1l111ll11_opy_() <= version.parse(bstack1llllll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1llll1l1l1_opy_ != bstack1llllll1_opy_ (u"ࠪࠫग"):
      return bstack1llllll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1llll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1l1l11l1_opy_
  if bstack1llll1l1l1_opy_ != bstack1llllll1_opy_ (u"࠭ࠧच"):
    return bstack1llllll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1llll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1ll1l111l1_opy_
def bstack1l1l1lll_opy_(options):
  return hasattr(options, bstack1llllll1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lllll1lll_opy_(options, bstack1l11l1111_opy_):
  for bstack11ll11l1_opy_ in bstack1l11l1111_opy_:
    if bstack11ll11l1_opy_ in [bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1llllll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack11ll11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11ll11l1_opy_] = update(options._experimental_options[bstack11ll11l1_opy_],
                                                         bstack1l11l1111_opy_[bstack11ll11l1_opy_])
    else:
      options.add_experimental_option(bstack11ll11l1_opy_, bstack1l11l1111_opy_[bstack11ll11l1_opy_])
  if bstack1llllll1_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1l11l1111_opy_:
    for arg in bstack1l11l1111_opy_[bstack1llllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1l11l1111_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1llllll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1l11l1111_opy_:
    for ext in bstack1l11l1111_opy_[bstack1llllll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1l11l1111_opy_[bstack1llllll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1l1ll111_opy_(options, bstack1l1l1lll1_opy_):
  if bstack1llllll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l1l1lll1_opy_:
    for bstack1l1l11111_opy_ in bstack1l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1l1l11111_opy_ in options._preferences:
        options._preferences[bstack1l1l11111_opy_] = update(options._preferences[bstack1l1l11111_opy_], bstack1l1l1lll1_opy_[bstack1llllll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1l1l11111_opy_])
      else:
        options.set_preference(bstack1l1l11111_opy_, bstack1l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l1l11111_opy_])
  if bstack1llllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l1l1lll1_opy_:
    for arg in bstack1l1l1lll1_opy_[bstack1llllll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1lll111ll1_opy_(options, bstack1ll1ll1lll_opy_):
  if bstack1llllll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1ll1ll1lll_opy_:
    options.use_webview(bool(bstack1ll1ll1lll_opy_[bstack1llllll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1lllll1lll_opy_(options, bstack1ll1ll1lll_opy_)
def bstack11l1ll1ll_opy_(options, bstack11llll1ll_opy_):
  for bstack11llll1l1_opy_ in bstack11llll1ll_opy_:
    if bstack11llll1l1_opy_ in [bstack1llllll1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1llllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack11llll1l1_opy_, bstack11llll1ll_opy_[bstack11llll1l1_opy_])
  if bstack1llllll1_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack11llll1ll_opy_:
    for arg in bstack11llll1ll_opy_[bstack1llllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1llllll1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack11llll1ll_opy_:
    options.bstack11l1lll1_opy_(bool(bstack11llll1ll_opy_[bstack1llllll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1ll1l11ll_opy_(options, bstack1ll1l11lll_opy_):
  for bstack11ll1ll1l_opy_ in bstack1ll1l11lll_opy_:
    if bstack11ll1ll1l_opy_ in [bstack1llllll1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1llllll1_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack11ll1ll1l_opy_] = bstack1ll1l11lll_opy_[bstack11ll1ll1l_opy_]
  if bstack1llllll1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1ll1l11lll_opy_:
    for bstack1llll1l11_opy_ in bstack1ll1l11lll_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1l111l111_opy_(
        bstack1llll1l11_opy_, bstack1ll1l11lll_opy_[bstack1llllll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1llll1l11_opy_])
  if bstack1llllll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1ll1l11lll_opy_:
    for arg in bstack1ll1l11lll_opy_[bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1l1l1l1ll_opy_(options, caps):
  if not hasattr(options, bstack1llllll1_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1llllll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1lllll1lll_opy_(options, caps[bstack1llllll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1llllll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1l1ll111_opy_(options, caps[bstack1llllll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1llllll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack11l1ll1ll_opy_(options, caps[bstack1llllll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1llllll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll111ll1_opy_(options, caps[bstack1llllll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1llllll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1ll1l11ll_opy_(options, caps[bstack1llllll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1lll1ll1ll_opy_(caps):
  global bstack1l1l11l1l_opy_
  if isinstance(os.environ.get(bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1l1l11l1l_opy_ = eval(os.getenv(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1l1l11l1l_opy_:
    if bstack1lll111lll_opy_() < version.parse(bstack1llllll1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1llllll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1llllll1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1llllll1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1llllll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1llllll1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1llllll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1llllll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1llllll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1llllll1_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1llllll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1llllll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1llllll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1llllll1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1lll_opy_(options):
        return None
      for bstack1l111111_opy_ in caps.keys():
        options.set_capability(bstack1l111111_opy_, caps[bstack1l111111_opy_])
      bstack1l1l1l1ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1ll1_opy_(options, bstack11l1l11l1_opy_):
  if not bstack1l1l1lll_opy_(options):
    return
  for bstack1l111111_opy_ in bstack11l1l11l1_opy_.keys():
    if bstack1l111111_opy_ in bstack1llll1l1ll_opy_:
      continue
    if bstack1l111111_opy_ in options._caps and type(options._caps[bstack1l111111_opy_]) in [dict, list]:
      options._caps[bstack1l111111_opy_] = update(options._caps[bstack1l111111_opy_], bstack11l1l11l1_opy_[bstack1l111111_opy_])
    else:
      options.set_capability(bstack1l111111_opy_, bstack11l1l11l1_opy_[bstack1l111111_opy_])
  bstack1l1l1l1ll_opy_(options, bstack11l1l11l1_opy_)
  if bstack1llllll1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1llllll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1ll11l11l_opy_(proxy_config):
  if bstack1llllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1llllll1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1llllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1llllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1llllll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1llllll1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1llllll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1llllll1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1llllll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1llllll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1llllll1_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1l1ll1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1llllll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1llllll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1ll11l11l_opy_(config[bstack1llllll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1llllll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1l111l11_opy_(self):
  global CONFIG
  global bstack1lll1lll_opy_
  try:
    proxy = bstack1llll1llll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1llllll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1lll11ll_opy_(proxy, bstack1l11ll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1l1l11_opy_ = proxies.popitem()
          if bstack1llllll1_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1ll1l1l11_opy_:
            return bstack1ll1l1l11_opy_
          else:
            return bstack1llllll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1ll1l1l11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1llllll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1lll1lll_opy_(self)
def bstack1ll11l1l11_opy_():
  global CONFIG
  return bstack1ll11ll1l_opy_(CONFIG) and bstack1l111ll11_opy_() >= version.parse(bstack1lll1llll_opy_)
def bstack111111lll_opy_(config):
  bstack1ll1lll1_opy_ = {}
  if bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॳ") in config:
    bstack1ll1lll1_opy_ = config[bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॴ")]
  if bstack1llllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॵ") in config:
    bstack1ll1lll1_opy_ = config[bstack1llllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॶ")]
  proxy = bstack1llll1llll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1llllll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ॷ")) and os.path.isfile(proxy):
      bstack1ll1lll1_opy_[bstack1llllll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬॸ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1llllll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")):
        proxies = bstack1ll11lll1l_opy_(config, bstack1l11ll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1l1l11_opy_ = proxies.popitem()
          if bstack1llllll1_opy_ (u"ࠦ࠿࠵࠯ࠣॺ") in bstack1ll1l1l11_opy_:
            parsed_url = urlparse(bstack1ll1l1l11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1llllll1_opy_ (u"ࠧࡀ࠯࠰ࠤॻ") + bstack1ll1l1l11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1lll1_opy_[bstack1llllll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩॼ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1lll1_opy_[bstack1llllll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪॽ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1lll1_opy_[bstack1llllll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫॾ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1lll1_opy_[bstack1llllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬॿ")] = str(parsed_url.password)
  return bstack1ll1lll1_opy_
def bstack11l1llll1_opy_(config):
  if bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨঀ") in config:
    return config[bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩঁ")]
  return {}
def bstack1ll1llll1l_opy_(caps):
  global bstack1l11lllll_opy_
  if bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ং") in caps:
    caps[bstack1llllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧঃ")][bstack1llllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭঄")] = True
    if bstack1l11lllll_opy_:
      caps[bstack1llllll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1llllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫআ")] = bstack1l11lllll_opy_
  else:
    caps[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨই")] = True
    if bstack1l11lllll_opy_:
      caps[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬঈ")] = bstack1l11lllll_opy_
def bstack1ll11l111_opy_():
  global CONFIG
  if bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩউ") in CONFIG and CONFIG[bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪঊ")]:
    bstack1ll1lll1_opy_ = bstack111111lll_opy_(CONFIG)
    bstack11l111l11_opy_(CONFIG[bstack1llllll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪঋ")], bstack1ll1lll1_opy_)
def bstack11l111l11_opy_(key, bstack1ll1lll1_opy_):
  global bstack111111l1_opy_
  logger.info(bstack1llll1l1l_opy_)
  try:
    bstack111111l1_opy_ = Local()
    bstack1ll1lll1ll_opy_ = {bstack1llllll1_opy_ (u"ࠨ࡭ࡨࡽࠬঌ"): key}
    bstack1ll1lll1ll_opy_.update(bstack1ll1lll1_opy_)
    logger.debug(bstack1l111ll1l_opy_.format(str(bstack1ll1lll1ll_opy_)))
    bstack111111l1_opy_.start(**bstack1ll1lll1ll_opy_)
    if bstack111111l1_opy_.isRunning():
      logger.info(bstack111ll1l1_opy_)
  except Exception as e:
    bstack11ll1l11_opy_(bstack1ll11lllll_opy_.format(str(e)))
def bstack1l111111l_opy_():
  global bstack111111l1_opy_
  if bstack111111l1_opy_.isRunning():
    logger.info(bstack111l1l1l_opy_)
    bstack111111l1_opy_.stop()
  bstack111111l1_opy_ = None
def bstack1lll1111l_opy_(bstack1l1l1ll1_opy_=[]):
  global CONFIG
  bstack1ll11ll1l1_opy_ = []
  bstack1lll111111_opy_ = [bstack1llllll1_opy_ (u"ࠩࡲࡷࠬ঍"), bstack1llllll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭঎"), bstack1llllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨএ"), bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧঐ"), bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ঑"), bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ঒")]
  try:
    for err in bstack1l1l1ll1_opy_:
      bstack1llll1l1_opy_ = {}
      for k in bstack1lll111111_opy_:
        val = CONFIG[bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫও")][int(err[bstack1llllll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨঔ")])].get(k)
        if val:
          bstack1llll1l1_opy_[k] = val
      bstack1llll1l1_opy_[bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩক")] = {
        err[bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩখ")]: err[bstack1llllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫগ")]
      }
      bstack1ll11ll1l1_opy_.append(bstack1llll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨঘ") + str(e))
  finally:
    return bstack1ll11ll1l1_opy_
def bstack1lll1ll1l_opy_():
  global bstack1l1111l11_opy_
  global bstack1ll1lllll_opy_
  global bstack1ll1l1l1l1_opy_
  percy.shutdown()
  if bstack1l1111l11_opy_:
    logger.warning(bstack11ll1111l_opy_.format(str(bstack1l1111l11_opy_)))
  else:
    try:
      bstack11llllll1_opy_ = bstack1llll1lll1_opy_(bstack1llllll1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ঙ"), logger)
      if bstack11llllll1_opy_.get(bstack1llllll1_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭চ")) and bstack11llllll1_opy_.get(bstack1llllll1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧছ")).get(bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬজ")):
        logger.warning(bstack11ll1111l_opy_.format(str(bstack11llllll1_opy_[bstack1llllll1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩঝ")][bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧঞ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1ll11l1_opy_)
  global bstack111111l1_opy_
  if bstack111111l1_opy_:
    bstack1l111111l_opy_()
  try:
    for driver in bstack1ll1lllll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll11111l_opy_)
  bstack1l1l111ll_opy_()
  if len(bstack1ll1l1l1l1_opy_) > 0:
    message = bstack1lll1111l_opy_(bstack1ll1l1l1l1_opy_)
    bstack1l1l111ll_opy_(message)
  else:
    bstack1l1l111ll_opy_()
  bstack11111111l_opy_(bstack1lll1111_opy_, logger)
def bstack1lll1l11_opy_(self, *args):
  logger.error(bstack11l1l111l_opy_)
  bstack1lll1ll1l_opy_()
  sys.exit(1)
def bstack11ll1l11_opy_(err):
  logger.critical(bstack1lll1111l1_opy_.format(str(err)))
  bstack1l1l111ll_opy_(bstack1lll1111l1_opy_.format(str(err)))
  atexit.unregister(bstack1lll1ll1l_opy_)
  sys.exit(1)
def bstack1l1l11l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l111ll_opy_(message)
  atexit.unregister(bstack1lll1ll1l_opy_)
  sys.exit(1)
def bstack111l1lll_opy_():
  global CONFIG
  global bstack11l111l1_opy_
  global bstack11l11ll11_opy_
  global bstack1ll11llll_opy_
  CONFIG = bstack11ll1l11l_opy_()
  bstack1ll1l1111l_opy_()
  bstack11ll1l111_opy_()
  CONFIG = bstack111lll1l_opy_(CONFIG)
  update(CONFIG, bstack11l11ll11_opy_)
  update(CONFIG, bstack11l111l1_opy_)
  CONFIG = bstack1l111l1ll_opy_(CONFIG)
  bstack1ll11llll_opy_ = bstack11111lll_opy_(CONFIG)
  bstack1l11l11l1_opy_.bstack1111l11ll_opy_(bstack1llllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧট"), bstack1ll11llll_opy_)
  if (bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪঠ") in CONFIG and bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫড") in bstack11l111l1_opy_) or (
          bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬঢ") in CONFIG and bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ণ") not in bstack11l11ll11_opy_):
    if os.getenv(bstack1llllll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨত")):
      CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧথ")] = os.getenv(bstack1llllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪদ"))
    else:
      bstack1ll11l1ll1_opy_()
  elif (bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪধ") not in CONFIG and bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪন") in CONFIG) or (
          bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ঩") in bstack11l11ll11_opy_ and bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭প") not in bstack11l111l1_opy_):
    del (CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ফ")])
  if bstack11ll11ll1_opy_(CONFIG):
    bstack11ll1l11_opy_(bstack1l1l1l11_opy_)
  bstack1llll11l1_opy_()
  bstack1lll1l1l11_opy_()
  if bstack1l1l11l1l_opy_:
    CONFIG[bstack1llllll1_opy_ (u"ࠬࡧࡰࡱࠩব")] = bstack11ll11111_opy_(CONFIG)
    logger.info(bstack1ll1l1l1_opy_.format(CONFIG[bstack1llllll1_opy_ (u"࠭ࡡࡱࡲࠪভ")]))
def bstack1lllllll1l_opy_(config, bstack11111l1l1_opy_):
  global CONFIG
  global bstack1l1l11l1l_opy_
  CONFIG = config
  bstack1l1l11l1l_opy_ = bstack11111l1l1_opy_
def bstack1lll1l1l11_opy_():
  global CONFIG
  global bstack1l1l11l1l_opy_
  if bstack1llllll1_opy_ (u"ࠧࡢࡲࡳࠫম") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack1lll111l1_opy_)
    bstack1l1l11l1l_opy_ = True
    bstack1l11l11l1_opy_.bstack1111l11ll_opy_(bstack1llllll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧয"), True)
def bstack11ll11111_opy_(config):
  bstack111l11ll_opy_ = bstack1llllll1_opy_ (u"ࠩࠪর")
  app = config[bstack1llllll1_opy_ (u"ࠪࡥࡵࡶࠧ঱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1111l1l11_opy_:
      if os.path.exists(app):
        bstack111l11ll_opy_ = bstack1ll1ll11ll_opy_(config, app)
      elif bstack1l11l1l11_opy_(app):
        bstack111l11ll_opy_ = app
      else:
        bstack11ll1l11_opy_(bstack1l11ll11l_opy_.format(app))
    else:
      if bstack1l11l1l11_opy_(app):
        bstack111l11ll_opy_ = app
      elif os.path.exists(app):
        bstack111l11ll_opy_ = bstack1ll1ll11ll_opy_(app)
      else:
        bstack11ll1l11_opy_(bstack11l1llll_opy_)
  else:
    if len(app) > 2:
      bstack11ll1l11_opy_(bstack11l111lll_opy_)
    elif len(app) == 2:
      if bstack1llllll1_opy_ (u"ࠫࡵࡧࡴࡩࠩল") in app and bstack1llllll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ঳") in app:
        if os.path.exists(app[bstack1llllll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ঴")]):
          bstack111l11ll_opy_ = bstack1ll1ll11ll_opy_(config, app[bstack1llllll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ঵")], app[bstack1llllll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫশ")])
        else:
          bstack11ll1l11_opy_(bstack1l11ll11l_opy_.format(app))
      else:
        bstack11ll1l11_opy_(bstack11l111lll_opy_)
    else:
      for key in app:
        if key in bstack111l111ll_opy_:
          if key == bstack1llllll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧষ"):
            if os.path.exists(app[key]):
              bstack111l11ll_opy_ = bstack1ll1ll11ll_opy_(config, app[key])
            else:
              bstack11ll1l11_opy_(bstack1l11ll11l_opy_.format(app))
          else:
            bstack111l11ll_opy_ = app[key]
        else:
          bstack11ll1l11_opy_(bstack1lllll1l11_opy_)
  return bstack111l11ll_opy_
def bstack1l11l1l11_opy_(bstack111l11ll_opy_):
  import re
  bstack11l1l11l_opy_ = re.compile(bstack1llllll1_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥস"))
  bstack1l11l1lll_opy_ = re.compile(bstack1llllll1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣহ"))
  if bstack1llllll1_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ঺") in bstack111l11ll_opy_ or re.fullmatch(bstack11l1l11l_opy_, bstack111l11ll_opy_) or re.fullmatch(bstack1l11l1lll_opy_, bstack111l11ll_opy_):
    return True
  else:
    return False
def bstack1ll1ll11ll_opy_(config, path, bstack1l1l1l111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1llllll1_opy_ (u"࠭ࡲࡣࠩ঻")).read()).hexdigest()
  bstack11l1l1lll_opy_ = bstack1lll1lll11_opy_(md5_hash)
  bstack111l11ll_opy_ = None
  if bstack11l1l1lll_opy_:
    logger.info(bstack11l111ll_opy_.format(bstack11l1l1lll_opy_, md5_hash))
    return bstack11l1l1lll_opy_
  bstack1111ll111_opy_ = MultipartEncoder(
    fields={
      bstack1llllll1_opy_ (u"ࠧࡧ࡫࡯ࡩ়ࠬ"): (os.path.basename(path), open(os.path.abspath(path), bstack1llllll1_opy_ (u"ࠨࡴࡥࠫঽ")), bstack1llllll1_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭া")),
      bstack1llllll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ি"): bstack1l1l1l111_opy_
    }
  )
  response = requests.post(bstack1lll11ll11_opy_, data=bstack1111ll111_opy_,
                           headers={bstack1llllll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪী"): bstack1111ll111_opy_.content_type},
                           auth=(config[bstack1llllll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧু")], config[bstack1llllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩূ")]))
  try:
    res = json.loads(response.text)
    bstack111l11ll_opy_ = res[bstack1llllll1_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨৃ")]
    logger.info(bstack1l1111111_opy_.format(bstack111l11ll_opy_))
    bstack1llll1lll_opy_(md5_hash, bstack111l11ll_opy_)
  except ValueError as err:
    bstack11ll1l11_opy_(bstack1lll11l1l_opy_.format(str(err)))
  return bstack111l11ll_opy_
def bstack1llll11l1_opy_():
  global CONFIG
  global bstack1lll11lll_opy_
  bstack11lll11ll_opy_ = 0
  bstack1ll1ll1ll_opy_ = 1
  if bstack1llllll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨৄ") in CONFIG:
    bstack1ll1ll1ll_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৅")]
  if bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৆") in CONFIG:
    bstack11lll11ll_opy_ = len(CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে")])
  bstack1lll11lll_opy_ = int(bstack1ll1ll1ll_opy_) * int(bstack11lll11ll_opy_)
def bstack1lll1lll11_opy_(md5_hash):
  bstack1llll11ll_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠬࢄࠧৈ")), bstack1llllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৉"), bstack1llllll1_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৊"))
  if os.path.exists(bstack1llll11ll_opy_):
    bstack111l11lll_opy_ = json.load(open(bstack1llll11ll_opy_, bstack1llllll1_opy_ (u"ࠨࡴࡥࠫো")))
    if md5_hash in bstack111l11lll_opy_:
      bstack1lllll1ll1_opy_ = bstack111l11lll_opy_[md5_hash]
      bstack1llll11l11_opy_ = datetime.datetime.now()
      bstack1llll11ll1_opy_ = datetime.datetime.strptime(bstack1lllll1ll1_opy_[bstack1llllll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬৌ")], bstack1llllll1_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾্࡙ࠪࠧ"))
      if (bstack1llll11l11_opy_ - bstack1llll11ll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1lllll1ll1_opy_[bstack1llllll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩৎ")]):
        return None
      return bstack1lllll1ll1_opy_[bstack1llllll1_opy_ (u"ࠬ࡯ࡤࠨ৏")]
  else:
    return None
def bstack1llll1lll_opy_(md5_hash, bstack111l11ll_opy_):
  bstack111l1l11_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"࠭ࡾࠨ৐")), bstack1llllll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ৑"))
  if not os.path.exists(bstack111l1l11_opy_):
    os.makedirs(bstack111l1l11_opy_)
  bstack1llll11ll_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠨࢀࠪ৒")), bstack1llllll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৓"), bstack1llllll1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৔"))
  bstack1ll1l11l_opy_ = {
    bstack1llllll1_opy_ (u"ࠫ࡮ࡪࠧ৕"): bstack111l11ll_opy_,
    bstack1llllll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৖"): datetime.datetime.strftime(datetime.datetime.now(), bstack1llllll1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪৗ")),
    bstack1llllll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৘"): str(__version__)
  }
  if os.path.exists(bstack1llll11ll_opy_):
    bstack111l11lll_opy_ = json.load(open(bstack1llll11ll_opy_, bstack1llllll1_opy_ (u"ࠨࡴࡥࠫ৙")))
  else:
    bstack111l11lll_opy_ = {}
  bstack111l11lll_opy_[md5_hash] = bstack1ll1l11l_opy_
  with open(bstack1llll11ll_opy_, bstack1llllll1_opy_ (u"ࠤࡺ࠯ࠧ৚")) as outfile:
    json.dump(bstack111l11lll_opy_, outfile)
def bstack11lll1l11_opy_(self):
  return
def bstack1l1111lll_opy_(self):
  return
def bstack1ll1l1ll1l_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1llll11_opy_(self):
  global bstack1ll1l1l1l_opy_
  global bstack11l1lll11_opy_
  global bstack1llll1l11l_opy_
  try:
    if bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ৛") in bstack1ll1l1l1l_opy_ and self.session_id != None and bstack1lll1l1lll_opy_(threading.current_thread(), bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨড়"), bstack1llllll1_opy_ (u"ࠬ࠭ঢ়")) != bstack1llllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ৞"):
      bstack1ll1l11l11_opy_ = bstack1llllll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧয়") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨৠ")
      bstack11ll1111_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬৡ"), bstack1llllll1_opy_ (u"ࠪࠫৢ"), bstack1ll1l11l11_opy_, bstack1llllll1_opy_ (u"ࠫ࠱ࠦࠧৣ").join(
        threading.current_thread().bstackTestErrorMessages), bstack1llllll1_opy_ (u"ࠬ࠭৤"), bstack1llllll1_opy_ (u"࠭ࠧ৥"))
      if self != None:
        self.execute_script(bstack11ll1111_opy_)
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ০") + str(e))
  bstack1llll1l11l_opy_(self)
  self.session_id = None
def bstack11l1111l1_opy_(self, *args, **kwargs):
  bstack1l1lllll1_opy_ = bstack1lll11l11l_opy_(self, *args, **kwargs)
  bstack1111l111l_opy_.bstack111ll11ll_opy_(self)
  return bstack1l1lllll1_opy_
def bstack1l11111l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l1lll11_opy_
  global bstack11l11111l_opy_
  global bstack1ll1llll11_opy_
  global bstack1l111llll_opy_
  global bstack1lll1l1111_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1lll11l11l_opy_
  global bstack1ll1lllll_opy_
  global bstack11lll111_opy_
  CONFIG[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ১")] = str(bstack1ll1l1l1l_opy_) + str(__version__)
  command_executor = bstack1l11ll11_opy_()
  logger.debug(bstack1ll11l1ll_opy_.format(command_executor))
  proxy = bstack1l1ll1l1_opy_(CONFIG, proxy)
  bstack1111l11l_opy_ = 0 if bstack11l11111l_opy_ < 0 else bstack11l11111l_opy_
  try:
    if bstack1l111llll_opy_ is True:
      bstack1111l11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1l1111_opy_ is True:
      bstack1111l11l_opy_ = int(threading.current_thread().name)
  except:
    bstack1111l11l_opy_ = 0
  bstack11l1l11l1_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1111l11l_opy_)
  logger.debug(bstack1111llll1_opy_.format(str(bstack11l1l11l1_opy_)))
  if bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭২") in CONFIG and CONFIG[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৩")]:
    bstack1ll1llll1l_opy_(bstack11l1l11l1_opy_)
  if desired_capabilities:
    bstack1lll1lll1l_opy_ = bstack111lll1l_opy_(desired_capabilities)
    bstack1lll1lll1l_opy_[bstack1llllll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ৪")] = bstack111l1ll11_opy_(CONFIG)
    bstack1ll11l1l1l_opy_ = bstack1l1ll111l_opy_(bstack1lll1lll1l_opy_)
    if bstack1ll11l1l1l_opy_:
      bstack11l1l11l1_opy_ = update(bstack1ll11l1l1l_opy_, bstack11l1l11l1_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1ll1_opy_(options, bstack11l1l11l1_opy_)
  if not options:
    options = bstack1lll1ll1ll_opy_(bstack11l1l11l1_opy_)
  if proxy and bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ৫")):
    options.proxy(proxy)
  if options and bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ৬")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l111ll11_opy_() < version.parse(bstack1llllll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭৭")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1l11l1_opy_)
  logger.info(bstack1l11111ll_opy_)
  if bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ৮")):
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ৯")):
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪৰ")):
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11lll1ll1_opy_ = bstack1llllll1_opy_ (u"ࠫࠬৱ")
    if bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭৲")):
      bstack11lll1ll1_opy_ = self.caps.get(bstack1llllll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ৳"))
    else:
      bstack11lll1ll1_opy_ = self.capabilities.get(bstack1llllll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ৴"))
    if bstack11lll1ll1_opy_:
      if bstack1l111ll11_opy_() <= version.parse(bstack1llllll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ৵")):
        self.command_executor._url = bstack1llllll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৶") + bstack1llll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ৷")
      else:
        self.command_executor._url = bstack1llllll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ৸") + bstack11lll1ll1_opy_ + bstack1llllll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ৹")
      logger.debug(bstack11111lll1_opy_.format(bstack11lll1ll1_opy_))
    else:
      logger.debug(bstack11l11l11_opy_.format(bstack1llllll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ৺")))
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(e))
  if bstack1llllll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭৻") in bstack1ll1l1l1l_opy_:
    bstack1lll1ll11_opy_(bstack11l11111l_opy_, bstack11lll111_opy_)
  bstack11l1lll11_opy_ = self.session_id
  if bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨৼ") in bstack1ll1l1l1l_opy_ or bstack1llllll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ৽") in bstack1ll1l1l1l_opy_:
    threading.current_thread().bstack1l11l11l_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1111l111l_opy_.bstack111ll11ll_opy_(self)
  bstack1ll1lllll_opy_.append(self)
  if bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৾") in CONFIG and bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ৿") in CONFIG[bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਀")][bstack1111l11l_opy_]:
    bstack1ll1llll11_opy_ = CONFIG[bstack1llllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਁ")][bstack1111l11l_opy_][bstack1llllll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਂ")]
  logger.debug(bstack1ll1ll1111_opy_.format(bstack11l1lll11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l11lll1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1l111ll_opy_
      if(bstack1llllll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥਃ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠩࢁࠫ਄")), bstack1llllll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪਅ"), bstack1llllll1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ਆ")), bstack1llllll1_opy_ (u"ࠬࡽࠧਇ")) as fp:
          fp.write(bstack1llllll1_opy_ (u"ࠨࠢਈ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1llllll1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਉ")))):
          with open(args[1], bstack1llllll1_opy_ (u"ࠨࡴࠪਊ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1llllll1_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ਋") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll111ll_opy_)
            lines.insert(1, bstack1l1llll1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1llllll1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ਌")), bstack1llllll1_opy_ (u"ࠫࡼ࠭਍")) as bstack111111ll_opy_:
              bstack111111ll_opy_.writelines(lines)
        CONFIG[bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ਎")] = str(bstack1ll1l1l1l_opy_) + str(__version__)
        bstack1111l11l_opy_ = 0 if bstack11l11111l_opy_ < 0 else bstack11l11111l_opy_
        try:
          if bstack1l111llll_opy_ is True:
            bstack1111l11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1l1111_opy_ is True:
            bstack1111l11l_opy_ = int(threading.current_thread().name)
        except:
          bstack1111l11l_opy_ = 0
        CONFIG[bstack1llllll1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨਏ")] = False
        CONFIG[bstack1llllll1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨਐ")] = True
        bstack11l1l11l1_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1111l11l_opy_)
        logger.debug(bstack1111llll1_opy_.format(str(bstack11l1l11l1_opy_)))
        if CONFIG.get(bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ਑")):
          bstack1ll1llll1l_opy_(bstack11l1l11l1_opy_)
        if bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ਒") in CONFIG and bstack1llllll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਓ") in CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਔ")][bstack1111l11l_opy_]:
          bstack1ll1llll11_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਕ")][bstack1111l11l_opy_][bstack1llllll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਖ")]
        args.append(os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠧࡿࠩਗ")), bstack1llllll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਘ"), bstack1llllll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਙ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1l11l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1llllll1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧਚ"))
      bstack1ll1l111ll_opy_ = True
      return bstack11l1ll1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11ll11ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l11111l_opy_
    global bstack1ll1llll11_opy_
    global bstack1l111llll_opy_
    global bstack1lll1l1111_opy_
    global bstack1ll1l1l1l_opy_
    CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ਛ")] = str(bstack1ll1l1l1l_opy_) + str(__version__)
    bstack1111l11l_opy_ = 0 if bstack11l11111l_opy_ < 0 else bstack11l11111l_opy_
    try:
      if bstack1l111llll_opy_ is True:
        bstack1111l11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1l1111_opy_ is True:
        bstack1111l11l_opy_ = int(threading.current_thread().name)
    except:
      bstack1111l11l_opy_ = 0
    CONFIG[bstack1llllll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਜ")] = True
    bstack11l1l11l1_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1111l11l_opy_)
    logger.debug(bstack1111llll1_opy_.format(str(bstack11l1l11l1_opy_)))
    if CONFIG.get(bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਝ")):
      bstack1ll1llll1l_opy_(bstack11l1l11l1_opy_)
    if bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ") in CONFIG and bstack1llllll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ") in CONFIG[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਠ")][bstack1111l11l_opy_]:
      bstack1ll1llll11_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਡ")][bstack1111l11l_opy_][bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਢ")]
    import urllib
    import json
    bstack11lll1111_opy_ = bstack1llllll1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧਣ") + urllib.parse.quote(json.dumps(bstack11l1l11l1_opy_))
    browser = self.connect(bstack11lll1111_opy_)
    return browser
except Exception as e:
    pass
def bstack1llllll11l_opy_():
    global bstack1ll1l111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11ll11ll_opy_
        bstack1ll1l111ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l11lll1l_opy_
      bstack1ll1l111ll_opy_ = True
    except Exception as e:
      pass
def bstack1llllll1l_opy_(context, bstack1ll1ll11l_opy_):
  try:
    context.page.evaluate(bstack1llllll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢਤ"), bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫਥ")+ json.dumps(bstack1ll1ll11l_opy_) + bstack1llllll1_opy_ (u"ࠣࡿࢀࠦਦ"))
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢਧ"), e)
def bstack11l11lll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1llllll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਨ"), bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ਩") + json.dumps(message) + bstack1llllll1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨਪ") + json.dumps(level) + bstack1llllll1_opy_ (u"࠭ࡽࡾࠩਫ"))
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥਬ"), e)
def bstack1llll1ll1_opy_(context, status, message = bstack1llllll1_opy_ (u"ࠣࠤਭ")):
  try:
    if(status == bstack1llllll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤਮ")):
      context.page.evaluate(bstack1llllll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਯ"), bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬਰ") + json.dumps(bstack1llllll1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢ਱") + str(message)) + bstack1llllll1_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪਲ") + json.dumps(status) + bstack1llllll1_opy_ (u"ࠢࡾࡿࠥਲ਼"))
    else:
      context.page.evaluate(bstack1llllll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ਴"), bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪਵ") + json.dumps(status) + bstack1llllll1_opy_ (u"ࠥࢁࢂࠨਸ਼"))
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣ਷"), e)
def bstack1lll1llll1_opy_(self, url):
  global bstack11ll11lll_opy_
  try:
    bstack1l11l1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll1lllll_opy_.format(str(err)))
  try:
    bstack11ll11lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll11l11_opy_ = str(e)
      if any(err_msg in bstack1lll11l11_opy_ for err_msg in bstack1ll11l11_opy_):
        bstack1l11l1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll1lllll_opy_.format(str(err)))
    raise e
def bstack1l1l1111l_opy_(self):
  global bstack1ll1ll1l1_opy_
  bstack1ll1ll1l1_opy_ = self
  return
def bstack111l1llll_opy_(self):
  global bstack1l11lll1_opy_
  bstack1l11lll1_opy_ = self
  return
def bstack1ll1llll_opy_(self, test):
  global CONFIG
  global bstack1l11lll1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11l1lll11_opy_
  global bstack111lllll_opy_
  global bstack1ll1llll11_opy_
  global bstack111111ll1_opy_
  global bstack1l11l1ll1_opy_
  global bstack1lll1ll11l_opy_
  global bstack1ll1lllll_opy_
  try:
    if not bstack11l1lll11_opy_:
      with open(os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠬࢄࠧਸ")), bstack1llllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ਹ"), bstack1llllll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ਺"))) as f:
        bstack1l1l11ll_opy_ = json.loads(bstack1llllll1_opy_ (u"ࠣࡽࠥ਻") + f.read().strip() + bstack1llllll1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻ਼ࠥࠫ") + bstack1llllll1_opy_ (u"ࠥࢁࠧ਽"))
        bstack11l1lll11_opy_ = bstack1l1l11ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1lllll_opy_:
    for driver in bstack1ll1lllll_opy_:
      if bstack11l1lll11_opy_ == driver.session_id:
        if test:
          bstack1l111l11l_opy_ = str(test.data)
        if not bstack11llll11l_opy_ and bstack1l111l11l_opy_:
          bstack1l1l11lll_opy_ = {
            bstack1llllll1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫਾ"): bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਿ"),
            bstack1llllll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩੀ"): {
              bstack1llllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬੁ"): bstack1l111l11l_opy_
            }
          }
          bstack111l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ੂ").format(json.dumps(bstack1l1l11lll_opy_))
          driver.execute_script(bstack111l1l1ll_opy_)
        if bstack111lllll_opy_:
          bstack1l11llll1_opy_ = {
            bstack1llllll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੃"): bstack1llllll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੄"),
            bstack1llllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੅"): {
              bstack1llllll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ੆"): bstack1l111l11l_opy_ + bstack1llllll1_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨੇ"),
              bstack1llllll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ੈ"): bstack1llllll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੉")
            }
          }
          bstack1l1l11lll_opy_ = {
            bstack1llllll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੊"): bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ੋ"),
            bstack1llllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧੌ"): {
              bstack1llllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷ੍ࠬ"): bstack1llllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੎")
            }
          }
          if bstack111lllll_opy_.status == bstack1llllll1_opy_ (u"ࠧࡑࡃࡖࡗࠬ੏"):
            bstack1l11ll111_opy_ = bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੐").format(json.dumps(bstack1l11llll1_opy_))
            driver.execute_script(bstack1l11ll111_opy_)
            bstack111l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧੑ").format(json.dumps(bstack1l1l11lll_opy_))
            driver.execute_script(bstack111l1l1ll_opy_)
          elif bstack111lllll_opy_.status == bstack1llllll1_opy_ (u"ࠪࡊࡆࡏࡌࠨ੒"):
            reason = bstack1llllll1_opy_ (u"ࠦࠧ੓")
            bstack1llllll111_opy_ = bstack1l111l11l_opy_ + bstack1llllll1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭੔")
            if bstack111lllll_opy_.message:
              reason = str(bstack111lllll_opy_.message)
              bstack1llllll111_opy_ = bstack1llllll111_opy_ + bstack1llllll1_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭੕") + reason
            bstack1l11llll1_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੖")] = {
              bstack1llllll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ੗"): bstack1llllll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ੘"),
              bstack1llllll1_opy_ (u"ࠪࡨࡦࡺࡡࠨਖ਼"): bstack1llllll111_opy_
            }
            bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧਗ਼")] = {
              bstack1llllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬਜ਼"): bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ੜ"),
              bstack1llllll1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ੝"): reason
            }
            bstack1l11ll111_opy_ = bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack1l11llll1_opy_))
            driver.execute_script(bstack1l11ll111_opy_)
            bstack111l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ੟").format(json.dumps(bstack1l1l11lll_opy_))
            driver.execute_script(bstack111l1l1ll_opy_)
  elif bstack11l1lll11_opy_:
    try:
      data = {}
      bstack1l111l11l_opy_ = None
      if test:
        bstack1l111l11l_opy_ = str(test.data)
      if not bstack11llll11l_opy_ and bstack1l111l11l_opy_:
        data[bstack1llllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ੠")] = bstack1l111l11l_opy_
      if bstack111lllll_opy_:
        if bstack111lllll_opy_.status == bstack1llllll1_opy_ (u"ࠫࡕࡇࡓࡔࠩ੡"):
          data[bstack1llllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ੢")] = bstack1llllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੣")
        elif bstack111lllll_opy_.status == bstack1llllll1_opy_ (u"ࠧࡇࡃࡌࡐࠬ੤"):
          data[bstack1llllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੥")] = bstack1llllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੦")
          if bstack111lllll_opy_.message:
            data[bstack1llllll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ੧")] = str(bstack111lllll_opy_.message)
      user = CONFIG[bstack1llllll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੨")]
      key = CONFIG[bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੩")]
      url = bstack1llllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ੪").format(user, key, bstack11l1lll11_opy_)
      headers = {
        bstack1llllll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭੫"): bstack1llllll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ੬"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1l111l_opy_.format(str(e)))
  if bstack1l11lll1_opy_:
    bstack1l11l1ll1_opy_(bstack1l11lll1_opy_)
  if bstack1ll1ll1l1_opy_:
    bstack1lll1ll11l_opy_(bstack1ll1ll1l1_opy_)
  bstack111111ll1_opy_(self, test)
def bstack1lll1ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111llll1l_opy_
  bstack111llll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111lllll_opy_
  bstack111lllll_opy_ = self._test
def bstack11ll1l1l_opy_():
  global bstack111l1111_opy_
  try:
    if os.path.exists(bstack111l1111_opy_):
      os.remove(bstack111l1111_opy_)
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ੭") + str(e))
def bstack1lll1l1l1l_opy_():
  global bstack111l1111_opy_
  bstack11llllll1_opy_ = {}
  try:
    if not os.path.isfile(bstack111l1111_opy_):
      with open(bstack111l1111_opy_, bstack1llllll1_opy_ (u"ࠪࡻࠬ੮")):
        pass
      with open(bstack111l1111_opy_, bstack1llllll1_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack111l1111_opy_):
      bstack11llllll1_opy_ = json.load(open(bstack111l1111_opy_, bstack1llllll1_opy_ (u"ࠬࡸࡢࠨੰ")))
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨੱ") + str(e))
  finally:
    return bstack11llllll1_opy_
def bstack1lll1ll11_opy_(platform_index, item_index):
  global bstack111l1111_opy_
  try:
    bstack11llllll1_opy_ = bstack1lll1l1l1l_opy_()
    bstack11llllll1_opy_[item_index] = platform_index
    with open(bstack111l1111_opy_, bstack1llllll1_opy_ (u"ࠢࡸ࠭ࠥੲ")) as outfile:
      json.dump(bstack11llllll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ੳ") + str(e))
def bstack11l1l1111_opy_(bstack111l1111l_opy_):
  global CONFIG
  bstack1lll11ll1_opy_ = bstack1llllll1_opy_ (u"ࠩࠪੴ")
  if not bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ੵ") in CONFIG:
    logger.info(bstack1llllll1_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ੶"))
  try:
    platform = CONFIG[bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੷")][bstack111l1111l_opy_]
    if bstack1llllll1_opy_ (u"࠭࡯ࡴࠩ੸") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"ࠧࡰࡵࠪ੹")]) + bstack1llllll1_opy_ (u"ࠨ࠮ࠣࠫ੺")
    if bstack1llllll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ੻") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭੼")]) + bstack1llllll1_opy_ (u"ࠫ࠱ࠦࠧ੽")
    if bstack1llllll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ੾") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ੿")]) + bstack1llllll1_opy_ (u"ࠧ࠭ࠢࠪ઀")
    if bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪઁ") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫં")]) + bstack1llllll1_opy_ (u"ࠪ࠰ࠥ࠭ઃ")
    if bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ઄") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઅ")]) + bstack1llllll1_opy_ (u"࠭ࠬࠡࠩઆ")
    if bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨઇ") in platform:
      bstack1lll11ll1_opy_ += str(platform[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩઈ")]) + bstack1llllll1_opy_ (u"ࠩ࠯ࠤࠬઉ")
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪઊ") + str(e))
  finally:
    if bstack1lll11ll1_opy_[len(bstack1lll11ll1_opy_) - 2:] == bstack1llllll1_opy_ (u"ࠫ࠱ࠦࠧઋ"):
      bstack1lll11ll1_opy_ = bstack1lll11ll1_opy_[:-2]
    return bstack1lll11ll1_opy_
def bstack1lll11l1l1_opy_(path, bstack1lll11ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111llll11_opy_ = ET.parse(path)
    bstack11111ll1_opy_ = bstack111llll11_opy_.getroot()
    bstack1l1llll1_opy_ = None
    for suite in bstack11111ll1_opy_.iter(bstack1llllll1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઌ")):
      if bstack1llllll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ઍ") in suite.attrib:
        suite.attrib[bstack1llllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ઎")] += bstack1llllll1_opy_ (u"ࠨࠢࠪએ") + bstack1lll11ll1_opy_
        bstack1l1llll1_opy_ = suite
    bstack1lll1l11l_opy_ = None
    for robot in bstack11111ll1_opy_.iter(bstack1llllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨઐ")):
      bstack1lll1l11l_opy_ = robot
    bstack111ll1l1l_opy_ = len(bstack1lll1l11l_opy_.findall(bstack1llllll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩઑ")))
    if bstack111ll1l1l_opy_ == 1:
      bstack1lll1l11l_opy_.remove(bstack1lll1l11l_opy_.findall(bstack1llllll1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ઒"))[0])
      bstack11111l11l_opy_ = ET.Element(bstack1llllll1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઓ"), attrib={bstack1llllll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ"): bstack1llllll1_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧક"), bstack1llllll1_opy_ (u"ࠨ࡫ࡧࠫખ"): bstack1llllll1_opy_ (u"ࠩࡶ࠴ࠬગ")})
      bstack1lll1l11l_opy_.insert(1, bstack11111l11l_opy_)
      bstack1lllll111l_opy_ = None
      for suite in bstack1lll1l11l_opy_.iter(bstack1llllll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩઘ")):
        bstack1lllll111l_opy_ = suite
      bstack1lllll111l_opy_.append(bstack1l1llll1_opy_)
      bstack11l1111ll_opy_ = None
      for status in bstack1l1llll1_opy_.iter(bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")):
        bstack11l1111ll_opy_ = status
      bstack1lllll111l_opy_.append(bstack11l1111ll_opy_)
    bstack111llll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪચ") + str(e))
def bstack1ll1ll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l11l1l1l_opy_
  global CONFIG
  if bstack1llllll1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥછ") in options:
    del options[bstack1llllll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦજ")]
  bstack1lllll1111_opy_ = bstack1lll1l1l1l_opy_()
  for bstack1l111l1l1_opy_ in bstack1lllll1111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1llllll1_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨઝ"), str(bstack1l111l1l1_opy_), bstack1llllll1_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ઞ"))
    bstack1lll11l1l1_opy_(path, bstack11l1l1111_opy_(bstack1lllll1111_opy_[bstack1l111l1l1_opy_]))
  bstack11ll1l1l_opy_()
  return bstack1l11l1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l11l111_opy_(self, ff_profile_dir):
  global bstack1l1ll11l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll11l1_opy_(self, ff_profile_dir)
def bstack11l111ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11lllll_opy_
  bstack1ll1ll1ll1_opy_ = []
  if bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ટ") in CONFIG:
    bstack1ll1ll1ll1_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1llllll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨડ")],
      pabot_args[bstack1llllll1_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢઢ")],
      argfile,
      pabot_args.get(bstack1llllll1_opy_ (u"ࠢࡩ࡫ࡹࡩࠧણ")),
      pabot_args[bstack1llllll1_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦત")],
      platform[0],
      bstack1l11lllll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1llllll1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤથ")] or [(bstack1llllll1_opy_ (u"ࠥࠦદ"), None)]
    for platform in enumerate(bstack1ll1ll1ll1_opy_)
  ]
def bstack11lllll1l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1lll1l_opy_=bstack1llllll1_opy_ (u"ࠫࠬધ")):
  global bstack11l11ll1l_opy_
  self.platform_index = platform_index
  self.bstack11l11ll1_opy_ = bstack1l1lll1l_opy_
  bstack11l11ll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack111l11l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1111ll_opy_
  global bstack1l1l111l1_opy_
  if not bstack1llllll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧન") in item.options:
    item.options[bstack1llllll1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ઩")] = []
  for v in item.options[bstack1llllll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩપ")]:
    if bstack1llllll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧફ") in v:
      item.options[bstack1llllll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫબ")].remove(v)
    if bstack1llllll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪભ") in v:
      item.options[bstack1llllll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭મ")].remove(v)
  item.options[bstack1llllll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧય")].insert(0, bstack1llllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨર").format(item.platform_index))
  item.options[bstack1llllll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ઱")].insert(0, bstack1llllll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨલ").format(item.bstack11l11ll1_opy_))
  if bstack1l1l111l1_opy_:
    item.options[bstack1llllll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫળ")].insert(0, bstack1llllll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭઴").format(bstack1l1l111l1_opy_))
  return bstack1lll1111ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1111ll_opy_(command, item_index):
  global bstack1l1l111l1_opy_
  if bstack1l1l111l1_opy_:
    command[0] = command[0].replace(bstack1llllll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ"), bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩશ") + str(
      item_index) + bstack1llllll1_opy_ (u"࠭ࠠࠨષ") + bstack1l1l111l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1llllll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭સ"),
                                    bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬહ") + str(item_index), 1)
def bstack1lll1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll11l111_opy_
  bstack1l1111ll_opy_(command, item_index)
  return bstack1lll11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l11ll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll11l111_opy_
  bstack1l1111ll_opy_(command, item_index)
  return bstack1lll11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1111l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll11l111_opy_
  bstack1l1111ll_opy_(command, item_index)
  return bstack1lll11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11llll111_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1l1llll_opy_
  bstack111ll111_opy_ = bstack1ll1l1llll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1llllll1_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ઺")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1llllll1_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ઻")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111ll111_opy_
def bstack111lll1l1_opy_(self, name, context, *args):
  global bstack11l11l11l_opy_
  if name == bstack1llllll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩ઼ࠬ"):
    bstack11l11l11l_opy_(self, name, context, *args)
    try:
      if not bstack11llll11l_opy_:
        bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllllll_opy_(bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫઽ")) else context.browser
        bstack1ll1ll11l_opy_ = str(self.feature.name)
        bstack1llllll1l_opy_(context, bstack1ll1ll11l_opy_)
        bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫા") + json.dumps(bstack1ll1ll11l_opy_) + bstack1llllll1_opy_ (u"ࠧࡾࡿࠪિ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1llllll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨી").format(str(e)))
  elif name == bstack1llllll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫુ"):
    bstack11l11l11l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1llllll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬૂ")):
        self.driver_before_scenario = True
      if (not bstack11llll11l_opy_):
        scenario_name = args[0].name
        feature_name = bstack1ll1ll11l_opy_ = str(self.feature.name)
        bstack1ll1ll11l_opy_ = feature_name + bstack1llllll1_opy_ (u"ࠫࠥ࠳ࠠࠨૃ") + scenario_name
        bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllllll_opy_(bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૄ")) else context.browser
        if self.driver_before_scenario:
          bstack1llllll1l_opy_(context, bstack1ll1ll11l_opy_)
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫૅ") + json.dumps(bstack1ll1ll11l_opy_) + bstack1llllll1_opy_ (u"ࠧࡾࡿࠪ૆"))
    except Exception as e:
      logger.debug(bstack1llllll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩે").format(str(e)))
  elif name == bstack1llllll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૈ"):
    try:
      bstack11ll1l1l1_opy_ = args[0].status.name
      bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1llllll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩૉ") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack11ll1l1l1_opy_).lower() == bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૊"):
        bstack111111111_opy_ = bstack1llllll1_opy_ (u"ࠬ࠭ો")
        bstack1lll11l1ll_opy_ = bstack1llllll1_opy_ (u"࠭ࠧૌ")
        bstack11ll11l11_opy_ = bstack1llllll1_opy_ (u"ࠧࠨ્")
        try:
          import traceback
          bstack111111111_opy_ = self.exception.__class__.__name__
          bstack1lll11ll1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1lll11l1ll_opy_ = bstack1llllll1_opy_ (u"ࠨࠢࠪ૎").join(bstack1lll11ll1l_opy_)
          bstack11ll11l11_opy_ = bstack1lll11ll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack111ll11l_opy_.format(str(e)))
        bstack111111111_opy_ += bstack11ll11l11_opy_
        bstack11l11lll_opy_(context, json.dumps(str(args[0].name) + bstack1llllll1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૏") + str(bstack1lll11l1ll_opy_)),
                            bstack1llllll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤૐ"))
        if self.driver_before_scenario:
          bstack1llll1ll1_opy_(context, bstack1llllll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ૑"), bstack111111111_opy_)
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ૒") + json.dumps(str(args[0].name) + bstack1llllll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ૓") + str(bstack1lll11l1ll_opy_)) + bstack1llllll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ૔"))
        if self.driver_before_scenario:
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ૕") + json.dumps(bstack1llllll1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ૖") + str(bstack111111111_opy_)) + bstack1llllll1_opy_ (u"ࠪࢁࢂ࠭૗"))
      else:
        bstack11l11lll_opy_(context, bstack1llllll1_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ૘"), bstack1llllll1_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ૙"))
        if self.driver_before_scenario:
          bstack1llll1ll1_opy_(context, bstack1llllll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૚"))
        bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૛") + json.dumps(str(args[0].name) + bstack1llllll1_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ૜")) + bstack1llllll1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ૝"))
        if self.driver_before_scenario:
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧ૞"))
    except Exception as e:
      logger.debug(bstack1llllll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭૟").format(str(e)))
  elif name == bstack1llllll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬૠ"):
    try:
      bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllllll_opy_(bstack1llllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬૡ")) else context.browser
      if context.failed is True:
        bstack1l1ll1ll1_opy_ = []
        bstack1ll1l1lll_opy_ = []
        bstack1lll1l111_opy_ = []
        bstack1111111l1_opy_ = bstack1llllll1_opy_ (u"ࠧࠨૢ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1ll1ll1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lll11ll1l_opy_ = traceback.format_tb(exc_tb)
            bstack1111l1l1_opy_ = bstack1llllll1_opy_ (u"ࠨࠢࠪૣ").join(bstack1lll11ll1l_opy_)
            bstack1ll1l1lll_opy_.append(bstack1111l1l1_opy_)
            bstack1lll1l111_opy_.append(bstack1lll11ll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack111ll11l_opy_.format(str(e)))
        bstack111111111_opy_ = bstack1llllll1_opy_ (u"ࠩࠪ૤")
        for i in range(len(bstack1l1ll1ll1_opy_)):
          bstack111111111_opy_ += bstack1l1ll1ll1_opy_[i] + bstack1lll1l111_opy_[i] + bstack1llllll1_opy_ (u"ࠪࡠࡳ࠭૥")
        bstack1111111l1_opy_ = bstack1llllll1_opy_ (u"ࠫࠥ࠭૦").join(bstack1ll1l1lll_opy_)
        if not self.driver_before_scenario:
          bstack11l11lll_opy_(context, bstack1111111l1_opy_, bstack1llllll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ૧"))
          bstack1llll1ll1_opy_(context, bstack1llllll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ૨"), bstack111111111_opy_)
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૩") + json.dumps(bstack1111111l1_opy_) + bstack1llllll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૪"))
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ૫") + json.dumps(bstack1llllll1_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ૬") + str(bstack111111111_opy_)) + bstack1llllll1_opy_ (u"ࠫࢂࢃࠧ૭"))
      else:
        if not self.driver_before_scenario:
          bstack11l11lll_opy_(context, bstack1llllll1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ૮") + str(self.feature.name) + bstack1llllll1_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ૯"), bstack1llllll1_opy_ (u"ࠢࡪࡰࡩࡳࠧ૰"))
          bstack1llll1ll1_opy_(context, bstack1llllll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ૱"))
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ૲") + json.dumps(bstack1llllll1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ૳") + str(self.feature.name) + bstack1llllll1_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ૴")) + bstack1llllll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ૵"))
          bstack1111l111_opy_.execute_script(bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ૶"))
    except Exception as e:
      logger.debug(bstack1llllll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૷").format(str(e)))
  else:
    bstack11l11l11l_opy_(self, name, context, *args)
  if name in [bstack1llllll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૸"), bstack1llllll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૹ")]:
    bstack11l11l11l_opy_(self, name, context, *args)
    if (name == bstack1llllll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫૺ") and self.driver_before_scenario) or (
            name == bstack1llllll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫૻ") and not self.driver_before_scenario):
      try:
        bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllllll_opy_(bstack1llllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૼ")) else context.browser
        bstack1111l111_opy_.quit()
      except Exception:
        pass
def bstack1llll1111l_opy_(config, startdir):
  return bstack1llllll1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦ૽").format(bstack1llllll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ૾"))
notset = Notset()
def bstack1111lll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11111ll11_opy_
  if str(name).lower() == bstack1llllll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ૿"):
    return bstack1llllll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ଀")
  else:
    return bstack11111ll11_opy_(self, name, default, skip)
def bstack11111llll_opy_(item, when):
  global bstack11lll11l_opy_
  try:
    bstack11lll11l_opy_(item, when)
  except Exception as e:
    pass
def bstack1llllllll_opy_():
  return
def bstack1l1lll111_opy_(type, name, status, reason, bstack111l1l111_opy_, bstack111llll1_opy_):
  bstack1l1l11lll_opy_ = {
    bstack1llllll1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଁ"): type,
    bstack1llllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଂ"): {}
  }
  if type == bstack1llllll1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଃ"):
    bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ଄")][bstack1llllll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଅ")] = bstack111l1l111_opy_
    bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଆ")][bstack1llllll1_opy_ (u"ࠩࡧࡥࡹࡧࠧଇ")] = json.dumps(str(bstack111llll1_opy_))
  if type == bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଈ"):
    bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଉ")][bstack1llllll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଊ")] = name
  if type == bstack1llllll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩଋ"):
    bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଌ")][bstack1llllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ଍")] = status
    if status == bstack1llllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଎"):
      bstack1l1l11lll_opy_[bstack1llllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଏ")][bstack1llllll1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫଐ")] = json.dumps(str(reason))
  bstack111l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଑").format(json.dumps(bstack1l1l11lll_opy_))
  return bstack111l1l1ll_opy_
def bstack1llll111ll_opy_(item, call, rep):
  global bstack11lll1lll_opy_
  global bstack1ll1lllll_opy_
  global bstack11llll11l_opy_
  name = bstack1llllll1_opy_ (u"࠭ࠧ଒")
  try:
    if rep.when == bstack1llllll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬଓ"):
      bstack11l1lll11_opy_ = threading.current_thread().bstack1l11l11l_opy_
      try:
        if not bstack11llll11l_opy_:
          name = str(rep.nodeid)
          bstack11ll1111_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଔ"), name, bstack1llllll1_opy_ (u"ࠩࠪକ"), bstack1llllll1_opy_ (u"ࠪࠫଖ"), bstack1llllll1_opy_ (u"ࠫࠬଗ"), bstack1llllll1_opy_ (u"ࠬ࠭ଘ"))
          for driver in bstack1ll1lllll_opy_:
            if bstack11l1lll11_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1111_opy_)
      except Exception as e:
        logger.debug(bstack1llllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ଙ").format(str(e)))
      try:
        bstack1lllllll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1llllll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨଚ"):
          status = bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଛ") if rep.outcome.lower() == bstack1llllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩଜ") else bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଝ")
          reason = bstack1llllll1_opy_ (u"ࠫࠬଞ")
          if status == bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬଟ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1llllll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫଠ") if status == bstack1llllll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଡ") else bstack1llllll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧଢ")
          data = name + bstack1llllll1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫଣ") if status == bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪତ") else name + bstack1llllll1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧଥ") + reason
          bstack1ll11ll11_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଦ"), bstack1llllll1_opy_ (u"࠭ࠧଧ"), bstack1llllll1_opy_ (u"ࠧࠨନ"), bstack1llllll1_opy_ (u"ࠨࠩ଩"), level, data)
          for driver in bstack1ll1lllll_opy_:
            if bstack11l1lll11_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11ll11_opy_)
      except Exception as e:
        logger.debug(bstack1llllll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ପ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧଫ").format(str(e)))
  bstack11lll1lll_opy_(item, call, rep)
def bstack1lll11111_opy_(framework_name):
  global bstack1ll1l1l1l_opy_
  global bstack1ll1l111ll_opy_
  global bstack11l1111l_opy_
  bstack1ll1l1l1l_opy_ = framework_name
  logger.info(bstack1ll1l11l1_opy_.format(bstack1ll1l1l1l_opy_.split(bstack1llllll1_opy_ (u"ࠫ࠲࠭ବ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll11llll_opy_:
      Service.start = bstack11lll1l11_opy_
      Service.stop = bstack1l1111lll_opy_
      webdriver.Remote.get = bstack1lll1llll1_opy_
      WebDriver.close = bstack1ll1l1ll1l_opy_
      WebDriver.quit = bstack1l1llll11_opy_
      webdriver.Remote.__init__ = bstack1l11111l1_opy_
    if not bstack1ll11llll_opy_ and bstack1111l111l_opy_.on():
      webdriver.Remote.__init__ = bstack11l1111l1_opy_
    bstack1ll1l111ll_opy_ = True
  except Exception as e:
    pass
  bstack1llllll11l_opy_()
  if not bstack1ll1l111ll_opy_:
    bstack1l1l11l11_opy_(bstack1llllll1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢଭ"), bstack111lllll1_opy_)
  if bstack1ll11l1l11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l111l11_opy_
    except Exception as e:
      logger.error(bstack1llll1ll_opy_.format(str(e)))
  if (bstack1llllll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬମ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l11l111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack111l1llll_opy_
      except Exception as e:
        logger.warn(bstack11l1ll111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1l1111l_opy_
      except Exception as e:
        logger.debug(bstack1l11ll1ll_opy_ + str(e))
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack11l1ll111_opy_)
    Output.end_test = bstack1ll1llll_opy_
    TestStatus.__init__ = bstack1lll1ll111_opy_
    QueueItem.__init__ = bstack11lllll1l_opy_
    pabot._create_items = bstack11l111ll1_opy_
    try:
      from pabot import __version__ as bstack1l111lll_opy_
      if version.parse(bstack1l111lll_opy_) >= version.parse(bstack1llllll1_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧଯ")):
        pabot._run = bstack1111l1ll1_opy_
      elif version.parse(bstack1l111lll_opy_) >= version.parse(bstack1llllll1_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨର")):
        pabot._run = bstack1l11ll1l1_opy_
      else:
        pabot._run = bstack1lll1l1ll1_opy_
    except Exception as e:
      pabot._run = bstack1lll1l1ll1_opy_
    pabot._create_command_for_execution = bstack111l11l1l_opy_
    pabot._report_results = bstack1ll1ll11_opy_
  if bstack1llllll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ଱") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack1l1l1ll11_opy_)
    Runner.run_hook = bstack111lll1l1_opy_
    Step.run = bstack11llll111_opy_
  if bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪଲ") in str(framework_name).lower():
    if not bstack1ll11llll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1llll1111l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1llllllll_opy_
      Config.getoption = bstack1111lll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll111ll_opy_
    except Exception as e:
      pass
def bstack111l1l1l1_opy_():
  global CONFIG
  if bstack1llllll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫଳ") in CONFIG and int(CONFIG[bstack1llllll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ଴")]) > 1:
    logger.warn(bstack11lll11l1_opy_)
def bstack1111111l_opy_(arg, bstack1111l1l1l_opy_):
  global CONFIG
  global bstack1llll1l1l1_opy_
  global bstack1l1l11l1l_opy_
  global bstack1ll11llll_opy_
  global bstack1l11l11l1_opy_
  bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ଵ")
  if bstack1111l1l1l_opy_ and isinstance(bstack1111l1l1l_opy_, str):
    bstack1111l1l1l_opy_ = eval(bstack1111l1l1l_opy_)
  CONFIG = bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧଶ")]
  bstack1llll1l1l1_opy_ = bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩଷ")]
  bstack1l1l11l1l_opy_ = bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫସ")]
  bstack1ll11llll_opy_ = bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ହ")]
  bstack1l11l11l1_opy_.bstack1111l11ll_opy_(bstack1llllll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ଺"), bstack1ll11llll_opy_)
  os.environ[bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ଻")] = bstack111l11ll1_opy_
  os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋ଼ࠬ")] = json.dumps(CONFIG)
  os.environ[bstack1llllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧଽ")] = bstack1llll1l1l1_opy_
  os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩା")] = str(bstack1l1l11l1l_opy_)
  os.environ[bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨି")] = str(True)
  if bstack1111l1lll_opy_(arg, [bstack1llllll1_opy_ (u"ࠪ࠱ࡳ࠭ୀ"), bstack1llllll1_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬୁ")]) != -1:
    os.environ[bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ୂ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll1lll_opy_)
    return
  bstack1ll11lll_opy_()
  global bstack1lll11lll_opy_
  global bstack11l11111l_opy_
  global bstack1l11lllll_opy_
  global bstack1l1l111l1_opy_
  global bstack1l1ll1l1l_opy_
  global bstack11l1111l_opy_
  global bstack1l111llll_opy_
  arg.append(bstack1llllll1_opy_ (u"ࠨ࠭ࡘࠤୃ"))
  arg.append(bstack1llllll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥୄ"))
  arg.append(bstack1llllll1_opy_ (u"ࠣ࠯࡚ࠦ୅"))
  arg.append(bstack1llllll1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣ୆"))
  global bstack1lll11l11l_opy_
  global bstack1llll1l11l_opy_
  global bstack111llll1l_opy_
  global bstack1l1ll11l1_opy_
  global bstack11l11ll1l_opy_
  global bstack1lll1111ll_opy_
  global bstack1ll1lll11_opy_
  global bstack11ll11lll_opy_
  global bstack1lll1lll_opy_
  global bstack11111ll11_opy_
  global bstack11lll11l_opy_
  global bstack11lll1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11l11l_opy_ = webdriver.Remote.__init__
    bstack1llll1l11l_opy_ = WebDriver.quit
    bstack1ll1lll11_opy_ = WebDriver.close
    bstack11ll11lll_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1ll11ll1l_opy_(CONFIG):
    if bstack1l111ll11_opy_() < version.parse(bstack1lll1llll_opy_):
      logger.error(bstack1lll1lll1_opy_.format(bstack1l111ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1lll1lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1llll1ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11111ll11_opy_ = Config.getoption
    from _pytest import runner
    bstack11lll11l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11ll1ll11_opy_)
  try:
    from pytest_bdd import reporting
    bstack11lll1lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1llllll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫେ"))
  bstack1l11lllll_opy_ = CONFIG.get(bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨୈ"), {}).get(bstack1llllll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୉"))
  bstack1l111llll_opy_ = True
  bstack1lll11111_opy_(bstack1llllll1ll_opy_)
  os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ୊")] = CONFIG[bstack1llllll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩୋ")]
  os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫୌ")] = CONFIG[bstack1llllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽ୍ࠬ")]
  os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭୎")] = bstack1ll11llll_opy_.__str__()
  from _pytest.config import main as bstack11l1ll11l_opy_
  bstack11l1ll11l_opy_(arg)
def bstack11lll111l_opy_(arg):
  bstack1lll11111_opy_(bstack1l1l1l1l1_opy_)
  from behave.__main__ import main as bstack1ll1lll11l_opy_
  bstack1ll1lll11l_opy_(arg)
def bstack1ll1l1ll11_opy_():
  logger.info(bstack111l1lll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ୏"), help=bstack1llllll1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭୐"))
  parser.add_argument(bstack1llllll1_opy_ (u"࠭࠭ࡶࠩ୑"), bstack1llllll1_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ୒"), help=bstack1llllll1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ୓"))
  parser.add_argument(bstack1llllll1_opy_ (u"ࠩ࠰࡯ࠬ୔"), bstack1llllll1_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩ୕"), help=bstack1llllll1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬୖ"))
  parser.add_argument(bstack1llllll1_opy_ (u"ࠬ࠳ࡦࠨୗ"), bstack1llllll1_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ୘"), help=bstack1llllll1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭୙"))
  bstack1llllll1l1_opy_ = parser.parse_args()
  try:
    bstack11l1l1l11_opy_ = bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬ୚")
    if bstack1llllll1l1_opy_.framework and bstack1llllll1l1_opy_.framework not in (bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ୛"), bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫଡ଼")):
      bstack11l1l1l11_opy_ = bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪଢ଼")
    bstack11llllll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l1l11_opy_)
    bstack11111l111_opy_ = open(bstack11llllll_opy_, bstack1llllll1_opy_ (u"ࠬࡸࠧ୞"))
    bstack111111l1l_opy_ = bstack11111l111_opy_.read()
    bstack11111l111_opy_.close()
    if bstack1llllll1l1_opy_.username:
      bstack111111l1l_opy_ = bstack111111l1l_opy_.replace(bstack1llllll1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ୟ"), bstack1llllll1l1_opy_.username)
    if bstack1llllll1l1_opy_.key:
      bstack111111l1l_opy_ = bstack111111l1l_opy_.replace(bstack1llllll1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩୠ"), bstack1llllll1l1_opy_.key)
    if bstack1llllll1l1_opy_.framework:
      bstack111111l1l_opy_ = bstack111111l1l_opy_.replace(bstack1llllll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩୡ"), bstack1llllll1l1_opy_.framework)
    file_name = bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬୢ")
    file_path = os.path.abspath(file_name)
    bstack11lll1ll_opy_ = open(file_path, bstack1llllll1_opy_ (u"ࠪࡻࠬୣ"))
    bstack11lll1ll_opy_.write(bstack111111l1l_opy_)
    bstack11lll1ll_opy_.close()
    logger.info(bstack1111l1ll_opy_)
    try:
      os.environ[bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭୤")] = bstack1llllll1l1_opy_.framework if bstack1llllll1l1_opy_.framework != None else bstack1llllll1_opy_ (u"ࠧࠨ୥")
      config = yaml.safe_load(bstack111111l1l_opy_)
      config[bstack1llllll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୦")] = bstack1llllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭୧")
      bstack111ll11l1_opy_(bstack11111l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1111ll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l11lll1_opy_.format(str(e)))
def bstack111ll11l1_opy_(bstack1ll111lll_opy_, config, bstack111l111l_opy_={}):
  global bstack1ll11llll_opy_
  if not config:
    return
  bstack1l11l111_opy_ = bstack1lll1l111l_opy_ if not bstack1ll11llll_opy_ else (
    bstack1ll1l1lll1_opy_ if bstack1llllll1_opy_ (u"ࠨࡣࡳࡴࠬ୨") in config else bstack1lllll1l1_opy_)
  data = {
    bstack1llllll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ୩"): config[bstack1llllll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ୪")],
    bstack1llllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୫"): config[bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୬")],
    bstack1llllll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ୭"): bstack1ll111lll_opy_,
    bstack1llllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ୮"): {
      bstack1llllll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭୯"): str(config[bstack1llllll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ୰")]) if bstack1llllll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪୱ") in config else bstack1llllll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ୲"),
      bstack1llllll1_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ୳"): bstack1llll11111_opy_(os.getenv(bstack1llllll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ୴"), bstack1llllll1_opy_ (u"ࠢࠣ୵"))),
      bstack1llllll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ୶"): bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ୷"),
      bstack1llllll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ୸"): bstack1l11l111_opy_,
      bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ୹"): config[bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ୺")] if config[bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ୻")] else bstack1llllll1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ୼"),
      bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୽"): str(config[bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ୾")]) if bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ୿") in config else bstack1llllll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ஀"),
      bstack1llllll1_opy_ (u"ࠬࡵࡳࠨ஁"): sys.platform,
      bstack1llllll1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨஂ"): socket.gethostname()
    }
  }
  update(data[bstack1llllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪஃ")], bstack111l111l_opy_)
  try:
    response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠨࡒࡒࡗ࡙࠭஄"), bstack1l1ll1111_opy_(bstack1lllll11l1_opy_), data, {
      bstack1llllll1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧஅ"): (config[bstack1llllll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬஆ")], config[bstack1llllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஇ")])
    })
    if response:
      logger.debug(bstack1lll1l1l1_opy_.format(bstack1ll111lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll111111_opy_.format(str(e)))
def bstack1llll11111_opy_(framework):
  return bstack1llllll1_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤஈ").format(str(framework), __version__) if framework else bstack1llllll1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢஉ").format(
    __version__)
def bstack1ll11lll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack111l1lll_opy_()
    logger.debug(bstack1ll1lllll1_opy_.format(str(CONFIG)))
    bstack1ll1ll1l_opy_()
    bstack111ll1l11_opy_()
  except Exception as e:
    logger.error(bstack1llllll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦஊ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1llllll_opy_
  atexit.register(bstack1lll1ll1l_opy_)
  signal.signal(signal.SIGINT, bstack1lll1l11_opy_)
  signal.signal(signal.SIGTERM, bstack1lll1l11_opy_)
def bstack1l1llllll_opy_(exctype, value, traceback):
  global bstack1ll1lllll_opy_
  try:
    for driver in bstack1ll1lllll_opy_:
      driver.execute_script(
        bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ஋") + json.dumps(
          bstack1llllll1_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ஌") + str(value)) + bstack1llllll1_opy_ (u"ࠪࢁࢂ࠭஍"))
  except Exception:
    pass
  bstack1l1l111ll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1l111ll_opy_(message=bstack1llllll1_opy_ (u"ࠫࠬஎ")):
  global CONFIG
  try:
    if message:
      bstack111l111l_opy_ = {
        bstack1llllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫஏ"): str(message)
      }
      bstack111ll11l1_opy_(bstack111lll11l_opy_, CONFIG, bstack111l111l_opy_)
    else:
      bstack111ll11l1_opy_(bstack111lll11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1111l1_opy_.format(str(e)))
def bstack1l1ll1l11_opy_(bstack1ll1ll111l_opy_, size):
  bstack1111ll1l1_opy_ = []
  while len(bstack1ll1ll111l_opy_) > size:
    bstack11ll1lll1_opy_ = bstack1ll1ll111l_opy_[:size]
    bstack1111ll1l1_opy_.append(bstack11ll1lll1_opy_)
    bstack1ll1ll111l_opy_ = bstack1ll1ll111l_opy_[size:]
  bstack1111ll1l1_opy_.append(bstack1ll1ll111l_opy_)
  return bstack1111ll1l1_opy_
def bstack11l1l1ll1_opy_(args):
  if bstack1llllll1_opy_ (u"࠭࠭࡮ࠩஐ") in args and bstack1llllll1_opy_ (u"ࠧࡱࡦࡥࠫ஑") in args:
    return True
  return False
def run_on_browserstack(bstack11ll1llll_opy_=None, bstack11l11l1l_opy_=None, bstack1lllll1ll_opy_=False):
  global CONFIG
  global bstack1llll1l1l1_opy_
  global bstack1l1l11l1l_opy_
  bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠨࠩஒ")
  bstack11111111l_opy_(bstack1lll1111_opy_, logger)
  if bstack11ll1llll_opy_ and isinstance(bstack11ll1llll_opy_, str):
    bstack11ll1llll_opy_ = eval(bstack11ll1llll_opy_)
  if bstack11ll1llll_opy_:
    CONFIG = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩஓ")]
    bstack1llll1l1l1_opy_ = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫஔ")]
    bstack1l1l11l1l_opy_ = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭க")]
    bstack1l11l11l1_opy_.bstack1111l11ll_opy_(bstack1llllll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ஖"), bstack1l1l11l1l_opy_)
    bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஗")
  if not bstack1lllll1ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll1lll_opy_)
      return
    if sys.argv[1] == bstack1llllll1_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ஘") or sys.argv[1] == bstack1llllll1_opy_ (u"ࠨ࠯ࡹࠫங"):
      logger.info(bstack1llllll1_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩச").format(__version__))
      return
    if sys.argv[1] == bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ஛"):
      bstack1ll1l1ll11_opy_()
      return
  args = sys.argv
  bstack1ll11lll_opy_()
  global bstack1lll11lll_opy_
  global bstack1l111llll_opy_
  global bstack1lll1l1111_opy_
  global bstack11l11111l_opy_
  global bstack1l11lllll_opy_
  global bstack1l1l111l1_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l1ll1l1l_opy_
  global bstack11l1111l_opy_
  if not bstack111l11ll1_opy_:
    if args[1] == bstack1llllll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫஜ") or args[1] == bstack1llllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭஝"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ஞ")
      args = args[2:]
    elif args[1] == bstack1llllll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ட"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஠")
      args = args[2:]
    elif args[1] == bstack1llllll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ஡"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ஢")
      args = args[2:]
    elif args[1] == bstack1llllll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬண"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭த")
      args = args[2:]
    elif args[1] == bstack1llllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭஥"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ஦")
      args = args[2:]
    elif args[1] == bstack1llllll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ஧"):
      bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩந")
      args = args[2:]
    else:
      if not bstack1llllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ன") in CONFIG or str(CONFIG[bstack1llllll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧப")]).lower() in [bstack1llllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ஫"), bstack1llllll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ஬")]:
        bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஭")
        args = args[1:]
      elif str(CONFIG[bstack1llllll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫம")]).lower() == bstack1llllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨய"):
        bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩர")
        args = args[1:]
      elif str(CONFIG[bstack1llllll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧற")]).lower() == bstack1llllll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫல"):
        bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬள")
        args = args[1:]
      elif str(CONFIG[bstack1llllll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪழ")]).lower() == bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨவ"):
        bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩஶ")
        args = args[1:]
      elif str(CONFIG[bstack1llllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ஷ")]).lower() == bstack1llllll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫஸ"):
        bstack111l11ll1_opy_ = bstack1llllll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬஹ")
        args = args[1:]
      else:
        os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ஺")] = bstack111l11ll1_opy_
        bstack11ll1l11_opy_(bstack1lll11llll_opy_)
  global bstack11l1ll1l_opy_
  if bstack11ll1llll_opy_:
    try:
      os.environ[bstack1llllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ஻")] = bstack111l11ll1_opy_
      bstack111ll11l1_opy_(bstack1111ll11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll1111l1_opy_.format(str(e)))
  global bstack1lll11l11l_opy_
  global bstack1llll1l11l_opy_
  global bstack111111ll1_opy_
  global bstack1lll1ll11l_opy_
  global bstack1l11l1ll1_opy_
  global bstack111llll1l_opy_
  global bstack1l1ll11l1_opy_
  global bstack1lll11l111_opy_
  global bstack11l11ll1l_opy_
  global bstack1lll1111ll_opy_
  global bstack1ll1lll11_opy_
  global bstack11l11l11l_opy_
  global bstack1ll1l1llll_opy_
  global bstack11ll11lll_opy_
  global bstack1lll1lll_opy_
  global bstack11111ll11_opy_
  global bstack11lll11l_opy_
  global bstack1l11l1l1l_opy_
  global bstack11lll1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11l11l_opy_ = webdriver.Remote.__init__
    bstack1llll1l11l_opy_ = WebDriver.quit
    bstack1ll1lll11_opy_ = WebDriver.close
    bstack11ll11lll_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l1ll1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1ll11ll1l_opy_(CONFIG):
    if bstack1l111ll11_opy_() < version.parse(bstack1lll1llll_opy_):
      logger.error(bstack1lll1lll1_opy_.format(bstack1l111ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1lll1lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1llll1ll_opy_.format(str(e)))
  if bstack111l11ll1_opy_ != bstack1llllll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ஼") or (bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஽") and not bstack11ll1llll_opy_):
    bstack1l1ll11l_opy_()
  if (bstack111l11ll1_opy_ in [bstack1llllll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩா"), bstack1llllll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪி"), bstack1llllll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ீ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l11l111_opy_
        bstack1l11l1ll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l1ll111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1ll11l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11ll1ll_opy_ + str(e))
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack11l1ll111_opy_)
    if bstack111l11ll1_opy_ != bstack1llllll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧு"):
      bstack11ll1l1l_opy_()
    bstack111111ll1_opy_ = Output.end_test
    bstack111llll1l_opy_ = TestStatus.__init__
    bstack1lll11l111_opy_ = pabot._run
    bstack11l11ll1l_opy_ = QueueItem.__init__
    bstack1lll1111ll_opy_ = pabot._create_command_for_execution
    bstack1l11l1l1l_opy_ = pabot._report_results
  if bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧூ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack1l1l1ll11_opy_)
    bstack11l11l11l_opy_ = Runner.run_hook
    bstack1ll1l1llll_opy_ = Step.run
  if bstack1llllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ௃") in CONFIG and CONFIG[bstack1llllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ௄")] == True:
    os.environ[bstack1llllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟࡚ࡏࡏࠫ௅")] = bstack1llllll1_opy_ (u"ࠫࡹࡸࡵࡦࠩெ")
  if bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬே") in CONFIG:
    os.environ[bstack1llllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧை")] = json.dumps(CONFIG[bstack1llllll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ௉")])
  os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧொ")] = bstack1llllll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧோ") if any([p.get(bstack1llllll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪௌ"), False) == True for p in CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ்ࠧ")]]) else bstack1llllll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ௎")
  if bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௏"):
    try:
      bstack1111l111l_opy_.launch(CONFIG, {
        bstack1llllll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨௐ"): bstack1llllll1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ௑") if bstack1l1lll11l_opy_() else bstack1llllll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ௒"),
        bstack1llllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௓"): bstack11l11l1ll_opy_.version(),
        bstack1llllll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௔"): __version__
      })
      if bstack1ll11llll_opy_ and bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ௕") in CONFIG and CONFIG[bstack1llllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭௖")] == True:
        bstack1ll11lll1_opy_, bstack1ll111l1_opy_ = bstack1lll1l1ll_opy_(CONFIG, bstack111l11ll1_opy_, bstack11l11l1ll_opy_.version());
        if not bstack1ll11lll1_opy_ is None:
          os.environ[bstack1llllll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬௗ")] = bstack1ll11lll1_opy_;
          os.environ[bstack1llllll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧ௘")] = str(bstack1ll111l1_opy_);
      from _pytest.config import Config
      bstack11111ll11_opy_ = Config.getoption
      from _pytest import runner
      bstack11lll11l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11ll1ll11_opy_)
    try:
      from pytest_bdd import reporting
      bstack11lll1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1llllll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ௙"))
  if bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௚"):
    bstack1l111llll_opy_ = True
    if bstack11ll1llll_opy_ and bstack1lllll1ll_opy_:
      bstack1l11lllll_opy_ = CONFIG.get(bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ௛"), {}).get(bstack1llllll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௜"))
      bstack1lll11111_opy_(bstack1lllll111_opy_)
    elif bstack11ll1llll_opy_:
      bstack1l11lllll_opy_ = CONFIG.get(bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௝"), {}).get(bstack1llllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௞"))
      global bstack1ll1lllll_opy_
      try:
        if bstack11l1l1ll1_opy_(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௟")]) and multiprocessing.current_process().name == bstack1llllll1_opy_ (u"ࠩ࠳ࠫ௠"):
          bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௡")].remove(bstack1llllll1_opy_ (u"ࠫ࠲ࡳࠧ௢"))
          bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௣")].remove(bstack1llllll1_opy_ (u"࠭ࡰࡥࡤࠪ௤"))
          bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ௥")] = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௦")][0]
          with open(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௧")], bstack1llllll1_opy_ (u"ࠪࡶࠬ௨")) as f:
            bstack1ll1ll111_opy_ = f.read()
          bstack1ll1llll1_opy_ = bstack1llllll1_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣ௩").format(str(bstack11ll1llll_opy_))
          bstack1lll11111l_opy_ = bstack1ll1llll1_opy_ + bstack1ll1ll111_opy_
          bstack111l11l11_opy_ = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௪")] + bstack1llllll1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨ௫")
          with open(bstack111l11l11_opy_, bstack1llllll1_opy_ (u"ࠧࡸࠩ௬")):
            pass
          with open(bstack111l11l11_opy_, bstack1llllll1_opy_ (u"ࠣࡹ࠮ࠦ௭")) as f:
            f.write(bstack1lll11111l_opy_)
          import subprocess
          bstack1l11111l_opy_ = subprocess.run([bstack1llllll1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ௮"), bstack111l11l11_opy_])
          if os.path.exists(bstack111l11l11_opy_):
            os.unlink(bstack111l11l11_opy_)
          os._exit(bstack1l11111l_opy_.returncode)
        else:
          if bstack11l1l1ll1_opy_(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௯")]):
            bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௰")].remove(bstack1llllll1_opy_ (u"ࠬ࠳࡭ࠨ௱"))
            bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௲")].remove(bstack1llllll1_opy_ (u"ࠧࡱࡦࡥࠫ௳"))
            bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௴")] = bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௵")][0]
          bstack1lll11111_opy_(bstack1lllll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௶")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1llllll1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭௷")] = bstack1llllll1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ௸")
          mod_globals[bstack1llllll1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ௹")] = os.path.abspath(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ௺")])
          exec(open(bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௻")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1llllll1_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ௼").format(str(e)))
          for driver in bstack1ll1lllll_opy_:
            bstack11l11l1l_opy_.append({
              bstack1llllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ௽"): bstack11ll1llll_opy_[bstack1llllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௾")],
              bstack1llllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௿"): str(e),
              bstack1llllll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬఀ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧఁ") + json.dumps(
                bstack1llllll1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦం") + str(e)) + bstack1llllll1_opy_ (u"ࠩࢀࢁࠬః"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1lllll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1l11l1l_opy_, CONFIG, logger)
      bstack1ll11l111_opy_()
      bstack111l1l1l1_opy_()
      bstack1111l1l1l_opy_ = {
        bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఄ"): args[0],
        bstack1llllll1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫఅ"): CONFIG,
        bstack1llllll1_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ఆ"): bstack1llll1l1l1_opy_,
        bstack1llllll1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨఇ"): bstack1l1l11l1l_opy_
      }
      percy.bstack11l1l111_opy_()
      if bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఈ") in CONFIG:
        bstack1ll1ll1l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l111l1_opy_ = manager.list()
        if bstack11l1l1ll1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఉ")]):
            if index == 0:
              bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఊ")] = args
            bstack1ll1ll1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111l1l1l_opy_, bstack111l111l1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1llllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఋ")]):
            bstack1ll1ll1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111l1l1l_opy_, bstack111l111l1_opy_)))
        for t in bstack1ll1ll1l1l_opy_:
          t.start()
        for t in bstack1ll1ll1l1l_opy_:
          t.join()
        bstack1ll1l1l1l1_opy_ = list(bstack111l111l1_opy_)
      else:
        if bstack11l1l1ll1_opy_(args):
          bstack1111l1l1l_opy_[bstack1llllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఌ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111l1l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll11111_opy_(bstack1lllll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1llllll1_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ఍")] = bstack1llllll1_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨఎ")
          mod_globals[bstack1llllll1_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩఏ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧఐ") or bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ఑"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack11l1ll111_opy_)
    bstack1ll11l111_opy_()
    bstack1lll11111_opy_(bstack1ll11ll111_opy_)
    if bstack1llllll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨఒ") in args:
      i = args.index(bstack1llllll1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩఓ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lll11lll_opy_))
    args.insert(0, str(bstack1llllll1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪఔ")))
    pabot.main(args)
  elif bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧక"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack11l1ll111_opy_)
    for a in args:
      if bstack1llllll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ఖ") in a:
        bstack11l11111l_opy_ = int(a.split(bstack1llllll1_opy_ (u"ࠨ࠼ࠪగ"))[1])
      if bstack1llllll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ఘ") in a:
        bstack1l11lllll_opy_ = str(a.split(bstack1llllll1_opy_ (u"ࠪ࠾ࠬఙ"))[1])
      if bstack1llllll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫచ") in a:
        bstack1l1l111l1_opy_ = str(a.split(bstack1llllll1_opy_ (u"ࠬࡀࠧఛ"))[1])
    bstack111l1l11l_opy_ = None
    if bstack1llllll1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬజ") in args:
      i = args.index(bstack1llllll1_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ఝ"))
      args.pop(i)
      bstack111l1l11l_opy_ = args.pop(i)
    if bstack111l1l11l_opy_ is not None:
      global bstack11lll111_opy_
      bstack11lll111_opy_ = bstack111l1l11l_opy_
    bstack1lll11111_opy_(bstack1ll11ll111_opy_)
    run_cli(args)
  elif bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨఞ"):
    bstack1llll111l_opy_ = bstack11l11l1ll_opy_(args, logger, CONFIG, bstack1ll11llll_opy_)
    bstack1llll111l_opy_.bstack1lll1ll1l1_opy_()
    bstack1ll11l111_opy_()
    bstack1lll1l1111_opy_ = True
    bstack11l1111l_opy_ = bstack1llll111l_opy_.bstack11lllll1_opy_()
    bstack1llll111l_opy_.bstack1111l1l1l_opy_(bstack11llll11l_opy_)
    bstack1l1ll1l1l_opy_ = bstack1llll111l_opy_.bstack111ll1ll1_opy_(bstack1111111l_opy_, {
      bstack1llllll1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪట"): bstack1llll1l1l1_opy_,
      bstack1llllll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬఠ"): bstack1l1l11l1l_opy_,
      bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧడ"): bstack1ll11llll_opy_
    })
  elif bstack111l11ll1_opy_ == bstack1llllll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬఢ"):
    try:
      from behave.__main__ import main as bstack1ll1lll11l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l11l11_opy_(e, bstack1l1l1ll11_opy_)
    bstack1ll11l111_opy_()
    bstack1lll1l1111_opy_ = True
    bstack1l111lll1_opy_ = 1
    if bstack1llllll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ణ") in CONFIG:
      bstack1l111lll1_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧత")]
    bstack11l1lllll_opy_ = int(bstack1l111lll1_opy_) * int(len(CONFIG[bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫథ")]))
    config = Configuration(args)
    bstack11lllllll_opy_ = config.paths
    if len(bstack11lllllll_opy_) == 0:
      import glob
      pattern = bstack1llllll1_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨద")
      bstack1ll11l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll11l1l1_opy_)
      config = Configuration(args)
      bstack11lllllll_opy_ = config.paths
    bstack1l1ll11ll_opy_ = [os.path.normpath(item) for item in bstack11lllllll_opy_]
    bstack1ll1ll1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11ll11l_opy_ = [item for item in bstack1ll1ll1l11_opy_ if item not in bstack1l1ll11ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1llllll1_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫధ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1ll11ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l11llll_opy_)))
                    for bstack11l11llll_opy_ in bstack1l1ll11ll_opy_]
    bstack11ll1ll1_opy_ = []
    for spec in bstack1l1ll11ll_opy_:
      bstack111llllll_opy_ = []
      bstack111llllll_opy_ += bstack1ll11ll11l_opy_
      bstack111llllll_opy_.append(spec)
      bstack11ll1ll1_opy_.append(bstack111llllll_opy_)
    execution_items = []
    for bstack111llllll_opy_ in bstack11ll1ll1_opy_:
      for index, _ in enumerate(CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧన")]):
        item = {}
        item[bstack1llllll1_opy_ (u"ࠬࡧࡲࡨࠩ఩")] = bstack1llllll1_opy_ (u"࠭ࠠࠨప").join(bstack111llllll_opy_)
        item[bstack1llllll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ఫ")] = index
        execution_items.append(item)
    bstack1ll11l1l_opy_ = bstack1l1ll1l11_opy_(execution_items, bstack11l1lllll_opy_)
    for execution_item in bstack1ll11l1l_opy_:
      bstack1ll1ll1l1l_opy_ = []
      for item in execution_item:
        bstack1ll1ll1l1l_opy_.append(bstack1l11l1l1_opy_(name=str(item[bstack1llllll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧబ")]),
                                             target=bstack11lll111l_opy_,
                                             args=(item[bstack1llllll1_opy_ (u"ࠩࡤࡶ࡬࠭భ")],)))
      for t in bstack1ll1ll1l1l_opy_:
        t.start()
      for t in bstack1ll1ll1l1l_opy_:
        t.join()
  else:
    bstack11ll1l11_opy_(bstack1lll11llll_opy_)
  if not bstack11ll1llll_opy_:
    bstack1111llll_opy_()
def browserstack_initialize(bstack1111lllll_opy_=None):
  run_on_browserstack(bstack1111lllll_opy_, None, True)
def bstack1111llll_opy_():
  global CONFIG
  bstack1111l111l_opy_.stop()
  bstack1111l111l_opy_.bstack111111l11_opy_()
  if bstack1llll111_opy_(CONFIG):
    bstack1l11ll1l_opy_()
  [bstack11lllll11_opy_, bstack11llll11_opy_] = bstack1l1lllll_opy_()
  if bstack11lllll11_opy_ is not None and bstack1lllll1l1l_opy_() != -1:
    sessions = bstack1ll11l1lll_opy_(bstack11lllll11_opy_)
    bstack111l11l1_opy_(sessions, bstack11llll11_opy_)
def bstack1ll1l1l111_opy_(bstack1ll111ll1_opy_):
  if bstack1ll111ll1_opy_:
    return bstack1ll111ll1_opy_.capitalize()
  else:
    return bstack1ll111ll1_opy_
def bstack11l1l1l1_opy_(bstack1111lll11_opy_):
  if bstack1llllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨమ") in bstack1111lll11_opy_ and bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩయ")] != bstack1llllll1_opy_ (u"ࠬ࠭ర"):
    return bstack1111lll11_opy_[bstack1llllll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫఱ")]
  else:
    bstack1l111l11l_opy_ = bstack1llllll1_opy_ (u"ࠢࠣల")
    if bstack1llllll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨళ") in bstack1111lll11_opy_ and bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩఴ")] != None:
      bstack1l111l11l_opy_ += bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪవ")] + bstack1llllll1_opy_ (u"ࠦ࠱ࠦࠢశ")
      if bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠬࡵࡳࠨష")] == bstack1llllll1_opy_ (u"ࠨࡩࡰࡵࠥస"):
        bstack1l111l11l_opy_ += bstack1llllll1_opy_ (u"ࠢࡪࡑࡖࠤࠧహ")
      bstack1l111l11l_opy_ += (bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ఺")] or bstack1llllll1_opy_ (u"ࠩࠪ఻"))
      return bstack1l111l11l_opy_
    else:
      bstack1l111l11l_opy_ += bstack1ll1l1l111_opy_(bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ఼ࠫ")]) + bstack1llllll1_opy_ (u"ࠦࠥࠨఽ") + (
              bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧా")] or bstack1llllll1_opy_ (u"࠭ࠧి")) + bstack1llllll1_opy_ (u"ࠢ࠭ࠢࠥీ")
      if bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠨࡱࡶࠫు")] == bstack1llllll1_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥూ"):
        bstack1l111l11l_opy_ += bstack1llllll1_opy_ (u"࡛ࠥ࡮ࡴࠠࠣృ")
      bstack1l111l11l_opy_ += bstack1111lll11_opy_[bstack1llllll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨౄ")] or bstack1llllll1_opy_ (u"ࠬ࠭౅")
      return bstack1l111l11l_opy_
def bstack111l1ll1l_opy_(bstack1lllllll11_opy_):
  if bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠨࡤࡰࡰࡨࠦె"):
    return bstack1llllll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪే")
  elif bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣై"):
    return bstack1llllll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౉")
  elif bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥొ"):
    return bstack1llllll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫో")
  elif bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦౌ"):
    return bstack1llllll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ్")
  elif bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ౎"):
    return bstack1llllll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౏")
  elif bstack1lllllll11_opy_ == bstack1llllll1_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥ౐"):
    return bstack1llllll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ౑")
  else:
    return bstack1llllll1_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨ౒") + bstack1ll1l1l111_opy_(
      bstack1lllllll11_opy_) + bstack1llllll1_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ౓")
def bstack1ll1l1ll_opy_(session):
  return bstack1llllll1_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭౔").format(
    session[bstack1llllll1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ౕࠫ")], bstack11l1l1l1_opy_(session), bstack111l1ll1l_opy_(session[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹౖࠧ")]),
    bstack111l1ll1l_opy_(session[bstack1llllll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౗")]),
    bstack1ll1l1l111_opy_(session[bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫౘ")] or session[bstack1llllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫౙ")] or bstack1llllll1_opy_ (u"ࠬ࠭ౚ")) + bstack1llllll1_opy_ (u"ࠨࠠࠣ౛") + (session[bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ౜")] or bstack1llllll1_opy_ (u"ࠨࠩౝ")),
    session[bstack1llllll1_opy_ (u"ࠩࡲࡷࠬ౞")] + bstack1llllll1_opy_ (u"ࠥࠤࠧ౟") + session[bstack1llllll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨౠ")], session[bstack1llllll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧౡ")] or bstack1llllll1_opy_ (u"࠭ࠧౢ"),
    session[bstack1llllll1_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫౣ")] if session[bstack1llllll1_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ౤")] else bstack1llllll1_opy_ (u"ࠩࠪ౥"))
def bstack111l11l1_opy_(sessions, bstack11llll11_opy_):
  try:
    bstack1ll1l1l1ll_opy_ = bstack1llllll1_opy_ (u"ࠥࠦ౦")
    if not os.path.exists(bstack111l11111_opy_):
      os.mkdir(bstack111l11111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1llllll1_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ౧")), bstack1llllll1_opy_ (u"ࠬࡸࠧ౨")) as f:
      bstack1ll1l1l1ll_opy_ = f.read()
    bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1llllll1_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪ౩"), str(len(sessions)))
    bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1llllll1_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ౪"), bstack11llll11_opy_)
    bstack1ll1l1l1ll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack1llllll1_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩ౫"),
                                              sessions[0].get(bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭౬")) if sessions[0] else bstack1llllll1_opy_ (u"ࠪࠫ౭"))
    with open(os.path.join(bstack111l11111_opy_, bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ౮")), bstack1llllll1_opy_ (u"ࠬࡽࠧ౯")) as stream:
      stream.write(bstack1ll1l1l1ll_opy_.split(bstack1llllll1_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ౰"))[0])
      for session in sessions:
        stream.write(bstack1ll1l1ll_opy_(session))
      stream.write(bstack1ll1l1l1ll_opy_.split(bstack1llllll1_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ౱"))[1])
    logger.info(bstack1llllll1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫ౲").format(bstack111l11111_opy_));
  except Exception as e:
    logger.debug(bstack1111ll1l_opy_.format(str(e)))
def bstack1ll11l1lll_opy_(bstack11lllll11_opy_):
  global CONFIG
  try:
    host = bstack1llllll1_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ౳") if bstack1llllll1_opy_ (u"ࠪࡥࡵࡶࠧ౴") in CONFIG else bstack1llllll1_opy_ (u"ࠫࡦࡶࡩࠨ౵")
    user = CONFIG[bstack1llllll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ౶")]
    key = CONFIG[bstack1llllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ౷")]
    bstack111lll1ll_opy_ = bstack1llllll1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭౸") if bstack1llllll1_opy_ (u"ࠨࡣࡳࡴࠬ౹") in CONFIG else bstack1llllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ౺")
    url = bstack1llllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ౻").format(user, key, host, bstack111lll1ll_opy_,
                                                                                bstack11lllll11_opy_)
    headers = {
      bstack1llllll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ౼"): bstack1llllll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ౽"),
    }
    proxies = bstack1ll11lll1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1llllll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ౾")], response.json()))
  except Exception as e:
    logger.debug(bstack111ll1ll_opy_.format(str(e)))
def bstack1l1lllll_opy_():
  global CONFIG
  try:
    if bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ౿") in CONFIG:
      host = bstack1llllll1_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫಀ") if bstack1llllll1_opy_ (u"ࠩࡤࡴࡵ࠭ಁ") in CONFIG else bstack1llllll1_opy_ (u"ࠪࡥࡵ࡯ࠧಂ")
      user = CONFIG[bstack1llllll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ಃ")]
      key = CONFIG[bstack1llllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ಄")]
      bstack111lll1ll_opy_ = bstack1llllll1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಅ") if bstack1llllll1_opy_ (u"ࠧࡢࡲࡳࠫಆ") in CONFIG else bstack1llllll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪಇ")
      url = bstack1llllll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩಈ").format(user, key, host, bstack111lll1ll_opy_)
      headers = {
        bstack1llllll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩಉ"): bstack1llllll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧಊ"),
      }
      if bstack1llllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಋ") in CONFIG:
        params = {bstack1llllll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಌ"): CONFIG[bstack1llllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ಍")], bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಎ"): CONFIG[bstack1llllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಏ")]}
      else:
        params = {bstack1llllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨಐ"): CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ಑")]}
      proxies = bstack1ll11lll1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111lll111_opy_ = response.json()[0][bstack1llllll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨಒ")]
        if bstack111lll111_opy_:
          bstack11llll11_opy_ = bstack111lll111_opy_[bstack1llllll1_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪಓ")].split(bstack1llllll1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ಔ"))[0] + bstack1llllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩಕ") + bstack111lll111_opy_[
            bstack1llllll1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬಖ")]
          logger.info(bstack1l1111l1_opy_.format(bstack11llll11_opy_))
          bstack1llll11l_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ಗ")]
          if bstack1llllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಘ") in CONFIG:
            bstack1llll11l_opy_ += bstack1llllll1_opy_ (u"ࠬࠦࠧಙ") + CONFIG[bstack1llllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಚ")]
          if bstack1llll11l_opy_ != bstack111lll111_opy_[bstack1llllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಛ")]:
            logger.debug(bstack1l1lll1ll_opy_.format(bstack111lll111_opy_[bstack1llllll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಜ")], bstack1llll11l_opy_))
          return [bstack111lll111_opy_[bstack1llllll1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬಝ")], bstack11llll11_opy_]
    else:
      logger.warn(bstack1llllllll1_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll1l1_opy_.format(str(e)))
  return [None, None]
def bstack1l11l1ll_opy_(url, bstack1111lll1l_opy_=False):
  global CONFIG
  global bstack1l1111l11_opy_
  if not bstack1l1111l11_opy_:
    hostname = bstack1l1l11ll1_opy_(url)
    is_private = bstack111lll11_opy_(hostname)
    if (bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧಞ") in CONFIG and not CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨಟ")]) and (is_private or bstack1111lll1l_opy_):
      bstack1l1111l11_opy_ = hostname
def bstack1l1l11ll1_opy_(url):
  return urlparse(url).hostname
def bstack111lll11_opy_(hostname):
  for bstack1ll1111l_opy_ in bstack11l1ll11_opy_:
    regex = re.compile(bstack1ll1111l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lllllllll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1ll11ll1_opy_(driver):
  global CONFIG
  if not bstack1llll111_opy_(CONFIG):
    logger.warning(bstack1llllll1_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣಠ"))
    return {}
  try:
    results = driver.execute_script(bstack1llllll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࡸࡨࡲࡹࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡇࡆࡖࡢࡖࡊ࡙ࡕࡍࡖࡖࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡨࡺࡪࡴࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࠬࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠱ࡨࡦࡺࡡࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡥࡩࡪࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡒࡆࡕࡓࡓࡓ࡙ࡅࠨ࠮ࠣࡪࡳ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩࡻ࡫࡮ࡵࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧ࡭ࡩࡨࡺࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂ࠯࠻ࠋࠢࠣࠤࠥࠨࠢࠣಡ"))
    return results
  except Exception:
    logger.error(bstack1llllll1_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤಢ"))
    return {}
def bstack1ll1lll111_opy_(driver):
  global CONFIG
  if not bstack1llll111_opy_(CONFIG):
    logger.warning(bstack1llllll1_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧಣ"))
    return {}
  try:
    bstack1lll1l11l1_opy_ = driver.execute_script(bstack1llllll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡊࡉ࡙ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡥࡷࡧࡱࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡓࡖࡏࡐࡅࡗ࡟࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡴࡲࡶࡦࠪࡨࡺࡪࡴࡴ࠯ࡦࡨࡸࡦ࡯࡬࠯ࡵࡸࡱࡲࡧࡲࡺࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࡶࡦࡰࡷ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠦࡣࡢࡶࡦ࡬ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩ࡯࡫ࡣࡵࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠣࠤࠥತ"))
    return bstack1lll1l11l1_opy_
  except Exception:
    logger.error(bstack1llllll1_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦಥ"))
    return {}