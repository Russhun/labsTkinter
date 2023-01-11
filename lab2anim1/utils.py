class RecurNumCounter:
    def __init__(self, nums: list[int]):
        self._num_list = nums
        self._current = 0

    def next(self) -> int:
        if self._current == (len(self._num_list) - 1):
            self._current = 0
        else:
            self._current += 1
        return self._num_list[self._current]

    def get_current(self) -> int:
        return self._num_list[self._current]

    def set_list(self, nums: list[int]):
        self._num_list = nums
        self._current = 0


class SystemNumConverter:
    def __init__(self):
        pass

    def from_n_to_10(self, num_sys, nums: list[int]) -> str:
        nums = nums
        res = 0
        s = ""
        print(nums)
        for n in range(len(nums)):
            if nums[n] != 0:
                s = f"+{nums[n]}*{num_sys}^{n}" + s
            res = res + nums[n] * (num_sys ** n)
        s = s[1:] + " = " + str(res)
        return s

    def from_2n10_to_10(self, nums: list[int]) -> str:
        n1 = self.from_n_to_10(2, nums[4:8])
        n2 = self.from_n_to_10(2, nums[0:4])
        s = n1.split("= ")[-1] + n2.split("= ")[-1]
        return s

