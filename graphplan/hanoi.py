import sys





def move_disk_to_Peg_not_empty(disk,peg,dest_peg,disk_on_1,disk_on_2):
    dictOfArgs = {'disk' : disk, 'peg' :peg, 'dest_peg': dest_peg, 'disk_on_1': disk_on_1, 'disk_on_2': disk_on_2}

    name = "Name: d_{disk}_{peg}_on_d_{disk_on_1}_toDest_{dest_peg}_on_d_{disk_on_2}\n".format(**dictOfArgs)

    preconds = "pre: d_{disk}_at_{peg} d_{disk}_top d_{disk}_on_d_{disk_on_1} d_{disk_on_2}_at_{dest_peg} d_{disk_on_2}_top\n".format(**dictOfArgs)
    add = "add: d_{disk}_at_{dest_peg} d_{disk}_on_d_{disk_on_2} d_{disk_on_1}_top\n".format(**dictOfArgs)
    delete = "del: d_{disk}_at_{peg} d_{disk}_on_d_{disk_on_1} d_{disk_on_2}_top\n".format(**dictOfArgs)

    return name  + preconds + add + delete

def move_disk_to_Peg_empty(disk,peg,dest_peg,disk_on_1):
    dictOfArgs = {'disk' : disk, 'peg' :peg, 'dest_peg': dest_peg, 'disk_on_1': disk_on_1}

    name = "Name: d_{disk}_{peg}_on_d_{disk_on_1}_toDest_{dest_peg}\n".format(**dictOfArgs)

    preconds = "pre: d_{disk}_at_{peg} d_{disk}_top d_{disk}_on_d_{disk_on_1} {dest_peg}_empty\n".format(**dictOfArgs)
    add = "add: d_{disk}_at_{dest_peg} d_{disk}_bottom d_{disk_on_1}_top\n".format(**dictOfArgs)
    delete = "del: d_{disk}_at_{peg} d_{disk}_on_d_{disk_on_1} {dest_peg}_empty\n".format(**dictOfArgs)

    return name  + preconds + add + delete

def move_from_single(disk,peg,dest_peg, disk_on_1):

    dictOfArgs = {'disk' : disk, 'peg' :peg, 'dest_peg': dest_peg, 'disk_on_1': disk_on_1}

    name = "Name: d_{disk}_{peg}_{dest_peg}_on_d_{disk_on_1}\n".format(**dictOfArgs)

    preconds = "pre: d_{disk}_at_{peg} d_{disk}_top d_{disk}_bottom {disk_on_1}_at_{dest_peg} d_{disk_on_1}_top\n".format(**dictOfArgs)
    add = "add: d_{disk}_at_{dest_peg} d_{disk}_on_d_{disk_on_1} {peg}_empty\n".format(**dictOfArgs)
    delete = "del: d_{disk}_at_{peg} d_{disk}_bottom d_{disk_on_1}_top\n".format(**dictOfArgs)

    return name  + preconds + add + delete

def move_from_single_to_empty_peg(disk,peg,dest_peg):

    dictOfArgs = {'disk' : disk, 'peg' :peg, 'dest_peg': dest_peg}

    name = "Name: d_{disk}_{peg}_{dest_peg}\n".format(**dictOfArgs)

    preconds = "pre: d_{disk}_at_{peg} d_{disk}_top d_{disk}_bottom {dest_peg}_empty\n".format(**dictOfArgs)
    add = "add: d_{disk}_at_{dest_peg} {peg}_empty\n".format(**dictOfArgs)
    delete = "del: d_{disk}_at_{peg} {dest_peg}_empty\n".format(**dictOfArgs)

    return name  + preconds + add + delete



def create_actions_for_not_empty_dests(disks, pegs):
    actions_for_not_empty_dests = []
    for disk in disks:
        for peg in pegs:
            for dest_peg in pegs:
                if (peg != dest_peg):
                    for disk_on_1 in disks:
                        if disk< disk_on_1:
                            for disk_on_2 in disks:
                                if (disk_on_1 != disk_on_2) and disk< disk_on_2:
                                    actions_for_not_empty_dests.append(move_disk_to_Peg_not_empty(disk,peg,dest_peg,disk_on_1,disk_on_2))

    return actions_for_not_empty_dests

def create_actions_for_empty_dests(disks,pegs):
    actions_for_empty_dests = []
    for disk in disks:
        for peg in pegs:
            for dest_peg in pegs:
                if (peg != dest_peg):
                    for disk_on_1 in disks:
                        if disk< disk_on_1:
                            actions_for_empty_dests.append(move_disk_to_Peg_empty(disk,peg,dest_peg,disk_on_1))
    return actions_for_empty_dests

def create_actions_from_single(disks,pegs):
    actions = []
    for disk in disks:
        for peg in pegs:
            for dest_peg in pegs:
                if (peg != dest_peg):
                    for disk_on_1 in disks:
                        if disk< disk_on_1:
                            actions.append(move_from_single(disk,peg,dest_peg,disk_on_1))
    return actions

def create_actions_from_single_to_empty(disks,pegs):
    actions = []
    for disk in disks:
        for peg in pegs:
            for dest_peg in pegs:
                if (peg != dest_peg):
                    actions.append(move_from_single_to_empty_peg(disk,peg,dest_peg))
    return actions



def create_domain_file(domain_file_name, n_, m_):

    numbers = list(range(n))
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"

    domain_file.write('Propositions: \n')

    disk_on_disk = ["d_{}_on_d_{}".format(disk1,disk2) for disk1 in numbers for disk2 in numbers if disk1 < disk2]

    disks_location = ["{}_at_{}".format(disk1,peg) for disk1 in disks for peg in pegs ]

    disk_on_top = ["%s_top" %d for d in disks]
    disk_on_bottom = ["%s_bottom" %d for d in disks]

    peg_are_empty = ["%s_empty" %peg for peg in pegs]

    a = list(map(lambda  x: domain_file.write(x + " "), disk_on_disk))
    a = list(map(lambda  x: domain_file.write(x + " "), disks_location))
    a = list(map(lambda  x: domain_file.write(x + " "), disk_on_top))
    a = list(map(lambda  x: domain_file.write(x + " "), disk_on_bottom))
    a = list(map(lambda  x: domain_file.write(x + " "), peg_are_empty))


    domain_file.write("\nActions: \n")

    actions_for_not_empty_dests = create_actions_for_not_empty_dests(numbers,pegs)

    action_for_empty_dests = create_actions_for_empty_dests(numbers,pegs)

    actions_from_single = create_actions_from_single(numbers,pegs)

    actions_from_single_to_empty = create_actions_from_single_to_empty(numbers,pegs)

    a = list(map(domain_file.write,actions_for_not_empty_dests))
    a = list(map(domain_file.write,action_for_empty_dests))
    a = list(map(domain_file.write,actions_from_single))
    a = list(map(domain_file.write,actions_from_single_to_empty))

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    numbers = list(range(n))

    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"

    disk_on_disk = ["d_{}_on_d_{}".format(disk1,disk2) for disk1 in numbers for disk2 in numbers if disk1 == disk2-1]

    disks_location = ["{}_at_p_{}".format(disk1,0) for disk1 in disks ]

    disk_top = ["d_0_top"]

    disk_bottom = ["d_{}_bottom".format(n_-1)]

    peg_are_empty = ["p_%s_empty" % i for i in list(range(1,m_ ))]

    problem_file.write("Initial state: ")

    a = list(map(lambda  x: problem_file.write(x + " "), disk_on_disk))
    a = list(map(lambda  x: problem_file.write(x + " "), disks_location))
    a = list(map(lambda  x: problem_file.write(x + " "), disk_top))
    a = list(map(lambda  x: problem_file.write(x + " "), disk_bottom))
    a = list(map(lambda  x: problem_file.write(x + " "), peg_are_empty))

    disks_location = ["{}_at_p_{}".format(disk,m_-1) for disk in disks]

    peg_are_empty = ["p_%s_empty" % i for i in list(range(m_ -1))  ]

    problem_file.write("\nGoal state: ")

    a = list(map(lambda  x: problem_file.write(x + " "), disk_on_disk))
    a = list(map(lambda  x: problem_file.write(x + " "), disks_location))
    a = list(map(lambda  x: problem_file.write(x + " "), disk_top))
    a = list(map(lambda  x: problem_file.write(x + " "), disk_bottom))
    a = list(map(lambda  x: problem_file.write(x + " "), peg_are_empty))


    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
