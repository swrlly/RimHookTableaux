import copy

class RimHookTableau:
    
    def __init__(self, buffer : list, ints : list):
        self.buffer = buffer
        self.ints = ints
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.buffer == other.buffer
        return False
        
    def Sign(self):
        sgn = 1
        for i in self.ints:
            sgn *= (-1) ** (sum(1 for row in self.buffer if i in row) - 1)
        return sgn

class RimHookTableaux:
    
    
    """
    Generates all rim hook tableaux with shape `shape` and content `weight` in French notation.
    shape: List of integers representing the shape of the rim hook tableaux. First element in list is shape of top row; last element is shape of last row.
    weight: Desired content to insert into the rim hook tableaux. Content is inserted from left to right in the list.
    
    Example:

    a = RimHookTableaux([1,2,3,4],[3,4,2,1])
    a.PrettyPrint()

    [2]
    [2, 2]
    [1, 2, 3]
    [1, 1, 3, 4]

    [2]
    [2, 2]
    [1, 2, 4]
    [1, 1, 3, 3]

    [3]
    [3, 4]
    [1, 2, 2]
    [1, 1, 2, 2]

    [4]
    [3, 3]
    [1, 2, 2]
    [1, 1, 2, 2]
    """
   
    
    def __init__(self, shape : list, weight : list):
        # list of all possible rim hook tableaux with given shape and weight
        self.emptyValue = 0
        self.cache = []
        self.AssertValidity(shape, weight)
        cache = self.CreateAllRimHookTableaux(shape, weight)
        ints = list(range(1, len(weight) + 1))
        for tableau in cache:
            self.cache.append(RimHookTableau(tableau, ints))
            
    def AssertValidity(self, shape, weight):
        if shape == []:
            raise Exception("Shape of rim hook tableaux is empty.")
        if weight == []:
            raise Exception("Content of rim hook tableaux is empty.")
        if sum(shape) != sum(weight):
            raise Exception("Ensure sum(shape) == sum(weight).")
        # check valid shape
        for i in range(1, len(shape)):
            if shape[i] < shape[i-1]:
                raise Exception("Invalid rim hook tableaux shape in french notation.")
        
        
    def CreateAllRimHookTableaux(self, shape : list, weight : list) -> list:
        # now create all rht, 0 means empty
        buffer = [[self.emptyValue for _ in range(i)] for i in shape]
        possibilities = [buffer]
        # rearrangements of RHT content does not change sign
        for w in weight:
            newRHT = []
            for p in possibilities:
                for i in self.AddRimHook(p, w):
                    newRHT.append(i)
            # after iteration, update possibilities. if newRHT is empty, then no new RHT could be generated in AddRimHook
            # this means invalid RHT were generated
            possibilities = newRHT
        
        # delete invalid rhts, only happens on last step
        #return possibilities
        return [buf for buf in possibilities if self.CheckRow(buf)]
            
    def CheckRow(self, buf: list) -> bool:
        for row in buf:
            if self.emptyValue in row:
                return False
        return True
        
    def Sign(self, aggregate = True):
        
        """
        Computes sign of all rim hook tableaux.
        aggregate: if true, returns only the sign. if false, returns a list of signs with respect to each rim hook tableaux.
        """
              
        if aggregate:
            totalSgn = 0
            for rht in self.cache:
                totalSgn += rht.Sign()
            return totalSgn
        else:
            l = []
            for rht in self.cache:
                l.append(rht.Sign())
            return l
    
    def AddRimHook(self, buffer : list, hookLength : int) -> list:
        """
        Given a partially completed rim hook tableaux, returns a list of valid rim hook tableaux after inserting a hook of length of hookLength
        
        Keyword arguments:
        buffer: partially completed rim hook tableaux
        
        hookLength: length of hook you wish to insert
        
        """
        
        if len(buffer) == 0: raise Exception("Buffer cannot be empty.")
        if hookLength == 0: raise Exception("Cannot insert a hook of length zero.")
        assert(type(buffer) == list)
        
        validLocations = []
        generatedRHT = []
        previousHookValue = max([max(i) for i in buffer])
        
        # first, get valid locations: outermost border
        for row in range(len(buffer)):
            for column in range(len(buffer[row])):

                # not last row case
                if row + 1 < len(buffer):
                    add = False
                    if column == 0 and buffer[row][column] == self.emptyValue and buffer[row + 1][column] != 1:
                        add = True
                    if buffer[row][column] == self.emptyValue and (buffer[row + 1][column] != self.emptyValue or (column > 0 and buffer[row + 1][column - 1] != self.emptyValue)):
                        add = True
                    if add:
                        validLocations.append((row, column))
                
                else:
                    if buffer[row][column] == self.emptyValue:
                        validLocations.append((row, column))
        # now attempt to insert a hook
        if len(validLocations) < hookLength or len(validLocations) == 0:
            return [buffer]
        
        # check each hookLength window for valid insertion
        for startingPoint in range(len(validLocations) - hookLength + 1):
            
            prevLoc = None
            canInsert = True
            cache = copy.deepcopy(buffer)
            # first, we check if we can draw a rim hook that does not break
            for idx in range(startingPoint, startingPoint + hookLength):
                # skip first pair comparison
                if idx == startingPoint:
                    cache[validLocations[idx][0]][validLocations[idx][1]] = previousHookValue + 1
                    prevLoc = validLocations[idx]
                    continue
                if validLocations[idx][0] > prevLoc[0] and validLocations[idx][1] > prevLoc[1]:
                    canInsert = False
                    break
                cache[validLocations[idx][0]][validLocations[idx][1]] = previousHookValue + 1
                prevLoc = validLocations[idx]

            # second, we check if this rim hook is in a valid position
            for idx in range(startingPoint, startingPoint + hookLength):
                rCheck = cache[validLocations[idx][0] + 1][validLocations[idx][1]] == self.emptyValue if validLocations[idx][0] + 1 < len(cache) else False
                cCheck = cache[validLocations[idx][0]][validLocations[idx][1] - 1] == self.emptyValue if validLocations[idx][1] > 0 else False            
                if rCheck or cCheck:
                    canInsert = False
                    break                    

            if canInsert:
                generatedRHT.append(cache)

        return generatedRHT

    def PrettyPrint(self) -> None:
        for rht in self.cache:
            for i in rht.buffer:
                print(i)
            print()