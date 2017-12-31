#! /usr/bin/env python3
import copy


def wall_to_string(wall):
    if wall == []:
        return '|_|'
    n = len(wall[0]) + 1
    l = int(n * (n + 1) / 2)
    l_str = l + n + 1
    s = ''
    for row in wall:
        _n = n
        str_row = '|'
        for i, gap in enumerate(row):
            x = 0
            if i != 0:
                x = row[i-1]
            str_row += '_' * (gap - x) + '|'
        left = l_str - len(str_row)
        str_row += '_' * (left - 1) + '|'
        s += str_row + '\n'

    return s

def construct_wall(n):
    wall = []
    box_of_bricks = [x for x in range(1, n+1)]
    used_positions = set()
    if n == 1:
        return wall
    while True:
        index = 0
        position = 0
        row = []
        new_box = copy.copy(box_of_bricks)
        while len(new_box) > 1:
            if index >= len(new_box):
                return wall
            if position + new_box[index] not in used_positions:
                position += new_box[index]
                row.append(position)
                used_positions.add(position)
                new_box.remove(new_box[index])
                index = 0
            else:
                index += 1
        wall.append(row)


if __name__ == '__main__':
    inp = int(input('blocks per row: '))
    w = construct_wall(inp)
    print(wall_to_string(w))