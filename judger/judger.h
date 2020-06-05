#include <cstring>
#include <stdexcept>
#include <boost/format.hpp>
#include <array>
#include <string>

#define     OK_MESS      "OK"
#define     TLE_MESS     "Time limit exceeded"
#define     MLE_MESS     "Memory limit exceeded"
#define     WA_MESS      "Wrong answer"
#define     RE_MESS      "Runtime error"


class Judger {
private:
	std::string command, input_file, output_file, checker, code_output, mem_lim, time_lim;
	bool exec_command(const std::string &cmd);
	bool exec_result(const std::string &cmd, std::string &result);

public:
	Judger(std::string c, std::string fi, std::string fo, std::string ck, std::string co,
	       std::string ml, std::string tl);
	bool parseParam(int argc, char **argv);
	std::string judge();
};
