
def findSecond(l, b):   # Findet zweithöchstes/niedrigstes Element in Liste: True-> höchstes; False -> niedrigstes
    tmp = []
    for e in l:
        tmp.append(e)
        tmp.sort(reverse=not b)
        while len(tmp) > 2:
            tmp.pop(0)
    return tmp[0]


def calculateIntersection(a, b):
    x = (a[0][0], a[1][0], b[0][0], b[1][0])
    y = (a[0][1], a[1][1], b[0][1], b[1][1])

    denominator = (y[3] - y[2]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[3] - x[2])
    if denominator == 0:
        return None

    upperLimX = findSecond(x, True)
    lowerLimX = findSecond(x, False)

    upperLimY = findSecond(y, True)
    lowerLimY = findSecond(y, False)

    sX = ( (x[3] - x[2]) * (x[1] * y[0] - x[0] * y[1]) - (x[1] - x[0]) * (x[3] * y[2] - x[2] * y[3]) ) / denominator
    sY = ( (y[0] - y[1]) * (x[3] * y[2] - x[2] * y[3]) - (y[2] - y[3]) * (x[1] * y[0] - x[0] * y[1]) ) / denominator

    S = (sX, sY)

    if (lowerLimX <= sX <= upperLimX) and (lowerLimY <= sY <= upperLimY):
        return S

    return None

def main():
    a = ( (0,2), (2,0))
    b = ( (2,0), (2,1))
    S = calculateIntersection(a, b)
    print(S)

if __name__ == '__main__':
    main()
