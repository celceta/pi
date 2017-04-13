TARGET=i2c_hdc1000
OBJS=i2c_hdc1000.o
LIBS=wiringPi

$(TARGET): $(OBJS)
	$(CC) -Wall -o $@ $(OBJS) -l $(LIBS)

all: $(TARGET)

clean:
	-rm -f $(TARGET) $(OBJS)

install:
	cp -p $(TARGET) /usr/local/bin
	chmod 755 /usr/local/bin/`basename "$(TARGET)"`
