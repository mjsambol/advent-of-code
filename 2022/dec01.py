with open("dec01in.txt") as my_input:

    the_total = 0
    happy_elf_1_calories = 0
    happy_elf_2_calories = 0
    happy_elf_3_calories = 0

    for line in my_input:
        line = line.strip()

        if len(line) > 0:
        #  print(line)
            the_total = the_total + int(line)

        if len(line) == 0:
            print("this elf has:",the_total, "calories")
            
            if the_total > happy_elf_1_calories:
                happy_elf_3_calories = happy_elf_2_calories
                happy_elf_2_calories = happy_elf_1_calories
                happy_elf_1_calories = the_total
            elif the_total > happy_elf_2_calories:
                happy_elf_3_calories = happy_elf_2_calories
                happy_elf_2_calories = the_total
            elif the_total > happy_elf_3_calories:
                happy_elf_3_calories = the_total

            the_total = 0
            continue

      #  print("total so far:", the_total)

# print("The final total is: ", the_total)
print("the elf with the most calories (smart dude!) has: ", happy_elf_1_calories)
print("the elf with the second most calories (OK dude!) has: ", happy_elf_2_calories)
print("the elf with the third most calories (hungry dude!) has: ", happy_elf_3_calories)

print(happy_elf_1_calories + happy_elf_2_calories + happy_elf_3_calories)