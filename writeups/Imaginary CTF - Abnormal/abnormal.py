import subprocess

to_match = '11d27b4b600148345996c0ca965545db5aca3ea4ac9a07ddd6cfa13858379eff'
build_cmd = 'iverilog -o abnormal_mod.vvp -s main abnormal_mod.v'.split(' ')
run_cmd = ['vvp', 'abnormal_mod.vvp']

orig = open('abnormal.v', 'r')
code = orig.read().split('\n')
orig.close()

flag = ['6','9','6','3','7','4','6','6','7','b','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','7','d']
alpha = '0123456789abcdef'
idx = len(flag) - 1

while idx > -1:
	for char in alpha:
		flag[idx] = char
		mod = open('abnormal_mod.v', 'w')
		for line in code:
			if line.startswith("    wire [255:0] flag = 256'h"):
				new_flag = "    wire [255:0] flag = 256'h" + ''.join(flag) + ';\n'
				mod.write(new_flag)
			else:
				mod.write(line + '\n')
		mod.close()
		subprocess.run(build_cmd)
		out = subprocess.run(run_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
		
		if out[idx] == to_match[idx]:
			print(f'\nMatch!\nFlag: {"".join(flag)}\nOut:  {out}Rgx:  {to_match}')
			break

	idx -= 1

print('Finished! Here\'s the flag:')
print(''.join(flag))