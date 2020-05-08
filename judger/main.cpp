#include "judger.h"
#include <iostream>

Judger judger;

int main(int argc, char **argv) {
    if (!judger.parseParam(argc, argv)) {
        std::cout << "Invalid params";
        return -1;
    }
    std::cout << judger.judge();
    return 0;
}
