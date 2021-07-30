""" 
This program takes the wikipedia requests JSON and 
returns the pages with the highest mean difference
as an effort to try to understand what caused the
2010 December spike in wikipedia data
"""

import json
import heapq
import math
from os import system


class Page:

    def __init__(self, name: str):
        # Takes the name of the page and the numRequestsPoint as (Date, Requests) 
        if type(name) != str:
            raise TypeError("Name should be a string not a " + str(type(name)))
        self.name = name
        self.requestsList: list = []
        
    def addRequest(self, numRequestsPoint: tuple):
        if type(numRequestsPoint) != tuple:
            raise TypeError("numRequestsPoint should be a tuple not a " + str(type(numRequestsPoint)))
        if numRequestsPoint[1] < 0:
            raise ValueError("Number of Requests can only be positive")
        if len(numRequestsPoint) != 2:
            raise KeyError("Tuple should be two elements")
        if type(numRequestsPoint[1]) != int:
            raise TypeError("numRequestsPoint(1) should be an integer not a " + str(type(numRequestsPoint)))
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
        sigmaRequests: int = 0
        for requestPoint in self.requestsList:
            sigmaRequests +=requestPoint[1]
        return sigmaRequests/len(self.requestsList)

    def getFurthestElementFromMean(self) -> tuple:
        if len(self.requestsList) < 1:
            raise IndexError('Requests list is empty')
        mean: float = self.getMean()
        max: tuple = self.requestsList[0]
        for dataPoint in self.requestsList:
            requestDiffMean: float = dataPoint[1] - mean
            if requestDiffMean > max[1]:
                max = dataPoint
        return max
    

    def getStdDev(self) -> float:
        stdDev: int = 0
        for requestPoint in self.requestsList:
            numRequests = requestPoint[1]
            stdDev += (numRequests - self.getMean())**2
        stdDev /= len(self.requestsList)
        return math.sqrt(stdDev)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.requestsList[-1][1] < other.requestsList[-1][1]

    def __gt__(self, other) -> bool:
        return self.requestsList[0][1] > other.requestsList[0][1]

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return "{}:{}".format(self.name, self.requestsList)


def main():
    json_file = open('wikipedia.json', 'r')
    originalDict: dict = json.load(json_file)
    pageList = initializePages(originalDict)
    deviatorsList = getMostDeviatingFromMean(pageList)
    maxPage:Page = getMaxPage(deviatorsList)
    print(maxPage)
    

def initializePages(data: dict) -> list:
    toReturn: list = []
    for pageName in data:
        page: Page = Page(pageName)
        for date in data[pageName]:
            requestsPointsDict = data[pageName]
            numRequests: int = requestsPointsDict[date]
            requestPointTuple: tuple = (date, numRequests)
            page.addRequest(requestPointTuple)
        toReturn.append(page)
    return toReturn


def getMostDeviatingFromMean(data: list) -> list:
    toReturn: list = []
    for page in data:
        page: Page
        outlierRequest = page.getFurthestElementFromMean()
        newPage = Page(page.name)
        newPage.addRequest(outlierRequest)
        toReturn.append(newPage)
    return toReturn


def getMaxPage(data: list) -> Page:
    return max(data)  


if __name__ == '__main__':
    main()
