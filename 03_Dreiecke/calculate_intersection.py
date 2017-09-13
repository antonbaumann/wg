def find_second(l, b):
    tmp = []
    for e in l:
        tmp.append(e)
        tmp.sort(reverse=not b)
        while len(tmp) > 2:
            tmp.pop(0)
    return tmp[0]


def calculate_intersection(a, b):
    x = (a[0][0], a[1][0], b[0][0], b[1][0])
    y = (a[0][1], a[1][1], b[0][1], b[1][1])

    denominator = (y[3] - y[2]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[3] - x[2])
    if denominator == 0:
        return None

    upper_x_a = max(a[0][0], a[1][0])
    lower_x_a = min(a[0][0], a[1][0])
    upper_y_a = max(a[0][1], a[1][1])
    lower_y_a = min(a[0][1], a[1][1])

    upper_x_b = max(b[0][0], b[1][0])
    lower_x_b = min(b[0][0], b[1][0])
    upper_y_b = max(b[0][1], b[1][1])
    lower_y_b = min(b[0][1], b[1][1])



    s_x = ((x[3] - x[2]) * (x[1] * y[0] - x[0] * y[1]) - (x[1] - x[0]) * (x[3] * y[2] - x[2] * y[3])) / denominator
    s_y = ((y[0] - y[1]) * (x[3] * y[2] - x[2] * y[3]) - (y[2] - y[3]) * (x[1] * y[0] - x[0] * y[1])) / denominator

    if s_x == -0.0:
        s_x = 0.0
    if s_y == -0.0:
        s_y = 0.0
    S = (s_x, s_y)

    if lower_x_a <= s_x <= upper_x_a and lower_x_b <= s_x <= upper_x_b:
        if lower_y_a <= s_y <= upper_y_a and lower_y_b <= s_y <= upper_y_b:
            plt.plot(S[0], S[1], marker='x', color='r')
            return S

    return None


if __name__ == '__main__':
    A = (2, 2)
    B = (6, 7)
    C = (5, 4)
    D = (6, 2)

    print(calculate_intersection((A, B), (C, D)))
