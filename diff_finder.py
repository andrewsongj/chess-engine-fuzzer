import os
import json

def findScore(analysis, engine): # locate the score from engine analysis
	analysis = analysis.split("\n")

	# locate the bestmove first
	bm_index = 1
	for i in range(len(analysis)-1, -1, -1): #iterate lines backwards
		if analysis[i].split(' ')[0] == 'bestmove':
			bm_index = i
			break
	depth_index = bm_index-1 #index of the line that contains the last depth the engine went to
	depth_line = analysis[depth_index].split(' ')
		#example depth line: "info depth 38 seldepth 10 score mate 5 time 789 nodes 1571543 nps 1991000 hashfull 20 tbhits 0 pv d1d2 e8d8 g8f6 c5f2"
	if depth_line[1] != 'depth': #sanity check make sure depth is there
		print("improper output from " + engine)
	depth = int(depth_line[2])
	if depth < 20:
		print(engine + " not depth 20")

	# locate the score
	score_index = 0
	while depth_line[score_index] != 'score' and score_index < len(depth_line):
		score_index += 1
	if not depth_line[score_index] == 'score':
		print(engine + " score not found")
	score = [depth_line[score_index+1], depth_line[score_index+2]]
	return score
		# is in format ["cp", "330"]

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

	num_sig_divs = 0
	sig_divs = [] # the final result; will contain all divergences that are deemed significant
		# e1e2score will be e1's score for e2's best move, and e2e1score follows same idea
	for d in divs:
		position = d["position"]
		e1move = d["e1move"]
		e2move = d["e2move"]
		e1score = d["e1score"].split(" ") # is in format ["cp", "330"]
		e2score = d["e2score"].split(" ") 

		with open("input_AC_searchmove.txt", "w") as input_ac: #the inputs to stockfish and halogen
			input_ac.write(f'position fen {position} w - - 0 1\ngo depth 20 searchmoves {e2move}\nucinewgame')
		with open("input_B_searchmove.txt", "w") as input_b: #the input to rubichess
			input_b.write(f'position fen {position} w - - 0 1\ngo depth 20 searchmoves {e1move}\nwait\n')

		if d["div"] == "AB":
			ret_A = os.system("Stockfish/src/stockfish < input_AC_searchmove.txt > out_searchmove.txt") 
			with open("out_searchmove.txt", "r") as sf_output: 
				stockfish_analysis = sf_output.read()
				e1e2score = findScore(stockfish_analysis, "stockfish")
				# now compare the stockfish scores
				stockfish_diff = 0
				if e1score[0] == 'mate' and e1e2score[0] == 'cp': # if stockfish gave one move a mate score and the other a cp score, then big difference
					stockfish_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e1score[0] == 'cp': # only care about scores that have centipawn values, not mates
					stockfish_diff = abs( int(e1score[1]) - int(e1e2score[1]) )

				# stockfish_diff will be zero if both moves are mate moves, which is fine since we don't consider mates to be different

			ret_B = os.system("RubiChess/src/RubiChess < input_B_searchmove.txt > out_searchmove.txt") 
			with open("out_searchmove.txt", "r") as rb_output: 
				rubi_analysis = rb_output.read()
				e2e1score = findScore(rubi_analysis, "rubi")
				# now compare the rubi scores
				rubi_diff = 0
				if e2score[0] == 'mate' and e2e1score[0] == 'cp': # if rubi gave one move a mate score and the other a cp score, then big difference
					rubi_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e2score[0] == 'cp': # only care about scores that have centipawn values, not mates
					rubi_diff = abs( int(e2score[1]) - int(e2e1score[1]) )

			if stockfish_diff >= 100 or rubi_diff >= 100:
				num_sig_divs += 1
				d["e1e2score"] = e1e2score
				d["e2e1score"] = e2e1score
				sig_divs.append(d)
				print("Number of significant differences: " + str(num_sig_divs))
				
		elif d["div"] == "BC":
			ret_B = os.system("RubiChess/src/RubiChess < input_B_searchmove.txt > out_searchmove.txt")
			with open("out_searchmove.txt", "r") as rb_output: 
				rubi_analysis = rb_output.read()
				e1e2score = findScore(rubi_analysis, "rubi")
				# now compare the rubi scores
				rubi_diff = 0
				if e1score[0] == 'mate' and e1e2score[0] == 'cp': 
					rubi_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e1score[0] == 'cp': # only care about scores that have centipawn values, not mates
					rubi_diff = abs( int(e1score[1]) - int(e1e2score[1]) )

			ret_C = os.system("Halogen/bin/Halogen-native.exe < input_AC_searchmove.txt > out_searchmove.txt")
			with open("out_searchmove.txt", "r") as hg_output: 
				halogen_analysis = hg_output.read()
				e2e1score = findScore(halogen_analysis, "halogen")
				# now compare the halogen scores
				halogen_diff = 0
				if e2score[0] == 'mate' and e2e1score[0] == 'cp': # if halogen gave one move a mate score and the other a cp score, then big difference
					halogen_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e2score[0] == 'cp': # only care about scores that have centipawn values, not mates
					rubi_diff = abs( int(e2score[1]) - int(e2e1score[1]) )

			if rubi_diff >= 100 or halogen_diff >= 100:
				num_sig_divs += 1
				d["e1e2score"] = e1e2score
				d["e2e1score"] = e2e1score
				sig_divs.append(d)
				print("Number of significant differences: " + str(num_sig_divs))

		else: # AC
			ret_A = os.system("Stockfish/src/stockfish < input_AC_searchmove.txt > out_searchmove.txt") 
			with open("out_searchmove.txt", "r") as sf_output: 
				stockfish_analysis = sf_output.read()
				e1e2score = findScore(stockfish_analysis, "stockfish")
				# now compare the stockfish scores
				stockfish_diff = 0
				if e1score[0] == 'mate' and e1e2score[0] == 'cp': # if stockfish gave one move a mate score and the other a cp score, then big difference
					stockfish_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e1score[0] == 'cp': # only care about scores that have centipawn values, not mates
					stockfish_diff = abs( int(e1score[1]) - int(e1e2score[1]) )

			ret_C = os.system("Halogen/bin/Halogen-native.exe < input_AC_searchmove.txt > out_searchmove.txt")
			with open("out_searchmove.txt", "r") as hg_output: 
				halogen_analysis = hg_output.read()
				e2e1score = findScore(halogen_analysis, "halogen")
				# now compare the halogen scores
				halogen_diff = 0
				if e2score[0] == 'mate' and e2e1score[0] == 'cp': # if halogen gave one move a mate score and the other a cp score, then big difference
					halogen_diff = 1000 #arbitrarily large number that will be deemed significant
				elif e2score[0] == 'cp': # only care about scores that have centipawn values, not mates
					rubi_diff = abs( int(e2score[1]) - int(e2e1score[1]) )

			if stockfish_diff >= 100 or halogen_diff >= 100:
				num_sig_divs += 1
				d["e1e2score"] = e1e2score
				d["e2e1score"] = e2e1score
				sig_divs.append(d)
				print("Number of significant differences: " + str(num_sig_divs))

	with open("significant_divergences.txt", "w") as f:
		for sd in sig_divs:
			f.write(str(sd))
			f.write("\n")
		
