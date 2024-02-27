import tkinter as tk
from calculator import Calculator


class Calculator_GUI:
    def __init__(self):
        self.previous_ans_len = 0
        self.constants = ['e', 'π', 'ANS']
        self.conversion_dict = {'e': '2.718281828459045',
                                'π': '3.141592653589793',
                                'ln(': 'nlg('}
        self.functions = ['SRT(', 'ln(', 'log(', 'sin(', 'cos(', 'tan(']
        self.calculator = Calculator()
        self.expression_list = []
        self.evaluation_list = []
        self.root = tk.Tk()
        self.root.title('Calculator')
        self.root.geometry('500x820')
        self.root.resizable(False, False)

        self.display = tk.Entry(self.root, state='readonly', font=('courier', 30, 'bold'))
        self.display.grid(row=0, columnspan=6, column=0, sticky='nesw')
        self.answer = tk.Entry(self.root, state='readonly', font=('calibre', 10, 'bold'))
        self.answer.grid(row=1, columnspan=6, column=0, sticky='nesw')
        self.get_buttons()

        self.root.mainloop()

    def add_text(self, text, display=None):
        if display is None:
            display = self.display
        display.config(state='normal')
        if display != self.display:
            display.insert(0, text)
            display.config(state='readonly')
            return None
        else:
            if text in self.conversion_dict.keys():
                if len(self.expression_list) == 0:
                    self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text, True)
                elif self.valid_expression(text):
                    # Prevents you writing epi without an operator
                    self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text, True)
                else:
                    pass
            else:
                if len(self.expression_list) == 0:
                    self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text, False)
                elif self.valid_expression(text):
                    self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text, False)

            display.config(state='readonly')
            return None
    def display_insert_tool(self, display, length, text, conversion: bool):
        display.insert(length, text)
        if conversion:
            self.evaluation_list.append(self.conversion_dict[text])
        else:
            self.evaluation_list.append(text)
        self.expression_list.append(text)
    def clear(self, display=None):
        if display is None:
            display = self.display
        if len(self.expression_list) != 0:
            display.config(state='normal')
            if display == self.display:
                display.delete(0, sum([len(x) for x in self.expression_list]))
            else:
                display.delete(0, self.previous_ans_len)
            display.config(state='readonly')
            if display == self.display:
                self.expression_list = []
                self.evaluation_list = []

    def delete(self):
        if len(self.expression_list) != 0:
            self.display.config(state='normal')
            self.display.delete(sum([len(x) for x in self.expression_list[:-1]]), sum([len(x) for x in self.expression_list]))
            self.display.config(state='readonly')
            self.expression_list = self.expression_list[:-1]
            self.evaluation_list = self.evaluation_list[:-1]

    def equals(self):
        if len(self.evaluation_list) != 0:
            expression = ''.join(self.evaluation_list)
            if 'ANS' in expression:
                changes = True
                while changes:
                    last_last_char = None
                    last_char = None
                    for i, char in enumerate(expression):
                        if last_last_char == 'A' and last_char == 'N' and char == 'S':
                            expression = expression[:i-2] + f'{self.calculator.ans:f}' + expression[i + 1:]
                            break
                        if i == len(expression) - 1:
                            changes = False
                        last_last_char = last_char
                        last_char = char
            self.clear(display=self.answer)
            try:
                txt = self.calculator.evaluate(expression)
            except ValueError as e:
                if 'could not convert string to float' in str(e):
                    txt = 'Syntax Error'
                else:
                    txt = 'Value Error'
            except ZeroDivisionError:
                txt = 'Divide By Zero Error'
            except Exception as e:
                txt = str(e)
            self.clear(display=self.answer)
            self.previous_ans_len = len(txt)
            self.add_text(txt, display=self.answer)

    def get_buttons(self):
        buttons = []
        for i in range(5):
            buttons.append([])
            for j in range(7):
                buttons[-1].append(None)

        buttons[0][0] = tk.Button(self.root, bd='5', height=6, width=12, text='DEG', fg='white', bg='blue',
                                  command=lambda: self.calculator.rad_set(False))
        buttons[1][0] = tk.Button(self.root, bd='5', height=6, width=12, text='RAD', fg='white', bg='blue',
                                  command=lambda: self.calculator.rad_set(True))
        buttons[2][0] = tk.Button(self.root, bd='5', height=6, width=12, text=',', fg='white', bg='blue',
                                  command=lambda: self.add_text(','))
        buttons[3][0] = tk.Button(self.root, bd='5', height=6, width=12, text='x^y', fg='white', bg='blue',
                                  command=lambda: self.add_text('^'))
        buttons[4][0] = tk.Button(self.root, bd='5', height=6, width=12, text='x^2', fg='white', bg='blue',
                                  command=lambda: self.add_text('^2'))

        buttons[0][1] = tk.Button(self.root, bd='5', height=6, width=12, text='SRT', fg='white', bg='blue',
                                  command=lambda: self.add_text('SRT('))
        buttons[1][1] = tk.Button(self.root, bd='5', height=6, width=12, text='π', fg='white', bg='blue',
                                  command=lambda: self.add_text('π'))
        buttons[2][1] = tk.Button(self.root, bd='5', height=6, width=12, text='e', fg='white', bg='blue',
                                  command=lambda: self.add_text('e'))
        buttons[3][1] = tk.Button(self.root, bd='5', height=6, width=12, text='ln', fg='white', bg='blue',
                                  command=lambda: self.add_text('ln('))
        buttons[4][1] = tk.Button(self.root, bd='5', height=6, width=12, text='log(b,v)', fg='white', bg='blue',
                                  command=lambda: self.add_text('log('))

        buttons[0][2] = tk.Button(self.root, bd='5', height=6, width=12, text='sin', fg='white', bg='blue',
                                  command=lambda: self.add_text('sin('))
        buttons[1][2] = tk.Button(self.root, bd='5', height=6, width=12, text='cos', fg='white', bg='blue',
                                  command=lambda: self.add_text('cos('))
        buttons[2][2] = tk.Button(self.root, bd='5', height=6, width=12, text='tan', fg='white', bg='blue',
                                  command=lambda: self.add_text('tan('))
        buttons[3][2] = tk.Button(self.root, bd='5', height=6, width=12, text='(', fg='white', bg='blue',
                                  command=lambda: self.add_text('('))
        buttons[4][2] = tk.Button(self.root, bd='5', height=6, width=12, text=')', fg='white', bg='blue',
                                  command=lambda: self.add_text(')'))

        buttons[0][3] = tk.Button(self.root, bd='5', height=6, width=12, text='7', fg='white', bg='blue',
                                  command=lambda: self.add_text('7'))
        buttons[1][3] = tk.Button(self.root, bd='5', height=6, width=12, text='8', fg='white', bg='blue',
                                  command=lambda: self.add_text('8'))
        buttons[2][3] = tk.Button(self.root, bd='5', height=6, width=12, text='9', fg='white', bg='blue',
                                  command=lambda: self.add_text('9'))
        buttons[3][3] = tk.Button(self.root, bd='5', height=6, width=12, text='DEL', fg='white', bg='blue',
                                  command=self.delete)
        buttons[4][3] = tk.Button(self.root, bd='5', height=6, width=12, text='AC', fg='white', bg='blue',
                                  command=self.clear)

        buttons[0][4] = tk.Button(self.root, bd='5', height=6, width=12, text='4', fg='white', bg='blue',
                                  command=lambda: self.add_text('4'))
        buttons[1][4] = tk.Button(self.root, bd='5', height=6, width=12, text='5', fg='white', bg='blue',
                                  command=lambda: self.add_text('5'))
        buttons[2][4] = tk.Button(self.root, bd='5', height=6, width=12, text='6', fg='white', bg='blue',
                                  command=lambda: self.add_text('6'))
        buttons[3][4] = tk.Button(self.root, bd='5', height=6, width=12, text='*', fg='white', bg='blue',
                                  command=lambda: self.add_text('*'))
        buttons[4][4] = tk.Button(self.root, bd='5', height=6, width=12, text='/', fg='white', bg='blue',
                                  command=lambda: self.add_text('/'))

        buttons[0][5] = tk.Button(self.root, bd='5', height=6, width=12, text='1', fg='white', bg='blue',
                                  command=lambda: self.add_text('1'))
        buttons[1][5] = tk.Button(self.root, bd='5', height=6, width=12, text='2', fg='white', bg='blue',
                                  command=lambda: self.add_text('2'))
        buttons[2][5] = tk.Button(self.root, bd='5', height=6, width=12, text='3', fg='white', bg='blue',
                                  command=lambda: self.add_text('3'))
        buttons[3][5] = tk.Button(self.root, bd='5', height=6, width=12, text='+', fg='white', bg='blue',
                                  command=lambda: self.add_text('+'))
        buttons[4][5] = tk.Button(self.root, bd='5', height=6, width=12, text='-', fg='white', bg='blue',
                                  command=lambda: self.add_text('-'))

        buttons[0][6] = tk.Button(self.root, bd='5', height=6, width=12, text='0', fg='white', bg='blue',
                                  command=lambda: self.add_text('0'))
        buttons[1][6] = tk.Button(self.root, bd='5', height=6, width=12, text='.', fg='white', bg='blue',
                                  command=lambda: self.add_text('.'))
        buttons[2][6] = tk.Button(self.root, bd='5', height=6, width=12, text='*10^x', fg='white', bg='blue',
                                  command=lambda: self.add_text('*10^'))
        buttons[3][6] = tk.Button(self.root, bd='5', height=6, width=12, text='ANS', fg='white', bg='blue',
                                  command=lambda: self.add_text('ANS'))
        buttons[4][6] = tk.Button(self.root, bd='5', height=6, width=12, text='=', fg='white', bg='blue',
                                  command=self.equals)

        for i, b in enumerate(buttons):
            for j, button in enumerate(b):
                if button is None:
                    buttons[i][j] = tk.Button(self.root, bd='5', height=6, width=12, text='', fg='white', bg='blue',
                                              command=self.equals)

        for i, button_ls in enumerate(buttons):
            for j, button in enumerate(button_ls):
                button.grid(column=i, row=j + 2)

        return buttons

    def valid_expression(self, txt):
        last_txt = self.expression_list[-1]
        if (last_txt == ')' or last_txt in self.constants) and (txt in self.constants or txt in '(1234567890.' or txt in self.functions):
            return False
        if (txt == '(' or txt in self.functions or txt in self.constants) and (last_txt in self.constants or last_txt in ')1234567890.'):
            return False
        return True
