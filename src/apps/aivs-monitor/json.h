#pragma once

/**
 * @brief Get value from json string by path
 * only support json object and array(one dimension)
 * e.g. json_str: {"payload":{"results":[{"text":"你好","is_final":true,"confidence":0.9999998807907104}],"status":0}}
 *     path: payload.results[0].text
 *    value_buf: 你好
 * @param json_str json string
 * @param path json path
 * @param value_buf value buffer
 * @param buf_size value buffer size
 * @return int 0: success, -1: failed
 * @note the value_buf must be large enough to hold the value
 */
extern int get_json_value(const char *json_str, const char *path, char *value_buf, int buf_size);

/**
 * @brief Compare the value from json string by path
 * @param json_str json string
 * @param path json path
 * @param value value to compare
 * @return int 0: equal, non-zero: not equal
 */
extern int compare_json_value(const char *json_str, const char *path, const char *value);