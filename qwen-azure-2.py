from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# API密钥
speech_key = "speech_key"
service_region = "service_region"

# 初始化Azure语音服务客户端
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    # 创建语音合成器
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # 合成语音并保存到文件
    result = synthesizer.speak_text_async(text).get()
    # 检查结果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("语音输出中...")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"语音合成被取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"错误详情: {cancellation_details.error_details}")

def play_audio(file_path):
    # 使用soundfile加载音频文件
    data, fs = sf.read(file_path, dtype='float32')
    # 使用sounddevice播放音频
    sd.play(data, fs)
    sd.wait()  # 等待音频播放完成

#语音识别转文字
def recognize_speech(timeout=5):
    r = sr.Recognizer()
    # 获取所有麦克风设备名称
    devices = sr.Microphone.list_microphone_names()
    #print("可用麦克风设备：", devices)
    # 假设我们选择第一个设备作为默认
    device_id = 0  # 可以根据实际情况更改  
    with sr.Microphone(device_index=device_id) as source:
        r.adjust_for_ambient_noise(source, duration=3)  # 调整灵敏度
        print("请说话...")
        while True:
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=5)  # 缩短phrase_time_limit
                if audio is not None and len(audio.get_wav_data()) > 0:
                    text = r.recognize_google(audio, language='zh-CN,en-US')
                    print("语音识别中...")
                    print(text)
                    return text
                else:
                    print("没有检测到有效语音，请再次尝试。")
            except sr.WaitTimeoutError:
                print("等待超时，没有检测到语音开始，请确保您已经开始说话或稍后再试。")
                continue

def should_exit(message):
    # 定义一个函数判断是否收到结束指令
    return message.lower() == '结束'

def chat_interaction():
    messages = []
    while True:
        message = recognize_speech()
        messages.append({'role': 'user', 'content': message})
        
        if should_exit(message):
            print("对话结束，程序即将退出。")
            break

        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_turbo, messages=messages, result_format='message', stream=True, incremental_output=True)
        print('通义千问:', end='')
        for response in responses:
            content = response.output.choices[0]['message']['content'] if response.output and response.output.choices else ""
            whole_message += content
            print(content, end='')
        print()
        messages.append({'role': 'assistant', 'content': whole_message})
        
        text_to_speech(whole_message)
        play_audio("output.wav")

def main():
    # 程序的入口点
    try:
        chat_interaction()
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
