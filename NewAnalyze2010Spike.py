""" 
This program takes the wikipedia requests JSON and 
returns the pages with the highest mean difference
as an effort to try to understand what caused the
2010 December spike in wikipedia data
"""

import json
import math
import numpy as np
from Page import Page


def main():
    json_file = open('wikipedia.json', 'r')
    originalDict: dict = json.load(json_file)
    pageList = initializePages(originalDict)
    getOutlierByStdDev(pageList)
    
        
def getOutlierByStdDev(pageList):
    outliers: Page = getHighestStdDev(pageList, 25)
    for outlier in outliers:
        print("Outlier is {} with a stdDev of {}".format(outlier, outlier.getStdDev()))

def getHighestStdDev(pageList: list, n: int = 10) -> list:
    if n > len(pageList):
        raise ValueError("n should be smaller than the length of the pagesList")
    pageList = pageList.copy()
    toReturn = []
    for i in range(n):
        toReturn.append(pageList.pop())
    for i in range(len(pageList)):
        page: Page = pageList[i]
        minInToReturnList = getLeastStdDev(toReturn)
        if page.getStdDev() > minInToReturnList.getStdDev():
            toReturn.remove(minInToReturnList)
            toReturn.append(page)
    toReturn.sort(reverse=True)
    return toReturn

def getLeastStdDev(pageList: list):
    min: Page = pageList[0]
    for page in pageList:
        page: Page
        if page.getStdDev() < min.getStdDev():
            min = page
    return min


def getOutlierByMostDeviatingFromMean(pageList) -> None:
    deviatorsList = getMostDeviatingFromMean(pageList)
    maxPages:list = getMaxDiffMeanPages(deviatorsList, 10)
    for page in maxPages:
        page: Page
        print("Outlier is {} with a mean difference of: {}".format(page, page.requestsList[0][1]- page.getMean()))

def initializePages(data: dict) -> list:
    """ 
    Converts the jsonDict into a list of Page objects.
    """
    toReturn: list = []
    for pageName in data:
        page: str = pageName.split(',')[1].lower()
        if isWeirdPage(page):            
            continue
        page: Page = Page(pageName)
        for date in data[pageName]:
            requestsPointsDict = data[pageName]
            numRequests: int = requestsPointsDict[date]
            requestPointTuple: tuple = (date, numRequests)
            page.addRequest(requestPointTuple)
        toReturn.append(page)
    return toReturn


def isWeirdPage(page: Page) -> bool:
    """ 
    Returns True if the  page is a logistical or an error page.
    Hardcoded for now
    """
    pageType = page.split(':')[0]
    try:
        pageName = page.split(':')[1]
    except:
        pageName = ""
    return pageType == "special" or pageType == "especial" or pageType =="speciale" or pageType == 'en' or pageType == 'fr' or pageType == 'de' or pageType == 'it' or pageType == 'speciaal' or pageType == 'spezial' or pageType == r'sp%c3%a9cial' or pageType[0] == '%' or pageName == "bannercontroller"


def getMostDeviatingFromMean(data: list) -> list:
    """ 
    Gets a new Page list where every page has only 
    one element that's the furthest from mean
    """
    toReturn: list = []
    for page in data:
        page: Page
        newPage = page.getFurthestElementFromMean()
        toReturn.append(newPage)
    return toReturn


def getMaxDiffMeanPages(data: list, n = 10) -> list:
    """ 
    Helper method that returns the top n pages 
    with most difference from mean
    """
    sortedData = mergeSortByFurthestFromMean(data)
    return sortedData[:n]    


def mergeSortByFurthestFromMean(list: list) -> list:
    # if the list has more than one element, we
    # half the list
    # if the list has one element, we merge
    # with the next list
    if len(list) == 1:
        return list    
    halfLength = len(list) // 2
    list1 = list[:halfLength]
    list2 = list[halfLength:]
    list1 = mergeSortByFurthestFromMean(list1)
    list2 = mergeSortByFurthestFromMean(list2)
    return merge(list1, list2)
        
def merge(list1: list, list2: list) -> list:
    newList = []
    if len(list1) == 1 and len(list2) == 1:
        page1: Page = list1[0]
        page2: Page = list2[0]
        if (page1.requestsList[0][1] -page1.getMean()) > (page2.requestsList[0][1] - page2.getMean()):
            newList.append(page1)
            newList.append(page2)
        else:
            newList.append(page2)
            newList.append(page1)
    else:
        for page1 in list1:
            if len(list2) < 1:
                newList.append(page1)
                continue
            page2 = list2[0]
            if (page1.requestsList[0][1] -page1.getMean()) > (page2.requestsList[0][1] - page2.getMean()):
                newList.append(page1)
            else:
                newList.append(page2)
                list2.pop(0)
        while len(list2) > 0:
            newList.append(list2.pop(0))
    return newList


def mergeSortByStdDev(list: list) -> list:
    # if the list has more than one element, we
    # half the list
    # if the list has one element, we merge
    # with the next list
    if len(list) == 1:
        return list    
    halfLength = len(list) // 2
    list1 = list[:halfLength]
    list2 = list[halfLength:]
    list1 = mergeSortByStdDev(list1)
    list2 = mergeSortByStdDev(list2)
    return mergeStdDev(list1, list2)
        
def mergeStdDev(list1: list, list2: list) -> list:
    newList = []
    if len(list1) == 1 and len(list2) == 1:
        page1: Page = list1[0]
        page2: Page = list2[0]
        if (page1.getStdDev()) > (page2.getStdDev()):
            newList.append(page1)
            newList.append(page2)
        else:
            newList.append(page2)
            newList.append(page1)
    else:
        for page1 in list1:
            if len(list2) < 1:
                newList.append(page1)
                continue
            page2 = list2[0]
            if (page1.getStdDev()) > (page2.getStdDev()):
                newList.append(page1)
            else:
                newList.append(page2)
                list2.pop(0)
        while len(list2) > 0:
            newList.append(list2.pop(0))
    return newList

    
if __name__ == '__main__':
    main()
