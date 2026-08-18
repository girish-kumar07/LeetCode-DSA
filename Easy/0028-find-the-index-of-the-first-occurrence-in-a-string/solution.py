class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        hay = ""
        for i in range(len(haystack)):
            if hay + haystack[i:i+len(needle)] == needle:
                return i

        return -1   