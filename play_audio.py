import sounddevice as sd
import soundfile as sf
def play_audio(file_path):
    # 使用soundfile加载音频文件
    data, fs = sf.read(file_path, dtype='float32')
    # 使用sounddevice播放音频
    sd.play(data, fs)
    sd.wait()  # 等待音频播放完成