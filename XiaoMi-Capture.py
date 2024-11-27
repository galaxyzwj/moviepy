import os
import moviepy
from moviepy import *

#from moviepy.editor import VideoFileClip, concatenate_videoclips

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip

# set ffmpeg path
#change_settings({"FFMPEG_BINARY": "/usr/bin/ffmpeg"})
#print(get_setting("FFMPEG_BINARY"))

# 对directory目录下的mp4文件进行拼接处理
# param 1: 需要执行拼接的目录
# param 2: 定义拼接后mp4名称
# param 3: 判断是第一阶段拼接，还是第二阶段拼接
#          0 表示 第一阶段拼接
#          1 表示 第二阶段拼接
def splicing_mp4(directory, mp4_name, process_flag):
    print("Splicing MP4 Dir: %s" %directory)
    if process_flag == 0:
        # 第一阶段拼接：读取directory目录下所有的以.mp4结尾的文件
        video_files = [f for f in os.listdir(directory) if  f.endswith('.mp4')]
    else:
        # 第二阶段拼接：读取directory目录下所有以prefix开头并以 .mp4 结尾的文件(排除掉其他日期mp4文件影响)
        video_files = [f for f in os.listdir(directory) if  f.startswith(prefix) and f.endswith('.mp4')]

    # 对文件名排序，以确保按正确顺序拼接
    video_files.sort()
    print("Splicing MP4 Count: %s" %len(video_files))

    # 创建视频片段列表
    clips = []
    for video_file in video_files:
        video_path = os.path.join(directory, video_file)
        print(">>>>>>Every Video Path:%s" %video_path)
        clip = VideoFileClip(video_path)
        clips.append(clip)
    # 拼接所有视频片段
    final_clip = concatenate_videoclips(clips)
    # 指定输出视频文件路径
    output_path = mp4_name + ".mp4"  # 替换为实际输出路径
    # 将拼接后的视频写入文件
    #final_clip.write_videofile(output_path, codec="libx265")
    # use nvidia encoder
    final_clip.write_videofile(output_path, codec="h264_nvenc")


# 拼接各个子目录下的所有小视频文件,合成一个以子目录命名的mp4
def splicing_mp4_in_folders(directory):
    # 获取当前路径下的所有文件夹
    for folder_name in os.listdir(directory):
        # 仅对以prefix开头名称的文件夹进行操作
        if folder_name.startswith(prefix):
            # 获取每一个文件夹的全路径
            folder_path = os.path.join(directory, folder_name)
            # 子文件夹全路径
            print("Processing SubDir:%s" %folder_path)
            # 确保处理的是子文件夹
            if os.path.isdir(folder_path):
                splicing_mp4(folder_path, folder_name, 0)

# 当前脚本所在的全路径
current_directory = os.getcwd()
print("current_dir: %s" %current_directory)
# 表示处理的是 2024.10.07的视频
prefix="20241007"
# 执行第一阶段：
# 拼接当天各个子文件夹内的所有小视频，最终生成以该子文件夹进行命名的mp4
# 也就是处理当天每一个小时的所有1分钟的小视频，拼接成一个 完整的1小时 的视频
print("-------------------------------------------------------------")
print("-------------------------------------------------------------")
print("-------------------------- Stage 1 --------------------------")
print("-------------------------------------------------------------")
print("-------------------------------------------------------------")
splicing_mp4_in_folders(current_directory)

# 执行第二阶段：
# 将第一阶段生成的以各个子目录命名的所有mp4文件拼接为 单个整天视频文件
# 
print("-------------------------------------------------------------")
print("-------------------------------------------------------------")
print("-------------------------- Stage 2 --------------------------")
print("-------------------------------------------------------------")
print("-------------------------------------------------------------")
splicing_mp4(current_directory, prefix, 1)
