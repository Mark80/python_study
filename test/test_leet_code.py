
def test_1():
    solution = Solution()
    assert solution.isValid("()")
    assert not solution.isValid("[][")
    assert solution.isValid("()[]{}")
    assert not solution.isValid("(]")
    assert not solution.isValid("([)]")
    assert solution.isValid("([])")
    assert solution.isValid("")
    assert solution.isValid("{[[]]()}")
    assert not solution.isValid("]")
    

class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        for par in s:
            if(par == '(' or par == '[' or par == '{'):
                stack.append(par)
            else:
                if(len(stack) == 0): 
                  return False
                close = stack.pop()
                if(par == ')' and close != '('):
                    return False
                if(par == ']' and close != '['):
                    return False
                if(par == '}' and close != '{'):
                    return False
        return len(stack) == 0                                

        