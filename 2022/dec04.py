with open("dec04in.txt") as my_input:
    inclusives = 0
    overlaps = 0
    for line in my_input:
        e1,e2 = line.strip().split(',')
        e1from,e1to = map(int, e1.split('-'))
        e2from,e2to = map(int, e2.split('-'))
        if (e1from >= e2from and e1to <= e2to) or (e2from >= e1from and e2to <= e1to):
            inclusives += 1
        if ((e2from <= e1from <= e2to) or (e2from <= e1to <= e2to) or 
            (e1from <= e2from <= e1to) or (e1from <= e2to <= e1to)):
            overlaps += 1

    print(inclusives)
    print(overlaps)