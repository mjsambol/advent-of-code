from computer import Computer
import itertools

amplifier_prog = [3,8,1001,8,10,8,105,1,0,0,21,34,51,76,101,126,207,288,369,450,99999,3,9,102,4,9,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,102,5,9,9,1001,9,2,9,102,2,9,9,101,3,9,9,1002,9,2,9,4,9,99,3,9,101,5,9,9,102,5,9,9,1001,9,2,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,1002,9,5,9,1001,9,5,9,1002,9,4,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99]

def do_p1_attempt(settings, program):
#    print(f"Starting do_attempt with params {settings}")

    incoming_signal = 0

    for thruster in settings:
    #    print(f"Executing thruster {thruster}, incoming_signal is {incoming_signal}")
        comp = Computer(program[:])
        comp.store_input(thruster)
        comp.store_input(incoming_signal)
        comp.run()
        result = comp.get_output()
#        print(f"Result of running thruster with input {incoming_signal} is {result}")
        incoming_signal = result

#    print(f"Finished do_attempt, returning {incoming_signal}")
    return incoming_signal


def do_p2_attempt(settings, program):
#    print(f"Starting do_attempt with params {settings}")

# instead of just creating a thruster per input setting
# and running it once, we need to create them all, then while-true loop through
# executing each of them, passing output from one to input to the other
# until first comp.is_halted()

    thursters = []

    for setting in settings:
    #    print(f"Executing thruster {thruster}, incoming_signal is {incoming_signal}")
        comp = Computer(program[:])
        comp.store_input(setting)
        thursters.append(comp)

    incoming_signal = 0
    thruster_num = 0

    while not thrusters[thruster_num].is_halted():
        thruster = thrusters[thruster_num]
        thruster.store_input(incoming_signal)
        thruster.run()  # what makes this return?
        result = thruster.get_output()
#        print(f"Result of running thruster with input {incoming_signal} is {result}")
        incoming_signal = result
        thruster_num = (thruster_num + 1) % 5

#    print(f"Finished do_attempt, returning {incoming_signal}")
    return incoming_signal




def do_tests():
    echo_settings = [4,3,2,1,0]
    echo_amplifier_prog = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

    reversish = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    reversish_settings = [0,1,2,3,4]

    last_test = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    last_test_settings = [1,0,4,3,2]

    tests = ((echo_settings, echo_amplifier_prog, 43210), (reversish_settings, reversish, 54321), (last_test_settings, last_test, 65210))

    for test_num, test in enumerate(tests):
        test_settings, test_prog, expected_result = test

        result = do_attempt(test_settings, test_prog)

        if result == expected_result:
            print(f"Test {test_num}: Success! Final signal is {result}\n")
        else:
            print(f"** UH OH: UNEXPECTED RESULT for test # {test_num}**")
            return(-1)

#do_tests()
# print(f"Done. Final signal is {incoming_signal}")

# def increment_settings(settings):
#     # settings is a list of 5 digits, each of which ranges from 0-4.
#     # this function increments the settings as if it's one large number
#     digit = 4
#     while digit >= 0:
#         settings[digit] = (settings[digit] + 1) % 5
#         if settings[digit] != 0:
#             return
#         digit -= 1

def d7p1():
    all_attempts = list(itertools.permutations([0,1,2,3,4]))
    max_result = 0

    for attempt in all_attempts:
    #    print(f"Attempting: {attempt}")
        result = do_p1_attempt(attempt, amplifier_prog)
        print(f"Attempt: {attempt}  -- Result: {result:10,}")
        if result > max_result:
            max_result = result
            max_input = attempt[:]

    print(f"Maximum result was {max_result:,} based on settings {max_input}")

d7p1()

def d7p2():
    all_attempts = list(itertools.permutations([5,6,7,8,9]))
    max_result = 0

    for attempt in all_attempts:
        result = do_p2_attempt(attempt, amplifier_prog)
        print(f"Attempt: {attempt}  -- Result: {result:10,}")
        if result > max_result:
            max_result = result
            max_input = attempt[:]

    print(f"Maximum result was {max_result:,} based on settings {max_input}")
