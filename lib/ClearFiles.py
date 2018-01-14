# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-10'

import ttk

from ModifyJob import *


class ClearFiles(Toplevel):
    def __init__(self, parent_window):
        self.clear_window = None
        self.context_menu = None
        self.parent = parent_window
        self.root_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir)) + '\Predelete'
        self.tree = None
        self.root_node = None
        self.tree_frame = None
        self.job = []
        self.init_ui()
        self.clear_window.focus_force()
        self.mj = ManageJob()

    def init_ui(self):
        self.clear_window = Toplevel()
        self.clear_window.protocol("WM_DELETE_WINDOW", self.job_cancel)
        self.clear_window.iconbitmap('ico.ico')
        self.clear_window.title(u'数据清理')
        self.clear_window.resizable(width=False, height=False)

        label = Label(self.clear_window, text=u'已经删除任务列表')
        label.grid(row=0, column=0, columnspan=3)

        self.tree = ttk.Treeview(self.clear_window, column=('JOB', u'任务'), show="headings")
        self.tree.column('JOB', width=100, anchor='w')
        self.tree.column(u'任务', width=200, anchor='w')
        self.tree.configure(height=15)
        self.tree.heading('JOB', text='JOB')
        self.tree.heading(u'任务', text=u'任务')
        self.tree.bind("<Button-3>", self.open_restore_job_menu)
        ysb = ttk.Scrollbar(self.clear_window, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.clear_window, orient='horizontal', command=self.tree.xview)

        self.tree.grid(row=0, column=0, rowspan=9, sticky=N + S + W + E)
        ysb.grid(row=0, column=1, rowspan=11, sticky=N + S)
        xsb.grid(row=12, column=0, rowspan=11, sticky=W + E)

        self.context_menu = Menu(self.tree)
        self.context_menu.add_command(label=u'刷新列表', command=self.bind_tree)
        self.context_menu.add_command(label=u'恢复任务', command=self.restore_file)
        self.context_menu.add_command(label=u'彻底删除', command=lambda: self.delete_jobs('selected'))

        button_delete_all = Button(self.clear_window)
        button_delete_all.configure(text=u'全部删除', command=lambda: self.delete_jobs('all'))
        button_delete_all.grid(row=0, column=2, padx=30, sticky='w')

        button_delete = Button(self.clear_window)
        button_delete.configure(text=u'彻底删除', command=lambda: self.delete_jobs('selected'))
        button_delete.grid(row=1, column=2, padx=30, sticky='w')

        button_cancel = Button(self.clear_window)
        button_cancel.configure(text=u'返回系统', command=self.job_cancel)
        button_cancel.grid(row=2, column=2, padx=30, sticky='w')
        # self.bind_deleted_jobs(root_node)
        self.bind_tree()
        self.parent.hide()

    def bind_tree(self):
        try:
            items = self.tree.get_children()
            [self.tree.delete(item) for item in items]
            job = []
            for job_dir in os.listdir(deleted_root_path):
                job.append(job_dir)
            for parent in job:
                job_list = os.listdir(os.path.join(deleted_root_path, parent + '/JobConf'))
                for job_name in job_list:
                    if '.dat' in job_name:
                        job_name = os.path.splitext(job_name)[0]
                        self.tree.insert('', 0, values=(parent.decode('gbk'), job_name.decode('gbk')))
        except Exception, e:
            tkMessageBox.showinfo(title=u'警告', message=e.message)

    def delete_jobs(self, content):
        u"""
        彻底删除已经预删除的文件
        :param content: content确认按下的是全部删除按钮还是删除按钮
        :parm parent: LISTVIEW选择的JOB名
        :parm job_name: LISTVIEW选择的任务名
        :return:
        """
        if content == 'all':
            for item in self.mj.scan_all_deleted_job(self.root_path):
                os.remove(item.decode('gbk'))
            self.bind_tree()
            self.clear_window.focus_force()
        else:
            if self.get_parent_and_job_name():
                parent, job_name = self.get_parent_and_job_name()
                try:
                    self.mj.clear_deleted_jobs(parent, job_name)
                    self.bind_tree()
                except Exception, e:
                    tkMessageBox.showinfo(title=u'提示', message=e.message)
                else:
                    pass

    def restore_file(self):
        u"""
        恢复已经预删除的任务到原始位置，如果有新文件存在，则不恢复。
        :return:
        """
        if self.get_parent_and_job_name():
            parent, job_name = self.get_parent_and_job_name()
            try:
                c = self.mj.restore_deleted_job(parent, job_name)
                if c == 'exists':
                    tkMessageBox.showinfo(title=u'警告', message=u'有新的任务配置文件存在了，停止恢复')
                    self.clear_window.focus_force()
                else:
                    self.bind_tree()
            except Exception, e:
                tkMessageBox.showinfo(title=u'提示', message=e.message)
            else:
                pass

    def get_parent_and_job_name(self):
        u"""
        获取所选择的节点的名称和父节点名称
        :return:
        """
        if self.tree.selection():
            item = self.tree.selection()
            parent = self.tree.item(item, "values")[0].decode('gbk')
            job_name = self.tree.item(item, "values")[1].decode('gbk')
            return parent, job_name
        else:
            pass

    def open_restore_job_menu(self, event):
        u"""
        弹出右键菜单
        :param event:
        :return:
        """
        self.context_menu.post(event.x_root, event.y_root)

    def job_cancel(self):
        u"""
        退出窗口
        :return:
        """
        self.clear_window.destroy()
        self.parent.show()
