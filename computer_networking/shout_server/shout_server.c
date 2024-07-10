#include <sys/socket.h>
#include <stdio.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

char *capitalize(char buff[], int len) {
    char *result = malloc(len);

    for (int i = 0; i < len; i++) {
        result[i] = toupper((unsigned char) buff[i]);
    }

    return result;
}

int main() {
    int status;
    char *port = "3490";
    struct addrinfo hints;
    struct addrinfo *servinfo;
    socklen_t addr_size;
    struct sockadd_storage *their_addr;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC; // IPv4 or IPv4, doesn't matter
    hints.ai_socktype = SOCK_STREAM; // TCP connection
    hints.ai_flags = AI_PASSIVE;

    if ((status = getaddrinfo(NULL, port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(1);
    }

    int sockfd = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo->ai_protocol);
    int bind_result = bind(sockfd, servinfo->ai_addr, servinfo->ai_addrlen);
    if (bind_result == -1) {
        printf("Error while binding to port: %s\n", port);
        exit(1);
    }

    listen(sockfd, 1);
    addr_size = sizeof(their_addr);

    while (1) {
        char buff[2048];
        int req_fd = accept(sockfd, (struct sockaddr *) &their_addr, &addr_size);
        int bytes_read = recv(req_fd, buff, 2048, 0);

        char *capitalized = capitalize(buff, bytes_read);
        send(req_fd, capitalized, bytes_read, 0);

        free(capitalized);
        shutdown(req_fd, 2);
    }
}