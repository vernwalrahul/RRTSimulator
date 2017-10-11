lines = [line.rstrip('\n') for line in open('../../../path.dat')]
for p in lines:
	p = p.split(' ')[:2]
	print(p)
print(lines)