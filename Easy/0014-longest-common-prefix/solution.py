class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        prefix = strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]

            if not prefix:
                return ""

        return prefix

## Another solution of this problem
# class Solution:
#     def longestCommonPrefix(self, strs: List[str]) -> str:
#         answer = ""
#         shortest = min(strs, key=len)

#         for i in range(len(shortest)):
#             for j in strs:
#                 if shortest[i] != j[i]:
#                     return answer

#             answer = answer + shortest[i]

#         return answer
