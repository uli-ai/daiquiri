import os

# creat a dummy large file 
with open("dummy.txt", "wb") as f:
	for x in range(3):
		for a in range(50000):
			for i in range(500):
				f.write("x")

print(os.path.getsize("dummy.txt"))