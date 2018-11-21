
bash('''
echo "I am secure"
''',
secure=True
)

bash('''
echo "I am secure but I fail"
exit 1
''', 
secure=True
)
