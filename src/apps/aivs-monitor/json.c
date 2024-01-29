#include <json-c/json.h>
#include <string.h>
#include <stdio.h>

const int BUFFER_SIZE = 1024;

int get_json_value(const char* json_str, const char* path, char* value_buf, int buf_size) {
    int index = -1;
    char tmp_path[BUFFER_SIZE];
    char* pch;
    struct json_object* parsed_json;
    struct json_object* tmp_json_obj;

    // "payload.results[0].text" -> "payload.results.text", index = 0
    strcpy(tmp_path, path);
    pch = strchr(tmp_path, '['); 
    if(pch != NULL){
        sscanf(pch, "[%d]", &index);
        *pch = '\0';  // cut the string
    }

    parsed_json = json_tokener_parse(json_str);
    if (parsed_json == NULL) {
        printf("Json parse error\n");
        return -1;
    }

    tmp_json_obj = parsed_json;
    pch = strtok(tmp_path, "."); // split by '.'
    while (pch != NULL) {
        if (json_object_object_get_ex(tmp_json_obj, pch, &tmp_json_obj)) {
            if (index != -1 && json_object_get_type(tmp_json_obj) == json_type_array) {
                int array_len = json_object_array_length(tmp_json_obj);
                if (index >= array_len) {
                    printf("Json index error\n");
                    json_object_put(parsed_json);
                    return -1;
                }
                tmp_json_obj = json_object_array_get_idx(tmp_json_obj, index);
            }
        } else {
            printf("Json path error at: %s\n", pch);
            json_object_put(parsed_json);
            return -1;
        }
        pch = strtok(NULL, ".");
    }

    const char *value_str = json_object_get_string(tmp_json_obj);
    if (value_str == NULL) {
        printf("Json value error\n");
        json_object_put(parsed_json);
        return -1;
    }
    strncpy(value_buf, value_str, buf_size - 1);
    value_buf[buf_size - 1] = '\0';

    // clean up and free memory
    json_object_put(parsed_json);

    return 0;
}

int compare_json_value(const char *json_str, const char *path, const char *value) {
    int value_size = strlen(value);
    char *buf = malloc(value_size + 1);
    get_json_value(json_str, path, buf, value_size + 1);
    return strcmp(buf, value);
}