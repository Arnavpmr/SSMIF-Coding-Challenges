"""
Arnav Marchareddy
I pledge my honor that I have abided by the Stevens Honor System
"""

lines = []

with open("logic_input.txt", 'r') as f:
    lines = [entry.strip() for entry in f.readlines()]

# variables declared here to store the alpha and sigma rates
alpha_rate = ""
sigma_rate = ""

# lists which will hold the delta and omega lists
delta = []
omega = []

bin_num_len = len(lines[0]) # the number of digits in each binary number is stored in the variable
half_num_lines = len(lines) / 2 # half the length of the list of binary numbers is stored

# Part 1
"""
In this initial loop, we loop through every column of digits in the list
For each column of digits we keep track of the number of 1's and 0's
"""
for i in range(bin_num_len):
    num_ones = 0 # initialize these count variables here to 0
    num_zeroes = 0

    for line in lines:
        if line[i] == "1": # increment num_ones or num_zeroes appropriately depending on the given digit
            num_ones += 1
        else:
            num_zeroes += 1

        """
        Because the goal is to get the most occuring digit, it isn't necessary
        to count anymore if the count of one of the digits exceeds half the length of
        the entire list.
        """
        if num_ones > half_num_lines: # if one is prevalent, add the necessary digits when constructing the alpha_rate and sigma_rate strings
            alpha_rate += "1"
            sigma_rate += "0" # 0 would be the less common digit if 1 is determined to be the most common

            break
        elif num_zeroes > half_num_lines: # if 0 is prevalent, add the necessary digits when constructing the alpha_rate and sigma_rate strings
            alpha_rate += "0"
            sigma_rate += "1" # 1 would be the less common digit if 0 is determined to be the most common

            break

"""
The power consumption is calculating through using the
built in int function in python. There is a second optional
parameter which is the base of the argument, which in this case is 2.
"""
power_consumption = int(alpha_rate, 2) * int(sigma_rate, 2)


# Part 2
"""
The purpose of this function is to determine the delta and omega rate.
This is done through specifying whether or not to filter out the binary by the most common digit.
If true, it determines the delta value.
If false, it determines the omega value.
"""
def reduce_bin_list(filter_by_common_digit):
    """
    The alpha and sigma rates have already been computed so the list can be filtered by their first digit depending
    on what filter_by_common_digit is.
    """
    bin_list = list(filter(lambda x: x[0] == (alpha_rate[0] if filter_by_common_digit else sigma_rate[0]), lines))
    counter = 1 # the counter which represents the index of the digit is set to 1 to account for this

    while len(bin_list) > 1: # keep looping as long as the length of the list is above 1
        # initialize the variables here
        num_ones = 0
        num_zeroes = 0

        half_bin_lines = len(bin_list) / 2

        for line in bin_list:
            if line[counter] == "1": # keep track of the num_ones and the num_zeroes accordingly
                num_ones += 1
            else:
                num_zeroes += 1

            if num_ones > half_bin_lines: # 1 is determined to be the most common digit since its greater than half of the list
                # the filter_by_common_digit directs whether or not to filter by a 1 or 0
                bin_list = list(filter(lambda x: x[counter] == ("1" if filter_by_common_digit else "0"), bin_list))
                counter += 1 # the counter is incremented by 1 in order to index the next column of digits

                break # break since we found the most common digit in this column and filtered the list
            elif num_zeroes > half_bin_lines: # 0 is determined to be the most common digit since its greater than half of the list
                # the filter_by_common_digit directs whether or not to filter by a 1 or 0
                bin_list = list(filter(lambda x: x[counter] == ("0" if filter_by_common_digit else "1"), bin_list))
                counter += 1 # the counter is incremented by 1 in order to index the next column of digits

                break # break since we found the most common digit in this column and filtered the list

        """
        In a case where you end up with the same number of 0's and 1's counted in a column
        Filter by some default value based on the filter_by_common_digit toggle
        """
        if num_ones == num_zeroes and num_ones > 0 and num_zeroes > 0:
            bin_list = list(filter(lambda x: x[counter] == ("1" if filter_by_common_digit else "0"), bin_list))
            counter += 1

    return bin_list


delta_list = reduce_bin_list(True)
omega_list = reduce_bin_list(False)

delta_omega_product = int(delta_list[0], 2) * int(omega_list[0], 2) # calculate the product of the two values here

# print the output of the program
print("Part One:", power_consumption)
print("Part Two:", delta_omega_product)
