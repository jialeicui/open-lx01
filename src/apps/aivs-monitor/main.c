#include <stdio.h>
#include <sys/inotify.h>
#include <sys/types.h>
#include <curl/curl.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>

CURL *curl;
struct curl_slist *headers = NULL;
int current_round = 0;
int thread_processed_rount = 0;
const char *instruction_json_path = "/tmp/mico_aivs_lab/instruction.log";
const char *default_server_url = "http://10.0.0.196:8007/message";
// full match
const char *keywords[] = {
    "停",
    "关灯",
    "开灯",
};

void speaker_pause() {
    // ubus call mediaplayer player_play_operation {\"action\":\"pause\"}
    int rc = system("/bin/ubus call mediaplayer player_play_operation {\\\"action\\\":\\\"pause\\\"}");
    if (rc != 0) {
        printf("pause speaker failed\n");
    }
}

int is_blocklist_keyword(const char *text) {
    // the text must contains '"is_final": true,' to make sure it's the final result
    if (strstr(text, "\"is_final\":true,") == NULL) {
        return 0;
    }

    // TODO pass the keywords from the outside to make it more flexible and configurable
    int len = sizeof(keywords) / sizeof(keywords[0]);
    for (int i = 0; i < len; i++) {
        char buf[1024] = {0};
        // the text must contains the '"text":"{text}"}'
        int rc = snprintf(buf, sizeof(buf), "\"text\":\"%s\"}", keywords[i]);
        if (rc < 0) {
            printf("snprintf failed\n");
            continue;
        }
        printf("check contains %s\n", buf);
        if (strstr(text, buf) != NULL) {
            return 1;
        }
    }
    return 0;
}

int speaker_playing() {
    char *cmd = "/bin/ubus call mediaplayer player_get_play_status";
    FILE *fp = NULL;
    char buf[1024] = {0};
    if ((fp = popen(cmd, "r")) == NULL) {
        printf("popen failed\n");
        return -1;
    }
    while (fgets(buf, sizeof(buf), fp) != NULL) {
        printf("ubus output: %s\n", buf);
        // 0 means no media playing, 1 means playing, 2 means paused
        if (strstr(buf, "\\\"status\\\": 1,") != NULL) {
            pclose(fp);
            return 1;
        }
    }

    pclose(fp);
    return 0;
}

void act_tts(char *text) {
    printf("tts: %s\n", text);
    // ubus call mibrain text_to_speech "{\"text\":\"text\",\"save\":0}"
    // use system() to call ubus command
    char cmd[1024 * 10] = {0};
    snprintf(cmd, sizeof(cmd), "/bin/ubus call mibrain text_to_speech \"{\\\"text\\\":\\\"%s\\\",\\\"save\\\":0}\"", text);
    int rc = system(cmd);
    if (rc != 0) {
        printf("tts failed\n");
    }
}

size_t write_callback(char *ptr, size_t size, size_t nmemb, char *userdata) {
    printf("response: %s\n", ptr);
    size_t body_size = size * nmemb;
    strncat(userdata, ptr, body_size);
    if (body_size > 2) {
        userdata[body_size - 2] = '\0';
        act_tts(userdata + 1);
    }
    return body_size;
}


int send_context_to_server(const char *url, const char *context) {
    printf("send context to server: %s\n", context);
    char body_buffer[1024 * 2] = {0};

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, context);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &body_buffer);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        printf("curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        return -1;
    }
    // check response status code
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("response code: %ld\n", response_code);
        return -1;
    }

    return 0;
}

void mute_speaker_thread(void *arg) {
    // dead loop and wait for tts playing and pause it
    for (;;) {
        if (speaker_playing()) {
            speaker_pause();
            break;
        }
        if (current_round != thread_processed_rount) {
            thread_processed_rount = current_round;
            break;
        }
        usleep(1000 * 100);
    }

    printf("mute speaker thread exit\n");
}

void wait_for_message_file_ready() {
    // wait for message file ready
    while (access(instruction_json_path, F_OK) != 0) {
        usleep(1000 * 1000);
    }
}

const char* get_server_url() {
    const char *file = "/data/aivs_monitor/server_url";
    FILE *fp = fopen(file, "r");
    if (fp == NULL) {
        printf("open file %s failed, use default\n", file);
        return default_server_url;
    }

    char *buf = calloc(1, 1024);
    while (fgets(buf, 1024, fp) != NULL) {
        break;
    }
    fclose(fp);
    return buf;
}

int main() {
    wait_for_message_file_ready();

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

    const char *server_url = get_server_url();

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
            current_round += 1;
            thread_processed_rount = current_round;

            continue;
        } else if (current_offset == laste_offset) {
            printf("file length not changed\n");
            continue;
        }

        // read file from last offset
        fseek(json_file, laste_offset, SEEK_SET);
        while (fgets(buf, sizeof(buf), json_file) != NULL) {
            printf("read %s from file\n", buf);
            // lines contains ',"name":"Speak",' means tts, ignore it
            if (strstr(buf, ",\"name\":\"Speak\",") != NULL) {
                continue;
            }

            const char* final_sig = "\"is_final\":true,";
            if (strstr(buf, final_sig) == NULL) {
                printf("not final result\n");
                continue;
            }

            if (is_blocklist_keyword(buf)) {
                printf("blocklist keyword detected\n");
                continue;
            }

            pthread_t tid;
            int rc = pthread_create(&tid, NULL, (void *)mute_speaker_thread, NULL);
            if (rc != 0) {
                printf("create thread failed\n");
            }

            send_context_to_server(server_url, buf);
        }
        laste_offset = ftell(json_file);
    }
    curl_easy_cleanup(curl);

    return 0;
}
