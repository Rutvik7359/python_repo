import random, sys


def estimate_pi(n_samples, rnd_seed=0):
    
    count = 0
    for i in range(0, n_samples):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        if (x**2 + y**2) <= 1:
            count +=1 

    pi = 4.*count/n_samples

    return pi



def main():

    num_args = len(sys.argv) - 1
    if num_args == 1:
        sample_size = int(sys.argv[1])
    else:
        sample_size = 100


    run1 = estimate_pi(sample_size)
    run2 = estimate_pi(sample_size)

    print "Run 1:\t" + str(run1)
    print "Run 2:\t" + str(run2)
    print "Avg:\t" + str((run1+run2)/2.)


if __name__ == '__main__':
    main()