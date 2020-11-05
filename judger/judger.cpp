#include "judger.h"
#include <iostream>

Judger::Judger(std::string c, std::string fi, std::string fo, std::string ck, std::string co,
           std::string ml, std::string tl) {
    command = c;
    input_file = fo;
    output_file = fo;
    code_output = co;
    mem_lim = ml;
    time_lim = tl;
    checker = ck;
}

bool Judger::exec_command(const std::string &cmd) {
    std::array<char, 256> buffer;

    auto pipe = popen(cmd.c_str(), "r");

    if (!pipe) {
        return false;
    }

    return (pclose(pipe) == EXIT_SUCCESS);
}

bool Judger::exec_result(const std::string &cmd, std::string &result) {
    std::array<char, 256> buffer;
    result = "";

    auto pipe = popen(cmd.c_str(), "r");

    if (!pipe) {
        return false;
    }

    while (!feof(pipe)) {
        // std::cout << "\nasdfasdf\n";
        if (fgets(buffer.data(), 128, pipe) != nullptr)
            result += buffer.data();
    }

    while (result[result.length() - 1] == '\n') {
        result.pop_back();
    }

    return (pclose(pipe) == EXIT_SUCCESS);
}

std::string get_command_name(std::string command_path) {
    std::string r = "";
    while (command_path[command_path.length() - 1] != '/') {
        r = command_path[command_path.length() - 1] + r;
        command_path.pop_back();
    }
    return r;
}

std::string Judger::judge() {
    std::string result = "";
    // Init sandbox
    // exec_command("isolate --cleanup");
    // exec_result("isolate --init", result);
    // exec_command("sudo cp " + command + " " + result + "/box/");

    // Run the program inside sandbox
    // std::cout << "asdf" << command << "\n";
    std::string isolate_format = "judger/timeout/timeout -t %1% -m %2% \"%3% < %4% > %5%\"  2>&1";
    std::string isolate_cmd = (boost::format{isolate_format}
                                                          % time_lim
                                                          % mem_lim
                                                          % command
                                                          % input_file
                                                          % code_output).str();
    // std::cout << "Running: " << isolate_cmd << "\n\n";
    bool success = exec_result(isolate_cmd, result);

    // std::cout << "Status: " << success << "\n\nTIMOUT RESPONSE: " << result << "\n\n";

    if (!success) {
        return RE_MESS;
    }

    if (result.rfind("TIMEOUT", 0) == 0) {
        std::cout << "Timeout\n";
        return TLE_MESS;
    }

    if (result.rfind("MEM", 0) == 0) {
        std::cout << "Mem\n";
        return MLE_MESS;
    }

    // Verify output
    std::string check_cmd = checker + " " + code_output + " " + output_file;
    exec_result(check_cmd, result);

    // Cleanup
    exec_command("rm " + code_output);

    return result;
}
