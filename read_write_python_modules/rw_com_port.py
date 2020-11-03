import serial
import time
counter_test = 0

trigger_port = None
tracer1_port = None


def write_trigLevel_gain(port: str, triggerLevel: str, gain: str):
    global counter_test, trigger_port
    counter_test += 1
    _port = port.replace(" ", "")
    _triggerLevel = triggerLevel.replace(" ", "").rjust(4, '0')
    _gain = gain.replace(" ", "").rjust(4, '0')
    message = b't' + _triggerLevel.encode('utf-8') + b'.g' + _gain.encode('utf-8') + b'.'
    print(message)
    try:
        if (trigger_port == None):
            trigger_port = serial.Serial(_port)
        trigger_port.write_timeout = 1  # Set write timeout, sec
        trigger_port.write(message)
        return "ok"
    except serial.SerialTimeoutException:
        print("TimeoutException")
        return "TimeoutException"
    except serial.SerialException:
        print("SerialException")
        return "SerialException" + str(counter_test)
    except Exception:
        print("something wrong")
        return "something wrong"

def write_gain(port: str, gain: str):
    global counter_test, tracer1_port
    counter_test += 1
    _port = port.replace(" ", "")
    _triggerLevel = "0".replace(" ", "").rjust(4, '0')
    _gain = gain.replace(" ", "").rjust(4, '0')
    message = b't' + _triggerLevel.encode('utf-8') + b'.g' + _gain.encode('utf-8') + b'.'
    print(message)
    try:
        if (tracer1_port == None):
            tracer1_port = serial.Serial(_port)
        tracer1_port.write_timeout = 1 #Set write timeout, sec
        tracer1_port.write(message)
        return "ok"
    except serial.SerialTimeoutException:
        print("TimeoutException")
        return "TimeoutException"
    except serial.SerialException:
        print("SerialException")
        return "SerialException"  + str(counter_test)
    except Exception:
        print("something wrong")
        return "something wrong"


def read_data_from_port(port):
    data = []

    while len(data) < 1002:
        try:
            port.write(b"req")  # <====================
        except serial.serialutil.SerialTimeoutException:
            print("time over")
        #print("send request...")

        startTime = time.time()
        while not port.inWaiting():
            # print('.')
            if time.time() - startTime > 1:
                #print("much time not in waiting")
                break

        i = 0
        inp = 0
        startTime = time.time()
        while (inp != 254):
            while port.inWaiting():
                # print(ord(port.read()), i)
                inp = ord(port.read())
                data.append(inp)
                # print("reading", i)
                i += 1
            if time.time() - startTime > 1:
                print("much time in trying to read")
                break

        try:
            if data[0] == 255 and data[-1] == 254 and len(data) == 1002:
                break
            else:
                #print("error", "start =", data[0] == 255, "stop =", data[-1] == 254, "len =", len(data))
                data = []
        except Exception:
            print(Exception)
            # a = 0

    port.write(b"ack")
    return data


def read_data_from_all_ports():
    global tracer1_port, trigger_port
    trigger = read_data_from_port(trigger_port)
    tracer1 = read_data_from_port(tracer1_port)
    return [trigger, tracer1]