#include "goatlatin.cpp"
#include <string.h>
#include <iostream>
using namespace std;

int main ()
{
    Solution s;
    string input = "I speak Goat Latin";
    string output = s.toGoatLatin(input);
    cout << input <<endl;
    cout << output <<endl;
    return 0;
}