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
    std::string result;
    // Init sandbox
    std::cout << "cleaning up\n";
    exec_command("isolate --cleanup");    
    exec_result("isolate --init", result);
    std::cout << "init sandbox " << result << "\n";
    exec_command("sudo cp " + command + " " + result + "/box/");

    // Run the program inside sandbox
    std::string isolate_format = "isolate --run -m %1% -t %2% %3% < %4% > %5%";
    std::string isolate_cmd = (boost::format{isolate_format} 
                                                          % mem_lim             
                                                          % time_lim            
                                                          % get_command_name(command)
                                                          % input_file          
                                                          % code_output).str(); 
    std::cout << isolate_cmd << "\n";
    bool success = exec_result(isolate_cmd, result);

    if (!success) {
        return RE_MESS;
    }

    if (result == "Time limit exceeded") {
        return TLE_MESS;
    }

    if (result == "Memory limit exceeded") {
        return MLE_MESS;
    }

    // Verify output
    std::string check_cmd = checker + " " + code_output + " " + output_file;
    exec_result(check_cmd, result);

    // Cleanup
    exec_command("rm " + code_output);

    return result;
}
