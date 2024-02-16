#include <stdio.h>
#include <sys/types.h>
#include <pthread.h>
#include <curl/curl.h>
#include "json.h"
#include "monitor.h"

const char *instruction_json_path = "/tmp/mico_aivs_lab/instruction.log";
const char *default_server_url = "http://10.0.0.196:8007/message";
const char *config_file = "/data/aivs_monitor/config.json";

// full match
const char *keywords[] = {
    "停",
    "关灯",
    "开灯",
    "几点了",
};

CURL *curl;
const char *final_url = NULL;
struct curl_slist *headers = NULL;

void speaker_pause() {
    // ubus call mediaplayer player_play_operation {\"action\":\"pause\"}
    int rc = system("/bin/ubus call mediaplayer player_play_operation {\\\"action\\\":\\\"pause\\\"}");
    if (rc != 0) {
        printf("pause speaker failed\n");
    }
}

int is_blocklist_keyword(const char *text) {
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

void act_tts(const char *text) {
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

/**
 * Response model:
 * {
 *    "code": 0,
 *    "data": {
 *      "action": "tts", // required, tts or ignore
 *      "tts": "你好" // optional
 *    }
 * }
 */
size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    printf("response: %s\n", ptr);
    size_t body_size = size * nmemb;

    char action_buf[16] = {0};
    int rc = get_json_value(ptr, "data.action", action_buf, 16);
    if (rc != 0) {
        printf("get action failed\n");
        return body_size;
    }

    if (strcmp(action_buf, "ignore") == 0) {
        printf("ignore this answer\n");
        return body_size;
    }

    char buf[1024 * 2] = {0};
    rc = get_json_value(ptr, "data.tts", buf, 1024 * 2);
    if (rc != 0) {
        printf("get tts failed\n");
        return body_size;
    }
    if (strlen(buf) == 0) {
        printf("tts is empty, use the original answer\n");
        return body_size;
    }

    act_tts(buf);
    return body_size;
}


int send_context_to_server(const char *url, const char *context) {
    printf("send context to server: %s\n", context);

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, context);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
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

void *mute_speaker_thread(void *arg) {
    muter_t *muter = (muter_t *)arg;
    // dead loop and wait for tts playing and pause it
    for (;;) {
        if (speaker_playing()) {
            speaker_pause();
            break;
        }
        if (muter->current_round != muter->thread_processed_rount) {
            // TODO should be atomic
            muter->thread_processed_rount = muter->current_round;
            break;
        }
        usleep(1000 * 100);
    }

    printf("mute speaker thread exit\n");
}

const char* get_server_url() {
    if (final_url != NULL) {
        return final_url;
    }

    // read the whole config file
    FILE *fp = fopen(config_file, "r");
    if (fp == NULL) {
        printf("open config file failed\n");
        final_url = default_server_url;
        return default_server_url;
    }

    char buf[1024] = {0};
    fread(buf, sizeof(buf), 1, fp);
    fclose(fp);

    const char *path = "server";
    char *server = calloc(1, 512);  // long enough?
    int rc = get_json_value(buf, path, server, 512);
    if (rc != 0) {
        printf("get server url failed\n");
        final_url = default_server_url;
        return default_server_url;
    }
    printf("server url: %s\n", server);
    final_url = server;
    return server;
}

void mute_cb(muter_t *muter) {
    printf("mute speaker\n");
    pthread_t tid;
    pthread_create(&tid, NULL, mute_speaker_thread, muter);
}

void send_context(const char *data) {
    const char *url = get_server_url();
    send_context_to_server(url, data);
}

int main() {
    curl = curl_easy_init();
    if (!curl) {
        printf("curl init failed\n");
        return -1;
    }
    headers = curl_slist_append(headers, "Content-Type: application/json");

    monitor_t monitor = {
        .mute_cb = mute_cb,
        .act_tts = act_tts,
        .is_blocklist_keyword = is_blocklist_keyword,
        .send_to_remote = send_context,
    };

    monitor_init(monitor);
    monitor_start(instruction_json_path);

    curl_easy_cleanup(curl);

    return 0;
}
