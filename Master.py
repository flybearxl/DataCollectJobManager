# --coding:utf-8--

from lib.UI import *
import sys

reload(sys)
sys.setdefaultencoding('gbk')

if __name__ == '__main__':
    app = Application()
    app.init_ui()
    app.mainloop()
