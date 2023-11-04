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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll111l_opy_, bstack111lll1l_opy_, update, bstack1lll1ll1ll_opy_,
                                       bstack1llll1111l_opy_, bstack1llllllll_opy_, bstack11lll1l11_opy_, bstack1l1111lll_opy_,
                                       bstack1ll1l1ll1l_opy_, bstack1ll1l1ll1_opy_, bstack1l1l11l11_opy_, bstack1lllllll1l_opy_,
                                       bstack1l1ll1l1_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1lll1lll_opy_
from bstack_utils.constants import bstack1lllll11l_opy_, bstack11ll11l1l_opy_, bstack1lll1llll_opy_, bstack1ll11l11_opy_, \
    bstack1llllll1ll_opy_
from bstack_utils.helper import bstack1lll1l1lll_opy_, bstack1l1l1l1ll1_opy_, bstack1l1l1ll1l1_opy_, bstack1ll1lll1l_opy_, bstack1l1l1l1l11_opy_, \
    bstack1l1l11lll1_opy_, bstack1l111ll11_opy_, bstack1l11ll11_opy_, bstack1l1l1l1111_opy_, bstack1l1lll11l_opy_, Notset, \
    bstack111l1ll11_opy_, bstack1l1ll11l1l_opy_, bstack1l1ll11111_opy_, Result, bstack1l1ll11lll_opy_, bstack1l1l11ll11_opy_, bstack1l1ll1l11l_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l11lll111_opy_
from bstack_utils.messages import bstack11l11l11_opy_, bstack11111lll1_opy_, bstack1l11111ll_opy_, bstack1ll11l1ll_opy_, bstack11ll1ll11_opy_, \
    bstack1llll1ll_opy_, bstack1lll1lll1_opy_, bstack1111llll1_opy_, bstack1lll1lllll_opy_, bstack1ll1ll1111_opy_, \
    bstack111lllll1_opy_, bstack1ll1l11l1_opy_
from bstack_utils.proxy import bstack1llll1llll_opy_, bstack1lll11ll_opy_
from bstack_utils.bstack1111l11l1_opy_ import bstack11llll111l_opy_, bstack11lll1l1ll_opy_, bstack11llll1111_opy_, bstack11lll1l111_opy_, \
    bstack11llll11l1_opy_, bstack11lll11lll_opy_, bstack11lll1l11l_opy_, bstack1lllllll1_opy_, bstack11llll1l11_opy_
from bstack_utils.bstack11ll1l1l1l_opy_ import bstack11ll1ll111_opy_
from bstack_utils.bstack11lll1ll1l_opy_ import bstack1l1lll111_opy_, bstack1l11l1ll_opy_, bstack1ll1llll1l_opy_
from bstack_utils.bstack11ll1111ll_opy_ import bstack11ll111l1l_opy_
from bstack_utils.bstack11l1l11ll_opy_ import bstack1111l111l_opy_
bstack1lll11l11l_opy_ = None
bstack1llll1l11l_opy_ = None
bstack111llll1l_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack11l11ll1l_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1lll1lll_opy_ = None
bstack1ll1lll11_opy_ = None
bstack11ll11lll_opy_ = None
bstack11l1ll1l_opy_ = None
bstack11111ll11_opy_ = None
bstack11lll11l_opy_ = None
bstack11lll1lll_opy_ = None
bstack1ll1l1l1l_opy_ = bstack1llllll1_opy_ (u"ࠪࠫጠ")
CONFIG = {}
bstack1l1l11l1l_opy_ = False
bstack1llll1l1l1_opy_ = bstack1llllll1_opy_ (u"ࠫࠬጡ")
bstack1l11lllll_opy_ = bstack1llllll1_opy_ (u"ࠬ࠭ጢ")
bstack1l111llll_opy_ = False
bstack1ll1lllll_opy_ = []
bstack11l1l1l1l_opy_ = bstack11ll11l1l_opy_
bstack11l11111ll_opy_ = bstack1llllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ጣ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l1l1l1l_opy_,
                    format=bstack1llllll1_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬጤ"),
                    datefmt=bstack1llllll1_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪጥ"),
                    stream=sys.stdout)
store = {
    bstack1llllll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ጦ"): []
}
def bstack1ll1ll1l_opy_():
    global CONFIG
    global bstack11l1l1l1l_opy_
    if bstack1llllll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬጧ") in CONFIG:
        bstack11l1l1l1l_opy_ = bstack1lllll11l_opy_[CONFIG[bstack1llllll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ጨ")]]
        logging.getLogger().setLevel(bstack11l1l1l1l_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l1111111_opy_ = {}
current_test_uuid = None
def bstack1llllll1l_opy_(page, bstack1ll1ll11l_opy_):
    try:
        page.evaluate(bstack1llllll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጩ"),
                      bstack1llllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪጪ") + json.dumps(
                          bstack1ll1ll11l_opy_) + bstack1llllll1_opy_ (u"ࠢࡾࡿࠥጫ"))
    except Exception as e:
        print(bstack1llllll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨጬ"), e)
def bstack11l11lll_opy_(page, message, level):
    try:
        page.evaluate(bstack1llllll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥጭ"), bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨጮ") + json.dumps(
            message) + bstack1llllll1_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧጯ") + json.dumps(level) + bstack1llllll1_opy_ (u"ࠬࢃࡽࠨጰ"))
    except Exception as e:
        print(bstack1llllll1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤጱ"), e)
def bstack1llll1ll1_opy_(page, status, message=bstack1llllll1_opy_ (u"ࠢࠣጲ")):
    try:
        if (status == bstack1llllll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣጳ")):
            page.evaluate(bstack1llllll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥጴ"),
                          bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫጵ") + json.dumps(
                              bstack1llllll1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨጶ") + str(message)) + bstack1llllll1_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩጷ") + json.dumps(status) + bstack1llllll1_opy_ (u"ࠨࡽࡾࠤጸ"))
        else:
            page.evaluate(bstack1llllll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣጹ"),
                          bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩጺ") + json.dumps(
                              status) + bstack1llllll1_opy_ (u"ࠤࢀࢁࠧጻ"))
    except Exception as e:
        print(bstack1llllll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢጼ"), e)
def pytest_configure(config):
    config.args = bstack1111l111l_opy_.bstack11l1l11l1l_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11l1111l1l_opy_ = item.config.getoption(bstack1llllll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ጽ"))
    plugins = item.config.getoption(bstack1llllll1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨጾ"))
    report = outcome.get_result()
    bstack11l111ll1l_opy_(item, call, report)
    if bstack1llllll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦጿ") not in plugins or bstack1l1lll11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1llllll1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣፀ"), None)
    page = getattr(item, bstack1llllll1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢፁ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11l111lll1_opy_(item, report, summary, bstack11l1111l1l_opy_)
    if (page is not None):
        bstack111lllll1l_opy_(item, report, summary, bstack11l1111l1l_opy_)
def bstack11l111lll1_opy_(item, report, summary, bstack11l1111l1l_opy_):
    if report.when in [bstack1llllll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣፂ"), bstack1llllll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧፃ")]:
        return
    if not bstack1l1l1ll1l1_opy_():
        return
    try:
        if (str(bstack11l1111l1l_opy_).lower() != bstack1llllll1_opy_ (u"ࠫࡹࡸࡵࡦࠩፄ")):
            item._driver.execute_script(
                bstack1llllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪፅ") + json.dumps(
                    report.nodeid) + bstack1llllll1_opy_ (u"࠭ࡽࡾࠩፆ"))
    except Exception as e:
        summary.append(
            bstack1llllll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢፇ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llllll1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥፈ")))
    bstack111111111_opy_ = bstack1llllll1_opy_ (u"ࠤࠥፉ")
    bstack11llll1l11_opy_(report)
    if not passed:
        try:
            bstack111111111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1llllll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥፊ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111111111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1llllll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨፋ")))
        bstack111111111_opy_ = bstack1llllll1_opy_ (u"ࠧࠨፌ")
        if not passed:
            try:
                bstack111111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llllll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨፍ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111111111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫፎ")
                    + json.dumps(bstack1llllll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤፏ"))
                    + bstack1llllll1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧፐ")
                )
            else:
                item._driver.execute_script(
                    bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨፑ")
                    + json.dumps(str(bstack111111111_opy_))
                    + bstack1llllll1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢፒ")
                )
        except Exception as e:
            summary.append(bstack1llllll1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥፓ").format(e))
def bstack111lllll1l_opy_(item, report, summary, bstack11l1111l1l_opy_):
    if report.when in [bstack1llllll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧፔ"), bstack1llllll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤፕ")]:
        return
    if (str(bstack11l1111l1l_opy_).lower() != bstack1llllll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ፖ")):
        bstack1llllll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llllll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦፗ")))
    bstack111111111_opy_ = bstack1llllll1_opy_ (u"ࠥࠦፘ")
    bstack11llll1l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llllll1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦፙ").format(e)
                )
        try:
            if passed:
                bstack1llll1ll1_opy_(item._page, bstack1llllll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧፚ"))
            else:
                if bstack111111111_opy_:
                    bstack11l11lll_opy_(item._page, str(bstack111111111_opy_), bstack1llllll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ፛"))
                    bstack1llll1ll1_opy_(item._page, bstack1llllll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ፜"), str(bstack111111111_opy_))
                else:
                    bstack1llll1ll1_opy_(item._page, bstack1llllll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ፝"))
        except Exception as e:
            summary.append(bstack1llllll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨ፞").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1llllll1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ፟"), default=bstack1llllll1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ፠"), help=bstack1llllll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ፡"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1llllll1_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣ።"), action=bstack1llllll1_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ፣"), default=bstack1llllll1_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ፤"),
                         help=bstack1llllll1_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ፥"))
def bstack11l111ll11_opy_(log):
    if not (log[bstack1llllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ፦")] and log[bstack1llllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ፧")].strip()):
        return
    active = bstack11l111llll_opy_()
    log = {
        bstack1llllll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ፨"): log[bstack1llllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ፩")],
        bstack1llllll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ፪"): datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"ࠨ࡜ࠪ፫"),
        bstack1llllll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ፬"): log[bstack1llllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ፭")],
    }
    if active:
        if active[bstack1llllll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ፮")] == bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ፯"):
            log[bstack1llllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭፰")] = active[bstack1llllll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፱")]
        elif active[bstack1llllll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭፲")] == bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺࠧ፳"):
            log[bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፴")] = active[bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ፵")]
    bstack1111l111l_opy_.bstack11l1ll1lll_opy_([log])
def bstack11l111llll_opy_():
    if len(store[bstack1llllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ፶")]) > 0 and store[bstack1llllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ፷")][-1]:
        return {
            bstack1llllll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ፸"): bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭፹"),
            bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ፺"): store[bstack1llllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ፻")][-1]
        }
    if store.get(bstack1llllll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ፼"), None):
        return {
            bstack1llllll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ፽"): bstack1llllll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ፾"),
            bstack1llllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፿"): store[bstack1llllll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᎀ")]
        }
    return None
bstack11l11l111l_opy_ = bstack1l1lll1lll_opy_(bstack11l111ll11_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack1111l111l_opy_.on() or bstack11l11111ll_opy_ != bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᎁ"):
            return
        global current_test_uuid, bstack11l11l111l_opy_
        bstack11l11l111l_opy_.start()
        bstack11l11l1ll1_opy_ = {
            bstack1llllll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᎂ"): uuid4().__str__(),
            bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᎃ"): datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"ࠬࡠࠧᎄ")
        }
        current_test_uuid = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᎅ")]
        store[bstack1llllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᎆ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᎇ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l1111111_opy_[item.nodeid] = {**_11l1111111_opy_[item.nodeid], **bstack11l11l1ll1_opy_}
        bstack11l111l11l_opy_(item, _11l1111111_opy_[item.nodeid], bstack1llllll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᎈ"))
    except Exception as err:
        print(bstack1llllll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬᎉ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l1l1l1111_opy_():
        atexit.register(bstack1lll1ll1l_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11llll111l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1llllll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᎊ")
    try:
        if not bstack1111l111l_opy_.on():
            return
        bstack11l11l111l_opy_.start()
        uuid = uuid4().__str__()
        bstack11l11l1ll1_opy_ = {
            bstack1llllll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᎋ"): uuid,
            bstack1llllll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᎌ"): datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"࡛ࠧࠩᎍ"),
            bstack1llllll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᎎ"): bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᎏ"),
            bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᎐"): bstack1llllll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᎑"),
            bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ᎒"): bstack1llllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ᎓")
        }
        threading.current_thread().bstack11l11l1lll_opy_ = uuid
        store[bstack1llllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᎔")] = item
        store[bstack1llllll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᎕")] = [uuid]
        if not _11l1111111_opy_.get(item.nodeid, None):
            _11l1111111_opy_[item.nodeid] = {bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᎖"): [], bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ᎗"): []}
        _11l1111111_opy_[item.nodeid][bstack1llllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᎘")].append(bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ᎙")])
        _11l1111111_opy_[item.nodeid + bstack1llllll1_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭᎚")] = bstack11l11l1ll1_opy_
        bstack11l111l111_opy_(item, bstack11l11l1ll1_opy_, bstack1llllll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᎛"))
    except Exception as err:
        print(bstack1llllll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ᎜"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack1111l111l_opy_.on():
            return
        bstack11l11l1ll1_opy_ = {
            bstack1llllll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᎝"): uuid4().__str__(),
            bstack1llllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᎞"): datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"ࠫ࡟࠭᎟"),
            bstack1llllll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᎠ"): bstack1llllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᎡ"),
            bstack1llllll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᎢ"): bstack1llllll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᎣ"),
            bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᎤ"): bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᎥ")
        }
        _11l1111111_opy_[item.nodeid + bstack1llllll1_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᎦ")] = bstack11l11l1ll1_opy_
        bstack11l111l111_opy_(item, bstack11l11l1ll1_opy_, bstack1llllll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ꭷ"))
    except Exception as err:
        print(bstack1llllll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᎨ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1111l111l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11lll1l111_opy_(fixturedef.argname):
        store[bstack1llllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭Ꭹ")] = request.node
    elif bstack11llll11l1_opy_(fixturedef.argname):
        store[bstack1llllll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭Ꭺ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1llllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᎫ"): fixturedef.argname,
            bstack1llllll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᎬ"): bstack1l1l1l1l11_opy_(outcome),
            bstack1llllll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Ꭽ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack111llll111_opy_ = store[bstack1llllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᎮ")]
        if not _11l1111111_opy_.get(bstack111llll111_opy_.nodeid, None):
            _11l1111111_opy_[bstack111llll111_opy_.nodeid] = {bstack1llllll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᎯ"): []}
        _11l1111111_opy_[bstack111llll111_opy_.nodeid][bstack1llllll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᎰ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1llllll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᎱ"), str(err))
if bstack1l1lll11l_opy_() and bstack1111l111l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l1111111_opy_[request.node.nodeid][bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᎲ")].bstack11ll11l1l1_opy_(id(step))
        except Exception as err:
            print(bstack1llllll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨᎳ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l1111111_opy_[request.node.nodeid][bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᎴ")].bstack11l1lll1l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1llllll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᎵ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11ll1111ll_opy_: bstack11ll111l1l_opy_ = _11l1111111_opy_[request.node.nodeid][bstack1llllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᎶ")]
            bstack11ll1111ll_opy_.bstack11l1lll1l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1llllll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᎷ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11l11111ll_opy_
        try:
            if not bstack1111l111l_opy_.on() or bstack11l11111ll_opy_ != bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᎸ"):
                return
            global bstack11l11l111l_opy_
            bstack11l11l111l_opy_.start()
            if not _11l1111111_opy_.get(request.node.nodeid, None):
                _11l1111111_opy_[request.node.nodeid] = {}
            bstack11ll1111ll_opy_ = bstack11ll111l1l_opy_.bstack11l1lll1ll_opy_(
                scenario, feature, request.node,
                name=bstack11lll11lll_opy_(request.node, scenario),
                bstack11ll11l11l_opy_=bstack1ll1lll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1llllll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᎹ"),
                tags=bstack11lll1l11l_opy_(feature, scenario)
            )
            _11l1111111_opy_[request.node.nodeid][bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ꮊ")] = bstack11ll1111ll_opy_
            bstack11l111l1l1_opy_(bstack11ll1111ll_opy_.uuid)
            bstack1111l111l_opy_.bstack11l1l1llll_opy_(bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᎻ"), bstack11ll1111ll_opy_)
        except Exception as err:
            print(bstack1llllll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᎼ"), str(err))
def bstack11l11l11ll_opy_(bstack11l11111l1_opy_):
    if bstack11l11111l1_opy_ in store[bstack1llllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᎽ")]:
        store[bstack1llllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᎾ")].remove(bstack11l11111l1_opy_)
def bstack11l111l1l1_opy_(bstack111lll1lll_opy_):
    store[bstack1llllll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᎿ")] = bstack111lll1lll_opy_
    threading.current_thread().current_test_uuid = bstack111lll1lll_opy_
@bstack1111l111l_opy_.bstack11l1ll1l11_opy_
def bstack11l111ll1l_opy_(item, call, report):
    global bstack11l11111ll_opy_
    try:
        if report.when == bstack1llllll1_opy_ (u"ࠩࡦࡥࡱࡲࠧᏀ"):
            bstack11l11l111l_opy_.reset()
        if report.when == bstack1llllll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᏁ"):
            if bstack11l11111ll_opy_ == bstack1llllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᏂ"):
                _11l1111111_opy_[item.nodeid][bstack1llllll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᏃ")] = bstack1l1ll11lll_opy_(report.stop)
                bstack11l111l11l_opy_(item, _11l1111111_opy_[item.nodeid], bstack1llllll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᏄ"), report, call)
                store[bstack1llllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᏅ")] = None
            elif bstack11l11111ll_opy_ == bstack1llllll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᏆ"):
                bstack11ll1111ll_opy_ = _11l1111111_opy_[item.nodeid][bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᏇ")]
                bstack11ll1111ll_opy_.set(hooks=_11l1111111_opy_[item.nodeid].get(bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᏈ"), []))
                exception, bstack1l1l11l1l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l11l1l1_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack11ll1111ll_opy_.stop(time=bstack1l1ll11lll_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1l11l1l1_opy_=bstack1l1l11l1l1_opy_))
                bstack1111l111l_opy_.bstack11l1l1llll_opy_(bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ꮙ"), _11l1111111_opy_[item.nodeid][bstack1llllll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᏊ")])
        elif report.when in [bstack1llllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᏋ"), bstack1llllll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᏌ")]:
            bstack111lll1ll1_opy_ = item.nodeid + bstack1llllll1_opy_ (u"ࠨ࠯ࠪᏍ") + report.when
            if report.skipped:
                hook_type = bstack1llllll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᏎ") if report.when == bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᏏ") else bstack1llllll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᏐ")
                _11l1111111_opy_[bstack111lll1ll1_opy_] = {
                    bstack1llllll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᏑ"): uuid4().__str__(),
                    bstack1llllll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᏒ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1llllll1_opy_ (u"࡛ࠧࠩᏓ"),
                    bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᏔ"): hook_type
                }
            _11l1111111_opy_[bstack111lll1ll1_opy_][bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᏕ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1llllll1_opy_ (u"ࠪ࡞ࠬᏖ")
            bstack11l11l11ll_opy_(_11l1111111_opy_[bstack111lll1ll1_opy_][bstack1llllll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᏗ")])
            bstack11l111l111_opy_(item, _11l1111111_opy_[bstack111lll1ll1_opy_], bstack1llllll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏘ"), report, call)
            if report.when == bstack1llllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᏙ"):
                if report.outcome == bstack1llllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᏚ"):
                    bstack11l11l1ll1_opy_ = {
                        bstack1llllll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ꮫ"): uuid4().__str__(),
                        bstack1llllll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ꮬ"): bstack1ll1lll1l_opy_(),
                        bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᏝ"): bstack1ll1lll1l_opy_()
                    }
                    _11l1111111_opy_[item.nodeid] = {**_11l1111111_opy_[item.nodeid], **bstack11l11l1ll1_opy_}
                    bstack11l111l11l_opy_(item, _11l1111111_opy_[item.nodeid], bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᏞ"))
                    bstack11l111l11l_opy_(item, _11l1111111_opy_[item.nodeid], bstack1llllll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏟ"), report, call)
    except Exception as err:
        print(bstack1llllll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᏠ"), str(err))
def bstack111llll11l_opy_(test, bstack11l11l1ll1_opy_, result=None, call=None, bstack1ll111lll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11ll1111ll_opy_ = {
        bstack1llllll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᏡ"): bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ꮲ")],
        bstack1llllll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᏣ"): bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࠨᏤ"),
        bstack1llllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏥ"): test.name,
        bstack1llllll1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᏦ"): {
            bstack1llllll1_opy_ (u"࠭࡬ࡢࡰࡪࠫᏧ"): bstack1llllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᏨ"),
            bstack1llllll1_opy_ (u"ࠨࡥࡲࡨࡪ࠭Ꮹ"): inspect.getsource(test.obj)
        },
        bstack1llllll1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ꮺ"): test.name,
        bstack1llllll1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᏫ"): test.name,
        bstack1llllll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᏬ"): bstack1111l111l_opy_.bstack11l1l1l1ll_opy_(test),
        bstack1llllll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᏭ"): file_path,
        bstack1llllll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᏮ"): file_path,
        bstack1llllll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᏯ"): bstack1llllll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᏰ"),
        bstack1llllll1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᏱ"): file_path,
        bstack1llllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᏲ"): bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᏳ")],
        bstack1llllll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᏴ"): bstack1llllll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭Ᏽ"),
        bstack1llllll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ᏶"): {
            bstack1llllll1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ᏷"): test.nodeid
        },
        bstack1llllll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᏸ"): bstack1l1l11lll1_opy_(test.own_markers)
    }
    if bstack1ll111lll_opy_ in [bstack1llllll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᏹ"), bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᏺ")]:
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠬࡳࡥࡵࡣࠪᏻ")] = {
            bstack1llllll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᏼ"): bstack11l11l1ll1_opy_.get(bstack1llllll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᏽ"), [])
        }
    if bstack1ll111lll_opy_ == bstack1llllll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ᏾"):
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᏿")] = bstack1llllll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᐀")
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᐁ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᐂ")]
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᐃ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᐄ")]
    if result:
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᐅ")] = result.outcome
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᐆ")] = result.duration * 1000
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐇ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᐈ")]
        if result.failed:
            bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᐉ")] = bstack1111l111l_opy_.bstack1l1l1lll1l_opy_(call.excinfo.typename)
            bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᐊ")] = bstack1111l111l_opy_.bstack11l11ll1ll_opy_(call.excinfo, result)
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᐋ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᐌ")]
    if outcome:
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐍ")] = bstack1l1l1l1l11_opy_(outcome)
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᐎ")] = 0
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᐏ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᐐ")]
        if bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐑ")] == bstack1llllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐒ"):
            bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᐓ")] = bstack1llllll1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᐔ")  # bstack11l1111ll1_opy_
            bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᐕ")] = [{bstack1llllll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᐖ"): [bstack1llllll1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᐗ")]}]
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᐘ")] = bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᐙ")]
    return bstack11ll1111ll_opy_
def bstack11l1111l11_opy_(test, bstack11l11l1l1l_opy_, bstack1ll111lll_opy_, result, call, outcome, bstack11l11l1111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᐚ")]
    hook_name = bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᐛ")]
    hook_data = {
        bstack1llllll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᐜ"): bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᐝ")],
        bstack1llllll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᐞ"): bstack1llllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᐟ"),
        bstack1llllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᐠ"): bstack1llllll1_opy_ (u"ࠨࡽࢀࠫᐡ").format(bstack11lll1l1ll_opy_(hook_name)),
        bstack1llllll1_opy_ (u"ࠩࡥࡳࡩࡿࠧᐢ"): {
            bstack1llllll1_opy_ (u"ࠪࡰࡦࡴࡧࠨᐣ"): bstack1llllll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᐤ"),
            bstack1llllll1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᐥ"): None
        },
        bstack1llllll1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᐦ"): test.name,
        bstack1llllll1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᐧ"): bstack1111l111l_opy_.bstack11l1l1l1ll_opy_(test, hook_name),
        bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᐨ"): file_path,
        bstack1llllll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᐩ"): file_path,
        bstack1llllll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐪ"): bstack1llllll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᐫ"),
        bstack1llllll1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᐬ"): file_path,
        bstack1llllll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᐭ"): bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᐮ")],
        bstack1llllll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᐯ"): bstack1llllll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᐰ") if bstack11l11111ll_opy_ == bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᐱ") else bstack1llllll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᐲ"),
        bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᐳ"): hook_type
    }
    bstack11l11l11l1_opy_ = bstack11l111111l_opy_(_11l1111111_opy_.get(test.nodeid, None))
    if bstack11l11l11l1_opy_:
        hook_data[bstack1llllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᐴ")] = bstack11l11l11l1_opy_
    if result:
        hook_data[bstack1llllll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᐵ")] = result.outcome
        hook_data[bstack1llllll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᐶ")] = result.duration * 1000
        hook_data[bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐷ")] = bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐸ")]
        if result.failed:
            hook_data[bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᐹ")] = bstack1111l111l_opy_.bstack1l1l1lll1l_opy_(call.excinfo.typename)
            hook_data[bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᐺ")] = bstack1111l111l_opy_.bstack11l11ll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1llllll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐻ")] = bstack1l1l1l1l11_opy_(outcome)
        hook_data[bstack1llllll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᐼ")] = 100
        hook_data[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐽ")] = bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐾ")]
        if hook_data[bstack1llllll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐿ")] == bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᑀ"):
            hook_data[bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᑁ")] = bstack1llllll1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᑂ")  # bstack11l1111ll1_opy_
            hook_data[bstack1llllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᑃ")] = [{bstack1llllll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑄ"): [bstack1llllll1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᑅ")]}]
    if bstack11l11l1111_opy_:
        hook_data[bstack1llllll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᑆ")] = bstack11l11l1111_opy_.result
        hook_data[bstack1llllll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᑇ")] = bstack1l1ll11l1l_opy_(bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᑈ")], bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᑉ")])
        hook_data[bstack1llllll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᑊ")] = bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᑋ")]
        if hook_data[bstack1llllll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᑌ")] == bstack1llllll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᑍ"):
            hook_data[bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᑎ")] = bstack1111l111l_opy_.bstack1l1l1lll1l_opy_(bstack11l11l1111_opy_.exception_type)
            hook_data[bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᑏ")] = [{bstack1llllll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᑐ"): bstack1l1ll11111_opy_(bstack11l11l1111_opy_.exception)}]
    return hook_data
def bstack11l111l11l_opy_(test, bstack11l11l1ll1_opy_, bstack1ll111lll_opy_, result=None, call=None, outcome=None):
    bstack11ll1111ll_opy_ = bstack111llll11l_opy_(test, bstack11l11l1ll1_opy_, result, call, bstack1ll111lll_opy_, outcome)
    driver = getattr(test, bstack1llllll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᑑ"), None)
    if bstack1ll111lll_opy_ == bstack1llllll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᑒ") and driver:
        bstack11ll1111ll_opy_[bstack1llllll1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᑓ")] = bstack1111l111l_opy_.bstack11l1l11ll1_opy_(driver)
    if bstack1ll111lll_opy_ == bstack1llllll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᑔ"):
        bstack1ll111lll_opy_ = bstack1llllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑕ")
    bstack11l1ll111l_opy_ = {
        bstack1llllll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᑖ"): bstack1ll111lll_opy_,
        bstack1llllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᑗ"): bstack11ll1111ll_opy_
    }
    bstack1111l111l_opy_.bstack11l1l111l1_opy_(bstack11l1ll111l_opy_)
def bstack11l111l111_opy_(test, bstack11l11l1ll1_opy_, bstack1ll111lll_opy_, result=None, call=None, outcome=None, bstack11l11l1111_opy_=None):
    hook_data = bstack11l1111l11_opy_(test, bstack11l11l1ll1_opy_, bstack1ll111lll_opy_, result, call, outcome, bstack11l11l1111_opy_)
    bstack11l1ll111l_opy_ = {
        bstack1llllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᑘ"): bstack1ll111lll_opy_,
        bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᑙ"): hook_data
    }
    bstack1111l111l_opy_.bstack11l1l111l1_opy_(bstack11l1ll111l_opy_)
def bstack11l111111l_opy_(bstack11l11l1ll1_opy_):
    if not bstack11l11l1ll1_opy_:
        return None
    if bstack11l11l1ll1_opy_.get(bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᑚ"), None):
        return getattr(bstack11l11l1ll1_opy_[bstack1llllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᑛ")], bstack1llllll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᑜ"), None)
    return bstack11l11l1ll1_opy_.get(bstack1llllll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᑝ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1111l111l_opy_.on():
            return
        places = [bstack1llllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᑞ"), bstack1llllll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᑟ"), bstack1llllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑠ")]
        bstack11l11ll1l1_opy_ = []
        for bstack11l1111lll_opy_ in places:
            records = caplog.get_records(bstack11l1111lll_opy_)
            bstack111llll1l1_opy_ = bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑡ") if bstack11l1111lll_opy_ == bstack1llllll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᑢ") else bstack1llllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑣ")
            bstack111llll1ll_opy_ = request.node.nodeid + (bstack1llllll1_opy_ (u"ࠬ࠭ᑤ") if bstack11l1111lll_opy_ == bstack1llllll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᑥ") else bstack1llllll1_opy_ (u"ࠧ࠮ࠩᑦ") + bstack11l1111lll_opy_)
            bstack111lll1lll_opy_ = bstack11l111111l_opy_(_11l1111111_opy_.get(bstack111llll1ll_opy_, None))
            if not bstack111lll1lll_opy_:
                continue
            for record in records:
                if bstack1l1l11ll11_opy_(record.message):
                    continue
                bstack11l11ll1l1_opy_.append({
                    bstack1llllll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᑧ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1llllll1_opy_ (u"ࠩ࡝ࠫᑨ"),
                    bstack1llllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᑩ"): record.levelname,
                    bstack1llllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑪ"): record.message,
                    bstack111llll1l1_opy_: bstack111lll1lll_opy_
                })
        if len(bstack11l11ll1l1_opy_) > 0:
            bstack1111l111l_opy_.bstack11l1ll1lll_opy_(bstack11l11ll1l1_opy_)
    except Exception as err:
        print(bstack1llllll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᑫ"), str(err))
def bstack11l11ll111_opy_(driver_command, response):
    if driver_command == bstack1llllll1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᑬ"):
        bstack1111l111l_opy_.bstack11l1l1l11l_opy_({
            bstack1llllll1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᑭ"): response[bstack1llllll1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᑮ")],
            bstack1llllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑯ"): store[bstack1llllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᑰ")]
        })
def bstack1lll1ll1l_opy_():
    global bstack1ll1lllll_opy_
    bstack1111l111l_opy_.bstack11l11llll1_opy_()
    for driver in bstack1ll1lllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l1111l1_opy_(self, *args, **kwargs):
    bstack1l1lllll1_opy_ = bstack1lll11l11l_opy_(self, *args, **kwargs)
    bstack1111l111l_opy_.bstack111ll11ll_opy_(self)
    return bstack1l1lllll1_opy_
def bstack1lll11111_opy_(framework_name):
    global bstack1ll1l1l1l_opy_
    global bstack1ll1l111ll_opy_
    bstack1ll1l1l1l_opy_ = framework_name
    logger.info(bstack1ll1l11l1_opy_.format(bstack1ll1l1l1l_opy_.split(bstack1llllll1_opy_ (u"ࠫ࠲࠭ᑱ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l1ll1l1_opy_():
            Service.start = bstack11lll1l11_opy_
            Service.stop = bstack1l1111lll_opy_
            webdriver.Remote.__init__ = bstack1l11111l1_opy_
            webdriver.Remote.get = bstack1lll1llll1_opy_
            if not isinstance(os.getenv(bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᑲ")), str):
                return
            WebDriver.close = bstack1ll1l1ll1l_opy_
            WebDriver.quit = bstack1l1llll11_opy_
        if not bstack1l1l1ll1l1_opy_() and bstack1111l111l_opy_.on():
            webdriver.Remote.__init__ = bstack11l1111l1_opy_
        bstack1ll1l111ll_opy_ = True
    except Exception as e:
        pass
    bstack1llllll11l_opy_()
    if os.environ.get(bstack1llllll1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᑳ")):
        bstack1ll1l111ll_opy_ = eval(os.environ.get(bstack1llllll1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᑴ")))
    if not bstack1ll1l111ll_opy_:
        bstack1l1l11l11_opy_(bstack1llllll1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᑵ"), bstack111lllll1_opy_)
    if bstack1ll11l1l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l111l11_opy_
        except Exception as e:
            logger.error(bstack1llll1ll_opy_.format(str(e)))
    if bstack1llllll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᑶ") in str(framework_name).lower():
        if not bstack1l1l1ll1l1_opy_():
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
def bstack1l1llll11_opy_(self):
    global bstack1ll1l1l1l_opy_
    global bstack11l1lll11_opy_
    global bstack1llll1l11l_opy_
    try:
        if bstack1llllll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᑷ") in bstack1ll1l1l1l_opy_ and self.session_id != None and bstack1lll1l1lll_opy_(threading.current_thread(), bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᑸ"), bstack1llllll1_opy_ (u"ࠬ࠭ᑹ")) != bstack1llllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑺ"):
            bstack1ll1l11l11_opy_ = bstack1llllll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑻ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑼ")
            bstack11ll1111_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᑽ"), bstack1llllll1_opy_ (u"ࠪࠫᑾ"), bstack1ll1l11l11_opy_, bstack1llllll1_opy_ (u"ࠫ࠱ࠦࠧᑿ").join(
                threading.current_thread().bstackTestErrorMessages), bstack1llllll1_opy_ (u"ࠬ࠭ᒀ"), bstack1llllll1_opy_ (u"࠭ࠧᒁ"))
            if self != None:
                self.execute_script(bstack11ll1111_opy_)
    except Exception as e:
        logger.debug(bstack1llllll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣᒂ") + str(e))
    bstack1llll1l11l_opy_(self)
    self.session_id = None
def bstack1l11111l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l1lll11_opy_
    global bstack1ll1llll11_opy_
    global bstack1l111llll_opy_
    global bstack1ll1l1l1l_opy_
    global bstack1lll11l11l_opy_
    global bstack1ll1lllll_opy_
    global bstack1llll1l1l1_opy_
    global bstack1l11lllll_opy_
    CONFIG[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᒃ")] = str(bstack1ll1l1l1l_opy_) + str(__version__)
    command_executor = bstack1l11ll11_opy_(bstack1llll1l1l1_opy_)
    logger.debug(bstack1ll11l1ll_opy_.format(command_executor))
    proxy = bstack1l1ll1l1_opy_(CONFIG, proxy)
    bstack1111l11l_opy_ = 0
    try:
        if bstack1l111llll_opy_ is True:
            bstack1111l11l_opy_ = int(os.environ.get(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒄ")))
    except:
        bstack1111l11l_opy_ = 0
    bstack11l1l11l1_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1111l11l_opy_)
    logger.debug(bstack1111llll1_opy_.format(str(bstack11l1l11l1_opy_)))
    if bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᒅ") in CONFIG and CONFIG[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᒆ")]:
        bstack1ll1llll1l_opy_(bstack11l1l11l1_opy_, bstack1l11lllll_opy_)
    if desired_capabilities:
        bstack1lll1lll1l_opy_ = bstack111lll1l_opy_(desired_capabilities)
        bstack1lll1lll1l_opy_[bstack1llllll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᒇ")] = bstack111l1ll11_opy_(CONFIG)
        bstack1ll11l1l1l_opy_ = bstack1l1ll111l_opy_(bstack1lll1lll1l_opy_)
        if bstack1ll11l1l1l_opy_:
            bstack11l1l11l1_opy_ = update(bstack1ll11l1l1l_opy_, bstack11l1l11l1_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l1ll1_opy_(options, bstack11l1l11l1_opy_)
    if not options:
        options = bstack1lll1ll1ll_opy_(bstack11l1l11l1_opy_)
    if proxy and bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᒈ")):
        options.proxy(proxy)
    if options and bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᒉ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l111ll11_opy_() < version.parse(bstack1llllll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᒊ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1l11l1_opy_)
    logger.info(bstack1l11111ll_opy_)
    if bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᒋ")):
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᒌ")):
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᒍ")):
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
        bstack11lll1ll1_opy_ = bstack1llllll1_opy_ (u"ࠬ࠭ᒎ")
        if bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧᒏ")):
            bstack11lll1ll1_opy_ = self.caps.get(bstack1llllll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᒐ"))
        else:
            bstack11lll1ll1_opy_ = self.capabilities.get(bstack1llllll1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᒑ"))
        if bstack11lll1ll1_opy_:
            if bstack1l111ll11_opy_() <= version.parse(bstack1llllll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᒒ")):
                self.command_executor._url = bstack1llllll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᒓ") + bstack1llll1l1l1_opy_ + bstack1llllll1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᒔ")
            else:
                self.command_executor._url = bstack1llllll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᒕ") + bstack11lll1ll1_opy_ + bstack1llllll1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᒖ")
            logger.debug(bstack11111lll1_opy_.format(bstack11lll1ll1_opy_))
        else:
            logger.debug(bstack11l11l11_opy_.format(bstack1llllll1_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᒗ")))
    except Exception as e:
        logger.debug(bstack11l11l11_opy_.format(e))
    bstack11l1lll11_opy_ = self.session_id
    if bstack1llllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᒘ") in bstack1ll1l1l1l_opy_:
        threading.current_thread().bstack1l11l11l_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1111l111l_opy_.bstack111ll11ll_opy_(self)
    bstack1ll1lllll_opy_.append(self)
    if bstack1llllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᒙ") in CONFIG and bstack1llllll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒚ") in CONFIG[bstack1llllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᒛ")][bstack1111l11l_opy_]:
        bstack1ll1llll11_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᒜ")][bstack1111l11l_opy_][bstack1llllll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᒝ")]
    logger.debug(bstack1ll1ll1111_opy_.format(bstack11l1lll11_opy_))
def bstack1lll1llll1_opy_(self, url):
    global bstack11ll11lll_opy_
    global CONFIG
    try:
        bstack1l11l1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll1lllll_opy_.format(str(err)))
    try:
        bstack11ll11lll_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll11l11_opy_ = str(e)
            if any(err_msg in bstack1lll11l11_opy_ for err_msg in bstack1ll11l11_opy_):
                bstack1l11l1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll1lllll_opy_.format(str(err)))
        raise e
def bstack11111llll_opy_(item, when):
    global bstack11lll11l_opy_
    try:
        bstack11lll11l_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll111ll_opy_(item, call, rep):
    global bstack11lll1lll_opy_
    global bstack1ll1lllll_opy_
    name = bstack1llllll1_opy_ (u"ࠧࠨᒞ")
    try:
        if rep.when == bstack1llllll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᒟ"):
            bstack11l1lll11_opy_ = threading.current_thread().bstack1l11l11l_opy_
            bstack11l1111l1l_opy_ = item.config.getoption(bstack1llllll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᒠ"))
            try:
                if (str(bstack11l1111l1l_opy_).lower() != bstack1llllll1_opy_ (u"ࠪࡸࡷࡻࡥࠨᒡ")):
                    name = str(rep.nodeid)
                    bstack11ll1111_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᒢ"), name, bstack1llllll1_opy_ (u"ࠬ࠭ᒣ"), bstack1llllll1_opy_ (u"࠭ࠧᒤ"), bstack1llllll1_opy_ (u"ࠧࠨᒥ"), bstack1llllll1_opy_ (u"ࠨࠩᒦ"))
                    for driver in bstack1ll1lllll_opy_:
                        if bstack11l1lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1111_opy_)
            except Exception as e:
                logger.debug(bstack1llllll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᒧ").format(str(e)))
            try:
                bstack1lllllll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1llllll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒨ"):
                    status = bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒩ") if rep.outcome.lower() == bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒪ") else bstack1llllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᒫ")
                    reason = bstack1llllll1_opy_ (u"ࠧࠨᒬ")
                    if status == bstack1llllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒭ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1llllll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᒮ") if status == bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᒯ") else bstack1llllll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᒰ")
                    data = name + bstack1llllll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᒱ") if status == bstack1llllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᒲ") else name + bstack1llllll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᒳ") + reason
                    bstack1ll11ll11_opy_ = bstack1l1lll111_opy_(bstack1llllll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᒴ"), bstack1llllll1_opy_ (u"ࠩࠪᒵ"), bstack1llllll1_opy_ (u"ࠪࠫᒶ"), bstack1llllll1_opy_ (u"ࠫࠬᒷ"), level, data)
                    for driver in bstack1ll1lllll_opy_:
                        if bstack11l1lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11ll11_opy_)
            except Exception as e:
                logger.debug(bstack1llllll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᒸ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1llllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᒹ").format(str(e)))
    bstack11lll1lll_opy_(item, call, rep)
notset = Notset()
def bstack1111lll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11111ll11_opy_
    if str(name).lower() == bstack1llllll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᒺ"):
        return bstack1llllll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᒻ")
    else:
        return bstack11111ll11_opy_(self, name, default, skip)
def bstack1l111l11_opy_(self):
    global CONFIG
    global bstack1lll1lll_opy_
    try:
        proxy = bstack1llll1llll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1llllll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᒼ")):
                proxies = bstack1lll11ll_opy_(proxy, bstack1l11ll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1l1l11_opy_ = proxies.popitem()
                    if bstack1llllll1_opy_ (u"ࠥ࠾࠴࠵ࠢᒽ") in bstack1ll1l1l11_opy_:
                        return bstack1ll1l1l11_opy_
                    else:
                        return bstack1llllll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᒾ") + bstack1ll1l1l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1llllll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᒿ").format(str(e)))
    return bstack1lll1lll_opy_(self)
def bstack1ll11l1l11_opy_():
    return bstack1llllll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᓀ") in CONFIG or bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᓁ") in CONFIG and bstack1l111ll11_opy_() >= version.parse(
        bstack1lll1llll_opy_)
def bstack11ll11ll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1llll11_opy_
    global bstack1l111llll_opy_
    global bstack1ll1l1l1l_opy_
    CONFIG[bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᓂ")] = str(bstack1ll1l1l1l_opy_) + str(__version__)
    bstack1111l11l_opy_ = 0
    try:
        if bstack1l111llll_opy_ is True:
            bstack1111l11l_opy_ = int(os.environ.get(bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᓃ")))
    except:
        bstack1111l11l_opy_ = 0
    CONFIG[bstack1llllll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᓄ")] = True
    bstack11l1l11l1_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1111l11l_opy_)
    logger.debug(bstack1111llll1_opy_.format(str(bstack11l1l11l1_opy_)))
    if CONFIG.get(bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᓅ")):
        bstack1ll1llll1l_opy_(bstack11l1l11l1_opy_, bstack1l11lllll_opy_)
    if bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᓆ") in CONFIG and bstack1llllll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᓇ") in CONFIG[bstack1llllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᓈ")][bstack1111l11l_opy_]:
        bstack1ll1llll11_opy_ = CONFIG[bstack1llllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᓉ")][bstack1111l11l_opy_][bstack1llllll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᓊ")]
    import urllib
    import json
    bstack11lll1111_opy_ = bstack1llllll1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᓋ") + urllib.parse.quote(json.dumps(bstack11l1l11l1_opy_))
    browser = self.connect(bstack11lll1111_opy_)
    return browser
def bstack1llllll11l_opy_():
    global bstack1ll1l111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11ll11ll_opy_
        bstack1ll1l111ll_opy_ = True
    except Exception as e:
        pass
def bstack111lllllll_opy_():
    global CONFIG
    global bstack1l1l11l1l_opy_
    global bstack1llll1l1l1_opy_
    global bstack1l11lllll_opy_
    global bstack1l111llll_opy_
    CONFIG = json.loads(os.environ.get(bstack1llllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᓌ")))
    bstack1l1l11l1l_opy_ = eval(os.environ.get(bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᓍ")))
    bstack1llll1l1l1_opy_ = os.environ.get(bstack1llllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᓎ"))
    bstack1lllllll1l_opy_(CONFIG, bstack1l1l11l1l_opy_)
    bstack1ll1ll1l_opy_()
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
    if bstack1llllll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᓏ") in CONFIG or bstack1llllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᓐ") in CONFIG:
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
        logger.debug(bstack1llllll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᓑ"))
    bstack1l11lllll_opy_ = CONFIG.get(bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᓒ"), {}).get(bstack1llllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᓓ"))
    bstack1l111llll_opy_ = True
    bstack1lll11111_opy_(bstack1llllll1ll_opy_)
if (bstack1l1l1l1111_opy_()):
    bstack111lllllll_opy_()
@bstack1l1ll1l11l_opy_(class_method=False)
def bstack11l11l1l11_opy_(hook_name, event, bstack111llllll1_opy_=None):
    if hook_name not in [bstack1llllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᓔ"), bstack1llllll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᓕ"), bstack1llllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᓖ"), bstack1llllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᓗ"), bstack1llllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᓘ"), bstack1llllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᓙ"), bstack1llllll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᓚ"), bstack1llllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᓛ")]:
        return
    node = store[bstack1llllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᓜ")]
    if hook_name in [bstack1llllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᓝ"), bstack1llllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᓞ")]:
        node = store[bstack1llllll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᓟ")]
    elif hook_name in [bstack1llllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᓠ"), bstack1llllll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᓡ")]:
        node = store[bstack1llllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᓢ")]
    if event == bstack1llllll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᓣ"):
        hook_type = bstack11llll1111_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l11l1l1l_opy_ = {
            bstack1llllll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᓤ"): uuid,
            bstack1llllll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᓥ"): bstack1ll1lll1l_opy_(),
            bstack1llllll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᓦ"): bstack1llllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᓧ"),
            bstack1llllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᓨ"): hook_type,
            bstack1llllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᓩ"): hook_name
        }
        store[bstack1llllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᓪ")].append(uuid)
        bstack111lllll11_opy_ = node.nodeid
        if hook_type == bstack1llllll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᓫ"):
            if not _11l1111111_opy_.get(bstack111lllll11_opy_, None):
                _11l1111111_opy_[bstack111lllll11_opy_] = {bstack1llllll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᓬ"): []}
            _11l1111111_opy_[bstack111lllll11_opy_][bstack1llllll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᓭ")].append(bstack11l11l1l1l_opy_[bstack1llllll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᓮ")])
        _11l1111111_opy_[bstack111lllll11_opy_ + bstack1llllll1_opy_ (u"ࠫ࠲࠭ᓯ") + hook_name] = bstack11l11l1l1l_opy_
        bstack11l111l111_opy_(node, bstack11l11l1l1l_opy_, bstack1llllll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᓰ"))
    elif event == bstack1llllll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᓱ"):
        bstack111lll1ll1_opy_ = node.nodeid + bstack1llllll1_opy_ (u"ࠧ࠮ࠩᓲ") + hook_name
        _11l1111111_opy_[bstack111lll1ll1_opy_][bstack1llllll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓳ")] = bstack1ll1lll1l_opy_()
        bstack11l11l11ll_opy_(_11l1111111_opy_[bstack111lll1ll1_opy_][bstack1llllll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓴ")])
        bstack11l111l111_opy_(node, _11l1111111_opy_[bstack111lll1ll1_opy_], bstack1llllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓵ"), bstack11l11l1111_opy_=bstack111llllll1_opy_)
def bstack11l111l1ll_opy_():
    global bstack11l11111ll_opy_
    if bstack1l1lll11l_opy_():
        bstack11l11111ll_opy_ = bstack1llllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᓶ")
    else:
        bstack11l11111ll_opy_ = bstack1llllll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᓷ")
@bstack1111l111l_opy_.bstack11l1ll1l11_opy_
def bstack11l11ll11l_opy_():
    bstack11l111l1ll_opy_()
    if bstack1l1l1l1ll1_opy_():
        bstack11ll1ll111_opy_(bstack11l11ll111_opy_)
    bstack1l11lllll1_opy_ = bstack1l11lll111_opy_(bstack11l11l1l11_opy_)
bstack11l11ll11l_opy_()