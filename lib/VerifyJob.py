# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-01'

import ttk
from ModifyJob import *
from Log import *


class VerifyIntegrity(Toplevel):
    def __init__(self, parent_window):
        self.verify = None
        Log()
        self.log = logging.getLogger("Data_Collect_Log")
        self.tree_frame = None
        self.text_label = StringVar()
        self.tree = None
        self.menu = None

        self.init_ui()
        self.verify.update_idletasks()
        self.verify.deiconify()
        x, y = self.center(600, 510)
        self.verify.geometry('%dx%d+%d+%d' % (600, 510, x, y))
        self.verify.deiconify()

        self.verify.parent = parent_window
        self.verify.focus_force()
        self.verify.parent.hide()
        self.mj = ManageJob()

    def init_ui(self):
        self.verify = Toplevel()
        self.verify.protocol("WM_DELETE_WINDOW", self.job_cancel)
        self.verify.resizable(width=False, height=False)
        self.verify.iconbitmap('ico.ico')
        self.verify.title(u'任务配置验证')
        self.text_label.set(u'任务列表')
        label_title = Label(self.verify, textvariable=self.text_label)
        label_title.grid(row=0, column=0, sticky=W)

        self.tree_frame = Frame(self.verify)
        self.tree_frame.configure(width=500)
        self.tree_frame.grid(row=1, column=0, columnspan=3, sticky=N + S + W + E)

        self.tree = ttk.Treeview(self.tree_frame, column=('JOB', u'任务', u'完整性'), show="headings")
        self.tree.column('JOB', width=100, anchor='center')
        self.tree.column(u'任务', width=150, anchor='center')
        self.tree.column(u'完整性', width=150, anchor='center')
        self.tree.configure(height=22)
        self.tree.heading('#0', text=u'任务清单', anchor='w')
        self.tree.heading('JOB', text='JOB')
        self.tree.heading(u'任务', text=u'任务')
        self.tree.heading(u'完整性', text=u'完整性')
        self.tree.bind("<Double-1>", self.edit_job)
        self.tree.bind("<Button-3>", self.open_context_menu)

        self.menu = Menu(self.tree)
        self.menu.add_command(label=u'刷新列表', command=self.bind_error_tree)
        self.menu.add_command(label=u'删除任务', command=self.delete_job)

        ysb = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)

        self.tree.grid(row=0, column=0, rowspan=9, sticky=N + S + W + E)
        ysb.grid(row=0, column=4, rowspan=11, sticky=N + S)
        xsb.grid(row=12, column=0, rowspan=11, sticky=W + E)
        button_test = Button(self.verify, text=u'执行检测', command=self.verify_job)
        button_test.grid(row=1, column=5, ipadx=5, padx=60, sticky='n')

        button_cancel = Button(self.verify, text=u'返回系统', command=self.job_cancel)
        button_cancel.grid(row=1, column=5, ipadx=5, pady=50, sticky='n')
        self.bind_error_tree()

    def bind_error_tree(self):
        u"""
        搜索任务配置目录中脚本文件丢失的JOB，绑定到JOB list
        :return:
        """
        try:
            items = self.tree.get_children()
            [self.tree.delete(item) for item in items]
            job = []
            for job_dir in os.listdir(job_root_path):
                job.append(job_dir)
            for parent in job:
                job_list = os.listdir(os.path.join(job_root_path, parent + '/JobConf'))
                for job_name in job_list:
                    if '.dat' in job_name:
                        job_name = os.path.splitext(job_name)[0]
                        script_file = ManageJob.get_script_path(parent, job_name)
                        if not os.path.exists(script_file):
                            self.tree.insert('', 0, values=(parent.decode('gbk'), job_name.decode('gbk'), u'脚本文件缺失'))
            if not self.tree.get_children():
                self.tree.insert('', 0, values=('', u'恭喜！没有任务配置损坏', ''))
                self.log.info(u'扫描任务配置完整性完成，没有发现受损任务')
        except Exception, e:
            self.log.error(u'扫描失败' + e.message.decode('gbk'))
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def open_context_menu(self, event):
        u"""
        弹出开始菜单
        :param event:
        :return:
        """
        try:
            self.menu.post(event.x_root, event.y_root)
        except Exception, e:
            self.log.error(u'无法弹出快捷菜单_' + e.message.decode('gbk'))
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def verify_job(self):
        u"""
        验证已经存在的JOB配置情况，是否受损
        :return:
        """
        try:
            self.bind_error_tree()
        except Exception, e:
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def edit_job(self, event):
        u"""
        调用修改JOB窗口，修复受损的JOB
        :param event:
        :return:
        """
        try:
            if self.tree.selection():
                item = self.tree.selection()[0]
                parent = self.tree.item(item, "values")[0].decode('gbk')
                job_name = self.tree.item(item, "values")[1].decode('gbk')
                job = 4
                JobUI(self, job, parent, job_name)
            else:
                pass
        except Exception, e:
            self.log.error(u'无法编辑选中任务_' + e.message.decode('gbk'))
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def delete_job(self):
        u"""
        调用ManageJob.logical_delete_job删除任务
        :return:
        """
        try:
            if self.get_parent_job_name():
                parent, job_name = self.get_parent_job_name()
                self.mj.logical_delete_job(parent, job_name)
                self.log.info(parent + '_' + job_name + u'删除成功')
                self.bind_error_tree()
            else:
                pass
        except Exception, e:
            self.log.error(parent + '_' + job_name + u'_删除失败' + e.message.decode('gbk'))
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def get_parent_job_name(self):
        u"""
        获取父节点名称
        :return:
        """
        try:
            if self.tree.selection():
                item = self.tree.selection()[0]
                parent = self.tree.item(item, "values")[0].decode('gbk')
                job_name = self.tree.item(item, "values")[1].decode('gbk')
                return parent, job_name
            else:
                pass
        except Exception, e:
            self.log.error(u'获取任务节点名称失败_' + e.message.decode('gbk'))
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def hide(self):
        u"""
        隐藏本窗口
        :return:
        """
        self.verify.withdraw()

    def show(self):
        u"""
        显示本窗口
        :return:
        """
        self.verify.update()
        self.verify.deiconify()
        self.bind_error_tree()

    def job_cancel(self):
        u"""
        退出本窗口
        :return:
        """
        self.verify.destroy()
        self.verify.parent.show()

    def center(self, width, height):
        screen_w = self.verify.winfo_screenwidth()
        screen_h = self.verify.winfo_screenheight()
        x = (screen_w - width) / 2
        y = (screen_h - height - 50) / 2
        return x, y
