# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-01'

from ModifyJob import *


class VerifyIntegrity(Toplevel):
    def __init__(self):
        self.verify = None
        self.text_label = StringVar()
        self.tree_view_list = None
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                      os.path.pardir)) + '\\JobConf\\'
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                        os.path.pardir)) + '\\Script\\'
        self.init_ui()
        self.verify.focus_force()

    def init_ui(self):
        self.verify = Toplevel()
        self.verify.resizable(width=False, height=False)
        self.verify.iconbitmap('ico.ico')
        self.verify.title('任务配置验证')
        self.text_label.set('任务列表')
        label_title = Label(self.verify, textvariable=self.text_label)
        label_title.grid(row=0, column=0, sticky=W)

        self.listbox_job = Listbox(self.verify)
        self.listbox_job.bind('<Double-Button-1>', self.edit)
        scrollbar_listbox = Scrollbar(self.verify)
        self.listbox_job.configure(width=50, height=20)
        self.listbox_job.grid(row=1, column=0, columnspan=3)
        scrollbar_listbox.grid(row=1, column=5, sticky=N + S)
        self.listbox_job.configure(yscrollcommand=scrollbar_listbox)

        button_test = Button(self.verify, text='执行检测', command=self.verify_job)
        button_test.grid(row=2, column=0, padx=60)

        button_cancel = Button(self.verify, text='返 回', command=self.job_cancel)
        button_cancel.grid(row=2, column=1, padx=50, ipadx=20)

    def job_cancel(self):
        self.verify.destroy()

    def verify_job(self):
        # job_list = []
        for item in os.listdir(self.file_path):
            if not os.path.exists(self.script_path + item.decode('gbk')[:-4] + '.bat'):
                self.listbox_job.insert(END, item.decode('gbk')[:-4] + '_损坏')
                self.text_label.set('缺失脚本的任务 可双击编辑该任务')

    def edit(self, event):
        edit_job_name = self.listbox_job.get(self.listbox_job.curselection())
        if edit_job_name:
            JobUI(edit_job_name)
        else:
            pass
