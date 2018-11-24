print('this is a print statement')

print('it is possible to access the runbook and role objects from role\'s main.py ('+str(runbook)+', '+str(role)+')')

bash('''
	echo "hello!"
''')

bash('''
	fsdafas
''')

bash('''
	echo "THIS SHOULD NOT BE EXECUTED!"
''')
