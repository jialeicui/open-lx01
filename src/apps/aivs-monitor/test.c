#include <stdio.h>
#include <pthread.h>

#include "CuTest.h"
#include "monitor.h"

void stop_monitor(void *args) {
	sleep(1);
	const char *file = (const char *)args;
	// insert new line to the dst file to make the inotify event
	FILE *fp = fopen(file, "a");
	fputs("\n", fp);
	fclose(fp);

	monitor_stop();
}

void copy_file_by_line(const char *src, const char *dst) {
	FILE *src_fp = fopen(src, "r");
	FILE *dst_fp = fopen(dst, "w");
	char buf[1024];
	while (fgets(buf, sizeof(buf), src_fp) != NULL) {
		fputs(buf, dst_fp);
	}
	fclose(src_fp);
	fclose(dst_fp);
}

void copy_file_in_thread(void *args) {
	const char **params = (const char **)args;
	copy_file_by_line(params[0], params[1]);
}

void TestFoo(CuTest* tc) {
	monitor_t monitor = {
		.mute_cb = NULL,
		.act_tts = NULL,
		.send_to_remote = NULL,
		.is_blocklist_keyword = NULL
	};

	const char *src = "test.json";
	const char *dst = "test.json.tmp";

	// touch dst file
	FILE *fp = fopen(dst, "w");
	fclose(fp);

	monitor_init(monitor);

	pthread_t tid1 = 0;
	pthread_create(&tid1, NULL, stop_monitor, dst);

	const char *params[] = {src, dst};
	pthread_t tid2 = 0;
	pthread_create(&tid2, NULL, copy_file_in_thread, (void *)params);

	monitor_start(dst);

	// remove the tmp file
	remove(dst);

	CuAssertTrue(tc, 1);
}

CuSuite* CuGetSuite() {
    CuSuite* suite = CuSuiteNew();
    SUITE_ADD_TEST(suite, TestFoo);
}

int RunAllTests() {
	CuString *output = CuStringNew();
	CuSuite* suite = CuSuiteNew();

	CuSuiteAddSuite(suite, CuGetSuite());

	CuSuiteRun(suite);
	CuSuiteSummary(suite, output);
	CuSuiteDetails(suite, output);
	printf("%s\n", output->buffer);
	return suite->failCount;
}

int main(void) {
	return RunAllTests();
}
