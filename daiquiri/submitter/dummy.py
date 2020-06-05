import os

# creat a dummy large file 
with open("dummy.txt", "w") as f:
	for x in range(15):
		for a in range(50000):
			for i in range(500):
				f.write("x")

print(os.path.getsize("dummy.txt"))