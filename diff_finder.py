import os
import json

#finds the divergences from fuzzer.py that have significant score difference

if __name__ == "__main__":
	divs = []
	with open("AB_Divergences.txt", "r") as file:
		AB_divs = file.read().split('\n')
		AB_divs = AB_divs[:len(AB_divs)-1] # remove last empty string
		for d in AB_divs:
			d = d.replace("\'", "\"") # json requires double quotes
			divs.append(json.loads(d))
	with open("BC_Divergences.txt", "r") as file:
		BC_divs = file.read().split('\n')
		BC_divs = BC_divs[:len(BC_divs)-1] 
		for d in BC_divs:
			d = d.replace("\'", "\"") # json requires double quotes
			divs.append(json.loads(d))
	with open("AC_Divergences.txt", "r") as file:
		AC_divs = file.read().split('\n')
		AC_divs = AC_divs[:len(AC_divs)-1] # remove last empty string
		for d in AC_divs:
			d = d.replace("\'", "\"") # json requires double quotes
			divs.append(json.loads(d))
	for d in divs:
		position = d["position"]
		e1move = d["e1move"]
		e2move = d["e2move"]
		e1score = d["e1score"].split(" ") # is in format ["cp", '330]
		e2score = d["e2score"].split(" ") 

		if d["div"] == "AB":
			with open("input_AC_searchmove.txt", "w") as input_ac: #the inputs to stockfish and halogen
				input_ac.write(f'position fen {position} w - - 0 1\ngo depth 20 searchmoves {e2move}\nucinewgame')
			with open("input_B_searchmove.txt", "w") as input_b: #the input to rubichess
				input_b.write(f'position fen {position} w - - 0 1\ngo depth 20 searchmoves {e1move}\nwait\n')
			ret_A = os.system("Stockfish/src/stockfish < input_AC_searchmove.txt > out_searchmove.txt")
			with open("out_searchmove.txt", "r") as sf_output: 
				stockfish_analysis = sf_output.read().split("\n")
				bm_index = 1
				for i in range(len(stockfish_analysis)-1, -1, -1): #iterate lines backwards
					if stockfish_analysis[i].split(' ')[0] == 'bestmove':
						bm_index = i
						break
				depth_index = bm_index-1 #index of the line that contains the last depth the engine went to
				depth_line = stockfish_analysis[depth_index].split(' ')
					#example depth line: "info depth 38 seldepth 10 score mate 5 time 789 nodes 1571543 nps 1991000 hashfull 20 tbhits 0 pv d1d2 e8d8 g8f6 c5f2"
				if depth_line[1] != 'depth': #sanity check make sure depth is there above bestmove line
					print("improper output")
				stockfish_depth = int(depth_line[2])
				if stockfish_depth < 20:
					print("stockfish not depth 20")
				stockfish_score = "N/A"
				score_index = 0
				while depth_line[score_index] != 'score' and score_index < len(depth_line):
					score_index += 1
				if depth_line[score_index] == 'score' and e1score[0] == 'cp': # only care about scores that have centipawn values, not mates
					stockfish_diff = abs( int(e1score[1]) - int(depth_line[score_index+2]) )
					print(stockfish_diff)
		elif d["div"] == "BC":
			continue
		else: # AC
			continue
		
