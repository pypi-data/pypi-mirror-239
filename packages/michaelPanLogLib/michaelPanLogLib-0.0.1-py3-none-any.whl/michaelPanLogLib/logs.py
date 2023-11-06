# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.11
# ***************************************************************
import inspect
import datetime
import os
import json
import random
import string
"""
	本程序实现日志的写入，查找，清空等功能，插入数据库功能暂时没有制作，以后如果有需要的话再补上
	本程序目前支持txt,json,yml格式的日志
"""


class AllKindLog(object):
	def __init__(self):
		frame = inspect.stack()[1]  # 获取代码位置
		info = inspect.getframeinfo(frame[0])
		args = "欢迎使用日志类功能，本程序作者是michaelPan，如果有任何问题请联系：panzhang1314@gmail.com"
		print(
			f"{os.path.basename(info.filename)}【{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}】 "
			f"{args}")
	
	@staticmethod
	def write_log_file(file_path="", content=None):  # 将log写到文件中
		time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
		# 生成一个5位随机字符串,避免插入在同一秒时内容被覆盖
		random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
		time_str = f"{time_str}_{random_string}"
		if file_path == "" or content is None:
			raise Exception("输入路径或者写入内容为空，请检查")
		dir_path = os.path.dirname(file_path)
		if not os.path.exists(dir_path):  # 路径不存在时自动创建
			print(f"写入日志模块 ==> 【日志路径不存在，自动创建】")
			os.makedirs(dir_path)
		if file_path.endswith("txt"):  # 文件类型为txt
			with open(file_path, "a") as f:
				f.write(f"{content}\n")
		elif file_path.endswith("json"):  # 文件类型json
			# 尝试读取文件
			try:
				with open(file_path, 'r') as file:
					data = json.load(file)
			except FileNotFoundError:
				data = {}  # 如果文件不存在，则开始一个空的字典
			# 修改或添加新内容到data字典中
			data[time_str] = content
			# 写入文件
			with open(file_path, 'w') as file:
				json.dump(data, file, indent=4)
		elif file_path.endswith("yml"):  # 文件类型为YAML
			# 尝试读取YAML文件
			import yaml
			try:
				with open(file_path, 'r') as file:
					data = yaml.safe_load(file)
			except FileNotFoundError:
				data = {}  # 如果文件不存在，则开始一个空的字典
			# 修改或添加新内容到data字典中
			data[time_str] = content
			# 写入YAML文件
			with open(file_path, 'w') as file:
				yaml.dump(data, file)
		else:
			raise Exception("目前只支持txt,json和YAML格式的日志文件")
		
	@staticmethod
	def insert_to_db():  # 将log插入数据库
		print(f"插入数据库模块 ==> 功能即将到来，敬请期待...")
	
	@staticmethod
	def find_log_file(file_path="", content=None):  # 查找log文件中的内容
		if file_path == "" or content is None:
			raise Exception("输入路径或者写入内容为空，请检查")
		if file_path.endswith("txt"):  # 文件类型为txt
			with open(file_path, "r") as f:
				for line in f:
					a_line_content = line.strip()  # 使用strip()去除每行末尾的换行符
					if content in a_line_content:
						print(f"查找指定日志内容模块 ==> 【{a_line_content}】")
		elif file_path.endswith("yml"):
			import yaml
			with open(file_path, 'r') as file:
				data = yaml.safe_load(file)
				for a_key in data.keys():
					if content in data[a_key]:
						print(f"查找指定日志内容模块 ==> 【{data[a_key]}】")
		elif file_path.endswith("json"):
			with open(file_path, 'r') as file:
				data = json.load(file)
				for a_key in data.keys():
					if content in data[a_key]:
						print(f"查找指定日志内容模块 ==> 【{data[a_key]}】")
	
	@staticmethod
	def clear_log_file(file_path=""):  # 清空log文件
		if file_path == "":
			raise Exception("输入路径为空，请检查")
		if file_path.endswith("txt"):  # 文件类型为txt
			with open(file_path, "w"):
				pass
		elif file_path.endswith("yml"):
			import yaml
			with open(file_path, 'w') as file:
				yaml.dump({}, file)
		elif file_path.endswith("json"):
			with open(file_path, 'w') as file:
				json.dump({}, file)
		print(f"清空日志模块 ==> 【清空日志成功】")
		
	@staticmethod
	def delete_file(file_path=""):
		if file_path == "":
			raise Exception("输入路径为空，请检查")
		if os.path.isfile(file_path):
			os.remove(file_path)
		print(f"删除日志文件模块 ==> 【删除日志文件成功】")
		
		
if __name__ == "__main__":
	a_log = AllKindLog()
	a_log.write_log_file(f"D:/pycharm_project/michaelPanLogLib/test1.yml","hello world")
	a_log.write_log_file(f"D:/pycharm_project/michaelPanLogLib/test1.yml", "hi world")
	a_log.find_log_file(f"D:/pycharm_project/michaelPanLogLib/test1.yml", "world")
	a_log.clear_log_file(f"D:/pycharm_project/michaelPanLogLib/test1.yml")
	a_log.delete_file(f"D:/pycharm_project/michaelPanLogLib/test1.yml")
	