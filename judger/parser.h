#include "parser_utils.h"
#include <map>
#include <vector>

class Parser {
    private:
        std::map<std::string, std::string&> paramsMap;
        std::vector<std::string> flagsList;
        std::string delimiter = "|";

    public:
        Parser();
        std::map<std::string, std::string&> getParamsMap();
        void addParamMapping(const std::string&, std::string&);
        void parseArguments(int, char**);
        std::string getDelimiter();
        void setDelimiter(const std::string&);
};