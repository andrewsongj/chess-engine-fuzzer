import os

if __name__ == "__main__":
	with open("position.txt", "w") as position_file:
		ret_val = os.system("Stockfish/src/stockfish < test.txt")
		print(ret_val)
		
			
