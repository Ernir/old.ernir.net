from django.db import models


class CasterLevelFormula(models.Model):

    displayed_formula = models.CharField(max_length=100)
    function_name = models.CharField(max_length=100)

    def calculate(self, cl):
        scaling_function = getattr(ScalingFunctions, self.function_name)
        return scaling_function(cl)

    def __str__(self):
        return self.displayed_formula

    class Meta:
        ordering = ("displayed_formula", )


class ScalingFunctions:
    @staticmethod
    def one(cl):
        return 1

    @staticmethod
    def two(cl):
        return 2

    @staticmethod
    def three(cl):
        return 3

    @staticmethod
    def four(cl):
        return 4

    @staticmethod
    def equal(cl):
        return cl

    @staticmethod
    def equal_max_20(cl):
        return min(cl, 20)

    @staticmethod
    def one_per_two(cl):
        return cl // 2

    @staticmethod
    def one_per_two_max_10(cl):
        return min(cl // 2, 10)

    @staticmethod
    def one_per_three(cl):
        return cl // 3

    @staticmethod
    def one_per_four_max_5(cl):
        return min(cl // 4, 5)

    @staticmethod
    def one_per_five_max_4(cl):
        return min(cl // 5, 4)

    @staticmethod
    def two_plus_one_per_three_above_three_max_5(cl):
        return min(2 + max((cl - 3) // 3, 0), 5)

    @staticmethod
    def twenty_five(cl):
        return 25

    @staticmethod
    def one_per_three_min_1_max_3(cl):
        return max(1, min(cl // 3, 3))

    @staticmethod
    def minus_two(cl):
        return -2

    @staticmethod
    def minus_one(cl):
        return -1

    @staticmethod
    def zero(cl):
        return 0

    @staticmethod
    def twelve_per_cl_max_120(cl):
        return min(cl*12, 120)

    @staticmethod
    def ten_increased_at_seven_and_eleven(cl):
        if cl >= 11:
            return 30
        elif cl >= 7:
            return 20
        else:
            return 10

    @staticmethod
    def three_increased_at_twelve_and_fifteen(cl):
        if cl >= 15:
            return 9
        elif cl >= 12:
            return 6
        else:
            return 3

    @staticmethod
    def two_plus_one_per_six_max_5(cl):
        return min(2 + cl // 6, 5)