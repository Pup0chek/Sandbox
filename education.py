


def main():
    int1 = 16
    ans = 1
    for i in range(1, int1+1):
        ans *= i
    ans1 = str(ans)
    print(ans1)
    print(ans1[:-1])
    if ans1[-1] == '0':
        cnt = 1
        ans1 = ans1[:-1]
        while ans1[-1] == '0':
            cnt += 1
            ans1 = ans1[:-1]
        # for i in range(1, len(ans1)+1):
        #     if
        #     print(ans1[-i])
    print(cnt)



if __name__ == "__main__":
    main()