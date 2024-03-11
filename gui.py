import tkinter as tk
from calculator import Calculator
import math


class Calculator_GUI:
    def __init__(self):
        self.previous_ans_len = 0
        self.constants = ['e', 'π', 'ANS']
        self.conversion_dict = {'e': str(math.e),
                                'π': str(math.pi),
                                'ln(': 'nlg(',
                                'log(': 'log((',
                                ',': '),',
                                'SQRT(': 'SRT('}
        self.functions = ['SQRT(', 'ln(', 'log(', 'sin(', 'cos(', 'tan(']
        self.calculator = Calculator()
        self.expression_list = []
        self.root = tk.Tk()
        self.root.title('Calculator')
        self.root.geometry('500x713')
        self.root.resizable(False, False)

        self.display = tk.Entry(self.root, state='readonly', font=('courier', 30, 'bold'))
        self.display.grid(row=0, columnspan=6, column=0, sticky='nesw')
        self.answer = tk.Entry(self.root, state='readonly', font=('courier', 10, 'bold'))
        self.answer.grid(row=1, columnspan=6, column=0, sticky='nesw')
        self.buttons = self.get_buttons()

        self.root.mainloop()

    def add_text(self, text, display=None):
        if text == '.':
            expression = ''.join(self.expression_list)
            if len(expression) == 0:
                text = '0.'
            else:
                if expression[-1] in '+-/*^':
                    text = '0.'

        if display is None:
            display = self.display
        display.config(state='normal')
        if display != self.display:
            display.insert(0, text)
            display.config(state='readonly')
            return None
        else:
            if len(self.expression_list) == 0:
                self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text)
            elif self.valid_expression(text):
                # Prevents you writing epi without an operator
                self.display_insert_tool(display, sum([len(x) for x in self.expression_list]), text)
            else:
                pass

            display.config(state='readonly')
            return None

    def display_insert_tool(self, display, length, text):
        display.insert(length, text)
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

    def delete(self):
        if len(self.expression_list) != 0:
            self.display.config(state='normal')
            self.display.delete(sum([len(x) for x in self.expression_list[:-1]]),
                                sum([len(x) for x in self.expression_list]))
            self.display.config(state='readonly')
            self.expression_list = self.expression_list[:-1]

    def equals(self):
        if len(self.expression_list) != 0:
            expression = ''
            for expr in self.expression_list:
                if expr in self.conversion_dict.keys():
                    expression += self.conversion_dict[expr]
                elif expr == 'ANS':
                    expression += f'{self.calculator.ans:f}'
                else:
                    expression += expr
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
                if 'string index out of range' in str(e):
                    txt = 'Missing a Value'
                else:
                    if len(str(e)) > 20:
                        txt = 'Error'
                    else:
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

        buttons[0][0] = tk.Button(self.root, bd='5', height=3, width=7, text='RAD', font=('courier', 15, 'bold'),
                                  bg='limegreen',
                                  command=lambda: self.rad_set(True))
        buttons[1][0] = tk.Button(self.root, bd='5', height=3, width=7, text='DEG', font=('courier', 15, 'bold'),
                                  bg='gray',
                                  command=lambda: self.rad_set(False))
        buttons[2][0] = tk.Button(self.root, bd='5', height=3, width=7, text=',', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text(','))
        buttons[3][0] = tk.Button(self.root, bd='5', height=3, width=7, text='x^y', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('^'))
        buttons[4][0] = tk.Button(self.root, bd='5', height=3, width=7, text='x^2', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('^2'))

        buttons[0][1] = tk.Button(self.root, bd='5', height=3, width=7, text='SQRT', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('SQRT('))
        buttons[1][1] = tk.Button(self.root, bd='5', height=3, width=7, text='π', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('π'))
        buttons[2][1] = tk.Button(self.root, bd='5', height=3, width=7, text='e', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('e'))
        buttons[3][1] = tk.Button(self.root, bd='5', height=3, width=7, text='ln', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('ln('))
        buttons[4][1] = tk.Button(self.root, bd='5', height=3, width=7, text='log(b,v)', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('log('))

        buttons[0][2] = tk.Button(self.root, bd='5', height=3, width=7, text='sin', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('sin('))
        buttons[1][2] = tk.Button(self.root, bd='5', height=3, width=7, text='cos', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('cos('))
        buttons[2][2] = tk.Button(self.root, bd='5', height=3, width=7, text='tan', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('tan('))
        buttons[3][2] = tk.Button(self.root, bd='5', height=3, width=7, text='(', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text('('))
        buttons[4][2] = tk.Button(self.root, bd='5', height=3, width=7, text=')', font=('courier', 15, 'bold'),
                                  bg='gold',
                                  command=lambda: self.add_text(')'))

        buttons[0][3] = tk.Button(self.root, bd='5', height=3, width=7, text='7', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('7'))
        buttons[1][3] = tk.Button(self.root, bd='5', height=3, width=7, text='8', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('8'))
        buttons[2][3] = tk.Button(self.root, bd='5', height=3, width=7, text='9', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('9'))
        buttons[3][3] = tk.Button(self.root, bd='5', height=3, width=7, text='DEL', font=('courier', 15, 'bold'),
                                  bg='tomato',
                                  command=self.delete)
        buttons[4][3] = tk.Button(self.root, bd='5', height=3, width=7, text='AC', font=('courier', 15, 'bold'),
                                  bg='tomato',
                                  command=self.clear)

        buttons[0][4] = tk.Button(self.root, bd='5', height=3, width=7, text='4', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('4'))
        buttons[1][4] = tk.Button(self.root, bd='5', height=3, width=7, text='5', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('5'))
        buttons[2][4] = tk.Button(self.root, bd='5', height=3, width=7, text='6', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('6'))
        buttons[3][4] = tk.Button(self.root, bd='5', height=3, width=7, text='*', font=('courier', 15, 'bold'),
                                  bg='DarkOrange',
                                  command=lambda: self.add_text('*'))
        buttons[4][4] = tk.Button(self.root, bd='5', height=3, width=7, text='/', font=('courier', 15, 'bold'),
                                  bg='DarkOrange',
                                  command=lambda: self.add_text('/'))

        buttons[0][5] = tk.Button(self.root, bd='5', height=3, width=7, text='1', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('1'))
        buttons[1][5] = tk.Button(self.root, bd='5', height=3, width=7, text='2', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('2'))
        buttons[2][5] = tk.Button(self.root, bd='5', height=3, width=7, text='3', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('3'))
        buttons[3][5] = tk.Button(self.root, bd='5', height=3, width=7, text='+', font=('courier', 15, 'bold'),
                                  bg='DarkOrange',
                                  command=lambda: self.add_text('+'))
        buttons[4][5] = tk.Button(self.root, bd='5', height=3, width=7, text='-', font=('courier', 15, 'bold'),
                                  bg='DarkOrange',
                                  command=lambda: self.add_text('-'))

        buttons[0][6] = tk.Button(self.root, bd='5', height=3, width=7, text='0', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('0'))
        buttons[1][6] = tk.Button(self.root, bd='5', height=3, width=7, text='.', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('.'))
        buttons[2][6] = tk.Button(self.root, bd='5', height=3, width=7, text='*10^x', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('*10^'))
        buttons[3][6] = tk.Button(self.root, bd='5', height=3, width=7, text='ANS', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=lambda: self.add_text('ANS'))
        buttons[4][6] = tk.Button(self.root, bd='5', height=3, width=7, text='=', font=('courier', 15, 'bold'),
                                  bg='#59e2dd',
                                  command=self.equals)

        for i, button_ls in enumerate(buttons):
            for j, button in enumerate(button_ls):
                button.grid(column=i, row=j + 2)

        return buttons

    def valid_expression(self, txt):
        last_txt = self.expression_list[-1]
        if (last_txt == ')' or last_txt in self.constants) and (
                txt in self.constants or txt in '(1234567890.' or txt in self.functions):
            return False
        if (txt == '(' or txt in self.functions or txt in self.constants) and (
                last_txt in self.constants or last_txt in ')1234567890.'):
            return False
        if txt == '.' and last_txt[-1] == '.':
            return False
        if txt in '*/' and last_txt in '*/+-':
            return False
        return True

    def rad_set(self, boolean: bool):
        self.calculator.rad_set(boolean)
        if boolean:
            self.buttons[0][0] = tk.Button(self.root, bd='5', height=3, width=7, text='RAD',
                                           font=('courier', 15, 'bold'), bg='limegreen',
                                           command=lambda: self.rad_set(True))
            self.buttons[1][0] = tk.Button(self.root, bd='5', height=3, width=7, text='DEG',
                                           font=('courier', 15, 'bold'), bg='gray',
                                           command=lambda: self.rad_set(False))
        else:
            self.buttons[0][0] = tk.Button(self.root, bd='5', height=3, width=7, text='RAD',
                                           font=('courier', 15, 'bold'), bg='gray',
                                           command=lambda: self.rad_set(True))
            self.buttons[1][0] = tk.Button(self.root, bd='5', height=3, width=7, text='DEG',
                                           font=('courier', 15, 'bold'), bg='limegreen',
                                           command=lambda: self.rad_set(False))
        self.buttons[0][0].grid(column=0, row=2)
        self.buttons[1][0].grid(column=1, row=2)
        # Toggles between radians and degrees.


if __name__ == '__main__':
    Calculator_GUI()
