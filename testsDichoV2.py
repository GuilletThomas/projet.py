def f(x):
    return 2 * x - 3


a = 1
b = 3

while b - a > 10e-6:
    m = (b + a) / 2
    if f(m) * f(a) > 0:
        a = m
    else:
        b = m
print(m)




