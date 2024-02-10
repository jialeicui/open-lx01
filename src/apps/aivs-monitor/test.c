#include <stdio.h>

#include "CuTest.h"

void TestFoo(CuTest* tc) {
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
