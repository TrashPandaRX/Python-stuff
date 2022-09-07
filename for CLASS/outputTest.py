def outputData(fileName, value, action):
	outputFile = open(f"{fileName}.txt", f"{action}")
	outputFile.write(f"{value}")
	outputFile.close()

outputData("hello", "HI THERE!!", "a")