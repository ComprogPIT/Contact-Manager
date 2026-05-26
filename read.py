try:
    with open("shopping_list.txt", "r") as f:
        lines = f.readlines()
        print("Shopping List Contents:")
        for line in lines:
            print(line.strip())
        print("Total lines: " + str(len(lines)))

except FileNotFoundError:
    print("File not found!")