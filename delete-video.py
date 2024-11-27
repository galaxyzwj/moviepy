import os
import shutil
# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有文件夹
folders = [f for f in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, f))]

# 筛选最后两位字符在"00"到"07"之间的文件夹
filtered_folders = []
for folder in folders:
    # 获取文件夹名称的最后两位
    last_two_chars = folder[-2:]

	# 检查最后两位字符是否在"00"到"07"之间
    if last_two_chars.isdigit() and 0 <= int(last_two_chars) <= 6:
	    filtered_folders.append(folder)

# 按照字母顺序排序
filtered_folders.sort()

# 打印符合条件的文件夹名称并 执行删除操作
if filtered_folders:
    print("符合条件的文件夹名称:")
    for folder in filtered_folders:
        print(f"删除文件夹: {folder}")
        shutil.rmtree(folder)
else:
    print("没有符合条件的文件夹。")
