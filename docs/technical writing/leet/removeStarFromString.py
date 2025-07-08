# 2390
# This implementation works and is O(n), but it's horrible compared to editorial:
# class Solution:
#     def removeStars(self, s):
#         st = []
#         for i in range(0, len(s)):
#             if s[i] == '*':
#                 st.pop()
#             else:
#                 st.append(s[i])

#         return ''.join(st)

# Went wrong by trying to cover the weird edge cases, when in reality I can just skip appending * to response and pop off if I see it


class Solution:
    def removeStars(self, s: str) -> str:
        # O(n)
        stack = [c for c in s]

        resp = []
        # stack = ['l', 'e']
        # O(n)
        while stack:
            # *
            curr = stack.pop()
            if curr != "*":
                # resp = [c, o, e]
                resp.insert(0, curr)
            else:
                star_count = 1
                while stack[-1] == "*" and stack:
                    stack.pop()
                    star_count += 1
                while star_count > 0 and stack:
                    curr = stack.pop()
                    if curr != "*":
                        star_count -= 1
                    else:
                        star_count += 1
            
        # O(n)? Space too
        return("".join(resp))