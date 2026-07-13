# Copyright (C) 2026 by Jason Lee,silent_wind
# This program is free software:
#  you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# x = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
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
    for i in range(4):
        for j in range(4):
            esdaout[i][j] = ASK[i][j] + dz[i][j]

    return esdaout
def unesda(esdaout = [[2,15,14,10],[15,21,18,-64],[12,5,-64,13],[15,14,4,5]],y = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
    x = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3],y[1][1],y[2][0],y[3][1]],[y[0][0],y[2][1],y[0][2],y[2][3]],[y[1][0],y[1][3],y[1][2],y[3][3]],[y[2][0],y[3][0],y[2][2],y[3][2]]]
    
    for i in range(4):
        for j in range(4):
            dz[i][j] = esdaout[i][j] - ASK[i][j]
    for i in range(4):
        z[3][i]=dz[0][i]
        for j in range(1,4):
            z[j-1][i]=dz[j][i]
    for i in range(4):
        for j in range(4):
            x[i][j] = z[i][j] - y[i][j]
    
    return x

