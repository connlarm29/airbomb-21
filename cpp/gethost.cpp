/*
Quick hostname tool,
gets hostname
-c
*/
#include <stdlib.h>
#include <iostream>
#include <string>
#include <netdb.h>
#include <arpa/inet.h>

using namespace std;

int main(int argc, char *argv[]) {
	
	if(argc>1 && sizeof(argv[1]) <= 16){
		unsigned char in_addr[sizeof(struct in_addr)];
		if(inet_pton(AF_INET,argv[1],in_addr) < 1) {
			cout << "Invalid IP\n";
			return -1;
		}
		struct addrinfo *res=0;
		getaddrinfo(argv[1],0,0,&res);
		char host[512];
		getnameinfo(res->ai_addr,res->ai_addrlen,host,512,0,0,0);
		cout << argv[1] << "Resolved to: \33[37;1m" << host << "\33[0m\n";
		freeaddrinfo(res);
	}
	else {
		cout << "Enter a valid IP!\n";
	}
	return 0;
}
