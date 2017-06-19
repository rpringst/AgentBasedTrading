import math, time
import matplotlib.pyplot as plt, numpy as np

def randNorm(avg, stdev):
    return np.random.normal(avg, stdev) + 1

class Market:
    def __init__(self, T, N, mu, sigma, initial):
        self.T, self.N, self.mu, self.sigma = T, N, mu, sigma
        self.avg, self.stdv = mu/T, sigma/math.sqrt(T)
        self.prices = [initial]
    def currentPrice(self):
        return self.prices[-1]
    def getNextPrice(self):
        self.prices.append(randNorm(self.avg, self.stdv) * 
                           self.currentPrice())
    def runMarket(self, iterations):
        self.t0 = time.time()
        for i in range(int(self.T*self.N*iterations)):
            self.getNextPrice()
            if i%int(self.T) == 0:
                print('Day: ' + str('{:05.4f}'.format(i/self.T)) + 
                      ', price: ' + 
                      str('{:07.6f}'.format(self.currentPrice())) +
                      ', time: ' + str(time.time()-self.t0))
                self.t0 = time.time()
        return np.array(self.prices)

class Agent:
    def __init__(self, initstock, initcash, buyfrac, sellfrac, buyprob,
                 sellprob, holdprob):
        self.stock, self.cash = [initstock], [initcash]
        self.bf, self.sf = buyfrac, sellfrac
        self.bp, self.sp, self.hp = buyprob, sellprob, holdprob
        self.options = {0 : self.buyStock,
                        1 : self.sellStock,
                        2 : self.holdStock}
    def getTransactionType(self):
        roll = np.random.uniform(0, 1)
        if roll <= self.bp:
            return 0
        elif roll > self.bp and roll <= (self.bp + self.sp):
            return 1
        else:
            return 2
    def buyStock(self, stockprice):
        cost = self.cash[-1]*self.bf
        shares = cost/stockprice
        self.stock.append(self.stock[-1]+shares)
        self.cash.append(self.cash[-1]-cost)
    def sellStock(self, stockprice):
        shares = self.stock[-1]*self.sf
        value = shares*stockprice
        self.stock.append(self.stock[-1]-shares)
        self.cash.append(self.cash[-1]+value)
    def holdStock(self, stockprice):
        self.stock.append(self.stock[-1])
        self.cash.append(self.cash[-1])
    def executeTransaction(self, stockprice):
        self.options[self.getTransactionType()](stockprice)
        

def main():
    # Parameters
    T = 8.0*60.0  # Number of trades in 1 day
    N = 252.0  # Number of days to trade
    mu = 0.07/252.0  # Return (annualized) per day
    sigma = 0.01 # Volatility
    initial = 1.0  # Initial price
    iterations = 1  # years
    netWorth = []
    finalPrices = []
    
    for j in range(100):
        broker = Agent(1000.0, 1000.0, 0.2, 0.2, 0.3, 0.4, 0.3)
        stock = Market(T, N, mu, sigma, initial)
        #print(stock.currentPrice())
        #print(broker.stock[-1])
        #print(broker.cash[-1])
        print(j)
        for i in range(int(T*N)):
            stock.getNextPrice()
            broker.executeTransaction(stock.currentPrice())
            #if i%int(T) == 0:
                #print('Trade number: ' + str(i))
                #print('Price: ' + str(stock.currentPrice()))
                #print('Stock: ' + str(broker.stock[-1]))
                #print('Cash: ' + str(broker.cash[-1]))
                #print('')
        #print('Total value: ' + str(broker.cash[-1]+(broker.stock[-1]*stock.currentPrice())))
        netWorth.append(broker.cash[-1]+(broker.stock[-1]*stock.currentPrice()))
        finalPrices.append(stock.prices[-1])
    print(((netWorth-np.array([2000.0]))/np.array([2000.0])))
    print(((netWorth-np.array([2000.0]))/np.array([2000.0]))-(finalPrices-np.array([1.0])))
    print(finalPrices-np.array([1.0]))
    plt.plot(((netWorth-np.array([2000.0]))/np.array([2000.0])))
    plt.plot(finalPrices-np.array([1.0]))
    plt.show()
    
        
    #plt.plot(broker.stock)
    #plt.show()
    #plt.clf()
    #plt.plot(broker.cash)
    #plt.show()
    #plt.clf()
    
    #for i in range(1000):
        #
        #stock.prices = stock.runMarket(iterations)
        #plt.plot(stock.prices)
        #plt.axis([0, T*N*iterations, np.amin(stock.prices), np.amax(stock.prices)])
        #plt.savefig('images/' + str(time.time()) + '.png')
        #plt.clf()

main()
