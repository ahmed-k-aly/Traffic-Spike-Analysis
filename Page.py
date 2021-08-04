import math

class Page:

    def __init__(self, name: str, mean = -1, stdDev = -1):
        # Takes the name of the page and the numRequestsPoint as (Date, Requests) 
        if type(name) != str:
            raise TypeError("Name should be a string not a " + str(type(name)))
        self.name = name
        self.requestsList: list = []
        self.mean = mean
        self.stdDev = stdDev
        
    def addRequest(self, numRequestsPoint: tuple):
        """Adds a request point to the request list.

        Args:
            numRequestsPoint (tuple): the request point in this form (Date, NumRequests)
            Date should be a string. However, no exceptions are raised if Date isn't a string

        Raises:
            TypeError: if a wrong type is passed for numRequestsPoint
            ValueError: if the number of requests is negative
            KeyError: if the tuple is longer than two elements
            TypeError: if the requests are not an int
            Warning: if date is not a string
        """        
        if type(numRequestsPoint) != tuple:
            raise TypeError("numRequestsPoint should be a tuple not a " + str(type(numRequestsPoint)))
        if numRequestsPoint[1] < 0:
            raise ValueError("Number of Requests can only be positive")
        if len(numRequestsPoint) != 2:
            raise KeyError("Tuple should be two elements")
        if type(numRequestsPoint[1]) != int:
            raise TypeError("numRequestsPoint(1) should be an integer not a " + str(type(numRequestsPoint)))
        if type(numRequestsPoint[0]) != str:
            raise Warning("Date passed is a {} not a string".format(type(numRequestsPoint[0])))
        
        self.requestsList.append(numRequestsPoint)
    
    def getMaxRequests(self):
        if len(self.requestsList < 1):
            raise IndexError("No Requests in the list")
        max = (0,0)
        for requestPoint in self.requestsList:
            if max[1] < requestPoint[1]:
                max = requestPoint
        return max

    def getMean(self) -> float:
        """Memoized method that calculates the mean 
        of all requests in the request list. If the mean
        is calculated once, it caches it, and doesn't
        calculate it again.

        Returns:
            float: the mean
        """        
        if self.mean > 0:
            return self.mean
        sigmaRequests: int = 0
        for requestPoint in self.requestsList:
            sigmaRequests +=requestPoint[1]
        self.mean = sigmaRequests/len(self.requestsList)
        return self.mean

    def getFurthestElementFromMean(self) -> object:
        """Gets the furthest data point from the
        mean for a single dataPoint

        Raises:
            IndexError: if the requests list is empty.

        Returns:
            Page: an instance of a Page object with the mean
            and stdDev of the original list
        """        
        if len(self.requestsList) < 1:
            raise IndexError('Requests list is empty')
        mean: float = self.getMean()
        max: tuple = self.requestsList[0]
        for dataPoint in self.requestsList:
            requestDiffMean: float = dataPoint[1] - mean
            if requestDiffMean > max[1]:
                max = dataPoint
        newPage:Page = Page(self.name, mean = self.mean, stdDev=self.stdDev)
        newPage.addRequest(max)
        return newPage
        
        
    def getStdDev(self) -> float:
        if len(self.requestsList) <1:
            raise IndexError("Request list is empty")
        if self.stdDev > 0:
            return self.stdDev
        stdDev: int = 0
        for requestPoint in self.requestsList:
            numRequests = requestPoint[1]
            stdDev += (numRequests - self.getMean())**2
        stdDev /= len(self.requestsList)
        self.stdDev = math.sqrt(stdDev) 
        return self.stdDev

    def getNthDiff(self, n: int = 1):
        """ 
        Recursive function that returns the nth Diff of the
        Requests list, essentially the same as np.diff
        """
        if len(self.requestsList) < 1:
            raise IndexError('Requests list is empty')
        if n > 0:
            return self.getNthDiff(self, n-1)
        toReturn = []
        for i in range(len(self.requestsList)-1):
            dataPoint0: tuple = self.requestsList[i]
            request0: int = dataPoint0[1]
            dataPoint1: tuple = self.requestsList[i+1]
            time1: str = dataPoint1[0]
            request1: int = dataPoint1[1]
            tupleToAppend: tuple = (time1, request1 - request0)
            toReturn.append(tupleToAppend)
        return toReturn

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.getStdDev() < other.getStdDev()

    def __gt__(self, other) -> bool:
        return self.getStdDev() > other.getStdDev()

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:        
        return self.name
    
    def __len__(self):
        return len(self.requestsList)

