# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-10'

import ttk
from ModifyJob import *


class ClearFiles(Toplevel):
    def __init__(self, ):
        self.clear_window = None
        self.context_menu = None
        self.root_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir)) + '\Predelete'
        self.tree = None
        self.root_node = None
        self.tree_frame = None
        self.job = []
        self.init_ui()
        self.clear_window.focus_force()

    def init_ui(self):
        self.clear_window = Toplevel()
        self.clear_window.iconbitmap('ico.ico')
        # self.clear_window.geometry('500x400')
        self.clear_window.title('数据清理')
        self.clear_window.resizable(width=False, height=False)
        label = Label(self.clear_window, text='已经删除任务列表')
        label.grid(row=0, column=0, columnspan=3)
        self.tree_frame = Frame(self.clear_window)
        self.tree_frame.configure(width=500)
        self.tree_frame.grid(row=1, column=0, columnspan=3, sticky=N + S + W + E)
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.configure(height=15)
        self.tree.heading('#0', text=u'任务清单', anchor='w')
        ysb = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)
        root_node = self.tree.insert('', 'end', text='JOB_TASK', open=True)

        self.tree.grid(row=0, column=0, rowspan=9, sticky=N + S + W + E)
        self.tree.bind("<Button-3>", self.open_restore_job_menu)

        ysb.grid(row=0, column=4, rowspan=11, sticky=N + S)
        xsb.grid(row=12, column=0, rowspan=11, sticky=W + E)
        self.context_menu = Menu(self.tree)
        self.context_menu.add_command(label='刷新列表', command=lambda: self.refresh_tree(root_node))
        self.context_menu.add_command(label='恢复任务', command=lambda: self.restore_file(root_node))
        self.context_menu.add_command(label='彻底删除', command=lambda: self.delete_jobs('selected', root_node))

        button_delete_all = Button(self.tree_frame)
        button_delete_all.configure(text='全部删除', command=lambda: self.delete_jobs('all', root_node))
        button_delete_all.grid(row=0, column=5, sticky='w', padx=30, pady=10, ipadx=3)

        button_delete = Button(self.tree_frame)
        button_delete.configure(text='删除任务', command=lambda: self.delete_jobs('selected', root_node))
        button_delete.grid(row=1, column=5, sticky='w', padx=30, ipadx=3)

        button_cancel = Button(self.tree_frame)
        button_cancel.configure(text='返回系统', command=lambda: self.clear_window.destroy())
        button_cancel.grid(row=2, column=5, sticky='w', padx=30, ipadx=3)
        self.bind_deleted_jobs(root_node)

    def bind_deleted_jobs(self, root_node):
        '''
        绑定已删除文件到JOB树
        :param root_node:
        :return:
        '''
        try:
            job_list = {}
            for job in os.listdir(self.root_path):
                # 构建路径
                self.job.append(job.decode('gbk'))
                job_list[job] = self.tree.insert(root_node, 'end', text=job.decode('gbk'), open=False)
            for task in job_list:
                conf_path = os.path.join(self.root_path, task.decode('gbk') + "\\JobConf".decode('gbk'))
                job_file_list = os.listdir(conf_path)
                for item in job_file_list:
                    self.tree.insert(job_list[task], 'end', text=item.decode('gbk')[:-4], open=False)
            self.job.append(self.tree.item(root_node, 'text'))
        except Exception, e:
            tkMessageBox._show(title='提示', message=e.message)

    def refresh_tree(self, root_node):
        '''
        刷新已删除JOB树_清空JOB树
        :param root_node:
        :return:
        '''
        x = self.tree.get_children(root_node)
        if x:
            for item in x:
                self.tree.delete(item)
        self.bind_deleted_jobs(root_node)

    def get_parent_and_job_name(self):
        '''
        获取所选择的节点的名称和父节点名称
        :return:
        '''
        item = self.tree.selection()
        job_name = self.tree.item(item, 'text')
        parent = self.tree.item(self.tree.parent(item), 'text')
        return parent, job_name

    def delete_jobs(self, content, root_node):
        '''
        彻底删除已经预删除的文件
        :param content: content确认按下的是全部删除按钮还是删除按钮
        :parm root_node:JOB树根节点
        :return:
        '''
        try:
            if content == 'all':
                for item in scan_all_deleted_job(self.root_path):
                    os.remove(item.decode('gbk'))
            else:
                parent, job_name = self.get_parent_and_job_name()
                ManageJob.clear_deleted_jobs(parent, job_name)
            self.refresh_tree(root_node)
        except Exception, e:
            tkMessageBox.showinfo(title='提示', message=e.message)

    def open_restore_job_menu(self, event):
        '''
        弹出右键菜单
        :param event:
        :return:
        '''
        self.context_menu.post(event.x_root, event.y_root)

    def restore_file(self, root_node):
        try:
            parent, job_name = self.get_parent_and_job_name()
            c = ManageJob.restore_deleted_job(parent, job_name)
            if c == 'exists':
                tkMessageBox.showinfo(title='警告', message='有新的任务配置文件存在了，停止恢复')
                self.clear_window.focus_force()
            else:
                self.refresh_tree(root_node)
        except Exception, e:
            tkMessageBox.showinfo(title='提示', message=e.message)
