def restoreIpAddresses(s):
    """
    :type s: str
    :rtype: List[str]
    """
    fs=[]
    sc=[]
    th=[]
    fr=[]
    # for i in range(0, len(s), 4):
    #     for y in range(3):
    #         match y:
    #             case 0:
    #                 fs += s[i+y]
    #             case 1:
    #                 sc += s[i+y]
    #             case 2:
    #                 th += s[i+y]
    sw = [[], [], [], []]
    cnt = 0
    while cnt !=4:
        for i in range(0, len(s)-3, 3):
            print(s[i])
            sw[cnt] += s[i]
            sw[cnt] += s[i+1]
            sw[cnt] += s[i+2]
            cnt += 1
        print(sw)
    return True





def main():
    s = '25525511135'
    print(restoreIpAddresses(s))


if __name__ == "__main__":
    main()