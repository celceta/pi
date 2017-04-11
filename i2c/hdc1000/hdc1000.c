/* #define USE_RDY_PIN */

#include <stdio.h>
#include <unistd.h>
#include <wiringPi.h>

#ifdef USE_RDY_PIN
#include <wiringPiI2C.h>
#define RDY_PIN					(4)
#endif

#define ADDRESS					(0x40)

#define TEMPERATURE_POINTER		(0x00)
#define HUMIDITY_POINTER		(0x01)
#define CONFIGURATION_POINTER	(0x02)
#define SERIAL_ID1_POINTER		(0xfb)
#define SERIAL_ID2_POINTER		(0xfc)
#define SERIAL_ID3_POINTER		(0xfd)
#define MANUFACTURER_ID_POINTER	(0xfe)
#define DEVICE_ID_POINTER		(0xff)

#define CONFIGURE_MSB			(0x10)
#define CONFIGURE_LSB			(0x00)


int main(int argc, char *argv[])
{
	int fd;
	int ret;

	int tData;					/* temperature	*/
	int hData;					/* humidity		*/

	unsigned char result[4];
	unsigned char set_value[3];
	unsigned char get_value[1];

#ifdef USE_RDY_PIN
	/* setup RDY-pin */
	wiringPiSetupGpio();
	pinMode(RDY_PIN, INPUT);
#endif

	/* setup I2C */
	fd = wiringPiI2CSetup(ADDRESS);

	if(argc == 2 && (strcmp(argv[1], "reset") == 0)){
		printf("resetting... ");
		set_value[0] = CONFIGURATION_POINTER;
		set_value[1] = CONFIGURE_MSB;
		set_value[2] = CONFIGURE_LSB;

		ret = write(fd, set_value, 3);
		if (ret < 0) {
			fprintf(stderr, "error: set configuration value\n");
			return __LINE__;
		} 

		printf("done.\n");
		return 0;
	}

	/* get Temperature and Humidity together */
	get_value[0] = TEMPERATURE_POINTER;
	ret = write(fd, get_value, 1);
	if(ret < 0){
		fprintf(stderr, "error: get value\n");
		return __LINE__;
	}

	/* wait */
#ifdef USE_RDY_PIN
	while(digitalRead(RDY_PIN) == 1){
		;
	}
#else
	usleep(20 * 1000);
#endif

	/* get result values */
	ret = read(fd, result, 4);
	if(ret < 0){
		fprintf(stderr, "error: read value\n");
		return __LINE__;
	}

	/* calculate */
	tData = result[0] << 8; tData |= result[1];
	hData = result[2] << 8; hData |= result[3];
	printf("%.2f %.2f\n", ((tData / (double)0x10000 * 165.) - 40.), (hData / (double)0x10000 * 100.));

	return 0;
}
