# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-01'

from MainWindow import *
from ModifyJob import *


class VerifyIntegrity(Toplevel, ClearFiles):
    def __init__(self):
        self.verify = None
        self.text_label = StringVar()
        self.tree_view_list = None
        self.root_node = None
        self.tree = None
        self.job = None
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

        self.tree_frame = Frame(self.verify)
        self.tree_frame.configure(width=500)
        self.tree_frame.grid(row=1, column=0, columnspan=3, sticky=N + S + W + E)

        self.tree = ttk.Treeview(self.tree_frame, column=('JOB', '任务', '完整性'), show="headings")
        self.tree.column('JOB', width=100, anchor='center')
        self.tree.column('任务', width=150, anchor='center')
        self.tree.column('完整性', width=150, anchor='center')
        self.tree.configure(height=15)
        self.tree.heading('#0', text=u'任务清单', anchor='w')
        self.tree.heading('JOB', text='JOB')
        self.tree.heading('任务', text='任务')
        self.tree.heading('完整性', text='完整性')
        self.tree.bind("<Double-1>", self.edit_job)
        ysb = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)

        self.tree.grid(row=0, column=0, rowspan=9, sticky=N + S + W + E)
        ysb.grid(row=0, column=4, rowspan=11, sticky=N + S)
        xsb.grid(row=12, column=0, rowspan=11, sticky=W + E)
        button_test = Button(self.verify, text='执行检测', command=self.verify_job)
        button_test.grid(row=1, column=5, ipadx=20, padx=60, sticky='n')

        button_cancel = Button(self.verify, text='返回系统', command=self.job_cancel)
        button_cancel.grid(row=1, column=5, ipadx=30, pady=50, sticky='n')
        self.bind_error_tree()

    def job_cancel(self):
        self.verify.destroy()

    def verify_job(self):
        try:
            self.bind_error_tree()
        except Exception, e:
            tkMessageBox.showinfo(title='警告', message=e.message)

    def bind_error_tree(self):
        '''
        搜索任务配置目录中脚本文件丢失的JOB，绑定到JOB listview
        :return:
        '''
        try:
            items = self.tree.get_children()
            [self.tree.delete(item) for item in items]
            job = []
            for job_dir in os.listdir(job_root_path):
                job.append(job_dir)
            for parent in job:
                job_list = os.listdir(os.path.join(job_root_path, parent + '/JobConf'))
                for job_name in job_list:
                    job_name = job_name[:-4]
                    script_file = get_script_path(parent, job_name)

                    if not os.path.exists(script_file):
                        self.tree.insert('', 0, values=(parent.decode('gbk'), job_name.decode('gbk'), '脚本文件缺失'))
        except Exception, e:
            print e.message

    def edit_job(self, event):
        try:
            item = self.tree.selection()[0]
            parent = self.tree.item(item, "values")[0].decode('gbk')
            job_name = self.tree.item(item, "values")[1].decode('gbk')
            JobUI(4, parent, job_name)
        except Exception, e:
            tkMessageBox.showinfo(title='警告', message=e.message)