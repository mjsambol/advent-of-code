class Program:
    def __init__(self):
        self.program = []

        with open("dec08in.txt") as in_file:
            for line in in_file:
                parts = line.strip().split(' ')
                self.program.append([parts[0], int(parts[1])])

    def run(self):
        accumulator, next_instruction_num = 0, 0
        visited_instructions = []

        while next_instruction_num not in visited_instructions:

            if next_instruction_num >= len(self.program):
                return (accumulator, next_instruction_num)

            visited_instructions.append(next_instruction_num)
            operation, operand = self.program[next_instruction_num]

            if operation == 'nop':
                next_instruction_num += 1
                continue
            if operation == 'acc':
                accumulator += operand
                next_instruction_num += 1
                continue
            if operation == 'jmp':
                next_instruction_num += operand
                continue

        return (accumulator, next_instruction_num)

    def run_alternative(self, start_pos):
        while self.program[start_pos][0] not in ('jmp', 'nop'):
            start_pos += 1
            # assumes that there is a valid solution and we won't run off the end

        self.program[start_pos][0] = 'nop' if self.program[start_pos][0] == 'jmp' else 'jmp'
        accumulator, next_instruction_num = self.run()
        self.program[start_pos][0] = 'nop' if self.program[start_pos][0] == 'jmp' else 'jmp'            
        return (accumulator, next_instruction_num, start_pos)


program = Program()
accumulator = program.run()[0]
print(f"Part 1: Accumulator is {accumulator}")

prog_len = len(program.program)
candidate_pos = 0
while candidate_pos < prog_len:
    accumulator, next_instruction_num, altered_instruction_num = program.run_alternative(candidate_pos)
    if next_instruction_num == prog_len:
        print(f"Success! accumulator = {accumulator}")
        exit()
    else:
        candidate_pos = altered_instruction_num + 1