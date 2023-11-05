__version__ = '2.0.0'

import serial
import time
import sys


def nfcsb(chuan, bo, lx=1):
    c = ""

    # port = '8888'
    # pub_server_name = 'bd_rfid'
    # topic = 'BD-RFID-PUB'
    try:
        if lx == 1:
            rfidr_ser = serial.Serial(port=chuan, baudrate=bo, timeout=0.5)
            for i in range(1, 101):
                print("\r", end="")

                print("rfid设备识别中: {}%: ".format(i), "▋" * (i // 2), end="")

                sys.stdout.flush()

                time.sleep(0.005)

            print("\n")
            # print(rfidr_ser.portstr)
            print("端口号:" + rfidr_ser.name)  # 输出串口名称
            print('波率：' + bo)
            if rfidr_ser.isOpen():  # 判断端口是否被打开+
                print('RFID连接成功')

                while True:
                    c = ""
                    count = rfidr_ser.inWaiting()  # 获取串口缓存区数据,返回接收字符串的长度值
                    if count != 0:
                        # recv = rfidr_ser.readlines()
                        # recv = rfidr_ser.readall()
                        recv = rfidr_ser.read(count)  # 读取串口数据
                        # bytes 转十六进制

                        for item in recv:
                            hex_str = ' '
                            hex_str += str(hex(item))[2:].zfill(2).upper()  # 分割字符串，并且大写
                            c += hex_str  # 以空格结束，避免换行、
                        print(c)

                    time.sleep(0.1)  # 延时0.1秒

            serial.Serial.close()
    except Exception:
        print('未发现RFID请尝试更换串口号或波率')
