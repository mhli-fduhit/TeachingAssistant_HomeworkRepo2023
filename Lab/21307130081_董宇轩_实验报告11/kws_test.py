import serial
import threading
import time
import wave
import numpy as np
import struct
import binascii
import os

result_buffer = ""

threading_end_flag = False

def Receiving():  
    # 接收函数,接收来自串口的结果数据

    global result_buffer # result_buffer是个全局变量
    while True:  # 循环接收数据
        if ser.in_waiting:  
            # 当接收缓冲区中的数据不为空时，按照gbk编码的方式读取数据，并将其push进result_buffer中
            str = ser.read(ser.in_waiting).decode("gbk")
            result_buffer += str
        elif threading_end_flag:
            break

def wavread(path):
    # wav文件解析函数
    # 输入参数path为wav文件的路径
    # 返回的是一个长度为8000的float类型的numpy数组

    wavfile = wave.open(path, "rb")
    params = wavfile.getparams()
    frameswav = params[3]  # 帧数=8000
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.frombuffer(datawav, dtype=np.short)
    if len(datause) < 8000:
        pad_len = 8000 - len(datause)
        pad = np.zeros(pad_len)
        datause = np.hstack((pad, datause))
    
    datause = datause / 1.0 # float类型
    np.savetxt('sample_in.txt', datause, fmt='%0.15f')
    return datause

def transform(datause):
    # 格式转换函数
    # 输入参数datause为wav文件解析后得到的float数组
    # 返回值是转换后的2进制数据
    # 将float类型数组转换成16进制字符串数组
    # 再将16进制字符串数组转换成2进制数据，根据ASCII格式译码

    datause_hex = []
    for i in datause:
        datause_hex.append(struct.pack('>f', i).hex())  # 打包成浮点数的16进制表示
    datause_hex_str = "".join(datause_hex) # 将数组拼成单个字符串
    datause_bin = binascii.unhexlify(datause_hex_str) # 将字符串按照ASCII格式译码得到2进制数据

    return datause_bin

if __name__ == '__main__':
    # 主函数

    word_list = [] # 标签数组
    with open('./ds_rnn_labels.txt', 'r') as f:
        line = f.readline()
        while line:
            word = line.strip('\n')
            word_list.append(word)
            line = f.readline()

    #------------------------step 1------------------------
    # 配置开启串口
    # 并发一个子线程，执行Receiving函数
    ser = serial.Serial('COM5', 115200, timeout=2) # COMx,可以使用设备管理器查看通信端口号
    t1 = threading.Thread(target=Receiving)
    t1.start()

###############################################################################
#------------------------------------CODE HERE---------------------------------
###############################################################################

    #------------------------step 2------------------------
    # 调用wavread函数解析wav文件，得到float类型数组
    # 调用transform函数进行格式转换，得到2进制数据
    total_num = 0
    error_num = 0
    output = open('output.txt','a')
    for folder in os.listdir("./audio"):
        folder_dir = os.path.join("./audio",folder)
        for wavfile in os.listdir(folder_dir):
            wav_dir = os.path.join(folder_dir,wavfile)
            datause = wavread(wav_dir)
            datause_bin = transform(datause)
    #------------------------step 3------------------------
    # 将译码得到的2进制数据写入UART串口
            ser.write(datause_bin)
            time.sleep(1)
    #------------------------step 4------------------------
    # 等待结果缓冲区(result_buffer)的数据,确保发送过去的音频数据被处理完，结果也已经发送回来
    # 根据result_buffer的数据和标签数据得到预测结果，判断预测是否正确
            #print(result_buffer)
            #result_buffer = ""
            while True:
                result = result_buffer.splitlines()
                if len(result) == 12:
                    output.write('wav num:' + wavfile.strip('.wav') + '\nactual keyword: ' + folder)
                    output.write('confidence list:',result)
                    index = result.index(max(result))
                    output.write('predicted keyword: ' + word_list[index])
                    if word_list[index] != folder:
                        error_num += 1
                    total_num += 1
                    output.write("")
                    result_buffer = ""
                    break
    acc = (total_num - error_num) / total_num
    output.write("Summary:\ntotal wav num:%d\ntotal error num:%d\ntotal accuracy:%f" %(total_num,error_num,acc))
    #------------------------step 5------------------------
    # UART串口传输结束后关闭Receiving函数对应的子线程
    # 关闭UART串口
    threading_end_flag = True
    ser.close()


