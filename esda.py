# 示例x = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
def esda(x = [[15,21,18,-64],[12,5,-64,13],[15,14,4,5],[2,15,14,10]],y = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
    esdaout = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3],y[1][1],y[2][0],y[3][1]],[y[0][0],y[2][1],y[0][2],y[2][3]],[y[1][0],y[1][3],y[1][2],y[3][3]],[y[2][0],y[3][0],y[2][2],y[3][2]]]
    
    for i in range(4):
        for j in range(4):
            z[i][j] = x[i][j] + y[i][j]
    for i in range(4):
        dz[0][i] = z[3][i]
        for j in range(1,4):
            dz[j][i] = z[j-1][i]
    # print("ffffffffffffffffffffffff")
    for i in range(4):
        for j in range(4):
            esdaout[i][j] = ASK[i][j] + dz[i][j]
    
    # 调试
    for i in range(4):
        for j in range(4):
            print(chr(esdaout[i][j]+96),end=" ")
        print("")
    return esdaout
# print(chr(esda()+96))