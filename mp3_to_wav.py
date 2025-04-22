from moviepy import AudioFileClip
import numpy as np
import soundfile as sf


def convert_to_mono_16bit_wav(input_file, output_file):
    try:
        # 加载音频文件
        audio_clip = AudioFileClip(input_file)

        # 临时文件路径
        temp_file = "temp_audio.wav"

        # 使用 ffmpeg 参数将音频转换为单声道
        audio_clip.write_audiofile(temp_file, ffmpeg_params=['-ac', '1'])

        # 读取临时文件
        audio, frame_rate = sf.read(temp_file)

        # 转换为 16 位
        audio = (audio * 32767).astype(np.int16)

        # 保存为无压缩的 WAV 格式
        sf.write(output_file, audio, frame_rate, subtype='PCM_16')

        print(f"成功将 {input_file} 转换为符合要求的 WAV 格式并保存为 {output_file}")

        # 关闭音频剪辑
        audio_clip.close()

        # 删除临时文件
        import os
        os.remove(temp_file)
    except Exception as e:
        print(f"转换过程中出现错误: {e}")




if __name__ == "__main__":
    input_file = r"C:\Users\n\Downloads\test.mp3" # 替换为你的输入音频文件路径
    output_file = r"C:\Users\n\Downloads\test.wav"  # 替换为输出的 WAV 文件路径
    convert_to_mono_16bit_wav(input_file, output_file)
