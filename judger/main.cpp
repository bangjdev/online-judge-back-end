#include "judger.h"
#include "parser.h"
#include <string>

Parser parser;
std::string command, input_file, output_file, time_limit, checker, code_output, mem_lim, time_lim;

int main(int argc, char **argv) {
	parser.addParamMapping("-c|--exec", command);
	parser.addParamMapping("-if|--input", input_file);
    parser.addParamMapping("-of|--output", output_file);
    parser.addParamMapping("-ck|--checker", checker);
    parser.addParamMapping("-uo|--user_output", code_output);
    parser.addParamMapping("-m|--mem_lim", mem_lim);
    parser.addParamMapping("-t|--time_lim", time_lim);
    parser.parseArguments(argc, argv);

    Judger judger(command, input_file, output_file, checker, code_output, mem_lim, time_lim);

    result = judger.judge();
    if (result == TLE_MESS) {
    	return 1;
    }
    if (result == MLE_MESS) {
    	return 2;
    }
    if (result == RE_MESS) {
    	return 3;
    }
    if (result != "") {
    	return 4;	// WA
    }
    return 0;
}