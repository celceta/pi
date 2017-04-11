TARGET=hdc1000
OBJS=hdc1000.o
LIBS=wiringPi

$(TARGET): $(OBJS)
	$(CC) -Wall -o $@ $(OBJS) -l $(LIBS)

all: $(TARGET)

clean:
	-rm -f $(TARGET) $(OBJS)

