#语音识别转文字
import speech_recognition as sr

def recognize_speech(timeout=5):
    r = sr.Recognizer()
    # 获取所有麦克风设备名称
    devices = sr.Microphone.list_microphone_names()
    #print("可用麦克风设备：", devices)

    device_id = 0  # 选择第一个设备作为默认,可以根据实际情况更改  

    with sr.Microphone(device_index=device_id) as source:
        #r.adjust_for_ambient_noise(source, duration=3)  # 调整灵敏度
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
