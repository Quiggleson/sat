This is another attempt at the ghost clause algo with the eleven
clause instance
[1, 2, 3]
[1, 2, -3]
[1, -2, 3]
[-1, 2, 3]
[-1, 2, -3]
[-1, -2, 3]
[4, 5, 6]
[4, 5, -6]
[4, -5, 6]
[4, -5, -6]
[-2, -3, -4]

assignments with the following condition are blocked:
$x_1 = x_2 = x_3 = 0$
$x_1 = x_2 = 0; x_3 = 1$
$x_1 = x_3 = 0; x_2 = 1$
$x_1 = 1; x_2 = x_3 = 0$
$x_1 = x_3 = 1; x_2 = 0$
$x_4 = x_5 = x_6 = 0$
$x_4 = x_5 = 0; x_6 = 1$
$x_4 = x_6 = 0; x_5 = 1$
$x_4 = 0; x_5 = x_6 = 1$
$x_2 = x_3 = x_4 = 1$

Two clause pattern - any assignment with two terminals constant and the
remaining terminal flipping signs:

term 1 = [1, 2], [1, 3], [-1, 2], [-1, 3]
term 2 = [2, 3], []
term 3
term 4
term 5
term 6
