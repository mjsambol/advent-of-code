starting_program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,5,19,23,1,23,5,27,2,27,10,31,1,5,31,35,2,35,6,39,1,6,39,43,2,13,43,47,2,9,47,51,1,6,51,55,1,55,9,59,2,6,59,63,1,5,63,67,2,67,13,71,1,9,71,75,1,75,9,79,2,79,10,83,1,6,83,87,1,5,87,91,1,6,91,95,1,95,13,99,1,10,99,103,2,6,103,107,1,107,5,111,1,111,13,115,1,115,13,119,1,13,119,123,2,123,13,127,1,127,6,131,1,131,9,135,1,5,135,139,2,139,6,143,2,6,143,147,1,5,147,151,1,151,2,155,1,9,155,0,99,2,14,0,0]

def run_program(program):
    processing_op_num = 0

    while processing_op_num + 3 < len(program):
        op_pos = processing_op_num * 4
        operation = program[op_pos]
        if operation == 99:
#            print("Done.")
#            print(program)
            return

        operand1 = program[op_pos + 1]
        operand2 = program[op_pos + 2]
        destination = program[op_pos + 3]

        val1 = program[ operand1 ]
        val2 = program[ operand2 ]

    #    print(f"operation: {operation} on {operand1}={val1} and {operand2}={val2} to {destination}")

        if operation == 1:
            result = val1 + val2
        elif operation == 2:
            result = val1 * val2
        else:
            print(f"Error - unexpected op code {operation}")

        program[destination] = result
        processing_op_num += 1


for noun in range(100):
    for verb in range(100):
        attempt = starting_program[:]
        attempt[1] = noun
        attempt[2] = verb
        run_program(attempt)
        print(f"Result of run with {noun}, {verb} is {attempt[0]}")
        if attempt[0] == 19690720:
            print (f"That's it! Result = {100 * noun + verb}")
            exit()
