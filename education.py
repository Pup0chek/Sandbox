def snail(array):
    ans = []
    while array:
        ans.extend(array.pop(0))

        if array:
            for i in array:
                ans.append(i.pop())
        if array:
            ans.extend(array.pop()[::-1])
        if array:
            for i in array[::-1]:
                ans.append(i.pop(0))
    return ans


def main():
    array = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
    print(snail(array))#=> [1,2,3,6,9,8,7,4,5])



if __name__ == "__main__":
    main()