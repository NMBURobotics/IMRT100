
print("Hello")
f = open("/dev/input/js0", "rb")

try:
    while True:
        line = f.readline()
        for byte in line:
            print(line)
            if (byte == ord('\n')):
                print(byte, "is a newline\n\n\n\n")
        print(type(line))
except KeyboardInterrupt:
    print("Bye")

f.close()
    
