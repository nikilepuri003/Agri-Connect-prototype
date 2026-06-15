print(f'=================================================',f'  EXPENSE TRACKER ',sep='\n',end='\n=================================================\n')
expenses = [1000,5000,2500,3569,4000]
ad = input('Enter Expenses if you need (Y/N): ').upper()
if ad == 'Y':
    ch = int(input('Enter how many Expenses do you want to add ?: '))
    if ch >0:
        element = list(map(int,input("Enter  Expenses to be added: ").split(',')))
        expenses.append(element)
    else:
        print('Invalid Zero expenses cannot be added ')
elif ad == 'N':
    pass
print(f'\nThe Total Expenses : {expenses}')  


"USING DICTIONARIES"

expenses = {
    'Electricity': 3000 ,
    'Groceries' : 7000 ,
    'Health Care' : 2500 ,
    'Medicines' : 3000 ,
    'Entertainment' : 2000 ,
    'Others' : 1500
}
ad = input('Enter Expenses if you need (Y/N): ').upper()
if ad == 'Y':
    ch = int(input('Enter how many Expenses do you want to add ?: '))
    for _ in range(ch):
        cat = input('Enter the catg of the expenses : ')
        ele = float(input('Enter the Expense: '))
        expenses[cat] = ele
elif ad == 'N':
    pass
print(f'Total Expenses: {sum(expenses.values())}')