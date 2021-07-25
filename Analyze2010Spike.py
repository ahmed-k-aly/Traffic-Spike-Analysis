import json
import heapq
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

    arr = []
    for page in newDict:
        if len(arr) < 10:
            arr.append({page: newDict[page]})
    for item in newDict:
        print(item + ':' + str(newDict[item]))
        
    
if __name__ == '__main__':
    main()