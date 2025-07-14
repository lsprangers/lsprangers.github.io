# 2215
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1_set = set(nums1)
        nums2_set = set(nums2)
        nums1_seen = set()
        nums2_seen = set()
        resp = [
            [],
            []
        ]

        for num1 in nums1:
            if num1 not in nums2_set and num1 not in nums1_seen:
                resp[0].append(num1)
                nums1_seen.add(num1)

        for num2 in nums2:
            if num2 not in nums1_set and num2 not in nums2_seen:
                resp[1].append(num2)
                nums2_seen.add(num2)


        return(resp)      