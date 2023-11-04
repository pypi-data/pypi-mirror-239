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
import threading
bstack11lll11ll1_opy_ = 1000
bstack11ll1ll1ll_opy_ = 5
bstack11lll11l1l_opy_ = 30
bstack11ll1lllll_opy_ = 2
class bstack11lll1111l_opy_:
    def __init__(self, handler, bstack11ll1lll1l_opy_=bstack11lll11ll1_opy_, bstack11lll11l11_opy_=bstack11ll1ll1ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11ll1lll1l_opy_ = bstack11ll1lll1l_opy_
        self.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack11ll1lll11_opy_()
    def bstack11ll1lll11_opy_(self):
        self.timer = threading.Timer(self.bstack11lll11l11_opy_, self.bstack11lll111l1_opy_)
        self.timer.start()
    def bstack11lll11111_opy_(self):
        self.timer.cancel()
    def bstack11lll111ll_opy_(self):
        self.bstack11lll11111_opy_()
        self.bstack11ll1lll11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11ll1lll1l_opy_:
                t = threading.Thread(target=self.bstack11lll111l1_opy_)
                t.start()
                self.bstack11lll111ll_opy_()
    def bstack11lll111l1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11ll1lll1l_opy_]
        del self.queue[:self.bstack11ll1lll1l_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11lll11111_opy_()
        while len(self.queue) > 0:
            self.bstack11lll111l1_opy_()