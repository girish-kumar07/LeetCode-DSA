class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        # Binary search हमेशा छोटी array पर करेंगे
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m = len(nums1)
        n = len(nums2)

        left = 0
        right = m

        while left <= right:
            partition1 = (left + right) // 2
            partition2 = (m + n + 1) // 2 - partition1

            # Left side के maximum values
            maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]

            # Right side के minimum values
            minRight1 = float('inf') if partition1 == m else nums1[partition1]
            minRight2 = float('inf') if partition2 == n else nums2[partition2]

            # Correct partition मिल गया
            if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:

                # Total length odd
                if (m + n) % 2 == 1:
                    return max(maxLeft1, maxLeft2)

                # Total length even
                return (
                    max(maxLeft1, maxLeft2) +
                    min(minRight1, minRight2)
                ) / 2

            # nums1 का partition बहुत right है
            elif maxLeft1 > minRight2:
                right = partition1 - 1

            # nums1 का partition बहुत left है
            else:
                left = partition1 + 1