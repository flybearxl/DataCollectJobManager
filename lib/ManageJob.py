# --coding:utf-8---
import os
import time
import shutil
import subprocess
import tkMessageBox

job_conf_ext = '.dat'
job_script_ext = '.bat'
job_root_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir)) + '\Job'
deleted_root_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir)) + '\Predelete'
file_list = []


class ManageJob:
    def __init__(self):
        pass

    @staticmethod
    def execute_job(script_path):
        u"""
        调用执行任务函数并输出执行信息到任务执行日志窗口
        :param script_path:
        :return:
        """
        try:
            shell_cmd = 'cmd.exe /c ' + script_path.decode('gbk')
            subprocess.Popen(shell_cmd,
                             # shell=True,
                             # stdout=subprocess.PIPE,
                             # stderr=subprocess.STDOUT,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)

            return time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime()) + ': JOB:  ' + script_path[script_path.find('Job\\'):].replace(
                'Script\\',
                '').replace(
                '\\',
                '->') + \
                   u'>>>>任务已开始运行，请在新开窗口中查看任务进度，注意不要重复提交，否则可能造成数据错误！' + '\r\n'
        except Exception, e:
            return e.message

    # @staticmethod
    def logical_delete_job(self, parent, job_name):
        u"""
        删除任务,将任务移动到预删除目录位置
        :param parent:
        :param job_name:
        :return:
        """
        try:
            job_file = self.get_conf_path(parent, job_name)
            job_script_file = self.get_script_path(parent, job_name)
            pre_delete_file = self.get_pre_delete_conf_path(parent, job_name)
            pre_delete_script = self.get_pre_delete_script_path(parent, job_name)
            shutil.move(job_file, pre_delete_file)  # 此处仅仅是将文件移走,并没有完全删除
            shutil.move(job_script_file, pre_delete_script)
            return time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime()) + ': JOB:  ' + job_name + u'>>>>>>>>删除成功'
        except Exception, e:
            return time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime()) + ': JOB:  ' + job_name + e.message

    @staticmethod
    def get_job_text_content(text_content):
        u"""
        保存任务配置时获取填入文本框中的值并返回
        :param text_content:
        :return:
        """
        try:
            pos = text_content.find(' ')
            text_content = text_content[pos:]
            return text_content.strip().lstrip().rstrip()
        except Exception, e:
            return e.message

    def clear_deleted_jobs(self, parent, job_name):
        u"""
        接受一个包含所有需要删除的文件的列表，并删除所有指定的文件
        :param parent: 父节点名称
        :param job_name: 任务名称
        :return:
        """
        try:
            job_deleted_file_path = self.get_pre_delete_conf_path(parent, job_name)
            job_deleted_script_path = self.get_pre_delete_script_path(parent, job_name)
            os.remove(job_deleted_file_path)
            os.remove(job_deleted_script_path)
        except Exception, e:
            return e.message

    def restore_deleted_job(self, parent, job_name):
        u"""
        恢复逻辑删除的文件到原位置，并在原位置已经有相同配置的情况下给出提示
        :param parent:
        :param job_name:
        :return:
        """
        try:
            deleted_file = self.get_pre_delete_conf_path(parent, job_name)
            deleted_script = self.get_pre_delete_script_path(parent, job_name)
            conf_file = self.get_conf_path(parent, job_name)
            conf_script = self.get_script_path(parent, job_name)
            if os.path.exists(conf_file):
                return 'exists'
            else:
                shutil.move(deleted_file, conf_file)
                shutil.move(deleted_script, conf_script)
        except Exception, e:
            return e.message

    @staticmethod
    def get_conf_path(parent, job_name):
        u"""
        获取任务配置路径
        :param parent:
        :param job_name:
        :return:
        """
        # job_conf_path = os.path.join(job_root_path, parent)
        job_conf_path = job_root_path + '\\' + parent + '\\JObConf\\' + str(job_name) + job_conf_ext
        return job_conf_path

    @staticmethod
    def get_script_path(parent, job_name):
        u"""
        获取任务脚本路径
        :param parent:
        :param job_name:
        :return:
        """
        job_script_path = job_root_path + '\\' + parent + '\\Script\\' + str(job_name) + job_script_ext
        return job_script_path

    @staticmethod
    def get_pre_delete_conf_path(parent, job_name):
        u"""
        获取任务删除时任务文件存放路径
        :param parent:
        :param job_name:
        :return:
        """
        pre_delete_file = deleted_root_path + '\\' + parent + '\\JObConf\\' + job_name + job_conf_ext
        return pre_delete_file

    @staticmethod
    def get_pre_delete_script_path(parent, job_name):
        u"""
        设置删除任务时脚本文件存放路径
        :param parent:
        :param job_name:
        :return:
        """
        pre_delete_script = deleted_root_path + '\\' + parent + '\\Script\\' + job_name + job_script_ext
        return pre_delete_script

    @staticmethod
    def check_job_file_exists(job_file):
        u"""
        检查任务配置文件是否已经存在
        :param job_file: 任务配置文件
        :return: 1 覆盖已存在文件，，0不覆盖，取消操作
        """
        if os.path.exists(job_file):
            yes_or_no = tkMessageBox.askyesno(u'是否覆盖？', u'任务文件已经存在，是否需要覆盖，谨慎操作，该操作不可逆！')
            if yes_or_no is True:
                return 1
            else:
                return 0
        else:
            return 1

    def scan_all_deleted_job(self, root_path):
        u"""
        遍历所有被删除的文件，包含任务配置文件和脚本文件，以及该目录下的所有其它文件
        :param root_path:
        :return:
        """
        for file_path in os.listdir(root_path):
            # 构建路径
            file_path = os.path.join(root_path, file_path)
            # 是否存在子目录
            isdir = os.path.isdir(file_path)
            if isdir:
                self.scan_all_deleted_job(file_path)
            else:
                file_list.append(file_path)
        return file_list

    @staticmethod
    def scan_all_job():
        u"""
        遍历所有被删除的文件，包含任务配置文件和脚本文件，以及该目录下的所有其它文件
        :param :
        :return:
        """
        for file_path in os.listdir(job_root_path):
            file_list.append(file_path.decode('gbk'))
        return file_list
