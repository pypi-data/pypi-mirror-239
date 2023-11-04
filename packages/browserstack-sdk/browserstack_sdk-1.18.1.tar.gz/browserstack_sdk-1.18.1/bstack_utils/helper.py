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
import os
import re
import subprocess
import traceback
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l1ll1lll1_opy_, bstack11l1ll11_opy_, bstack1l1l11l1_opy_, bstack1ll1l111l1_opy_
from bstack_utils.messages import bstack11111l1ll_opy_
from bstack_utils.proxy import bstack1ll11lll1l_opy_
bstack1l11l11l1_opy_ = Config.get_instance()
def bstack1l1lllll11_opy_(config):
    return config[bstack1llllll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩཬ")]
def bstack1l1llll1ll_opy_(config):
    return config[bstack1llllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ཭")]
def bstack1l1l11l11l_opy_(obj):
    values = []
    bstack1l1ll111l1_opy_ = re.compile(bstack1llllll1_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ཮"), re.I)
    for key in obj.keys():
        if bstack1l1ll111l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l1l1ll111_opy_(config):
    tags = []
    tags.extend(bstack1l1l11l11l_opy_(os.environ))
    tags.extend(bstack1l1l11l11l_opy_(config))
    return tags
def bstack1l1l11lll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l1l1l1l1l_opy_(bstack1l1ll11l11_opy_):
    if not bstack1l1ll11l11_opy_:
        return bstack1llllll1_opy_ (u"ࠪࠫ཯")
    return bstack1llllll1_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧ཰").format(bstack1l1ll11l11_opy_.name, bstack1l1ll11l11_opy_.email)
def bstack1ll111111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l1l1ll11l_opy_ = repo.common_dir
        info = {
            bstack1llllll1_opy_ (u"ࠧࡹࡨࡢࠤཱ"): repo.head.commit.hexsha,
            bstack1llllll1_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤི"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1llllll1_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ཱིࠢ"): repo.active_branch.name,
            bstack1llllll1_opy_ (u"ࠣࡶࡤ࡫ུࠧ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1llllll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶཱུࠧ"): bstack1l1l1l1l1l_opy_(repo.head.commit.committer),
            bstack1llllll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦྲྀ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1llllll1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦཷ"): bstack1l1l1l1l1l_opy_(repo.head.commit.author),
            bstack1llllll1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥླྀ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1llllll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢཹ"): repo.head.commit.message,
            bstack1llllll1_opy_ (u"ࠢࡳࡱࡲࡸེࠧ"): repo.git.rev_parse(bstack1llllll1_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ཻࠥ")),
            bstack1llllll1_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴོࠥ"): bstack1l1l1ll11l_opy_,
            bstack1llllll1_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨཽ"): subprocess.check_output([bstack1llllll1_opy_ (u"ࠦ࡬࡯ࡴࠣཾ"), bstack1llllll1_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣཿ"), bstack1llllll1_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤྀ")]).strip().decode(
                bstack1llllll1_opy_ (u"ࠧࡶࡶࡩ࠱࠽ཱྀ࠭")),
            bstack1llllll1_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥྂ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1llllll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦྃ"): repo.git.rev_list(
                bstack1llllll1_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿ྄ࠥ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l1l11llll_opy_ = []
        for remote in remotes:
            bstack1l1l111ll1_opy_ = {
                bstack1llllll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ྅"): remote.name,
                bstack1llllll1_opy_ (u"ࠧࡻࡲ࡭ࠤ྆"): remote.url,
            }
            bstack1l1l11llll_opy_.append(bstack1l1l111ll1_opy_)
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ྇"): bstack1llllll1_opy_ (u"ࠢࡨ࡫ࡷࠦྈ"),
            **info,
            bstack1llllll1_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤྉ"): bstack1l1l11llll_opy_
        }
    except Exception as err:
        print(bstack1llllll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧྊ").format(err))
        return {}
def bstack1ll1l1l11l_opy_():
    env = os.environ
    if (bstack1llllll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣྋ") in env and len(env[bstack1llllll1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤྌ")]) > 0) or (
            bstack1llllll1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦྍ") in env and len(env[bstack1llllll1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧྎ")]) > 0):
        return {
            bstack1llllll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྏ"): bstack1llllll1_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤྐ"),
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧྑ"): env.get(bstack1llllll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨྒ")),
            bstack1llllll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨྒྷ"): env.get(bstack1llllll1_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢྔ")),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧྕ"): env.get(bstack1llllll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨྖ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠣࡅࡌࠦྗ")) == bstack1llllll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ྘") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧྙ"))):
        return {
            bstack1llllll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤྚ"): bstack1llllll1_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢྛ"),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤྜ"): env.get(bstack1llllll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥྜྷ")),
            bstack1llllll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥྞ"): env.get(bstack1llllll1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨྟ")),
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤྠ"): env.get(bstack1llllll1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢྡ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠧࡉࡉࠣྡྷ")) == bstack1llllll1_opy_ (u"ࠨࡴࡳࡷࡨࠦྣ") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢྤ"))):
        return {
            bstack1llllll1_opy_ (u"ࠣࡰࡤࡱࡪࠨྥ"): bstack1llllll1_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧྦ"),
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨྦྷ"): env.get(bstack1llllll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦྨ")),
            bstack1llllll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢྩ"): env.get(bstack1llllll1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣྪ")),
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྫ"): env.get(bstack1llllll1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢྫྷ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠤࡆࡍࠧྭ")) == bstack1llllll1_opy_ (u"ࠥࡸࡷࡻࡥࠣྮ") and env.get(bstack1llllll1_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧྯ")) == bstack1llllll1_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢྰ"):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦྱ"): bstack1llllll1_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤྲ"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦླ"): None,
            bstack1llllll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦྴ"): None,
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤྵ"): None
        }
    if env.get(bstack1llllll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢྶ")) and env.get(bstack1llllll1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣྷ")):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦྸ"): bstack1llllll1_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥྐྵ"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦྺ"): env.get(bstack1llllll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢྻ")),
            bstack1llllll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧྼ"): None,
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ྽"): env.get(bstack1llllll1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ྾"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠨࡃࡊࠤ྿")) == bstack1llllll1_opy_ (u"ࠢࡵࡴࡸࡩࠧ࿀") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢ࿁"))):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿂"): bstack1llllll1_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤ࿃"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ࿄"): env.get(bstack1llllll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣ࿅")),
            bstack1llllll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ࿆ࠣ"): None,
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ࿇"): env.get(bstack1llllll1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ࿈"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠤࡆࡍࠧ࿉")) == bstack1llllll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ࿊") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢ࿋"))):
        return {
            bstack1llllll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ࿌"): bstack1llllll1_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤ࿍"),
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ࿎"): env.get(bstack1llllll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢ࿏")),
            bstack1llllll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ࿐"): env.get(bstack1llllll1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ࿑")),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ࿒"): env.get(bstack1llllll1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣ࿓"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠨࡃࡊࠤ࿔")) == bstack1llllll1_opy_ (u"ࠢࡵࡴࡸࡩࠧ࿕") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦ࿖"))):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿗"): bstack1llllll1_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥ࿘"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ࿙"): env.get(bstack1llllll1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤ࿚")),
            bstack1llllll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ࿛"): env.get(bstack1llllll1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ࿜")),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ࿝"): env.get(bstack1llllll1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧ࿞"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠥࡇࡎࠨ࿟")) == bstack1llllll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ࿠") and bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣ࿡"))):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿢"): bstack1llllll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥ࿣"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ࿤"): env.get(bstack1llllll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ࿥")),
            bstack1llllll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ࿦"): env.get(bstack1llllll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨ࿧")) or env.get(bstack1llllll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ࿨")),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ࿩"): env.get(bstack1llllll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ࿪"))
        }
    if bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ࿫"))):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿬"): bstack1llllll1_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥ࿭"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ࿮"): bstack1llllll1_opy_ (u"ࠧࢁࡽࡼࡿࠥ࿯").format(env.get(bstack1llllll1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ࿰")), env.get(bstack1llllll1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧ࿱"))),
            bstack1llllll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ࿲"): env.get(bstack1llllll1_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣ࿳")),
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ࿴"): env.get(bstack1llllll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ࿵"))
        }
    if bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢ࿶"))):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿷"): bstack1llllll1_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤ࿸"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ࿹"): bstack1llllll1_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣ࿺").format(env.get(bstack1llllll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩ࿻")), env.get(bstack1llllll1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬ࿼")), env.get(bstack1llllll1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭࿽")), env.get(bstack1llllll1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࿾"))),
            bstack1llllll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ࿿"): env.get(bstack1llllll1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧက")),
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣခ"): env.get(bstack1llllll1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦဂ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧဃ")) and env.get(bstack1llllll1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢင")):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦစ"): bstack1llllll1_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤဆ"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦဇ"): bstack1llllll1_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧဈ").format(env.get(bstack1llllll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ဉ")), env.get(bstack1llllll1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩည")), env.get(bstack1llllll1_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬဋ"))),
            bstack1llllll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣဌ"): env.get(bstack1llllll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢဍ")),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢဎ"): env.get(bstack1llllll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤဏ"))
        }
    if any([env.get(bstack1llllll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣတ")), env.get(bstack1llllll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥထ")), env.get(bstack1llllll1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤဒ"))]):
        return {
            bstack1llllll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦဓ"): bstack1llllll1_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢန"),
            bstack1llllll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦပ"): env.get(bstack1llllll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣဖ")),
            bstack1llllll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧဗ"): env.get(bstack1llllll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤဘ")),
            bstack1llllll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦမ"): env.get(bstack1llllll1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦယ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧရ")):
        return {
            bstack1llllll1_opy_ (u"ࠣࡰࡤࡱࡪࠨလ"): bstack1llllll1_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤဝ"),
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨသ"): env.get(bstack1llllll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨဟ")),
            bstack1llllll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢဠ"): env.get(bstack1llllll1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧအ")),
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨဢ"): env.get(bstack1llllll1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨဣ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥဤ")) or env.get(bstack1llllll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧဥ")):
        return {
            bstack1llllll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤဦ"): bstack1llllll1_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨဧ"),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤဨ"): env.get(bstack1llllll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦဩ")),
            bstack1llllll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥဪ"): bstack1llllll1_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤါ") if env.get(bstack1llllll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧာ")) else None,
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥိ"): env.get(bstack1llllll1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥီ"))
        }
    if any([env.get(bstack1llllll1_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦု")), env.get(bstack1llllll1_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣူ")), env.get(bstack1llllll1_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣေ"))]):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢဲ"): bstack1llllll1_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤဳ"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢဴ"): None,
            bstack1llllll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢဵ"): env.get(bstack1llllll1_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥံ")),
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ့"): env.get(bstack1llllll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥး"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉ္ࠧ")):
        return {
            bstack1llllll1_opy_ (u"ࠥࡲࡦࡳࡥ်ࠣ"): bstack1llllll1_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢျ"),
            bstack1llllll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣြ"): env.get(bstack1llllll1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧွ")),
            bstack1llllll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤှ"): bstack1llllll1_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤဿ").format(env.get(bstack1llllll1_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬ၀"))) if env.get(bstack1llllll1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨ၁")) else None,
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ၂"): env.get(bstack1llllll1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ၃"))
        }
    if bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ၄"))):
        return {
            bstack1llllll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ၅"): bstack1llllll1_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ၆"),
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ၇"): env.get(bstack1llllll1_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ၈")),
            bstack1llllll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ၉"): env.get(bstack1llllll1_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ၊")),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ။"): env.get(bstack1llllll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ၌"))
        }
    if bstack1l1l1ll1ll_opy_(env.get(bstack1llllll1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤ၍"))):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ၎"): bstack1llllll1_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ၏"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢၐ"): bstack1llllll1_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨၑ").format(env.get(bstack1llllll1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪၒ")), env.get(bstack1llllll1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫၓ")), env.get(bstack1llllll1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨၔ"))),
            bstack1llllll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦၕ"): env.get(bstack1llllll1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧၖ")),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥၗ"): env.get(bstack1llllll1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧၘ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠨࡃࡊࠤၙ")) == bstack1llllll1_opy_ (u"ࠢࡵࡴࡸࡩࠧၚ") and env.get(bstack1llllll1_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣၛ")) == bstack1llllll1_opy_ (u"ࠤ࠴ࠦၜ"):
        return {
            bstack1llllll1_opy_ (u"ࠥࡲࡦࡳࡥࠣၝ"): bstack1llllll1_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦၞ"),
            bstack1llllll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣၟ"): bstack1llllll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤၠ").format(env.get(bstack1llllll1_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫၡ"))),
            bstack1llllll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥၢ"): None,
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣၣ"): None,
        }
    if env.get(bstack1llllll1_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨၤ")):
        return {
            bstack1llllll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤၥ"): bstack1llllll1_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢၦ"),
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤၧ"): None,
            bstack1llllll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤၨ"): env.get(bstack1llllll1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤၩ")),
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣၪ"): env.get(bstack1llllll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤၫ"))
        }
    if any([env.get(bstack1llllll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢၬ")), env.get(bstack1llllll1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧၭ")), env.get(bstack1llllll1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦၮ")), env.get(bstack1llllll1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣၯ"))]):
        return {
            bstack1llllll1_opy_ (u"ࠣࡰࡤࡱࡪࠨၰ"): bstack1llllll1_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧၱ"),
            bstack1llllll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨၲ"): None,
            bstack1llllll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨၳ"): env.get(bstack1llllll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨၴ")) or None,
            bstack1llllll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧၵ"): env.get(bstack1llllll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤၶ"), 0)
        }
    if env.get(bstack1llllll1_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨၷ")):
        return {
            bstack1llllll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢၸ"): bstack1llllll1_opy_ (u"ࠥࡋࡴࡉࡄࠣၹ"),
            bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢၺ"): None,
            bstack1llllll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢၻ"): env.get(bstack1llllll1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦၼ")),
            bstack1llllll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨၽ"): env.get(bstack1llllll1_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢၾ"))
        }
    if env.get(bstack1llllll1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢၿ")):
        return {
            bstack1llllll1_opy_ (u"ࠥࡲࡦࡳࡥࠣႀ"): bstack1llllll1_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢႁ"),
            bstack1llllll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣႂ"): env.get(bstack1llllll1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧႃ")),
            bstack1llllll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤႄ"): env.get(bstack1llllll1_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦႅ")),
            bstack1llllll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣႆ"): env.get(bstack1llllll1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣႇ"))
        }
    return {bstack1llllll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥႈ"): None}
def get_host_info():
    uname = os.uname()
    return {
        bstack1llllll1_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢႉ"): uname.nodename,
        bstack1llllll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣႊ"): uname.sysname,
        bstack1llllll1_opy_ (u"ࠢࡵࡻࡳࡩࠧႋ"): uname.machine,
        bstack1llllll1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤႌ"): uname.version,
        bstack1llllll1_opy_ (u"ࠤࡤࡶࡨ࡮ႍࠢ"): uname.machine
    }
def bstack1l1l1l1ll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1ll1111l_opy_():
    if bstack1l11l11l1_opy_.get_property(bstack1llllll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫႎ")):
        return bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪႏ")
    return bstack1llllll1_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫ႐")
def bstack1l1l1l1lll_opy_(driver):
    info = {
        bstack1llllll1_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ႑"): driver.capabilities,
        bstack1llllll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ႒"): driver.session_id,
        bstack1llllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ႓"): driver.capabilities.get(bstack1llllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ႔"), None),
        bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ႕"): driver.capabilities.get(bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ႖"), None),
        bstack1llllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧ႗"): driver.capabilities.get(bstack1llllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ႘"), None),
    }
    if bstack1l1ll1111l_opy_() == bstack1llllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭႙"):
        info[bstack1llllll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩႚ")] = bstack1llllll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨႛ") if bstack11111l1l1_opy_() else bstack1llllll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬႜ")
    return info
def bstack11111l1l1_opy_():
    if bstack1l11l11l1_opy_.get_property(bstack1llllll1_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪႝ")):
        return True
    if bstack1l1l1ll1ll_opy_(os.environ.get(bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭႞"), None)):
        return True
    return False
def bstack1ll111l11_opy_(bstack1l1l111lll_opy_, url, data, config):
    headers = config.get(bstack1llllll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ႟"), None)
    proxies = bstack1ll11lll1l_opy_(config, url)
    auth = config.get(bstack1llllll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬႠ"), None)
    response = requests.request(
            bstack1l1l111lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll1l11_opy_(bstack1ll1ll111l_opy_, size):
    bstack1111ll1l1_opy_ = []
    while len(bstack1ll1ll111l_opy_) > size:
        bstack11ll1lll1_opy_ = bstack1ll1ll111l_opy_[:size]
        bstack1111ll1l1_opy_.append(bstack11ll1lll1_opy_)
        bstack1ll1ll111l_opy_ = bstack1ll1ll111l_opy_[size:]
    bstack1111ll1l1_opy_.append(bstack1ll1ll111l_opy_)
    return bstack1111ll1l1_opy_
def bstack1l1l11l1ll_opy_(message, bstack1l1l1l111l_opy_=False):
    os.write(1, bytes(message, bstack1llllll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧႡ")))
    os.write(1, bytes(bstack1llllll1_opy_ (u"ࠩ࡟ࡲࠬႢ"), bstack1llllll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩႣ")))
    if bstack1l1l1l111l_opy_:
        with open(bstack1llllll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪႤ") + os.environ[bstack1llllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫႥ")] + bstack1llllll1_opy_ (u"࠭࠮࡭ࡱࡪࠫႦ"), bstack1llllll1_opy_ (u"ࠧࡢࠩႧ")) as f:
            f.write(message + bstack1llllll1_opy_ (u"ࠨ࡞ࡱࠫႨ"))
def bstack1l1l1ll1l1_opy_():
    return os.environ[bstack1llllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬႩ")].lower() == bstack1llllll1_opy_ (u"ࠪࡸࡷࡻࡥࠨႪ")
def bstack1l1ll1111_opy_(bstack1l1l11ll1l_opy_):
    return bstack1llllll1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪႫ").format(bstack1l1ll1lll1_opy_, bstack1l1l11ll1l_opy_)
def bstack1ll1lll1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1llllll1_opy_ (u"ࠬࡠࠧႬ")
def bstack1l1ll11l1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1llllll1_opy_ (u"࡚࠭ࠨႭ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1llllll1_opy_ (u"࡛ࠧࠩႮ")))).total_seconds() * 1000
def bstack1l1ll11lll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1llllll1_opy_ (u"ࠨ࡜ࠪႯ")
def bstack1l1l1l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1llllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩႰ")
    else:
        return bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪႱ")
def bstack1l1l1ll1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1llllll1_opy_ (u"ࠫࡹࡸࡵࡦࠩႲ")
def bstack1l1l1l11l1_opy_(val):
    return val.__str__().lower() == bstack1llllll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫႳ")
def bstack1l1ll1l11l_opy_(bstack1l1l1lllll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1l1lllll_opy_ as e:
                print(bstack1llllll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨႴ").format(func.__name__, bstack1l1l1lllll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l1l1l11ll_opy_(bstack1l1l1llll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l1l1llll1_opy_(cls, *args, **kwargs)
            except bstack1l1l1lllll_opy_ as e:
                print(bstack1llllll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢႵ").format(bstack1l1l1llll1_opy_.__name__, bstack1l1l1lllll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l1l1l11ll_opy_
    else:
        return decorator
def bstack11111lll_opy_(bstack1ll111l11l_opy_):
    if bstack1llllll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬႶ") in bstack1ll111l11l_opy_ and bstack1l1l1l11l1_opy_(bstack1ll111l11l_opy_[bstack1llllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴗ")]):
        return False
    if bstack1llllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬႸ") in bstack1ll111l11l_opy_ and bstack1l1l1l11l1_opy_(bstack1ll111l11l_opy_[bstack1llllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴙ")]):
        return False
    return True
def bstack1l1lll11l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l11ll11_opy_(hub_url):
    if bstack1l111ll11_opy_() <= version.parse(bstack1llllll1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬႺ")):
        if hub_url != bstack1llllll1_opy_ (u"࠭ࠧႻ"):
            return bstack1llllll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣႼ") + hub_url + bstack1llllll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧႽ")
        return bstack1l1l11l1_opy_
    if hub_url != bstack1llllll1_opy_ (u"ࠩࠪႾ"):
        return bstack1llllll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧႿ") + hub_url + bstack1llllll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧჀ")
    return bstack1ll1l111l1_opy_
def bstack1l1l1l1111_opy_():
    return isinstance(os.getenv(bstack1llllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫჁ")), str)
def bstack1l1l11ll1_opy_(url):
    return urlparse(url).hostname
def bstack111lll11_opy_(hostname):
    for bstack1ll1111l_opy_ in bstack11l1ll11_opy_:
        regex = re.compile(bstack1ll1111l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l1l1lll11_opy_(bstack1l1ll111ll_opy_, file_name, logger):
    bstack111l1l11_opy_ = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"࠭ࡾࠨჂ")), bstack1l1ll111ll_opy_)
    try:
        if not os.path.exists(bstack111l1l11_opy_):
            os.makedirs(bstack111l1l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1llllll1_opy_ (u"ࠧࡿࠩჃ")), bstack1l1ll111ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1llllll1_opy_ (u"ࠨࡹࠪჄ")):
                pass
            with open(file_path, bstack1llllll1_opy_ (u"ࠤࡺ࠯ࠧჅ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11111l1ll_opy_.format(str(e)))
def bstack1l1l11l111_opy_(file_name, key, value, logger):
    file_path = bstack1l1l1lll11_opy_(bstack1llllll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ჆"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11llllll1_opy_ = json.load(open(file_path, bstack1llllll1_opy_ (u"ࠫࡷࡨࠧჇ")))
        else:
            bstack11llllll1_opy_ = {}
        bstack11llllll1_opy_[key] = value
        with open(file_path, bstack1llllll1_opy_ (u"ࠧࡽࠫࠣ჈")) as outfile:
            json.dump(bstack11llllll1_opy_, outfile)
def bstack1llll1lll1_opy_(file_name, logger):
    file_path = bstack1l1l1lll11_opy_(bstack1llllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭჉"), file_name, logger)
    bstack11llllll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1llllll1_opy_ (u"ࠧࡳࠩ჊")) as bstack1ll1lll1l1_opy_:
            bstack11llllll1_opy_ = json.load(bstack1ll1lll1l1_opy_)
    return bstack11llllll1_opy_
def bstack11111111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1llllll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ჋") + file_path + bstack1llllll1_opy_ (u"ࠩࠣࠫ჌") + str(e))
def bstack1l111ll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1llllll1_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧჍ")
def bstack111l1ll11_opy_(config):
    if bstack1llllll1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ჎") in config:
        del (config[bstack1llllll1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ჏")])
        return False
    if bstack1l111ll11_opy_() < version.parse(bstack1llllll1_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬა")):
        return False
    if bstack1l111ll11_opy_() >= version.parse(bstack1llllll1_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ბ")):
        return True
    if bstack1llllll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨგ") in config and config[bstack1llllll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩდ")] is False:
        return False
    else:
        return True
def bstack1111l1lll_opy_(args_list, bstack1l1ll1l111_opy_):
    index = -1
    for value in bstack1l1ll1l111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l11l1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l11l1l1_opy_ = bstack1l1l11l1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1llllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪე"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1llllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫვ"), exception=exception)
    def bstack1l1l1lll1l_opy_(self):
        if self.result != bstack1llllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬზ"):
            return None
        if bstack1llllll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤთ") in self.exception_type:
            return bstack1llllll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣი")
        return bstack1llllll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤკ")
    def bstack1l1ll11ll1_opy_(self):
        if self.result != bstack1llllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩლ"):
            return None
        if self.bstack1l1l11l1l1_opy_:
            return self.bstack1l1l11l1l1_opy_
        return bstack1l1ll11111_opy_(self.exception)
def bstack1l1ll11111_opy_(exc):
    return traceback.format_exception(exc)
def bstack1l1l11ll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll1l1lll_opy_(object, key, default_value):
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value