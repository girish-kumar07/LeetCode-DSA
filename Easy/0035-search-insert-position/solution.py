class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # i = 0
        # while i <len(nums):
        #         if nums[i] == target:
        #             return i
        #         elif nums[i]>target:
        #             return i
        #         i = i+1

        # if i==len(nums):
        #     return len(nums)

        start = 0
        end = len(nums) - 1
        while (start <= end):
            mid = (start + end) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid]<target:
                start = mid + 1
            else:
                end = mid - 1
            
        return start