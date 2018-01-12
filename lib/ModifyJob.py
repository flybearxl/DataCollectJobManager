# --coding:utf-8--
__author__ = 'FlyBear'
__date__ = '2018-01-01'

from Tkinter import *
from ScrolledText import ScrolledText
from ManageJob import *
from ttk import Combobox

rn = '\r\n'


class JobUI(Toplevel):  # 编辑任务窗口
    def __init__(self, job, parent, job_name):
        self.edit_job = Toplevel()
        self.job_file_ext = '.dat'
        self.job_script_ext = '.bat'
        self.txt_text_job = StringVar()
        self.txt_text_task = StringVar()
        self.txt_text_desc = StringVar()
        self.txt_text_server = StringVar()
        self.txt_text_user = StringVar()
        self.txt_text_pwd = StringVar()
        self.txt_text_tablespace = StringVar()
        self.txt_text_script = StringVar()

        self.job_conf_content = None  # JOB配置内容
        self.job_script_content = None  # JOB脚本内容

        self.edit_job.geometry('600x520')
        self.edit_job.title('任务编辑')
        self.edit_job.iconbitmap('ico.ico')
        self.edit_job.resizable(width=False, height=False)

        top_frame = Frame(self.edit_job)
        top_frame.configure(borderwidth=2, bg='gray')
        Label(top_frame, text="JOB", bg='gray').grid(row=0, column=1, sticky=W)
        self.combobox_Job_name = Combobox(top_frame, width=12, textvariable=self.txt_text_job,state='readonly')
        self.combobox_Job_name.grid(row=0, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="任务名称", bg='gray').grid(row=1, column=1, sticky=W)
        self.entry_text_name = Entry(top_frame, textvariable=self.txt_text_task)
        self.entry_text_name.grid(row=1, column=2, ipadx=30, sticky=W)

        Label(top_frame, text="任务名称不能为空表空，间用户名密码等信息并没有实际意义。仅仅是为了方便在主界面查看代码是否匹配！", bg='gray',
              wraplength=290, justify='left', fg='red').grid(row=2,
                                                             column=2,
                                                             sticky=E,
                                                             rowspan=3)

        Label(top_frame, text="任务描述", bg='gray').grid(row=2, column=1, sticky=W)
        self.entry_text_desc = Entry(top_frame, textvariable=self.txt_text_desc)
        self.entry_text_desc.grid(row=2, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="服务器地址", bg='gray').grid(row=3, column=1, sticky=W)
        self.entry_text_server = Entry(top_frame, textvariable=self.txt_text_server)
        self.entry_text_server.grid(row=3, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="用户名", bg='gray').grid(row=4, column=1, sticky=W)
        self.entry_text_user = Entry(top_frame, textvariable=self.txt_text_user)
        self.entry_text_user.grid(row=4, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="密码", bg='gray').grid(row=5, column=1, sticky=W)
        self.entry_text_pwd = Entry(top_frame, textvariable=self.txt_text_pwd)
        self.entry_text_pwd.grid(row=5, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="表空间", bg='gray').grid(row=6, column=1, sticky=W)
        self.entry_text_tablespace = Entry(top_frame, textvariable=self.txt_text_tablespace)
        self.entry_text_tablespace.grid(row=6, column=2, ipadx=30, sticky=W)
        Label(top_frame, text="脚本", bg='gray').grid(row=7, column=1, sticky=W)
        self.entry_text_script = ScrolledText(top_frame, width=64, height=25)
        self.entry_text_script.grid(row=7, column=2, ipadx=30, sticky=W)
        top_frame.pack(side=TOP)

        bottom_frame = Frame(self.edit_job)
        bottom_frame.configure(height=30, borderwidth=2)
        bottom_frame.pack_propagate(0)
        button_ok = Button(bottom_frame, text="保 存",
                           command=self.check_entry_is_empty)
        button_ok.pack(side=LEFT, padx=150, ipadx=10)

        button_cancel = Button(bottom_frame, text="取 消", command=self.job_cancel)
        button_cancel.pack(side=LEFT, ipadx=10, )
        bottom_frame.pack(side=BOTTOM, fill=X)

        self.init_ui(job, parent, job_name)
        self.edit_job.focus_force()

    def init_ui(self, job, parent, job_name):
        '''
        根据传入的参数，决定窗口的初始状态
        :param job: 0-新建菜单点击创建 1-JOB树右键新建JOB菜单 2-双击JOB
        :param parent: 父节点
        :param job_name: 节点名称_job_name
        :return:
        '''
        if job == 0:
            value_combobox = scan_all_job()
            tuple(value_combobox)
            self.combobox_Job_name['values'] = value_combobox
        elif job == 1:
            self.txt_text_job.set(job_name)
            self.combobox_Job_name.configure(state='disabled')
        elif job == 2:
            file_path = get_conf_path(parent, job_name)
            script_path = get_script_path(parent, job_name)
            try:
                self.job_conf_content = open(file_path).readlines()  # 读取配置文件内容填充列表
                self.job_script_content = open(script_path).read()
            except Exception, e:
                tkMessageBox.showwarning(title='警告', message=e.message)
                self.edit_job.destroy()
            self.set_text_value(parent)
            self.combobox_Job_name.configure(state='disabled')

    def check_entry_is_empty(self):
        '''
        保存任务，检查是否输入了任务名称，有就调用save_job_conf_file保存配置文件
        没有任务名称则不保存
        :param job_name:JOB名字
        :param parent:父节点名称
        :return:
        '''
        try:
            parent = self.combobox_Job_name.get()
            job_name = self.entry_text_name.get()
            if self.combobox_Job_name.get() and self.entry_text_name.get():
                job_file = get_conf_path(parent, job_name)
                job_script = get_script_path(parent, job_name)
                if check_job_file_exists(job_file):
                    self.save_job_conf_file(job_file, job_script)
                self.edit_job.focus_force()
            else:
                tkMessageBox.showerror('Error', 'JOB和任务名称不能为空')
                self.edit_job.focus_force()
        except Exception, e:
            tkMessageBox.showerror('Error', e.message)
            self.edit_job.focus_force()

    def save_job_conf_file(self, job_file, job_script):  # 保存任务配置文件
        try:
            rn = '\r\n'
            # print '即将写入脚本配置文件：', job_file
            # print '即将写入脚本文件：', job_script
            job_conf_file = open(job_file, 'w')
            job_conf_file.writelines(u'任务名称:  ' + (self.entry_text_name.get() if self.combobox_Job_name.get() else ''))
            job_conf_file.writelines(
                rn + u'任务描述:  ' + (self.entry_text_desc.get() if self.entry_text_desc.get() else ''))
            job_conf_file.writelines(
                rn + u'服务器地址:  ' + (self.entry_text_server.get() if self.entry_text_server else ''))
            job_conf_file.writelines(rn + u'用户名:  ' + (self.entry_text_user.get() if self.entry_text_user else ''))
            job_conf_file.writelines(
                rn + u'密码:  ' + (self.entry_text_pwd.get() if self.entry_text_pwd.get() else ''))
            job_conf_file.writelines(
                rn + u'表空间:  ' + (self.entry_text_tablespace.get() if self.entry_text_tablespace.get() else ''))
            job_conf_file.writelines(rn + u'脚本路径:  ' + job_script[job_script.find('Script'):])
            job_conf_file.close()
            script_file = open(job_script, 'w')
            script_content = self.entry_text_script.get(0.0, END)
            script_content.rstrip()
            script_file.writelines(script_content)
            script_file.close()
            self.edit_job.destroy()
        except Exception, e:
            return e.message

    @staticmethod
    def open_or_new_job(job, parent, job_name):  # 判断新建还是打开任务，job保存的是分类信息
        if job_name not in job and job_name != '':
            return '', parent, job_name
        else:
            return job, parent, job_name

    def set_text_value(self, parent):  #
        '''
        #打开任务绑定输入栏值
        :param parent:
        :return:
        '''
        try:
            self.txt_text_job.set(parent)
            self.txt_text_task.set(ManageJob.get_job_text_content(self.job_conf_content[0]).decode('gbk'))
            self.txt_text_desc.set(ManageJob.get_job_text_content(self.job_conf_content[1]).decode('gbk'))
            self.txt_text_server.set(ManageJob.get_job_text_content(self.job_conf_content[2]).decode('gbk'))
            self.txt_text_user.set(ManageJob.get_job_text_content(self.job_conf_content[3]).decode('gbk'))
            self.txt_text_pwd.set(ManageJob.get_job_text_content(self.job_conf_content[4]).decode('gbk'))
            self.txt_text_tablespace.set(ManageJob.get_job_text_content(self.job_conf_content[5]).decode('gbk'))
            # self.txt_text_script.set(open(get_script_file(get_text_content(self.job_conf_content[0]).decode('gbk'))).read())
            # script = open(get_script_path(self.txt_text_task.get())).read()
            self.entry_text_script.insert(0.0, self.job_script_content.decode('gbk'))
        except Exception, e:
            print e.message

    def job_cancel(self):  # 退出窗口
        self.edit_job.destroy()
