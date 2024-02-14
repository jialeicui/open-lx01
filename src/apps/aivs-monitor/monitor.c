#include <stddef.h>
#include <stdio.h>
#include <sys/inotify.h>
#include "json.h"
#include "monitor.h"

monitor_t g_monitor;
int play_the_original_answer = 0;
int stop = 0;

void wait_for_message_file_ready(const char *file_path) {
    while (access(file_path, F_OK) != 0) {
        usleep(1000 * 1000);
    }
}


void monitor_init(monitor_t monitor) {
    g_monitor = monitor;
}

int monitor_start(const char *file_to_monitor) {
    wait_for_message_file_ready(file_to_monitor);

    int fd = inotify_init();
    if (fd < 0) {
        perror("inotify_init");
        return -1;
    }

    int wd = inotify_add_watch(fd, file_to_monitor, IN_MODIFY);
    if (wd < 0) {
        perror("inotify_add_watch");
        return -1;
    }

    FILE *json_file = fopen(file_to_monitor, "r");
    fseek(json_file, 0, SEEK_END);
    long laste_offset = ftell(json_file);

    muter_t muter = {0};

    char buf[1024];
    while (!stop) {
        ssize_t n = read(fd, buf, sizeof(buf));
        if (n < 0) {
            perror("read");
            return -1;
        }

        int user_sound_final = 0;
        int user_sound_filterd = 0;
        int speaker_muted = 0;

        struct inotify_event *event = (struct inotify_event *)buf;

        // check if file length changed
        fseek(json_file, 0, SEEK_END);
        long current_offset = ftell(json_file);
        if (current_offset == 0) {
            printf("file is reset\n");
            laste_offset = 0;

            user_sound_final = 0;
            user_sound_filterd = 0;
            speaker_muted = 0;
            play_the_original_answer = 0;

            muter.current_round += 1;
            // TODO should be atomic
            muter.thread_processed_rount = muter.current_round;

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

            // the text must contains '"is_final": true,' to make sure it's the final result
            if (user_sound_final == 0 && compare_json_value(buf, "payload.is_final", "true") != 0) {
                printf("not final result\n");
                continue;
            }
            user_sound_final = 1;

            if (user_sound_filterd == 0 && g_monitor.is_blocklist_keyword != NULL && g_monitor.is_blocklist_keyword(buf) == 1 ) {
                printf("blocklist keyword detected\n");
                user_sound_filterd = 1;
                continue;
            }
            user_sound_filterd = 1;

            if (speaker_muted == 0) {
                speaker_muted = 1;
                if (g_monitor.mute_cb != NULL) {
                    g_monitor.mute_cb(&muter);
                }
            }

            if (play_the_original_answer) {
                // try to get the original answer
                char answer[1024 * 2] = {0};
                int rc = get_json_value(buf, "payload.text", answer, 1024 * 2);
                if (rc != 0) {
                    continue;
                }
                if (strlen(answer) != 0) {
                    if (g_monitor.act_tts != NULL) {
                        g_monitor.act_tts(answer);
                    }
                }
                play_the_original_answer = 0;
            }

            if (g_monitor.send_to_remote != NULL) {
                g_monitor.send_to_remote(buf);
            }
        }
        laste_offset = ftell(json_file);
    }
}

void monitor_stop() {
    stop = 1;
}
