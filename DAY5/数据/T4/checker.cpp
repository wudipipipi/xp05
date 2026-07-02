#include "testlib.h"

const double EPS = 1e-2 + 1e-9;

int main(int argc, char *argv[])
{
	registerTestlibCmd(argc, argv);
	double pans = ouf.readDouble();
	double jans = ans.readDouble();
	if (fabs(pans - jans) > EPS)
		quitf(_wa, "expected: '%.3f', found: '%.3f', error = '%.3f'",
                jans, pans, fabs(pans - jans));
	quitf(_ok, "ok");
	return 0;
}