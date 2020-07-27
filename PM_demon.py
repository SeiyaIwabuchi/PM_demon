import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application
import threading
class PM_Demon:
    """
    ifttt連携してPCの電源を管理するのが目的
    10秒おきにサーバーにリクエストの状態を問い合わせ、それに応じてスリープに入れる
    """
    def __init__(self):
        delay = 10 #十秒後にスリープに入るってこと
    @classmethod
    def 