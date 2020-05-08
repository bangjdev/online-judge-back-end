#include "judger.h"

Judger::Judger() {
    command = "";
    input_file = "";
    output_file = "";
    code_output = "code_output.tmp";
    mem_lim = "256000";
    time_lim = "1";
    checker = "diffcheck";
}

bool Judger::parseParam(int argc, char **argv) {
    for (int i = 1; i < argc; i ++) {
        if (strcmp(argv[i], "-c")) {
            if (i + 1 < argc) {
                command = argv[i];
            } else {
                return false;
            }
        }
        if (strcmp(argv[i], "-i")) {
            if (i + 1 < argc) {
                input_file = argv[i];
            } else {
                return false;
            }
        }
        if (strcmp(argv[i], "-o")) {
            if (i + 1 < argc) {
                output_file = argv[i];
            } else {
                return false;
            }
        }
        if (strcmp(argv[i], "-m")) {
            if (i + 1 < argc) {
                mem_lim = argv[i];
            } else {
                return false;
            }
        }
        if (strcmp(argv[i], "-t")) {
            if (i + 1 < argc) {
                time_lim = argv[i];
            } else {
                return false;
            }
        }
    }
    return true;
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

    return (pclose(pipe) == EXIT_SUCCESS);
}

std::string Judger::judge() {
    std::string result;
    // Init sandbox
    exec_command("isolate --cleanup");
    exec_result("isolate --init", result);
    exec_command("sudo mv " + command + " " + result + "/box/");

    // Run the program inside sandbox
    std::string isolate_format = "isolate --run -m=%1% -t=%2% %3% < %4% > %5%";
    std::string isolate_cmd = (boost::format{isolate_format} 
                                                          % mem_lim             
                                                          % time_lim            
                                                          % command             
                                                          % input_file          
                                                          % code_output).str(); 
    bool success = exec_result(isolate_cmd, result);

    if (!success) {
        return RE_MESS; 
    }

    if (result == "Time limit exceeded") {
        return TLE_MESS;
    }

    // Verify output
    std::string check_cmd = checker + " " + code_output + " " + output_file;
    exec_result(check_cmd, result);

    // Cleanup
    exec_command("mv " + code_output);

    return result;
}
