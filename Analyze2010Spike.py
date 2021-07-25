import json
import heapq


class Page:
    def __init__(self, name: str, numRequests: int):
        self.name = name
        self.numRequests = numRequests

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.numRequests < other.numRequests

    def __gt__(self, other) -> bool:
        return self.numRequests > other.numRequests

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return "{}:{}".format(self.name, self.numRequests)
def main():

    json_file = open('wikipedia.json', 'r')
    originalDict: dict = json.load(json_file)
    newDict: dict = {}
    # Loop through all pages.
    for page in originalDict:
        # Loop through all entries per page.
        pageArr = []
        requestArr = []
        for entry in originalDict[page]:
            # put all entries in one page together in an array.
            pageArr.append(entry)
        # find max element from mean in that array.
        max = 0
        toReturn = '0'
        mean = 0
        for entry in pageArr:
            request = originalDict[page][entry]
            mean += request
            if request > max:
                max = request
                toReturn = entry
        mean = mean // len(originalDict[page])
        # return that entry only as {page: {time: requests}} or {page: (time, requests)}
        # put that entry into the main dict as returned above.
        newDict[page] = max-mean
    # loop through that dict in search of the 10 highest values.

    pageArr: list = []
    
    for pageName in newDict:
        rq: int = newDict[pageName]
        newPg: Page = Page(pageName, rq)
        pageArr.append(newPg)
    pageArr.sort(reverse=True)
    for i in range(50):
        item = pageArr[i]
        item: Page
        print(item)


if __name__ == '__main__':
    main()
