#include "parser_utils.h"
#include <regex>


std::vector<std::string> split(std::string str, const std::string &delimiter) {
    std::regex delimRegex("([" + delimiter + "])");
    std::regex_token_iterator<std::string::iterator> itEnd;
    std::regex_token_iterator<std::string::iterator> it(str.begin(), str.end(), delimRegex, -1);

    std::vector<std::string> splitResult;

    while (it != itEnd) {
        std::string flag = trim(*it);
        if (flag != "") {
            splitResult.push_back(flag);
        }
        it ++;
    }
    return splitResult;
}


std::string leftTrim(const std::string& str) {
    return std::regex_replace(str, std::regex("^\\s+"), "");
}

std::string rightTrim(const std::string& str) {
    return std::regex_replace(str, std::regex("\\s+$"), "");
}

std::string trim(const std::string& str) {
    return leftTrim(rightTrim(str));
}