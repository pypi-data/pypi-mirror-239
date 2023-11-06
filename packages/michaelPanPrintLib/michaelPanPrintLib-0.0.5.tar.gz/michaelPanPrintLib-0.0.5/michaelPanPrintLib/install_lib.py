# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.11
# ***************************************************************
import importlib
import inspect
import subprocess
"""
	本程序实现检测库是否已经安装与未安装库自动安装功能
"""


def check_and_install_lib(libs=None, url='https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'):
	"""
	:param libs: 需要检查安装的库列表
	:param url: 指定的下载源(默认为清华源)
	:return: 无返回值
	"""
	frame = inspect.stack()[1]  # 获取代码位置
	info = inspect.getframeinfo(frame[0])
	for i in range(len(libs)):
		try:
			importlib.import_module(libs[i])
		except ModuleNotFoundError:
			try:
				print(f"{info.filename}:{info.lineno} 【开始下载安装{libs[i]}库...】")
				subprocess.run(f'pip install {libs[i]} -i {url}', shell=True, timeout=30)  # 设置超时时间为30秒
			except subprocess.TimeoutExpired:
				print(f"{info.filename}:{info.lineno} 【{libs[i]}库下载失败，请检查网络】")
				