import math


class Calculator:
    def __init__(self):

        self.__func_dict = {'NLG': math.log,
                            'LOG': math.log,
                            'SRT': math.sqrt,
                            'TAN': self.__tan,
                            'COS': self.__cos,
                            'SIN': self.__sin}
        self.__ans = 0
        self.__rad = True

    def rad_set(self, rad: bool) -> None:
        self.__rad = rad

    def __tan(self, degrees):
        if not self.__rad:
            degrees *= math.pi / 180
        return math.tan(degrees)

    def __cos(self, degrees):
        if not self.__rad:
            degrees *= math.pi / 180
        return math.cos(degrees)

    def __sin(self, degrees):
        if not self.__rad:
            degrees *= math.pi / 180
        return math.sin(degrees)

    @property
    def ans(self) -> float:
        return self.__ans

    def evaluate(self, data: str) -> str:
        data = self.__process(data)
        self.__ans = float(self.__recursive_evaluate(data))
        return f'{self.__ans:f}'

    def __process(self, data: str) -> str:
        spaceless = ''.join([x for x in data if x != ' ']).upper()
        add_pluses = ''
        for i, d in enumerate(spaceless):
            if i > 0 and d == '-':
                if spaceless[i - 1] not in ['/', '*', '+', '-']:
                    add_pluses += '+'
            add_pluses += d
        returnable = self.__remove_double_negatives(add_pluses)
        if returnable[0] == '+' and returnable[1] == '-':
            returnable = '-' + returnable[2:]
        if returnable[0] == '+':
            returnable = returnable[1:]
        returnable = self.__indices_format(returnable)
        # self.__check_for_lack_of_operations(returnable)
        # Handled by the GUI - prevents the input rather than filtering the output
        return returnable

    @staticmethod
    def __remove_double_negatives(data: str) -> str:
        d_before_last = None
        last_d = None
        returnable = ''
        for d in data:
            if d == '-' and last_d == '-':
                returnable = returnable[:-1]
            elif d == '-' and last_d == '+' and d_before_last == '-':
                returnable = returnable[:-2]
            else:
                returnable += d
            d_before_last = last_d
            last_d = d
        return returnable

    def __recursive_evaluate(self, data: str) -> str:
        # Check for functions at the same time you check for brackets.
        open_count = 0
        bracket_contents = []
        writing = False
        for i, d in enumerate(data):
            if d == '(':
                writing = True
                open_count += 1
                if open_count == 1:
                    if i > 2:
                        if data[i - 3:i] in self.__func_dict.keys():
                            bracket_contents.append([data[i - 3:i], '', i])
                        else:
                            bracket_contents.append([None, '', i])
                    else:
                        bracket_contents.append([None, '', i])
            elif d == ')':
                open_count -= 1
                if open_count == 0:
                    writing = False
                    bracket_contents[-1].append(i)
            if writing and not (d == '(' and open_count == 1):
                bracket_contents[-1][1] += d
        bracket_evals = []
        for func, b_c, s, f in bracket_contents:
            if func is not None:
                if func == 'LOG':
                    if self.count(',', b_c) != 1:
                        raise Exception('Base Error')
                    base, b_c = b_c.split(',')
                    base_val = float(self.__recursive_evaluate(base))
                    if base_val == 1 or base_val <= 0:
                        raise Exception('Unacceptable Base')
                    bracket_evals.append([f'{self.__func_dict[func](float(self.__recursive_evaluate(b_c)), base_val):f}', s - 3, f])
                else:
                    bracket_evals.append([f'{self.__func_dict[func](float(self.__recursive_evaluate(b_c))):f}', s - 3, f])

            else:
                bracket_evals.append([self.__recursive_evaluate(b_c), s, f])
        # Now the functions - the brackets should have evaluated, so now you can do the functions preceding them
        # Each function should have a 3-letter code
        bracketless_expression = data
        bracketless_expression = self.__insert(bracketless_expression, bracket_evals)
        bracketless_expression = self.__post_operation_processing(bracketless_expression)
        changes = True
        while changes:
            for i, d in enumerate(bracketless_expression):
                if d == '^':
                    n1, start = self.__get_previous_num(bracketless_expression, i - 1)
                    n2, finish = self.__get_next_num(bracketless_expression, i + 1)
                    ans = float(n1) ** float(n2)
                    bracketless_expression = self.__insert(bracketless_expression, [[f'{ans:f}', start, finish]])
                    bracketless_expression = self.__post_operation_processing(bracketless_expression)
                    break
                if i == len(bracketless_expression) - 1:
                    changes = False

        changes = True
        while changes:
            for i, d in enumerate(bracketless_expression):
                if d in ['*', '/']:
                    n1, start = self.__get_previous_num(bracketless_expression, i - 1)
                    n2, finish = self.__get_next_num(bracketless_expression, i + 1)
                    if d == '*':
                        ans = float(n1) * float(n2)
                    elif d == '/':
                        ans = float(n1) / float(n2)

                    bracketless_expression = self.__insert(bracketless_expression, [[f'{ans:f}', start, finish]])
                    bracketless_expression = self.__post_operation_processing(bracketless_expression)
                    break
                if i == len(bracketless_expression) - 1:
                    changes = False
        changes = True
        while changes:
            for i, d in enumerate(bracketless_expression):
                if d == '+':
                    n1, start = self.__get_previous_num(bracketless_expression, i - 1)
                    n2, finish = self.__get_next_num(bracketless_expression, i + 1)
                    ans = float(n1) + float(n2)
                    bracketless_expression = self.__insert(bracketless_expression, [[f'{ans:f}', start, finish]])
                    bracketless_expression = self.__post_operation_processing(bracketless_expression)
                    break
                if i == len(bracketless_expression) - 1:
                    changes = False
        return bracketless_expression

    @staticmethod
    def __remove_double_positives(data: str) -> str:
        last_d = None
        returnable = ''
        for d in data:
            if not (d == '+' and last_d == '+'):
                returnable += d
            last_d = d
        return returnable

    @staticmethod
    def __remove_following_positives(data: str) -> str:
        last_d = None
        returnable = ''
        for d in data:
            if not (d == '+' and (last_d == '*' or last_d == '/')):
                returnable += d
            last_d = d
        return returnable

    def __post_operation_processing(self, data: str) -> str:
        data = self.__remove_double_positives(self.__remove_double_negatives(data))
        data = self.__remove_following_positives(data)
        if data[0] == '+' and data[1] == '-':
            data = '-' + data[2:]
        if data[0] == '+':
            data = data[1:]
        return data

    @staticmethod
    def __get_previous_num(bracketless_expression: str, finish: int) -> tuple[str, int]:
        n = ''
        acceptable_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']

        for i in range(-1, finish):
            if bracketless_expression[finish - i - 1] in acceptable_list:
                n += bracketless_expression[finish - i - 1]
                if bracketless_expression[finish - i - 1] == '-':
                    break
            else:
                i -= 1
                break
        n = n[::-1]
        return n, finish - i - 1

    @staticmethod
    def __get_next_num(bracketless_expression: str, start: int) -> tuple[str, int]:
        n = ''

        for i in range(len(bracketless_expression) - start):
            if bracketless_expression[start + i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.']:
                if i > 0 and bracketless_expression[start + i] == '-':
                    break
                n += bracketless_expression[start + i]
            else:
                i -= 1
                break
        return n, start + i

    @staticmethod
    def __insert(expression: str, evals: list[list[str, int, int]]) -> str:
        index = 0
        for eval, s, f in evals:
            expression = expression[:s + index] + eval + expression[f + index + 1:]
            index += s - f + len(eval) - 1
        return expression

    def __indices_format(self, data: str) -> str:
        changes = True
        carat_count = 0
        while changes:
            last_last_d = None
            last_d = None
            carat_num = 0
            for i, d in enumerate(data):
                if d == '^':
                    carat_num += 1
                if last_d == ')' and d == '^' and last_last_d != ')' and carat_num > carat_count:
                    data = self.__add_brackets_for_indices(data, i)
                    carat_count += 1
                    break
                elif carat_num > carat_count:
                    data = self.__bracket_remove_signs(data, i)
                    carat_count += 1
                    break
                last_last_d = last_d
                last_d = d
                if i == len(data) - 1:
                    changes = False
        return data

    def __add_brackets_for_indices(self, data: str, carat_location: int) -> str:
        num, end = self.__get_next_num(data, carat_location + 1)
        close_count = 0
        end += 1
        for i in range(carat_location):
            if data[carat_location - 1 - i] == ')':
                close_count += 1
            elif data[carat_location - 1 - i] == '(':
                close_count -= 1
            if close_count == 0:
                if carat_location - i - 1 >= 2:
                    if data[carat_location - i - 4: carat_location - i - 1] in self.__func_dict.keys():
                        return data[:carat_location - i - 4] + '(' + data[carat_location - i - 4: end] + ')' + data[
                                                                                                               end:]
                return data[:carat_location - i] + '(' + data[carat_location - i:end] + ')' + data[end:]

    def __bracket_remove_signs(self, data, carat_location):
        if carat_location > 0:
            if data[carat_location-1] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return data
            num, end = self.__get_next_num(data, carat_location + 1)
            for i in range(carat_location):
                if data[carat_location - 1 - i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    return data[:carat_location - i] + '(' + data[carat_location - i:end + 1] + ')' + data[end + 1:]
                return '(' + data[:end + 1] + ')' + data[end + 1:]
        else:
            return data

    @staticmethod
    def count(searching, b_c):
        count = 0
        for val in b_c:
            if searching == val:
                count += 1
        return count
    #
    # def __check_for_lack_of_operations(self, data):
    #     for i, d in enumerate(data):
    #         if d == '(':
    #             if i > 0:
    #                 if data[i-1] in ')1234567890':
    #                     raise Exception('Lack of Operation')
    #                 elif i > 3:
    #                     if data[i - 3:i] in self.__func_dict.keys():
    #                         if data[i-4] in ')1234567890':
    #                             raise Exception('Lack of Operation')


