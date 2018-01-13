# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-01'

import threading
import tkFileDialog
from ClearFiles import *
from VerifyJob import *

rn = '\r\n'


class Application(Frame):  # 主窗口
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title(u'财政数据采集还原助手')
        self.master.resizable(width=False, height=False)
        # w = self.master.winfo_screenwidth()
        # h = self.master.winfo_screenheight()
        self.master.geometry("1050x680")
        self.master.iconbitmap('ico.ico')
        # self.master.geometry("%dx%d" % (w, h))
        self.scrolled_execute_job_log = None
        self.c_menu = None

        self.tree = None
        self.job = []  # 存放JOB名称,用来检测选中的是否是叶节点
        self.item = None  # 存放当前选择的任务节点
        self.parent = None  # 当前选择任务的父节点名字——-JOB名字
        self.job_name = None  # 任务名称
        self.root_node = None  # 根节点

    def init_ui(self):
        '''
        初始化界面，完成初始数据绑定
        :return:
        '''
        self.pack()
        menubar = Menu(self.master)

        # 任务菜单
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建JOB", command=lambda: self.new_job('New'))
        file_menu.add_command(label="打开JOB", command=self.open_job)
        file_menu.add_separator()  # 分割线
        file_menu.add_command(label="退出助手", command=self.master.quit)
        menubar.add_cascade(label="任务", menu=file_menu)

        # 设置菜单
        setmenu = Menu(menubar, tearoff=0)
        setmenu.add_command(label='数据清理', command=self.clear_deleted_jobs)
        setmenu.add_command(label='任务完整性验证', command=self.verify_integrity)
        menubar.add_cascade(label='辅助工具', menu=setmenu)
        #
        # # 日志
        # logmenu = Menu(menubar, tearoff=0)
        # logmenu.add_command(label='添加服务器', command='')
        # logmenu.add_command(label='修改服务器信息', command='')
        # menubar.add_cascade(label='系统日志', menu=logmenu)

        # About
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label='关于本软件', command=self.about)
        menubar.add_cascade(label='关于', menu=about_menu)
        self.master.config(menu=menubar)

        # 右键菜单
        self.c_menu = Menu(self.tree)
        self.c_menu.add_command(label='刷新列表', command=self.refresh_tree)
        self.c_menu.add_command(label='新建任务', command=lambda: self.new_job('Context'))
        self.c_menu.add_command(label='执行任务', command=self.confirm_exec_cmd)
        self.c_menu.add_command(label='删除任务', command=self.delete_job)
        frame_top = Frame(self.master)
        frame_top.config(width=1000, height=645)
        frame_top_left = Frame(frame_top)
        frame_top_left.pack_propagate(0)
        self.tree = ttk.Treeview(frame_top_left)
        self.tree.configure(height=30)
        self.tree.heading('#0', text='JOB导航', anchor='w')
        ysb = ttk.Scrollbar(frame_top_left, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame_top_left, orient='horizontal', command=self.tree.xview)
        self.root_node = self.tree.insert('', 'end', text='任务清单', open=True)

        self.tree.grid(row=0, column=0, sticky=N + S)
        self.tree.bind("<Double-1>", self.edit_job)
        self.tree.bind("<Button-3>", self.open_context_menu)
        self.tree.bind("<<TreeviewSelect>>", self.bind_selected_job_conf_to_scrolled_text)
        ysb.grid(row=0, column=1, sticky=N + S)
        xsb.grid(row=1, column=0, sticky=W + E)
        frame_top.pack_propagate(0)
        frame_top_left.pack(side=LEFT, anchor='n', fill=Y)
        frame_top_right = Frame(frame_top)
        frame_top_right.config(width=860, height=640, borderwidth=1)
        frame_top_right.pack_propagate(0)

        frame_top_right_top = Frame(frame_top_right)
        frame_top_right_top.config(width=860, height=20)
        frame_top_right_top.pack_propagate(0)

        label_title = Label(frame_top_right_top, text='任务配置信息', width=100, )
        label_title.pack(side=LEFT, anchor='n')
        execute_button = Button(frame_top_right_top)
        execute_button.configure(text='执行', font=('微软雅黑', 10),
                                 command=self.confirm_exec_cmd)  # 先确认要执行的脚本是否存在，再决定是否执行
        execute_button.pack(side=RIGHT, anchor='n', ipadx=20)
        frame_top_right_top.pack(side=TOP, anchor='n')

        frame_top_right_bottom = Frame(frame_top_right)
        frame_top_right_bottom.config(width=860, height=640)
        frame_top_right_bottom.pack_propagate(0)

        self.scorlled_text_job_conf_info = ScrolledText(frame_top_right_bottom, width=101, height=20, font=('微软雅黑', 10),
                                                        wrap=WORD, state=DISABLED)
        self.scorlled_text_job_conf_info.grid(sticky='w')
        self.scorlled_text_job_conf_info.insert(END, '点击左边任务列表，查看任务信息')

        self.scrolled_execute_job_log = ScrolledText(frame_top_right_bottom)
        self.scrolled_execute_job_log.configure(font=('微软雅黑', 10), width=101, height=12,
                                                state=DISABLED,
                                                wrap=WORD)

        self.scrolled_execute_job_log.grid(sticky=W)
        frame_top_right_bottom.pack(side=BOTTOM, fill=Y)
        frame_top_right.pack(side=LEFT, fill=X)
        frame_top.pack(side=TOP, fill=X)

        frame_bottom = Frame(self.master)
        frame_bottom.config(width=1000, height=20)
        frame_bottom.pack_propagate(0)
        label_job_status = Label(frame_bottom, text="就绪", bd=1, relief=SUNKEN, anchor=W)
        label_job_status.pack(side=BOTTOM, fill=X)
        frame_bottom.pack(side=BOTTOM, fill=X)
        self.bind_job_tree(self.root_node)

    def bind_job_tree(self, root_node):
        '''
        绑定任务配置文件到任务树
        :param 任务树的根节点:
        :param 任务配置根目录目录:
        :return:
        '''
        try:
            job_list = {}
            self.job = []
            for job in os.listdir(job_root_path):
                # 构建路径
                self.job.append(job.decode('gbk'))
                job_list[job] = self.tree.insert(root_node, 'end', text=job.decode('gbk'), open=False)
            for task in job_list:
                conf_path = os.path.join(job_root_path, task.decode('gbk') + "\\JobConf".decode('gbk'))
                job_file_list = os.listdir(conf_path)
                for item in job_file_list:
                    self.tree.insert(job_list[task], 'end', text=item.decode('gbk')[:-4], open=False)
            self.job.append(self.tree.item(self.root_node, 'text'))
        except Exception, e:
            self.scrolled_execute_job_log.insert(END, e.message)

    def refresh_tree(self):
        '''
        刷新任务树
        :return:
        '''
        x = self.tree.get_children(self.root_node)
        if x:
            for item in x:
                self.tree.delete(item)
        self.bind_job_tree(self.root_node)

    # def print_selected(self, event):
    # 测试获取树节点名称
    #     try:
    #         item = self.tree.selection()
    #         if self.tree.item(item, 'text') not in self.job:
    #             print self.tree.item(item, 'text')
    #             # print self.tree.item(self.tree.parent(item),'text')   获取父节点名称
    #     except Exception, e:
    #         self.scrolled_execute_job_log.insert(END, time.strftime('%Y-%m-%d %H:%M:%S',
    #                                                                 time.localtime()) + ': JOB:  ' + self.tree.item(
    #             item, 'text').decode(
    #             'gbk') + e.message)
    #     # for item in self.job:
    #     #     print item

    def open_job(self):
        '''
        菜单打开JOB处理
        :return:
        '''
        try:
            file_name = tkFileDialog.askopenfilename(initialdir=job_root_path, parent=self.master, title='打开JOB配置文件',
                                                     defaultextension='.dat')
            if file_name:
                JobUI(3, 0, file_name)
            else:
                return
        except Exception, e:
            tkMessageBox.showinfo(title='警告', message='请先选择任务')

    def new_job(self, choice):
        '''
        新建JOB
        :return:
        '''
        if choice == 'New':  # 第一个参数0表示新建菜单进入
            JobUI(0, 0, 0, )
        if choice == 'Context':
            parent, job_name = self.get_parent_and_job_name()
            if job_name in self.job:
                JobUI(1, parent, job_name)  # 第一个参数1表示右键单击JOB树选择新建JOB

    @staticmethod
    def about():
        '''
        关于菜单
        :return:
        '''
        tkMessageBox.showinfo(message='财政数据采集助手 V0.01 作者：FLYBEAR', title='关于')
        pass

    @staticmethod
    def clear_deleted_jobs():
        ClearFiles()

    @staticmethod
    def verify_integrity():
        '''
        调用验证任务配置完整性窗口
        :return:
        '''
        VerifyIntegrity()

    def edit_job(self, event):
        '''
         双击任务调用调用任务窗口,调用参数2表示双击JOB树的调用
        :param event:
        :return:
        '''
        parent, job_name = self.get_parent_and_job_name()
        if job_name not in self.job and job_name != '':
            JobUI(2, parent, job_name)

    def bind_selected_job_conf_to_scrolled_text(self, event):
        '''
        填充所选任务的内容到任务描述框
        '''
        try:
            self.scorlled_text_job_conf_info.configure(state=NORMAL)
            self.scorlled_text_job_conf_info.delete(0.0, END)
            parent, job_name = self.get_parent_and_job_name()
            file_path, script_path = get_conf_path(parent, job_name), get_script_path(parent, job_name)
            if job_name not in self.job:
                for item in open(file_path.decode('gbk')):
                    self.scorlled_text_job_conf_info.insert(END, item.decode('gbk'))
                self.scorlled_text_job_conf_info.insert(END, rn + '脚本内容：')
                script_content = open(script_path.decode('gbk')).read()
                self.scorlled_text_job_conf_info.insert(END, rn + script_content.decode('gbk'))
                self.scorlled_text_job_conf_info.see(END)
                self.scorlled_text_job_conf_info.configure(state=DISABLED)
                self.scorlled_text_job_conf_info.update()
            else:
                pass
        except Exception, e:
            self.scrolled_execute_job_log.configure(state=NORMAL)
            if 'Non' in e.message:
                pass
            else:
                self.scrolled_execute_job_log.insert(END, rn + e.message)
                self.scorlled_text_job_conf_info.see(END)
            self.scrolled_execute_job_log.configure(state=DISABLED)

    def confirm_exec_cmd(self):
        '''
        检查传过来的任务名称，开启一个新的线程执行选定任务
        :return:
        '''
        try:
            job_name = self.tree.item(self.tree.selection(), 'text')
            if job_name not in self.job and job_name != '':
                parent, job_name = self.get_parent_and_job_name()
                script_path = get_script_path(parent, job_name)
                th = threading.Thread(target=lambda: self.final_execute_cmd(script_path))
                th.setDaemon(True)
                th.start()
            else:
                self.scrolled_execute_job_log.configure(state=NORMAL)
                self.scrolled_execute_job_log.insert(END, '请先选择需要执行的任务')
                self.scrolled_execute_job_log.configure(state=DISABLED)

        except Exception, e:
            self.scrolled_execute_job_log.insert(0.0, e.message)

    def final_execute_cmd(self, script_path):
        '''
        调用ManageJOb.execute_job执行任务,并接受输出执行信息到任务执行日志窗口
        :param script_path: 任务名称
        :return:
        '''
        try:
            exec_result = ManageJob.execute_job(script_path)
            self.scrolled_execute_job_log.configure(state=NORMAL)
            self.scrolled_execute_job_log.insert(END, exec_result)
            self.scrolled_execute_job_log.see(END)
            self.scrolled_execute_job_log.configure(state=DISABLED)
        except Exception, e:
            self.scrolled_execute_job_log.configure(state=NORMAL)
            self.scrolled_execute_job_log.insert(END, u'出错了' + e.message + rn)
            self.scrolled_execute_job_log.see(END)
            self.scrolled_execute_job_log.configure(state=DISABLED)

    def open_context_menu(self, event):
        '''
        任务树右键弹出菜单
        :param event:
        :return:
        '''
        try:
            self.c_menu.post(event.x_root, event.y_root)
        except Exception, e:
            self.scrolled_execute_job_log.insert(END, e.message)

    def delete_job(self):
        '''
        删除已经存在任务，尚未完成,需要修改ManagerJOb中相关代码
        :return:
        '''
        try:
            self.scrolled_execute_job_log.configure(state=NORMAL)
            parent, job_name = self.get_parent_and_job_name()
            # self.scrolled_execute_job_log.insert(END, parent)
            # self.scrolled_execute_job_log.insert(END, job_name)
            c = ManageJob.logical_delete_job(parent, job_name)
            self.scrolled_execute_job_log.insert(END, c + rn)
            self.refresh_tree()
            self.scrolled_execute_job_log.see(END)
            self.scrolled_execute_job_log.configure(state=DISABLED)
        except Exception, e:
            self.scrolled_execute_job_log.configure(state=NORMAL)
            self.scrolled_execute_job_log.insert(END, 'Error==>' + job_name + e.message + rn)
            self.scrolled_execute_job_log.configure(state=DISABLED)

    def get_parent_and_job_name(self):
        '''
        获取所选择的节点的名称和父节点名称
        :return:
        '''
        item = self.tree.selection()
        job_name = self.tree.item(item, 'text')
        parent = self.tree.item(self.tree.parent(item), 'text')
        return parent, job_name
