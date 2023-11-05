这是一个通过serial库访问开发板（rfid）的整合库
本库只有一个函数:nfssb()
示例代码：
import rfid
print(rfid.nfcsb('设备串口号','波率')
如果您不使用本库您将编写的代码为：
import serial
import time
import sys
rfidr_ser = serial.Serial(port=chuan, baudrate=bo, timeout=0.5)
            if rfidr_ser.isOpen():  # 判断端口是否被打开+
                print('RFID连接成功')

                while True:
                    c=""
                    count = rfidr_ser.inWaiting()  # 获取串口缓存区数据,返回接收字符串的长度值
                    if count != 0:
                        # recv = rfidr_ser.readlines()
                        # recv = rfidr_ser.readall()
                        recv = rfidr_ser.read(count)  # 读取串口数据
                        # bytes 转十六进制

                        for item in recv:
                            hex_str = ' '
                            hex_str += str(hex(item))[2:].zfill(2).upper()  # 分割字符串，并且大写
                            c+=hex_str # 以空格结束，避免换行、
                        print(c)

                    time.sleep(0.1)  # 延时0.1秒

            serial.Serial.close()
