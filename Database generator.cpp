#include <vector>
#include <queue>
#include <map>
#include <string>
#include <tuple>
#include <random>
#include <cstdint>
#include <iostream>
#include <chrono>
#include <fstream>
#include <bits/stdc++.h>
using namespace std;

vector<vector<int8_t>> generate()
{
    vector<vector<int8_t>> result = {{0, 0, 0, 0, 0, 0, 0, 0, 0},
                                     {1, 1, 1, 1, 1, 1, 1, 1, 1},
                                     {2, 2, 2, 2, 2, 2, 2, 2, 2},
                                     {3, 3, 3, 3, 3, 3, 3, 3, 3},
                                     {4, 4, 4, 4, 4, 4, 4, 4, 4},
                                     {5, 5, 5, 5, 5, 5, 5, 5, 5}};
    return result;
}

void applymoves(vector<vector<int8_t>> &cube, string move)
{
    if (move == "R")
    {
        // side face
        int8_t temp = cube[1][6];
        cube[1][6] = cube[1][8];
        cube[1][8] = cube[1][2];
        cube[1][2] = cube[1][0];

        cube[1][0] = temp;
        temp = cube[1][3];
        cube[1][3] = cube[1][7];
        cube[1][7] = cube[1][5];
        cube[1][5] = cube[1][1];
        cube[1][1] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][2], cube[0][5], cube[0][8]};
        cube[0][2] = cube[5][2];
        cube[0][5] = cube[5][5];
        cube[0][8] = cube[5][8];
        cube[5][2] = cube[2][6];
        cube[5][5] = cube[2][3];
        cube[5][8] = cube[2][0];
        cube[2][6] = cube[4][2];
        cube[2][3] = cube[4][5];
        cube[2][0] = cube[4][8];
        cube[4][2] = temp1[0];
        cube[4][5] = temp1[1];
        cube[4][8] = temp1[2];
    }
    if (move == "L")
    {
        // side face
        int8_t temp = cube[3][6];
        cube[3][6] = cube[3][8];
        cube[3][8] = cube[3][2];
        cube[3][2] = cube[3][0];
        cube[3][0] = temp;
        temp = cube[3][3];
        cube[3][3] = cube[3][7];
        cube[3][7] = cube[3][5];
        cube[3][5] = cube[3][1];
        cube[3][1] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][3], cube[0][6]};
        cube[0][0] = cube[4][0];
        cube[0][3] = cube[4][3];
        cube[0][6] = cube[4][6];
        cube[4][0] = cube[2][8];
        cube[4][3] = cube[2][5];
        cube[4][6] = cube[2][2];
        cube[2][8] = cube[5][0];
        cube[2][5] = cube[5][3];
        cube[2][2] = cube[5][6];
        cube[5][0] = temp1[0];
        cube[5][3] = temp1[1];
        cube[5][6] = temp1[2];
    }
    if (move == "U")
    {
        // top face
        int8_t temp = cube[4][6];
        cube[4][6] = cube[4][8];
        cube[4][8] = cube[4][2];
        cube[4][2] = cube[4][0];
        cube[4][0] = temp;
        temp = cube[4][3];
        cube[4][3] = cube[4][7];
        cube[4][7] = cube[4][5];
        cube[4][5] = cube[4][1];
        cube[4][1] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][1], cube[0][2]};
        cube[0][0] = cube[1][0];
        cube[0][1] = cube[1][1];
        cube[0][2] = cube[1][2];
        cube[1][0] = cube[2][0];
        cube[1][1] = cube[2][1];
        cube[1][2] = cube[2][2];
        cube[2][0] = cube[3][0];
        cube[2][1] = cube[3][1];
        cube[2][2] = cube[3][2];
        cube[3][0] = temp1[0];
        cube[3][1] = temp1[1];
        cube[3][2] = temp1[2];
    }
    if (move == "D")
    {
        // bottom face
        int8_t temp = cube[5][6];
        cube[5][6] = cube[5][8];
        cube[5][8] = cube[5][2];
        cube[5][2] = cube[5][0];
        cube[5][0] = temp;
        temp = cube[5][3];
        cube[5][3] = cube[5][7];
        cube[5][7] = cube[5][5];
        cube[5][5] = cube[5][1];
        cube[5][1] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[0][6], cube[0][7], cube[0][8]};
        cube[0][6] = cube[3][6];
        cube[0][7] = cube[3][7];
        cube[0][8] = cube[3][8];
        cube[3][6] = cube[2][6];
        cube[3][7] = cube[2][7];
        cube[3][8] = cube[2][8];
        cube[2][6] = cube[1][6];
        cube[2][7] = cube[1][7];
        cube[2][8] = cube[1][8];
        cube[1][6] = temp1[0];
        cube[1][7] = temp1[1];
        cube[1][8] = temp1[2];
    }
    if (move == "F")
    {
        // front face
        int8_t temp = cube[0][6];
        cube[0][6] = cube[0][8];
        cube[0][8] = cube[0][2];
        cube[0][2] = cube[0][0];
        cube[0][0] = temp;
        temp = cube[0][3];
        cube[0][3] = cube[0][7];
        cube[0][7] = cube[0][5];
        cube[0][5] = cube[0][1];
        cube[0][1] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[1][0], cube[1][3], cube[1][6]};
        cube[1][0] = cube[4][6];
        cube[1][3] = cube[4][7];
        cube[1][6] = cube[4][8];
        cube[4][6] = cube[3][8];
        cube[4][7] = cube[3][5];
        cube[4][8] = cube[3][2];
        cube[3][8] = cube[5][2];
        cube[3][5] = cube[5][1];
        cube[3][2] = cube[5][0];
        cube[5][2] = temp1[0];
        cube[5][1] = temp1[1];
        cube[5][0] = temp1[2];
    }
    if (move == "B")
    {
        // back face
        int8_t temp = cube[2][6];
        cube[2][6] = cube[2][8];
        cube[2][8] = cube[2][2];
        cube[2][2] = cube[2][0];
        cube[2][0] = temp;

        temp = cube[2][3];
        cube[2][3] = cube[2][7];
        cube[2][7] = cube[2][5];
        cube[2][5] = cube[2][1];
        cube[2][1] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[1][2], cube[1][5], cube[1][8]};
        cube[1][2] = cube[5][8];
        cube[1][5] = cube[5][7];
        cube[1][8] = cube[5][6];
        cube[5][8] = cube[3][6];
        cube[5][7] = cube[3][3];
        cube[5][6] = cube[3][0];
        cube[3][6] = cube[4][0];
        cube[3][3] = cube[4][1];
        cube[3][0] = cube[4][2];
        cube[4][2] = temp1[2];
        cube[4][1] = temp1[1];
        cube[4][0] = temp1[0];
    }
    if (move == "R'")
    {
        // side face
        int8_t temp = cube[1][6];
        cube[1][6] = cube[1][0];
        cube[1][0] = cube[1][2];
        cube[1][2] = cube[1][8];

        cube[1][8] = temp;
        temp = cube[1][3];
        cube[1][3] = cube[1][1];
        cube[1][1] = cube[1][5];
        cube[1][5] = cube[1][7];
        cube[1][7] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][2], cube[0][5], cube[0][8]};
        cube[0][2] = cube[4][2];
        cube[0][5] = cube[4][5];
        cube[0][8] = cube[4][8];
        cube[4][2] = cube[2][6];
        cube[4][5] = cube[2][3];
        cube[4][8] = cube[2][0];
        cube[2][6] = cube[5][2];
        cube[2][3] = cube[5][5];
        cube[2][0] = cube[5][8];
        cube[5][2] = temp1[0];
        cube[5][5] = temp1[1];
        cube[5][8] = temp1[2];
    }
    if (move == "L'")
    {
        // side face
        int8_t temp = cube[3][6];
        cube[3][6] = cube[3][0];
        cube[3][0] = cube[3][2];
        cube[3][2] = cube[3][8];

        cube[3][8] = temp;
        temp = cube[3][3];
        cube[3][3] = cube[3][1];
        cube[3][1] = cube[3][5];
        cube[3][5] = cube[3][7];
        cube[3][7] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][3], cube[0][6]};
        cube[0][0] = cube[5][0];
        cube[0][3] = cube[5][3];
        cube[0][6] = cube[5][6];
        cube[5][0] = cube[2][8];
        cube[5][3] = cube[2][5];
        cube[5][6] = cube[2][2];
        cube[2][8] = cube[4][0];
        cube[2][5] = cube[4][3];
        cube[2][2] = cube[4][6];
        cube[4][0] = temp1[0];
        cube[4][3] = temp1[1];
        cube[4][6] = temp1[2];
    }
    if (move == "U'")
    {
        // top face
        int8_t temp = cube[4][6];
        cube[4][6] = cube[4][0];
        cube[4][0] = cube[4][2];
        cube[4][2] = cube[4][8];
        cube[4][8] = temp;
        temp = cube[4][3];
        cube[4][3] = cube[4][1];
        cube[4][1] = cube[4][5];
        cube[4][5] = cube[4][7];
        cube[4][7] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][1], cube[0][2]};
        cube[0][0] = cube[3][0];
        cube[0][1] = cube[3][1];
        cube[0][2] = cube[3][2];
        cube[3][0] = cube[2][0];
        cube[3][1] = cube[2][1];
        cube[3][2] = cube[2][2];
        cube[2][0] = cube[1][0];
        cube[2][1] = cube[1][1];
        cube[2][2] = cube[1][2];
        cube[1][0] = temp1[0];
        cube[1][1] = temp1[1];
        cube[1][2] = temp1[2];
    }
    if (move == "D'")
    {
        // bottom face
        int8_t temp = cube[5][6];
        cube[5][6] = cube[5][0];
        cube[5][0] = cube[5][2];
        cube[5][2] = cube[5][8];
        cube[5][8] = temp;
        temp = cube[5][3];
        cube[5][3] = cube[5][1];
        cube[5][1] = cube[5][5];
        cube[5][5] = cube[5][7];
        cube[5][7] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[0][6], cube[0][7], cube[0][8]};
        cube[0][6] = cube[1][6];
        cube[0][7] = cube[1][7];
        cube[0][8] = cube[1][8];
        cube[1][6] = cube[2][6];
        cube[1][7] = cube[2][7];
        cube[1][8] = cube[2][8];
        cube[2][6] = cube[3][6];
        cube[2][7] = cube[3][7];
        cube[2][8] = cube[3][8];
        cube[3][6] = temp1[0];
        cube[3][7] = temp1[1];
        cube[3][8] = temp1[2];
    }
    if (move == "F'")
    {
        // front face
        int8_t temp = cube[0][6];
        cube[0][6] = cube[0][0];
        cube[0][0] = cube[0][2];
        cube[0][2] = cube[0][8];
        cube[0][8] = temp;
        temp = cube[0][3];
        cube[0][3] = cube[0][1];
        cube[0][1] = cube[0][5];
        cube[0][5] = cube[0][7];
        cube[0][7] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[1][0], cube[1][3], cube[1][6]};
        cube[1][0] = cube[5][2];
        cube[1][3] = cube[5][1];
        cube[1][6] = cube[5][0];
        cube[5][2] = cube[3][8];
        cube[5][1] = cube[3][5];
        cube[5][0] = cube[3][2];
        cube[3][8] = cube[4][6];
        cube[3][5] = cube[4][7];
        cube[3][2] = cube[4][8];
        cube[4][6] = temp1[0];
        cube[4][7] = temp1[1];
        cube[4][8] = temp1[2];
    }
    if (move == "B'")
    {
        // back face
        int8_t temp = cube[2][6];
        cube[2][6] = cube[2][0];
        cube[2][0] = cube[2][2];
        cube[2][2] = cube[2][8];
        cube[2][8] = temp;

        temp = cube[2][3];
        cube[2][3] = cube[2][1];
        cube[2][1] = cube[2][5];
        cube[2][5] = cube[2][7];
        cube[2][7] = temp;

        // rest four faces
        vector<int8_t> temp1 = {cube[1][2], cube[1][5], cube[1][8]};
        cube[1][2] = cube[4][0];
        cube[1][5] = cube[4][1];
        cube[1][8] = cube[4][2];
        cube[4][0] = cube[3][6];
        cube[4][1] = cube[3][3];
        cube[4][2] = cube[3][0];
        cube[3][0] = cube[5][6];
        cube[3][3] = cube[5][7];
        cube[3][6] = cube[5][8];
        cube[5][6] = temp1[2];
        cube[5][7] = temp1[1];
        cube[5][8] = temp1[0];
    }
    if (move == "R2")
    {
        // side face
        int8_t temp = cube[1][6];
        cube[1][6] = cube[1][2];
        cube[1][2] = temp;
        temp = cube[1][7];
        cube[1][7] = cube[1][1];
        cube[1][1] = temp;
        temp = cube[1][8];
        cube[1][8] = cube[1][0];
        cube[1][0] = temp;
        temp = cube[1][5];
        cube[1][5] = cube[1][3];
        cube[1][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][2], cube[0][5], cube[0][8]};

        cube[0][2] = cube[2][6];
        cube[0][5] = cube[2][3];
        cube[0][8] = cube[2][0];
        cube[2][6] = temp1[0];
        cube[2][3] = temp1[1];
        cube[2][0] = temp1[2];
        temp1 = {cube[4][2], cube[4][5], cube[4][8]};
        cube[4][2] = cube[5][2];
        cube[4][5] = cube[5][5];
        cube[4][8] = cube[5][8];
        cube[5][2] = temp1[0];
        cube[5][5] = temp1[1];
        cube[5][8] = temp1[2];
    }
    if (move == "L2")
    {
        // side face
        int8_t temp = cube[3][6];
        cube[3][6] = cube[3][2];
        cube[3][2] = temp;
        temp = cube[3][7];
        cube[3][7] = cube[3][1];
        cube[3][1] = temp;
        temp = cube[3][8];
        cube[3][8] = cube[3][0];
        cube[3][0] = temp;
        temp = cube[3][5];
        cube[3][5] = cube[3][3];
        cube[3][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][3], cube[0][6]};

        cube[0][0] = cube[2][8];
        cube[0][3] = cube[2][5];
        cube[0][6] = cube[2][2];
        cube[2][8] = temp1[0];
        cube[2][5] = temp1[1];
        cube[2][2] = temp1[2];
        temp1 = {cube[4][0], cube[4][3], cube[4][6]};
        cube[4][0] = cube[5][0];
        cube[4][3] = cube[5][3];
        cube[4][6] = cube[5][6];
        cube[5][0] = temp1[0];
        cube[5][3] = temp1[1];
        cube[5][6] = temp1[2];
    }
    if (move == "U2")
    {
        // top face
        int8_t temp = cube[4][6];
        cube[4][6] = cube[4][2];
        cube[4][2] = temp;
        temp = cube[4][7];
        cube[4][7] = cube[4][1];
        cube[4][1] = temp;
        temp = cube[4][8];
        cube[4][8] = cube[4][0];
        cube[4][0] = temp;
        temp = cube[4][5];
        cube[4][5] = cube[4][3];
        cube[4][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][0], cube[0][1], cube[0][2]};

        cube[0][0] = cube[2][0];
        cube[0][1] = cube[2][1];
        cube[0][2] = cube[2][2];
        cube[2][0] = temp1[0];
        cube[2][1] = temp1[1];
        cube[2][2] = temp1[2];
        temp1 = {cube[1][0], cube[1][1], cube[1][2]};
        cube[1][0] = cube[3][0];
        cube[1][1] = cube[3][1];
        cube[1][2] = cube[3][2];
        cube[3][0] = temp1[0];
        cube[3][1] = temp1[1];
        cube[3][2] = temp1[2];
    }
    if (move == "D2")
    {
        // bottom face
        int8_t temp = cube[5][6];
        cube[5][6] = cube[5][2];
        cube[5][2] = temp;
        temp = cube[5][7];
        cube[5][7] = cube[5][1];
        cube[5][1] = temp;
        temp = cube[5][8];
        cube[5][8] = cube[5][0];
        cube[5][0] = temp;
        temp = cube[5][5];
        cube[5][5] = cube[5][3];
        cube[5][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[0][6], cube[0][7], cube[0][8]};

        cube[0][6] = cube[2][6];
        cube[0][7] = cube[2][7];
        cube[0][8] = cube[2][8];
        cube[2][6] = temp1[0];
        cube[2][7] = temp1[1];
        cube[2][8] = temp1[2];
        temp1 = {cube[1][6], cube[1][7], cube[1][8]};
        cube[1][6] = cube[3][6];
        cube[1][7] = cube[3][7];
        cube[1][8] = cube[3][8];
        cube[3][6] = temp1[0];
        cube[3][7] = temp1[1];
        cube[3][8] = temp1[2];
    }
    if (move == "F2")
    {
        // front face
        int8_t temp = cube[0][6];
        cube[0][6] = cube[0][2];
        cube[0][2] = temp;
        temp = cube[0][7];
        cube[0][7] = cube[0][1];
        cube[0][1] = temp;
        temp = cube[0][8];
        cube[0][8] = cube[0][0];
        cube[0][0] = temp;
        temp = cube[0][5];
        cube[0][5] = cube[0][3];
        cube[0][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[1][0], cube[1][3], cube[1][6]};

        cube[1][0] = cube[3][8];
        cube[1][3] = cube[3][5];
        cube[1][6] = cube[3][2];
        cube[3][8] = temp1[0];
        cube[3][5] = temp1[1];
        cube[3][2] = temp1[2];
        temp1 = {cube[4][6], cube[4][7], cube[4][8]};
        cube[4][6] = cube[5][2];
        cube[4][7] = cube[5][1];
        cube[4][8] = cube[5][0];
        cube[5][2] = temp1[0];
        cube[5][1] = temp1[1];
        cube[5][0] = temp1[2];
    }
    if (move == "B2")
    {
        // back face
        int8_t temp = cube[2][6];
        cube[2][6] = cube[2][2];
        cube[2][2] = temp;
        temp = cube[2][7];
        cube[2][7] = cube[2][1];
        cube[2][1] = temp;
        temp = cube[2][8];
        cube[2][8] = cube[2][0];
        cube[2][0] = temp;
        temp = cube[2][5];
        cube[2][5] = cube[2][3];
        cube[2][3] = temp;
        // rest four faces
        vector<int8_t> temp1 = {cube[1][2], cube[1][5], cube[1][8]};

        cube[1][2] = cube[3][6];
        cube[1][5] = cube[3][3];
        cube[1][8] = cube[3][0];
        cube[3][6] = temp1[0];
        cube[3][3] = temp1[1];
        cube[3][0] = temp1[2];
        temp1 = {cube[4][0], cube[4][1], cube[4][2]};
        cube[4][0] = cube[5][8];
        cube[4][1] = cube[5][7];
        cube[4][2] = cube[5][6];
        cube[5][8] = temp1[0];
        cube[5][7] = temp1[1];
        cube[5][6] = temp1[2];
    }
}
char num2color(int8_t num)
{
    if (num == 0)
    {
        return 'W';
    }
    if (num == 1)
    {
        return 'G';
    }
    if (num == 2)
    {
        return 'Y';
    }
    if (num == 3)
    {
        return 'B';
    }
    if (num == 4)
    {
        return 'R';
    }
    if (num == 5)
    {
        return 'O';
    }
}
void printcube(vector<vector<int8_t>> cube)
{

    cout << "Front Face   " << "Right Face   " << "Back Face    " << "Left Face    " << "Top Face     " << "Bottom Face   " << endl;
    for (int i = 0; i < 54; i++)
    {
        int k = (i / 3) % 6;
        int r = i / 18;
        if (i != 0 && i % 18 == 0)
        {
            cout << endl;
        }
        cout << num2color(cube[k][3 * r + i % 3]) << " ";
        if (i % 3 == 2)
        {
            cout << "       ";
        }
    }
}
int hash_stage0(const vector<vector<int8_t>> &cube)
{
    // Edges represented as compressed positions
    vector<int> reqedgelist = {2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517};

    int num = 0;

    for (int i : reqedgelist)
    {
        int a = i % 10;
        int b = (i / 10) % 10;
        int c = (i / 100) % 10;
        int d = i / 1000;

        // Bounds checking
        if (d >= cube.size() || c >= cube[d].size() || b >= cube.size() || a >= cube[b].size())
        {
            throw std::out_of_range("Invalid edge index in reqedgelist");
        }

        num = num << 1; // Shift left to make space for the new bit

        // Determine edge orientation
        if (cube[d][c] == 1 || cube[d][c] == 3)
        {
            num = num | 1;
        }
        else if (cube[d][c] == 4 || cube[d][c] == 5)
        {
            if (cube[b][a] == 0 || cube[b][a] == 2)
            {
                num = num | 1;
            }
            else
            {
                num = num | 0;
            }
        }
        else
        {
            num = num | 0;
        }
    }
    return num;
}

bool check_stage0(vector<vector<int8_t>> &cube)
{
    if (hash_stage0(cube) == 0)
    {
        return true;
    }
    return false;
}

int hash_stage1(const vector<vector<int8_t>> &cube)
{
    // Corners represented as compressed positions
    vector<int> reqcornerlist = {302240, 122042, 100248, 320046, 362856, 182658, 160852, 380650};
    vector<int> reqedgelist = {2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517};
    vector<int> reqedgescolor = {42, 40, 52, 50};

    long long num = 0; // Use long long to prevent overflow

    // Process corners
    for (int i : reqcornerlist)
    {
        int f = (i / 100000);
        int e = (i / 10000) % 10;
        int d = (i / 1000) % 10;
        int c = (i / 100) % 10;

        int orientation = 0;
        if (cube[f][e] == 1 || cube[f][e] == 3)
        {
            orientation = 0;
        }
        else if (cube[d][c] == 1 || cube[d][c] == 3)
        {
            orientation = 1;
        }
        else
        {
            orientation = 2;
        }

        num = (num << 2) | orientation; // Pack 2 bits for each corner
    }

    // Process edges
    for (int i : reqedgelist)
    {
        int color = cube[i / 1000][(i / 100) % 10] * 10 + cube[(i / 10) % 10][i % 10];

        // Determine edge orientation
        bool matches = false;
        for (int j = 0; j < 4; j++)
        {
            if (color == reqedgescolor[j] || (color % 10) * 10 + (color / 10) == reqedgescolor[j])
            {
                matches = true;
                break;
            }
        }

        num = (num << 1) | (matches ? 0 : 1); // Pack 1 bit for each edge
    }

    return num;
}

int getcolor(vector<vector<int8_t>> cube, int i)
{
    int f = i / 100000;
    int e = (i / 10000) % 10;
    int d = (i / 1000) % 10;
    int c = (i / 100) % 10;
    int b = (i / 10) % 10;
    int a = i % 10;

    vector<int> colors = {cube[f][e], cube[d][c], cube[b][a]};
    sort(colors.begin(), colors.end());
    return colors[0] * 100 + colors[1] * 10 + colors[2];
}
void imitateMove(const std::string &move, std::array<int, 8> &tetradsPerm)
{
    std::array<int, 4> indices, positions;

    if (move == "U2")
        indices = {0, 6, 1, 7};
    else if (move == "D2")
        indices = {2, 4, 3, 5};
    else if (move == "L2")
        indices = {0, 2, 1, 3};
    else if (move == "R2")
        indices = {4, 6, 5, 7};
    else if (move == "F2")
        indices = {2, 6, 1, 5};
    else if (move == "B2")
        indices = {0, 4, 3, 7};
    else
        throw std::logic_error("G2_G3_database::imitateMove invalid move: " + move);

    // Initialize positions to avoid undefined behavior
    positions.fill(-1);

    // Find the positions of the affected indices
    for (int i = 0; i < 8; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            if (tetradsPerm[i] == indices[j] && positions[j] == -1)
            {
                positions[j] = i;
                break;
            }
        }
    }

    // Perform swaps to simulate the move
    std::swap(tetradsPerm[positions[0]], tetradsPerm[positions[1]]);
    std::swap(tetradsPerm[positions[2]], tetradsPerm[positions[3]]);
}

int64_t hash3(vector<vector<int8_t>> &cube)
{

    vector<int> reqcornerlist = {302240, 320046, 380650, 362856, 182658, 160852, 100248, 122042};
    vector<int> color = {234, 34, 35, 235, 125, 15, 14, 124};
    vector<int> reqedgelist = {2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517};
    vector<int> reqedgescolor = {43, 41, 53, 51};
    vector<int> even, odd;
    int64_t num = 0;
    vector<int> actual(8, -1);
    int k = 0;
    for (int i : reqcornerlist)
    {
        int value = getcolor(cube, i);
        for (int j = 0; j < 8; j++)
        {
            if (value == color[j])
            {
                actual[k] = j;
                k++;
                break;
            }
        }
    }

    for (int i = 0; i < 8; i++)
    {
        if (actual[i] % 2 == 0)
        {
            num = num << 1 | 1;
        }
        else
        {
            num = num << 1 | 0;
        }
    }
    // Process edges
    for (int i : reqedgelist)
    {
        int color = cube[i / 1000][(i / 100) % 10] * 10 + cube[(i / 10) % 10][i % 10];

        // Determine edge orientation
        bool matches = false;
        for (int j = 0; j < 4; j++)
        {
            if (color == reqedgescolor[j] || (color % 10) * 10 + (color / 10) == reqedgescolor[j])
            {
                matches = true;
                break;
            }
        }

        num = (num << 1) | (matches ? 0 : 1); // Pack 1 bit for each edge
        
    }

    // stores the positions of the 4 corners that need to be brought back to the even tetrad
    std::array<int, 4> C_posComb;
    // extracts the corners into their tetrads while keeping the same relative order from the initial perm
    std::array<int, 4> C_eTetrad, C_oTetrad;
    std::array<int, 8> C_tetradsPerm;
    vector<vector<string>> C_evenTetradSolvingMoves = {{"U2", "L2", "B2"}, {"D2", "F2"}, {"R2"}};
    vector<vector<string>> C_oddTetradSolvingMoves = {{"F2", "L2", "F2", "U2"}, {"U2", "F2", "U2", "L2"}, {"L2", "U2", "L2", "F2"}};
    // used to check the positions of the even tetrad first
    const std::array<int, 8> C_map = {0, 2, 4, 6, 1, 3, 5, 7};

    for (int i = 0, e = 0, c = 0, ce = 0, co = 0; i < 8; ++i)
    {

        // even tetrad (even indices)
        if (actual[C_map[i]] % 2 == 0)
        {
            C_posComb[c++] = i+1 ;
        }
        // splits the corners while keeping the relative order
        if (actual[i] % 2 == 0)
            C_eTetrad[ce++] = actual[i];
        else
            C_oTetrad[co++] = actual[i];
    }
    
    // forms the new permutation with the corners in their tetrads in relative order
    for (unsigned i = 0; i < 8; ++i)
    {
        C_tetradsPerm[i] = (i & 1) ? C_oTetrad[i >> 1] : C_eTetrad[i >> 1];
    }

    // solves the even tetrad (ULB = 0, DLF = 2, DRB = 4, URF = 6)
    for (int i = 0; i < 6; i += 2)
    {
        if (C_tetradsPerm[i] == i)
            continue;

        for (auto move : C_evenTetradSolvingMoves[i / 2])
        {
            imitateMove(move, C_tetradsPerm);
            if (C_tetradsPerm[i] == i)
                break;
            imitateMove(move, C_tetradsPerm);
        }
    }
    
    // solves one corner in the odd tetrad (ULF = 1)
    int move_sequence = 0;
    while (C_tetradsPerm[1] != 1)
    {
        for (int j = 0; j < 4; ++j)
        {
            imitateMove(C_oddTetradSolvingMoves[move_sequence][j], C_tetradsPerm);
        }
        if (C_tetradsPerm[1] == 1)
            break;
        for (int j = 3; j >= 0; --j)
        {
            imitateMove(C_oddTetradSolvingMoves[move_sequence][j], C_tetradsPerm);
        }
        move_sequence++;
        
      
        
    }
    
    
    // stores the permutation of the remaining 3 corners in the odd tetrad (3,5,7) as (0,1,2)
    std::array<int, 3> C_tetradTwist = {
        (int)((C_tetradsPerm[3] >> 1) - 1),
        (int)((C_tetradsPerm[5] >> 1) - 1),
        (int)((C_tetradsPerm[7] >> 1) - 1),
    };
    for (int i=0;i<3;i++){
        num=num<<2 | C_tetradTwist[i];
    }
    
    return num;
}
int64_t hash4(vector<vector<int8_t>> &cube){
    vector<int> reqcornerlist = {302240, 320046, 380650, 362856, 182658, 160852, 100248, 122042};
    vector<int> color = {234, 34, 35, 235, 125, 15, 14, 124};
    vector<int> reqedgelist = {2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517};
    vector<int> reqedgescolor = {43, 41, 53, 51};    
     vector<int> actual(8, -1);
    int k = 0;
    for (int i : reqcornerlist)
    {
        int value = getcolor(cube, i);
        for (int j = 0; j < 8; j++)
        {
            if (value == color[j])
            {
                actual[k] = j;
                k++;
                break;
            }
        }
    }
   
    int64_t num = 0;
    for (int i = 0; i < 8; i+=2)
    {
        num=num<<2|(actual[i]/2);
    }
    for(int i=1;i<8;i+=2){
        num=num<<2|(actual[i]/2);
    }
    // E slice edges
    vector<int> E_slice={147,751,2141,2757};
    vector<int> E_color={42, 40, 52, 50};
    for(int i=0;i<4;i++){
        int color = cube[E_slice[i] / 1000][(E_slice[i] / 100) % 10] * 10 + cube[(E_slice[i] / 10) % 10][E_slice[i] % 10];
 
        for (int j = 0; j < 4; j++)
        {
            if (color == E_color[j] || (color % 10) * 10 + (color / 10) == E_color[j])
            {
               num = num << 2 | j;
                break;
            }
        }
        
    }
    //s slice
    vector<int> S_slice={ 4331,4511, 5337, 5517};
    vector<int> S_color={43, 41, 53, 51};
    for(int i=0;i<4;i++){
        int color = cube[S_slice[i] / 1000][(S_slice[i] / 100) % 10] * 10 + cube[(S_slice[i] / 10) % 10][S_slice[i] % 10];
    
        for (int j = 0; j < 4; j++)
        {
            if (color == S_color[j] || (color % 10) * 10 + (color / 10) == S_color[j])
            {
                num = num << 2 | j;
                break;
            }
        }
        
    }
    //m slice
    vector<int> M_slice={335, 513,2315,2533};
    vector<int> M_color={30, 10,21,23};
    for(int i=0;i<4;i++){
        int color = cube[M_slice[i] / 1000][(M_slice[i] / 100) % 10] * 10 + cube[(M_slice[i] / 10) % 10][M_slice[i] % 10];
    
        for (int j = 0; j < 4; j++)
        {
            if (color == M_color[j] || (color % 10) * 10 + (color / 10) == M_color[j])
            {
                num = num << 2 | j;
                break;
            }
        }
        
    }
    return num;


}
void bfs(vector<vector<int8_t>> &cube, vector<string> &moves, map<int64_t, int> &visitedStates)
{
    // Open the file in append mode to write the hash and depth
    ofstream outFile("G3.txt", ios::app);

    if (!outFile)
    {
        cerr << "Error opening file for writing!" << endl;
        return;
    }

    // Use a queue to explore states level by level
    queue<pair<vector<vector<int8_t>>, int>> q;
    q.push({cube, 0});

    // Initially, mark the starting state as visited
    int64_t hash = hash4(cube);
    visitedStates[hash] = 0;

    // Write the initial state hash and depth to the file
    outFile << hash << " " << 0 << endl;

    int total = 663552;

    while (!q.empty())
    {
        pair<vector<vector<int8_t>>, int> frontElement = q.front();
        vector<vector<int8_t>> currentCube = frontElement.first;
        int depth = frontElement.second;

        q.pop();

        // If we've reached the maximum depth, stop
        if (depth > 100)
        {
            break;
        }

        // For each move, apply it and check if we reach a new state
        for (const auto &move : moves)
        {
            // Apply the move to the cube
            applymoves(currentCube, move);

            // Generate a hash of the new state
            int64_t newHash = hash4(currentCube);

            // If this new state hasn't been visited before
            if (visitedStates.find(newHash) == visitedStates.end())
            {
                // Mark it as visited and push to queue with the new depth
                visitedStates[newHash] = depth + 1;
                q.push({currentCube, depth + 1});

                // Write the hash and depth to the file
                outFile << newHash << " " << depth + 1 << endl;
            }

            // Undo the move to backtrack
            applymoves(currentCube, move);
            applymoves(currentCube, move);
            applymoves(currentCube, move);
        }

        // Output the number of visited states at intervals
        if (visitedStates.size() % 1000 == 0)
        {
            cout << "Visited states: " << visitedStates.size() << endl;
        }

        // If all states are visited, we are done
        if (visitedStates.size() == total)
        {
            cout << "All permutations found!" << endl;
        }
    }
    cout << "Total states visited: " << visitedStates.size() << endl;
    // Close the file after all writing is done
    outFile.close();
}

int main()
{
    vector<vector<int8_t>> cube = generate();
    vector<string> moves = { "R2", "L2", "U2", "D2", "F2", "B2"};
    map<int64_t, int> visitedStates;
    auto start = std::chrono::high_resolution_clock::now();

    bfs(cube, moves, visitedStates);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";

    return 0;
}