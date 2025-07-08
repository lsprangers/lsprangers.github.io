#include <vector>;
using namespace std;

//704 
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int resp = -1;
        int left = 0;
        int right = nums.size() - 1;
        while(left <= right) {
            int mid = left + ((right - left) / 2);
            if(nums[mid] == target) {
                return(mid);
            }
            else if (nums[mid] > target) {
                right = mid - 1;
            }
            else {
                left = mid + 1;
            }
        }
        return(resp);
    }
};