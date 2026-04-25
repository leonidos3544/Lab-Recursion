#!/usr/bin/env python3
import os

cpp_code = """#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

class BashBuilder {
    std::ostringstream out;
    int indent_level = 0;
    std::string indent() const { return std::string(indent_level * 4, ' '); }

public:
    BashBuilder& raw(std::string line) {
        out << indent() << line << "\\n";
        return *this;
    }

    BashBuilder& shebang() { return raw("#!/bin/bash"); }

    BashBuilder& assign(std::string var, std::string expr) {
        out << indent() << var << "=" << expr << "\\n";
        return *this;
    }

    BashBuilder& if_stmt(std::string cond) {
        out << indent() << "if [ " << cond << " ]" << "\\n";
        indent_level++;
        out << indent() << "then" << "\\n";
        return *this;
    }

    BashBuilder& else_stmt() {
        indent_level--;
        out << indent() << "else" << "\\n";
        indent_level++;
        return *this;
    }

    BashBuilder& fi() {
        indent_level--;
        out << indent() << "fi" << "\\n";
        return *this;
    }

    BashBuilder& echo(std::string msg) {
        out << indent() << "echo \\"" << msg << "\\"\\n";
        return *this;
    }

    BashBuilder& elif_(std::string cond) {
        indent_level--;
        out << indent() << "elif [[ " << cond << " ]]" << "\\n";
        indent_level++;
        out << indent() << "then" << "\\n";
        return *this;
    }

    std::string build() const { return out.str(); }
};

std::string generate_dz_script() {
    BashBuilder sh;
    sh.shebang()
      .assign("player", "$1")
      .assign("z", "$((RANDOM % 100))")
      .assign("b", "$((RANDOM % 25 + 42))")
      .if_stmt("\\"$z\\" -lt \\"$b\\"")
          .assign("game", "0")
      .else_stmt()
          .assign("game", "1")
      .fi()
      .if_stmt("\\"$game\\" -eq 1")
          .assign("q", "$((RANDOM % 3))")
          .raw("options=(\\"камень\\" \\"ножницы\\" \\"бумага\\")")
          .assign("comp", "${options[q]}")
          .if_stmt("\\"$comp\\" = \\"$player\\"")
              .echo("ничья")
          .elif_("\\"$player\\" = \\"камень\\" && \\"$comp\\" = \\"ножницы\\" || \\"$player\\" = \\"ножницы\\" && \\"$comp\\" = \\"бумага\\" || \\"$player\\" = \\"бумага\\" && \\"$comp\\" = \\"камень\\"")
              .echo("Вы победили!")
          .else_stmt()
              .echo("Вы проиграли!")
          .fi()
      .fi()
      .if_stmt("\\"$game\\" -eq 0")
          .if_stmt("\\"$player\\" = \\"камень\\"")
              .echo("компьютер выбрал бумагу, вы проиграли")
          .elif_("\\"$player\\" = \\"ножницы\\"")
              .echo("компьютер выбрал камень, вы проиграли")
          .else_stmt()
              .echo("компьютер выбрал ножницы, вы проиграли")
          .fi()
      .fi();
    return sh.build();
}

int main() {
    const std::string filename = "DZ_generated.sh";
    std::string script_content = generate_dz_script();
    std::ofstream out_file(filename, std::ios::binary);
    if (!out_file) { std::cerr << "Error\\n"; return 1; }
    out_file << script_content;
    out_file.close();
    system(("chmod +x " + filename).c_str());
    std::cout << "Generated: " << filename << "\\n";
    return 0;
}"""

hex_data = cpp_code.encode('utf-8').hex()
lines = [hex_data[i:i + 100] for i in range(0, len(hex_data), 100)]

hex_lines = 'HEX="' + lines[0] + '"\n'
for line in lines[1:]:
    hex_lines += 'HEX+="' + line + '"\n'

bash_script = f"""#!/bin/bash
{hex_lines}
for ((i=0; i<${{#HEX}}; i+=2)); do
    printf "\\x${{HEX:$i:2}}"
done > generator.cpp
chmod +x generator.cpp
echo "C++ файл успешно расшифрован из Hex: generator.cpp"
"""

with open("generator_creator_hex.sh", "w") as f:
    f.write(bash_script)

os.chmod("generator_creator_hex.sh", 0o755)
print("Bash script created: generator_creator_hex.sh")
