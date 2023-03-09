"""
Arnav Marchareddy
I pledge my honor that I have abided by the Stevens Honor System
"""

from typing import List

def redistribute(weights : List[float], min : float = 0.02, max : float = 0.25):
    """
    Redistribute weights to fall within [min, max]
    Returns: weights (and prints sum)
    """

    # Some error checking
    if not weights: # check if weights is an empty list since there would be nothing to do
        print("No weights were provided!")
        return weights

    num_weights = len(weights) # get the number of weights as well as the average weight in the list
    avrg_weight = sum(weights) / num_weights

    """
    With the most even distribution (average of the weights), if the
    the average falls above the maximum or below the minimum,
    then its simply not possible to redistribute the weights
    to fall within the max
    """
    if avrg_weight > max:
        print("It is not possible to redistribute the weights to fall below the maximum!")
        return weights
    elif avrg_weight < min:
        print("It is not possible to redistribute the weights to fall above the minimum!")
        return weights

    extra_weights: float = 0 # A variable to store the accumulated weight as its being trimmed from weights > max

    """
    The purpose of this array is to keep track of the weights that
    have been trimmed. The reason I have a list as opposed to simply checking
    if the weight is less than max is because of floating point error.
    Ex: (0.249999999997) should be counted as equal to the max since the difference
    is negligible. I want to avoid adding extremely small weights to this value during
    the distribution process so I just keep track of the weights I trimmed
    """
    is_trimmed: List[bool] = [False] * num_weights

    """
    This is a boolean flag to determine weather any weights fall during the distribution process
    in which case, another iteration would be made to redistribute the accumulated excess.
    """
    is_not_redistributed: bool = True

    sum_non_trimmed_weights: float = 0 # stores the sum of weights that haven't been trimmed in an iteration

    """
    In our initial iteration, we trim any weights greater than max while adding it to extra_weights.
    At the same time, any weights that fall below the minimum have the extra weight distributed to them
    to get them to the minimum.
    If the extra_weights is negative after this iteration, that indicates that there isn't enough weight to
    distribute.
    """
    for i in range(num_weights):
        if weights[i] > max: # if any weight is bigger than the max
            extra_weights += weights[i] - max # add the difference betweent the weight and max to the extra weight
            weights[i] = max # set the weight back to the max

            is_trimmed[i] = True # mark the is_trimmed as true at i to indicate the i_th weight in the list has been trimmed
        elif weights[i] < min: # if any weight is smaller than the min
            extra_weights -= min - weights[i] # subtract the difference between the min and weight from extra weight
            weights[i] = min # set the weight to the minimum to get it within bounds

            sum_non_trimmed_weights += min #the weight wasnt trimmed so its weight could be added to the non trimmed sum
        else:
            sum_non_trimmed_weights += weights[i] # if the weight is within the bounds, its weight can be added to the non trimmed sum

    """
    At this point, there should be some sort of value stored in extra_weight
    because all weights above the bound should've been trimmed while any weights
    below the minimum was set to the minimum.
    It can also be safely assumed that a weight below the minimum will never be
    encountered again since the weights will only be incremented from this point
    with the exception of trimming weights that go above the max.
    """
    while is_not_redistributed: # keep iterating until is_not_redistributed is false
        is_not_redistributed = False # reset the boolean flag to false to ensure it remains false if no weights above the max are encountered

        for i in range(num_weights):
            if is_trimmed[i]: # if the value has been previously trimmed, then skip over it
                continue
            """
            The proportion of the weights to the sum of the non trimmed weights is
            equivalent to the proportion between the added weight and the total extra weight
            """
            weights[i] += extra_weights * weights[i] / sum_non_trimmed_weights # adding the correct proportion of the extra weight to the current weight

            if weights[i] > max:  # set the flag to true if any weight goes above the max
                is_not_redistributed = True

        # Reset these variables since we're recalculating their values in the next loop
        extra_weights = 0
        sum_non_trimmed_weights = 0

        is_trimmed = [False] * num_weights

        for i in range(num_weights):
            if weights[i] > max: # reset the weight to its max and increment extra_weights by its excess value
                extra_weights += weights[i] - max
                weights[i] = max

                is_trimmed[i] = True # is_trimmed is set to true at i to indicate the ith weight has been trimmed
            else:
                sum_non_trimmed_weights += weights[i] # collect the sum of any weights that fall within the bounds

    print(f'The sum is {sum(weights)}')

    return weights


# some testcases here
if __name__ == "__main__":
    print(redistribute([0.4, 0.248, 0.03, 0.1, 0.12, 0.001, 0.0, 0.02, 0.04, .161]))
    print(redistribute([0.056, 0.219, 0.322, 0.025, 0.012, 0.048, .105, .097, .065, .051]))
    print(redistribute([0.01195615, 0.04479124, 0.01239616, 0.07624428, 0.15352109, 0.28317437, 0.23725617, 0.02611223, 0.13620537, 0.01834294]))
    print(redistribute([0.36515358, 0.2742581, 0.00618948, 0.03771716, 0.01165502, 0.0048555, 0.06809406, 0.20242359, 0.01526042, 0.01439309]))
    print(redistribute([0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    print(redistribute([0.5, 0.5, 0.0, 0.0, 0.0, 0.0]))
    print(redistribute([0.15, 0.5, -0.1501, 0.1999, 0]))
    print(redistribute([0.16, 0.5, 0.14, 0.19, 0.01]))
    print(redistribute([0.4, 0.3, 0.2, 0.01, 0.01, 0.02, 0.01, 0.03, 0.02]))
    print(redistribute([1, 0, 0, 0]))
