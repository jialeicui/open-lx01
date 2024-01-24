#include <stdio.h>
#include <sys/inotify.h>
#include <sys/types.h>
#include <curl/curl.h>

CURL *curl;
struct curl_slist *headers = NULL;


int send_context_to_server(const char *context) {
    const char * url = "http://192.168.1.14:8080/message";
    printf("send context to server: %s\n", context);

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, context);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        printf("curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        return -1;
    }

    return 0;
}


int main() {
    const char *instruction_json_path = "/tmp/mico_aivs_lab/instruction.log";

    FILE *json_file = fopen(instruction_json_path, "r");
    fseek(json_file, 0, SEEK_END);
    long laste_offset = ftell(json_file);

    curl = curl_easy_init();
    if (!curl) {
        printf("curl init failed\n");
        return -1;
    }
    headers = curl_slist_append(headers, "Content-Type: application/json");

    int fd = inotify_init();
    if (fd < 0) {
        perror("inotify_init");
        return -1;
    }

    int wd = inotify_add_watch(fd, instruction_json_path, IN_MODIFY);
    if (wd < 0) {
        perror("inotify_add_watch");
        return -1;
    }

    char buf[1024];
    while (1) {
        ssize_t n = read(fd, buf, sizeof(buf));
        if (n < 0) {
            perror("read");
            return -1;
        }
        struct inotify_event *event = (struct inotify_event *)buf;

        // check if file length changed
        fseek(json_file, 0, SEEK_END);
        long current_offset = ftell(json_file);
        if (current_offset == 0) {
            printf("file is reset\n");
            laste_offset = 0;
            continue;
        } else if (current_offset == laste_offset) {
            printf("file length not changed\n");
            continue;
        }

        // read file from last offset
        fseek(json_file, laste_offset, SEEK_SET);
        while (fgets(buf, sizeof(buf), json_file) != NULL) {
            printf("read %s from file\n", buf);
            send_context_to_server(buf);
        }
        laste_offset = ftell(json_file);
    }
    curl_easy_cleanup(curl);

    return 0;
}