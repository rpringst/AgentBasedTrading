import math, time
import matplotlib.pyplot as plt, numpy as np

T, N, mu, sigma = 8.0*60.0*60.0, 252.0, 0.07/252.0, 0.015
startingPrice = 1.0
numOfYears = 100.0
dailycloses = []

def main(initial):
    avg, stdev, price = mu/T, sigma/math.sqrt(T), [initial]
    
    t0 = time.time()
    for i in range(int(T*N)):
        price.append((np.random.normal(avg, stdev) + 1)*price[-1])
        if i%int(T) == 0:  # Print daily results
            print('Day: ' + str(int(i/T)) + ', price: ' + 
                  str('{:07.4f}'.format(price[-1])) +
                  ', time: ' + str(time.time()-t0))
            t0 = time.time()
            dailycloses.append(price[-1])

    plt.plot(np.array(price))
    plt.axis([0, T*N, np.amin(price), np.amax(price)])
    plt.savefig('images/' + str(time.time()) + '.png')
    plt.clf()
    return price[-1]


for i in range(int(numOfYears)):
    startingPrice = main(startingPrice)

plt.plot(np.array(dailycloses))
plt.axis([0, N*numOfYears, np.amin(dailycloses), np.amax(dailycloses)])
plt.savefig('images/' + str(time.time()) + '.png')
plt.clf()
