from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from recognize_speech import recognize_speech
from text_to_speech import text_to_speech
from play_audio import play_audio
# 浏览器相关调用
from website_mapping import keyword_to_url  # 导入外部文件中的字典
from website_mapping import website_keyword
from website_mapping import software_keyword
from website_mapping import software_mapping
import webbrowser
# 打开程序等系统调用
import os

# 判断是否退出函数
def should_exit(message):
     return message.lower() in {'结束','你退下吧','退下','退下吧'}
# 打开网站函数
def open_website(message):
    url = keyword_to_url.get(message.lower(), None)
    if url:
        print(f"正在打开: {url}")
        webbrowser.open(url)
    else:
        print("未知的关键词，请输入有效的网站关键词。")
# 打开程序函数
def open_software(message):
    command = software_mapping.get(message.lower(), None)
    if command is None:
        print("未知的软件名称，请输入正确的软件名。")
    else:
        # 使用os.system执行命令
        os.system(command)

def main():
    try:
        messages = []
        while True:
            message = recognize_speech()
            messages.append({'role': 'user', 'content': message})
            
            # 判断退出指令
            if should_exit(message):
                text_to_speech('好的，如果你需要任何帮助或有其他问题，请随时告诉我。祝你有美好的一天！')
                play_audio("output.wav")
                print("对话结束，程序即将退出。")
                break
            
            # 判断是否打开网站指令
            if message.strip().lower() in website_keyword:
                if message.strip().lower() == '打开网站': #去掉前后空格转换为小写
                    text_to_speech('请问你要打开什么网站')
                    play_audio("output.wav")
                    continue
                else:
                    open_website(message)
                    text_to_speech('已为你打开网站')
                    play_audio("output.wav")
                    continue
            
            # 判断是否打开程序指令
            if message.strip().lower() in software_keyword:
                open_software(message)
                text_to_speech('已为你打开')
                play_audio("output.wav")
                continue
            
            # 如果以上都不是，调用AI回复
            whole_message = ''
            
            # 调用通义千问大模型，接收流式输出
            responses = Generation.call(Generation.Models.qwen_plus, messages=messages, result_format='message', stream=True, incremental_output=True)
            print('通义千问:', end='')
            for response in responses:
                content = response.output.choices[0]['message']['content'] if response.output and response.output.choices else ""
                whole_message += content
                print(content, end='')
            print()
            # 把流式输出的所有消息合成一条输出
            messages.append({'role': 'assistant', 'content': whole_message})
            text_to_speech(whole_message)
            play_audio("output.wav")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
