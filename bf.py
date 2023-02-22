import sys

class BrainfuckInterpreter:
    def __init__(self):
        self.DATA_SIZE = 30000
        self.program = ''
        self.data = [0] * self.DATA_SIZE
        self.data_ptr = 0
        self.code_ptr = 0
        self.loop_stack = []
        self.jump_table = {}

    def load_program(self, filename):
        with open(filename, 'r') as f:
            self.program = ''.join(filter(lambda c: c in ['>', '<', '+', '-', '.', ',', '[', ']'], f.read()))
        self.data = [0] * self.DATA_SIZE
        self.data_ptr = 0
        self.code_ptr = 0
        self.loop_stack = []
        self.jump_table = {}
        self.build_jump_table()

    def build_jump_table(self):
        stack = []
        for i, c in enumerate(self.program):
            if c == '[':
                stack.append(i)
            elif c == ']':
                start = stack.pop()
                self.jump_table[start] = i
                self.jump_table[i] = start

    def interpret(self, instruction):
        if instruction == '>':
            self.data_ptr += 1
        elif instruction == '<':
            self.data_ptr -= 1
        elif instruction == '+':
            self.data[self.data_ptr] += 1
        elif instruction == '-':
            self.data[self.data_ptr] -= 1
        elif instruction == '.':
            sys.stdout.write(chr(self.data[self.data_ptr]))
        elif instruction == ',':
            self.data[self.data_ptr] = ord(sys.stdin.read(1))
        elif instruction == '[':
            if self.data[self.data_ptr] == 0:
                self.code_ptr = self.jump_table[self.code_ptr]
            else:
                self.loop_stack.append(self.code_ptr)
        elif instruction == ']':
            if self.data[self.data_ptr] != 0:
                self.code_ptr = self.loop_stack[-1]
            else:
                self.loop_stack.pop()
        else:
            pass

    def run(self):
        while self.code_ptr < len(self.program):
            instruction = self.program[self.code_ptr]
            self.interpret(instruction)
            self.code_ptr += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 bf.py program.bf")
        exit(1)

    filename = sys.argv[1]
    interpreter = BrainfuckInterpreter()
    interpreter.load_program(filename)
    interpreter.run()
