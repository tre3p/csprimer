int sum(int *nums, int n) {
    int total1 = 0, total2 = 0, total3 = 0, total4 = 0;
    int i;

    for (i = 0; i < n - 4 + 1; i+=4) {
        total1 += nums[i];
        total2 += nums[i + 1];
        total3 += nums[i + 2];
        total4 += nums[i + 3];
    }

    for (; i < n; i++)
    {
        total1 += nums[i];
    }

    return total1 + total2 + total3 + total4;
}
