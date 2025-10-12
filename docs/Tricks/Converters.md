


## m4s_to_mp4

bilibil 的缓存在 ```Android/data/tv.danmaku.bilibilihd/download/{...}``` 中，点进去后每个视频都有一个文件夹

```bash
audio.m4s
video.m4s
index.json
```


WSL中```sudo apt install ffmpeg``` 后，在相应文件夹内运行 ```python m4s_to_mp4.py ``` 转换视频为 ```.mp4``` 格式

```py
import subprocess

def convert_hevc_to_h264(video_path, audio_path, output_path):
    """
    将 HEVC 视频转换为 H.264 编码
    """
    try:
        command = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'libx264',      # 使用 H.264 视频编码
            '-c:a', 'aac',          # 使用 AAC 音频编码
            '-crf', '23',           # 视频质量参数 (0-51，越小质量越好)
            '-preset', 'medium',    # 编码速度与压缩率的平衡
            '-y',
            output_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"转换成功！输出文件: {output_path}")
        else:
            print(f"转换失败: {result.stderr}")
            
    except Exception as e:
        print(f"发生错误: {e}")

# 使用示例
convert_hevc_to_h264("video.m4s", "audio.m4s", "output_h264.mp4")
```









