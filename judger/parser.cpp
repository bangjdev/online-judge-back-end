#include "parser.h"
#include <cstring>
#include <string>
#include <iostream>

Parser::Parser() {
    this->paramsMap.clear();
    this->flagsList.clear();
}

// Get current params map
std::map<std::string, std::string&> Parser::getParamsMap() {
    return this->paramsMap;
}

// Set the delimiter for multi-flag parameter
void Parser::setDelimiter(const std::string &delim) {
    this->delimiter = delim;
}

// Get the current delimiter
std::string Parser::getDelimiter() {
    return this->delimiter;
}

void Parser::addParamMapping(const std::string &flags, std::string &variable) {
    std::vector<std::string> newFlags = split(flags, this->delimiter);
    for (const std::string &newFlag : newFlags) {
        this->flagsList.push_back(newFlag);
    }

    for (std::string &flag: flagsList) {
        this->paramsMap.insert(std::pair<std::string, std::string&>(flag, variable));
    } 
}

void Parser::parseArguments(int argc, char **argv)  {
    std::map<std::string, std::string&>::iterator mapping;
    for (int i = 0; i < argc; i ++) {
        for (std::string &flag : this->flagsList) {
            if (strcmp(flag.c_str(), argv[i]) == 0) {
                if (i + 1 < argc) {
                    mapping = paramsMap.find(flag);
                    if (mapping != paramsMap.end()) {
                        (*mapping).second = argv[i + 1];
                    }
                }
                break;
            }
        }
    }
}