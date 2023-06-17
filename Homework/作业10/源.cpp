#include <stdio.h>
#include <iostream>

using std::cout;		using std::endl;

int main()
{
	int a[30] = { 0,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1 };
	long long b[30] = {};
	int temp = 0;
	long long sum = 0;
	int c = 0;
	bool flag = false;
	
	for (int h = 5;h != 31;h++)						//更改检测上限和下限
	{
		cout << "H=" << h << endl;
		c = -1;
		for (int i = 0;i != 30;i++)
		{
			b[i] = c;
			c--;
		}

		for (int i = 0;i != 30;i++)
		{
			sum = 0;
			for (int j = 0;j != h;j++)
			{
				sum *= 2;
				temp = i - h + j;
				if (temp < 0)
					temp += 30;
				sum += a[temp];
			}
			b[i] = sum;
		}

		flag = false;
		for (int i = 0;i != 29;i++)
		{
			for (int j = i + 1;j != 30;j++)
			{
				if (b[i] == b[j] && a[i] != a[j])
				{
					cout << i << "  " << j << "  ";
					cout << "false" << endl;
					flag = true;
					break;
				}
			}
			if (flag)
				break;
		}
		if (!flag)
			cout << "pass" << endl;

	}

}