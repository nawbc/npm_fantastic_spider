def demo():
    for i in range(4):
        yield i
        yield i + 4

a = demo()

print(next(a))
print(next(a))
print(next(a))
print(next(a))
