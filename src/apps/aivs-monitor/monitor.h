#include <unistd.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int current_round;
    int thread_processed_rount;
} muter_t;

typedef struct {
    void (*mute_cb)(muter_t *muter);
    void (*act_tts)(const char *text);
    int (*is_blocklist_keyword)(const char *text);
    void (*send_to_remote)(const char *data);
} monitor_t;

void monitor_init(monitor_t monitor);
int monitor_start(const char *file_to_monitor);
void monitor_stop();
