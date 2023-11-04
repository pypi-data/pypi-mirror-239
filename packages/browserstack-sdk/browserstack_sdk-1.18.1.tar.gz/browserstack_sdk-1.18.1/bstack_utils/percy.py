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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1ll1111_opy_, bstack1ll111l11_opy_
class bstack1lllll11ll_opy_:
  working_dir = os.getcwd()
  bstack11111l1l1_opy_ = False
  config = {}
  binary_path = bstack1llllll1_opy_ (u"ࠨࠩᅂ")
  bstack1l1111l111_opy_ = bstack1llllll1_opy_ (u"ࠩࠪᅃ")
  bstack1l111111ll_opy_ = False
  bstack1l11111l1l_opy_ = None
  bstack1l11l11111_opy_ = {}
  bstack1l11111lll_opy_ = 300
  bstack1l111l1l11_opy_ = False
  logger = None
  bstack1l111ll1ll_opy_ = False
  bstack1l1111l1ll_opy_ = bstack1llllll1_opy_ (u"ࠪࠫᅄ")
  bstack1l1111llll_opy_ = {
    bstack1llllll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᅅ") : 1,
    bstack1llllll1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᅆ") : 2,
    bstack1llllll1_opy_ (u"࠭ࡥࡥࡩࡨࠫᅇ") : 3,
    bstack1llllll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᅈ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1l11l1ll11_opy_(self):
    bstack1l11l1llll_opy_ = bstack1llllll1_opy_ (u"ࠨࠩᅉ")
    bstack1l11l1ll1l_opy_ = sys.platform
    bstack11lllllll1_opy_ = bstack1llllll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᅊ")
    if re.match(bstack1llllll1_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᅋ"), bstack1l11l1ll1l_opy_) != None:
      bstack1l11l1llll_opy_ = bstack1l1ll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᅌ")
      self.bstack1l1111l1ll_opy_ = bstack1llllll1_opy_ (u"ࠬࡳࡡࡤࠩᅍ")
    elif re.match(bstack1llllll1_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᅎ"), bstack1l11l1ll1l_opy_) != None:
      bstack1l11l1llll_opy_ = bstack1l1ll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᅏ")
      bstack11lllllll1_opy_ = bstack1llllll1_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᅐ")
      self.bstack1l1111l1ll_opy_ = bstack1llllll1_opy_ (u"ࠩࡺ࡭ࡳ࠭ᅑ")
    else:
      bstack1l11l1llll_opy_ = bstack1l1ll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᅒ")
      self.bstack1l1111l1ll_opy_ = bstack1llllll1_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᅓ")
    return bstack1l11l1llll_opy_, bstack11lllllll1_opy_
  def bstack1l11l1l11l_opy_(self):
    try:
      bstack1l11l111ll_opy_ = [os.path.join(expanduser(bstack1llllll1_opy_ (u"ࠧࢄࠢᅔ")), bstack1llllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᅕ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1l11l111ll_opy_:
        if(self.bstack1l11111ll1_opy_(path)):
          return path
      raise bstack1llllll1_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᅖ")
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᅗ").format(e))
  def bstack1l11111ll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1l111l111l_opy_(self, bstack1l11l1llll_opy_, bstack11lllllll1_opy_):
    try:
      bstack1l11l1l1l1_opy_ = self.bstack1l11l1l11l_opy_()
      bstack1l1111l1l1_opy_ = os.path.join(bstack1l11l1l1l1_opy_, bstack1llllll1_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᅘ"))
      bstack1l11l11ll1_opy_ = os.path.join(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_)
      if os.path.exists(bstack1l11l11ll1_opy_):
        self.logger.info(bstack1llllll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᅙ").format(bstack1l11l11ll1_opy_))
        return bstack1l11l11ll1_opy_
      if os.path.exists(bstack1l1111l1l1_opy_):
        self.logger.info(bstack1llllll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᅚ").format(bstack1l1111l1l1_opy_))
        return self.bstack1l111llll1_opy_(bstack1l1111l1l1_opy_, bstack11lllllll1_opy_)
      self.logger.info(bstack1llllll1_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᅛ").format(bstack1l11l1llll_opy_))
      response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"࠭ࡇࡆࡖࠪᅜ"), bstack1l11l1llll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1l1111l1l1_opy_, bstack1llllll1_opy_ (u"ࠧࡸࡤࠪᅝ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l111lll1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࡧ࡯࡮ࡢࡴࡼࡣࡿ࡯ࡰࡠࡲࡤࡸ࡭ࢃࠢᅞ"))
        return self.bstack1l111llll1_opy_(bstack1l1111l1l1_opy_, bstack11lllllll1_opy_)
      else:
        raise(bstack1l111lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࡹࡴࡢࡶࡸࡷࡤࡩ࡯ࡥࡧࢀࠦᅟ"))
    except:
      self.logger.error(bstack1llllll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᅠ"))
  def bstack1l11l1111l_opy_(self, bstack1l11l1llll_opy_, bstack11lllllll1_opy_):
    try:
      bstack1l11l11ll1_opy_ = self.bstack1l111l111l_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_)
      bstack11llllll1l_opy_ = self.bstack1l11l1l1ll_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_, bstack1l11l11ll1_opy_)
      return bstack1l11l11ll1_opy_, bstack11llllll1l_opy_
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᅡ").format(e))
    return bstack1l11l11ll1_opy_, False
  def bstack1l11l1l1ll_opy_(self, bstack1l11l1llll_opy_, bstack11lllllll1_opy_, bstack1l11l11ll1_opy_, bstack1l1111lll1_opy_ = 0):
    if bstack1l1111lll1_opy_ > 1:
      return False
    if bstack1l11l11ll1_opy_ == None or os.path.exists(bstack1l11l11ll1_opy_) == False:
      self.logger.warn(bstack1llllll1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᅢ"))
      bstack1l11l11ll1_opy_ = self.bstack1l111l111l_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_)
      self.bstack1l11l1l1ll_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_, bstack1l11l11ll1_opy_, bstack1l1111lll1_opy_+1)
    bstack1l111l1ll1_opy_ = bstack1llllll1_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᅣ")
    command = bstack1llllll1_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᅤ").format(bstack1l11l11ll1_opy_)
    bstack1l111l1111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1l111l1ll1_opy_, bstack1l111l1111_opy_) != None:
      return True
    else:
      self.logger.error(bstack1llllll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᅥ"))
      bstack1l11l11ll1_opy_ = self.bstack1l111l111l_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_)
      self.bstack1l11l1l1ll_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_, bstack1l11l11ll1_opy_, bstack1l1111lll1_opy_+1)
  def bstack1l111llll1_opy_(self, bstack1l1111l1l1_opy_, bstack11lllllll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1l1111l1l1_opy_)
      shutil.unpack_archive(bstack1l1111l1l1_opy_, working_dir)
      bstack1l11l11ll1_opy_ = os.path.join(working_dir, bstack11lllllll1_opy_)
      os.chmod(bstack1l11l11ll1_opy_, 0o755)
      return bstack1l11l11ll1_opy_
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᅦ"))
  def bstack1l11l11lll_opy_(self):
    try:
      percy = str(self.config.get(bstack1llllll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᅧ"), bstack1llllll1_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᅨ"))).lower()
      if percy != bstack1llllll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᅩ"):
        return False
      self.bstack1l111111ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᅪ").format(e))
  def init(self, bstack11111l1l1_opy_, config, logger):
    self.bstack11111l1l1_opy_ = bstack11111l1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1l11l11lll_opy_():
      return
    self.bstack1l11l11111_opy_ = config.get(bstack1llllll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅫ"), {})
    try:
      bstack1l11l1llll_opy_, bstack11lllllll1_opy_ = self.bstack1l11l1ll11_opy_()
      bstack1l11l11ll1_opy_, bstack11llllll1l_opy_ = self.bstack1l11l1111l_opy_(bstack1l11l1llll_opy_, bstack11lllllll1_opy_)
      if bstack11llllll1l_opy_:
        self.binary_path = bstack1l11l11ll1_opy_
        thread = Thread(target=self.bstack11llllllll_opy_)
        thread.start()
      else:
        self.bstack1l111ll1ll_opy_ = True
        self.logger.error(bstack1llllll1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧᅬ").format(bstack1l11l11ll1_opy_))
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᅭ").format(e))
  def bstack1l1111ll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1llllll1_opy_ (u"ࠪࡰࡴ࡭ࠧᅮ"), bstack1llllll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧᅯ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1llllll1_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤᅰ").format(logfile))
      self.bstack1l1111l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᅱ").format(e))
  def bstack11llllllll_opy_(self):
    bstack1l11111l11_opy_ = self.bstack1l11l1lll1_opy_()
    if bstack1l11111l11_opy_ == None:
      self.bstack1l111ll1ll_opy_ = True
      self.logger.error(bstack1llllll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥᅲ"))
      return False
    command_args = [bstack1llllll1_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤᅳ") if self.bstack11111l1l1_opy_ else bstack1llllll1_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭ᅴ")]
    bstack1l11l111l1_opy_ = self.bstack1l111ll11l_opy_()
    if bstack1l11l111l1_opy_ != None:
      command_args.append(bstack1llllll1_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤᅵ").format(bstack1l11l111l1_opy_))
    env = os.environ.copy()
    env[bstack1llllll1_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤᅶ")] = bstack1l11111l11_opy_
    bstack1l111ll1l1_opy_ = [self.binary_path]
    self.bstack1l1111ll11_opy_()
    self.bstack1l11111l1l_opy_ = self.bstack1l111111l1_opy_(bstack1l111ll1l1_opy_ + command_args, env)
    self.logger.debug(bstack1llllll1_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨᅷ"))
    bstack1l1111lll1_opy_ = 0
    while self.bstack1l11111l1l_opy_.poll() == None:
      bstack1l1111l11l_opy_ = self.bstack1l1111ll1l_opy_()
      if bstack1l1111l11l_opy_:
        self.logger.debug(bstack1llllll1_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤᅸ"))
        self.bstack1l111l1l11_opy_ = True
        return True
      bstack1l1111lll1_opy_ += 1
      self.logger.debug(bstack1llllll1_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥᅹ").format(bstack1l1111lll1_opy_))
      time.sleep(2)
    self.logger.error(bstack1llllll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨᅺ").format(bstack1l1111lll1_opy_))
    self.bstack1l111ll1ll_opy_ = True
    return False
  def bstack1l1111ll1l_opy_(self, bstack1l1111lll1_opy_ = 0):
    try:
      if bstack1l1111lll1_opy_ > 10:
        return False
      bstack1l111lll11_opy_ = os.environ.get(bstack1llllll1_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩᅻ"), bstack1llllll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫᅼ"))
      bstack1l111l11ll_opy_ = bstack1l111lll11_opy_ + bstack1l1ll1l1ll_opy_
      response = requests.get(bstack1l111l11ll_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1l11l1lll1_opy_(self):
    bstack1l11l11l11_opy_ = bstack1llllll1_opy_ (u"ࠫࡦࡶࡰࠨᅽ") if self.bstack11111l1l1_opy_ else bstack1llllll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᅾ")
    bstack1l1l11ll1l_opy_ = bstack1llllll1_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠧᅿ").format(self.config[bstack1llllll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᆀ")], bstack1l11l11l11_opy_)
    uri = bstack1l1ll1111_opy_(bstack1l1l11ll1l_opy_)
    try:
      response = bstack1ll111l11_opy_(bstack1llllll1_opy_ (u"ࠨࡉࡈࡘࠬᆁ"), uri, {}, {bstack1llllll1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᆂ"): (self.config[bstack1llllll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᆃ")], self.config[bstack1llllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᆄ")])})
      if response.status_code == 200:
        bstack1l111lllll_opy_ = response.json()
        if bstack1llllll1_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᆅ") in bstack1l111lllll_opy_:
          return bstack1l111lllll_opy_[bstack1llllll1_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᆆ")]
        else:
          raise bstack1llllll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧᆇ").format(bstack1l111lllll_opy_)
      else:
        raise bstack1llllll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣᆈ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥᆉ").format(e))
  def bstack1l111ll11l_opy_(self):
    bstack1l11ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll1_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨᆊ"))
    try:
      if bstack1llllll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᆋ") not in self.bstack1l11l11111_opy_:
        self.bstack1l11l11111_opy_[bstack1llllll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᆌ")] = 2
      with open(bstack1l11ll1111_opy_, bstack1llllll1_opy_ (u"࠭ࡷࠨᆍ")) as fp:
        json.dump(self.bstack1l11l11111_opy_, fp)
      return bstack1l11ll1111_opy_
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᆎ").format(e))
  def bstack1l111111l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1l1111l1ll_opy_ == bstack1llllll1_opy_ (u"ࠨࡹ࡬ࡲࠬᆏ"):
        bstack1l11l1l111_opy_ = [bstack1llllll1_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᆐ"), bstack1llllll1_opy_ (u"ࠪ࠳ࡨ࠭ᆑ")]
        cmd = bstack1l11l1l111_opy_ + cmd
      cmd = bstack1llllll1_opy_ (u"ࠫࠥ࠭ᆒ").join(cmd)
      self.logger.debug(bstack1llllll1_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᆓ").format(cmd))
      with open(self.bstack1l1111l111_opy_, bstack1llllll1_opy_ (u"ࠨࡡࠣᆔ")) as bstack1l111l11l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1l111l11l1_opy_, text=True, stderr=bstack1l111l11l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1l111ll1ll_opy_ = True
      self.logger.error(bstack1llllll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᆕ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1l111l1l11_opy_:
        self.logger.info(bstack1llllll1_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᆖ"))
        cmd = [self.binary_path, bstack1llllll1_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᆗ")]
        self.bstack1l111111l1_opy_(cmd)
        self.bstack1l111l1l11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᆘ").format(cmd, e))
  def bstack11l1l111_opy_(self):
    if not self.bstack1l111111ll_opy_:
      return
    try:
      bstack1l1111111l_opy_ = 0
      while not self.bstack1l111l1l11_opy_ and bstack1l1111111l_opy_ < self.bstack1l11111lll_opy_:
        if self.bstack1l111ll1ll_opy_:
          self.logger.info(bstack1llllll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤᆙ"))
          return
        time.sleep(1)
        bstack1l1111111l_opy_ += 1
      os.environ[bstack1llllll1_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᆚ")] = str(self.bstack1l111ll111_opy_())
      self.logger.info(bstack1llllll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢᆛ"))
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᆜ").format(e))
  def bstack1l111ll111_opy_(self):
    if self.bstack11111l1l1_opy_:
      return
    try:
      bstack1l111l1lll_opy_ = [platform[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᆝ")].lower() for platform in self.config.get(bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆞ"), [])]
      bstack1l11111111_opy_ = sys.maxsize
      bstack1l111l1l1l_opy_ = bstack1llllll1_opy_ (u"ࠪࠫᆟ")
      for browser in bstack1l111l1lll_opy_:
        if browser in self.bstack1l1111llll_opy_:
          bstack1l11l11l1l_opy_ = self.bstack1l1111llll_opy_[browser]
        if bstack1l11l11l1l_opy_ < bstack1l11111111_opy_:
          bstack1l11111111_opy_ = bstack1l11l11l1l_opy_
          bstack1l111l1l1l_opy_ = browser
      return bstack1l111l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1llllll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᆠ").format(e))