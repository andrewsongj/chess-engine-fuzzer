import tempfile
import os
import random

piece_dict = {
    0: 'p',
    1: 'P',
    2: 'n',
    3: 'N',
    4: 'b',
    5: 'B',
    6: 'r',
    7: 'R',
    8: 'q',
    9: 'Q',
	10: 'k',
	11: 'K'
}

#Position format: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

def rowIsEmpty(row): #check if row is empty (considered empty if it has only a king)
    for i in range(0, len(row)):
        if not row[i].isnumeric() and row[i] != 'k' and row[i] != 'K':
            return False
    return True

def change_piece(position): #change a piece to another piece
    changed = False
    rows = position.split("/")
    while not changed:
        row_num = random.randrange(0, 8) # pick the row which we change
        if not rowIsEmpty(rows[row_num]): # rows[row_num] != "8": # found a row thats not empty i.e. has pieces in it
            pieces = 8 # track the number of pieces in the row
            row = rows[row_num] # a single row like "rnb2bnr"
            for j in range(0, len(row)): # iterate through a row, like "rnb2bnr" to count number of pieces in row
                if row[j].isnumeric() or row[j]=='k' or row[j]=='K': # this indicates an empty square(s), or any king
                    if row[j].isnumeric():
                        pieces = pieces - int(row[j])
                    else: #means we found a king so we skip
                        pieces -= 1
            piece_num = random.randrange(0, pieces) # pick random piece which we will change
            #print(piece_num)
            for j in range(0, len(row)): # iterate the row again to actually remove the piece
                if not row[j].isnumeric() and row[j]!='k' and row[j]!='K' and piece_num == 0: # if you found a non king piece and are on the piece_num
                    to_change = j #the index of string to change
                    break
                elif not row[j].isnumeric() and row[j]!='k' and row[j]!='K': #found a piece but not yet the piece we wanted to change
                    piece_num = piece_num - 1
            new_piece = random.randrange(2, 10) if row_num==0 or row_num==7 else random.randrange(0, 10) #pick new piece, not a pawn if one of edge rows
            while piece_dict[new_piece] == row[to_change]: #change the new piece while its the same as existing piece
                new_piece = random.randrange(2, 10) if row_num==0 or row_num==7 else random.randrange(0, 10)
            rows[row_num] = row[0:to_change] + piece_dict[new_piece] + row[to_change+1:]
            changed = True
    return "/".join(rows)

def change_color(position): #change the color of a piece
    changed = False
    rows = position.split("/")
    while not changed:
        row_num = random.randrange(0, 8) # pick the row which we change
        if not rowIsEmpty(rows[row_num]): # rows[row_num] != "8": # found a row thats not empty i.e. has pieces in it
            pieces = 8 # track the number of pieces in the row
            row = rows[row_num] # a single row like "rnb2bnr"
            for j in range(0, len(row)): # iterate through a row, like "rnb2bnr" to count number of pieces in row
                if row[j].isnumeric() or row[j]=='k' or row[j]=='K': # this indicates an empty square(s), or any king
                    if row[j].isnumeric():
                        pieces = pieces - int(row[j])
                    else: #means we found a king so we skip
                        pieces -= 1
            piece_num = random.randrange(0, pieces) # pick random piece which we will change
            #print(piece_num)
            for j in range(0, len(row)): # iterate the row again to actually remove the piece
                if not row[j].isnumeric() and row[j]!='k' and row[j]!='K' and piece_num == 0: # if you found a non king piece and are on the piece_num
                    to_change = j #the index of string to change
                    break
                elif not row[j].isnumeric() and row[j]!='k' and row[j]!='K': #found a piece but not yet the piece we wanted to change
                    piece_num = piece_num - 1
            if row[to_change].isupper(): #if black, make white
                rows[row_num] = row[0:to_change] + row[to_change].lower() + row[to_change+1:]
            else:
                rows[row_num] = row[0:to_change] + row[to_change].upper() + row[to_change+1:]
            changed = True
    return "/".join(rows)

def rowHasEmptySquares(row):
    for i in range(0, len(row)):
        if row[i].isnumeric():
            return True
    return False

def findEmptySquare(position, row_lower=0, row_upper=8):
	foundRow = False
	rows = position.split("/")
	while not foundRow: #find a row with empty squares in it
		row_num = random.randrange(row_lower, row_upper) # pick the row which we change
		if rowHasEmptySquares(rows[row_num]):
		    break
	row = rows[row_num]
	total_spaces = 0
	for i in range(0, len(row)):
		if row[i].isnumeric():
		    total_spaces += int(row[i])
	rand_space = random.randrange(1, total_spaces+1) # from 1 to nth space, max n=8
		#now that random space in the row has been chosen, find the column its in
	col = 0
	spaces = 0 #track how many spaces we counted along the row
	for i in range(0, len(row)):
		if row[i].isnumeric() and spaces+int(row[i]) < rand_space:
		    spaces += int(row[i])
		    col += int(row[i])
		elif not row[i].isnumeric():
		    col += 1
		elif row[i].isnumeric() and spaces+int(row[i]) >= rand_space: #found the space
		    col += (rand_space - spaces)
		    break
	return row_num, col #row_num is 0-index of row , but col is 1-index of col

def add_piece(position, r=-1, col=-1, piece=-1): #add a piece somewhere
	rows = position.split("/")
	if r == -1 and col == -1:
		r, col = findEmptySquare(position)
		#print("r=" + str(r) + " ; col=" + str(col))
	row = rows[r]
	if piece == -1:
		piece = random.randrange(2, 10) if r==0 or r==7 else random.randrange(0, 10) # must not add pawn to edge rows
	c = 0 #track column were at
	for i in range(0, len(row)):
		if row[i].isnumeric() and c+int(row[i]) < col:
		    c += int(row[i])
		elif row[i].isnumeric() and c+int(row[i]) >= col:
			first_num = col-c-1
			second_num = c+int(row[i])-col
			if first_num != 0 and second_num != 0:
			    rows[r] = row[0:i] + str(first_num) + piece_dict[piece] + str(second_num) + row[i+1:]
			elif first_num != 0 and second_num == 0:
			    rows[r] = row[0:i] + str(first_num) + piece_dict[piece] + row[i+1:]
			elif first_num == 0 and second_num != 0:
			    rows[r] = row[0:i] + piece_dict[piece] + str(second_num) + row[i+1:]
			else: # both zero
			    rows[r] = row[0:i] + piece_dict[piece] + row[i+1:]
			break
		elif not row[i].isnumeric():
		    c += 1
	return "/".join(rows)

def findPieceSquare(position): #find a square that has a piece on it
	foundRow = False
	rows = position.split("/")
	while not foundRow: #find a row with pieces in it
		row_num = random.randrange(0, 8) # pick the row which we change, 0-7
		if rows[row_num] != "8": #if not 8 spaces then has pieces on it
		    break
	row = rows[row_num]
	total_pieces = 0
	for i in range(0, len(row)):
		if not row[i].isnumeric():
		    total_pieces += 1
	rand_piece = random.randrange(1, total_pieces+1) # from 1 to nth piece, max n=8
		#now that random piece in the row has been chosen, find the column its in
	col = 0
	pieces = 0 #track how many pieces we counted along the row
	p = 'X' # will be the actual class of the piece on the square (p, n, etc.)
	for i in range(0, len(row)):
		if not row[i].isnumeric() and pieces+1 < rand_piece:
		    pieces += 1
		    col += 1
		elif row[i].isnumeric():
		    col += int(row[i])
		elif not row[i].isnumeric() and pieces+1 == rand_piece: #found the piece
		    col += 1
		    p = row[i]
		    break
	return row_num, col, p # row_num is 0-index of row , but col is 1-index of columns

def remove_piece(position, r=-1, col=-1): #remove some piece (can be specified by coordinate r, col)
	rows = position.split("/")
	if r == -1 and col == -1:
		r, col, p = findPieceSquare(position)
		#if p == "k" or p == "K": #king cant be removed in theory
		#print("r=" + str(r) + " ; col=" + str(col))
	row = rows[r]
	c = 0 #track column were at
	for i in range(0, len(row)):
		if row[i].isnumeric() and c+int(row[i]) < col:
		    c += int(row[i])
		elif not row[i].isnumeric() and c+1 < col:
		    c += 1
		elif not row[i].isnumeric() and c+1 == col:
			if i > 0 and i < len(row)-1:
				if row[i-1].isnumeric() and row[i+1].isnumeric():
					new_spaces = int(row[i-1]) + 1 + int(row[i+1])
					rows[r] = row[:i-1] + str(new_spaces) + row[i+2:]
				elif row[i-1].isnumeric() and not row[i+1].isnumeric():
					new_spaces = int(row[i-1]) + 1
					rows[r] = row[:i-1] + str(new_spaces) + row[i+1:]
				elif not row[i-1].isnumeric() and row[i+1].isnumeric():
					new_spaces = 1 + int(row[i+1])
					rows[r] = row[:i] + str(new_spaces) + row[i+2:]
				else: # both not numeric
					rows[r] = row[:i] + str(1) + row[i+1:]
			elif i == 0:
			    if row[i+1].isnumeric():
			        new_spaces = 1 + int(row[i+1])
			        rows[r] = str(new_spaces) + row[i+2:]
			    else:
			        rows[r] = str(1) + row[i+1:]
			elif i == len(row)-1:
			    if row[i-1].isnumeric():
			        new_spaces = int(row[i-1]) + 1
			        rows[r] = row[:i-1] + str(new_spaces)
			    else:
			        rows[r] = row[:i] + str(1)
			break
	return "/".join(rows)

def move_piece(position): #move a random piece somewhere
	old_r, old_col, piece = findPieceSquare(position)
	p = -1
	for key, value in piece_dict.items():
		if piece == value:
		    p = key
		    break
	if p <= 1:
		new_r, new_col = findEmptySquare(position, row_lower=1, row_upper=7)
	else:
		new_r, new_col = findEmptySquare(position)

	removed = remove_piece(position, r=old_r, col=old_col)
	added = add_piece(removed, r=new_r, col=new_col, piece=p)

	return added

def analyze(position):
	ret_stockfish = os.system("Stockfish/src/stockfish < input_sh.txt > out_stockfish.txt")
	if ret_stockfish != 0: # the position is invalid
		print("invalid position detected by stockfish")
		return ["invalid"]

	print("valid position (by stockfish)")
	
	with open("out_stockfish.txt", "r") as out_stockfish: 
		stockfish_analysis = out_stockfish.read().split("\n")
		bm_index = -1
		for i in range(len(stockfish_analysis)-1, -1, -1): #iterate lines backwards
			if stockfish_analysis[i].split(' ')[0] == 'bestmove':
				bm_index = i
				break
		if bm_index == -1:
			print("no stockfish best move")
			return ["invalid"]
		stockfish_bm = stockfish_analysis[bm_index].split(' ')[1]
		if stockfish_bm == '(none)': #this should indicate checkmate, which we dont care about
			print("valid but checkmate position")
			return ["invalid"] 
		depth_index = bm_index-1 #index of the line that contains the last depth the engine went to
		depth_line = stockfish_analysis[depth_index].split(' ')
			#example depth line: "info depth 38 seldepth 10 score mate 5 time 789 nodes 1571543 nps 1991000 hashfull 20 tbhits 0 pv d1d2 e8d8 g8f6 c5f2"
		if depth_line[1] != 'depth': #sanity check make sure depth is there above bestmove line
			print("stockfish depth not above bestmove")
			return ["invalid"]
		stockfish_depth = int(depth_line[2])
		if stockfish_depth <= 3:
			print("stockfish low depth")
		stockfish_score = "N/A"
		score_index = 0
		while depth_line[score_index] != 'score' and score_index < len(depth_line):
			score_index += 1
		if depth_line[score_index] == 'score':
			stockfish_score = depth_line[score_index+1] + " " + depth_line[score_index+2]
	
	ret_rubichess = os.system("RubiChess/src/RubiChess < input_r.txt > out_rubichess.txt")
	if ret_rubichess != 0:
		print("invalid position detected by rubi")
		return ["invalid"]

	with open("out_rubichess.txt", "r") as out_rubi:
		rubi_analysis = out_rubi.read().split("\n")
		bm_index = -1
		for i in range(len(rubi_analysis)-1, -1, -1): #iterate lines backwards
			if rubi_analysis[i].split(' ')[0] == 'bestmove':
				bm_index = i
				break
		if bm_index == -1:
			print("no rubi best move")
			return ["invalid"]
		rubi_bm = rubi_analysis[bm_index].split(' ')[1]
		depth_index = bm_index-1
		depth_line = rubi_analysis[depth_index].split(' ')
		if depth_line[1] != 'depth': #sanity check make sure depth is there above bestmove line
			print("rubi depth not above bestmove")
			return ["invalid"]
		rubi_depth = int(depth_line[2])
		if rubi_depth <= 3:
			print("rubi low depth")
		rubi_score = "N/A"
		score_index = 0
		while depth_line[score_index] != 'score' and score_index < len(depth_line):
			score_index += 1
		if depth_line[score_index] == 'score':
			rubi_score = depth_line[score_index+1] + " " + depth_line[score_index+2]

	ret_halogen = os.system("Halogen/bin/Halogen-native.exe < input_sh.txt > out_halogen.txt")
	if ret_halogen != 0:
		print("invalid position detected by halogen")
		return ["invalid"]

	with open("out_halogen.txt", "r") as out_halogen:
		halogen_analysis = out_halogen.read().split("\n")
		bm_index = -1
		for i in range(len(halogen_analysis)-1, -1, -1): #iterate lines backwards
			if halogen_analysis[i].split(' ')[0] == 'bestmove':
				bm_index = i
				break
		if bm_index == -1:
			print("no halogen best move")
			return ["invalid"]
		halogen_bm = halogen_analysis[bm_index].split(' ')[1]
		depth_index = bm_index-1
		depth_line = halogen_analysis[depth_index].split(' ')
		if depth_line[1] != 'depth': #sanity check make sure depth is there above bestmove line
			print("halogen depth not above bestmove")
			return ["invalid"]
		halogen_depth = int(depth_line[2]) 
		if halogen_depth <= 3:
			print("halogen low depth")
		halogen_score = "N/A"
		score_index = 0
		while depth_line[score_index] != 'score' and score_index < len(depth_line):
			score_index += 1
		if depth_line[score_index] == 'score':
			halogen_score = depth_line[score_index+1] + " " + depth_line[score_index+2]
	to_ret = []
	# will contain objects of the form {position: position, div: AB, e1move: e2e4, e1score: , e2move: d2d4, e2score: }
	if stockfish_bm != rubi_bm: #There is an A B divergence
		to_ret.append({"position":position, "div":"AB", "e1move":stockfish_bm, "e1score":stockfish_score, "e1depth":stockfish_depth, "e2move":rubi_bm, "e2score": rubi_score, "e2depth":rubi_depth})
	if rubi_bm != halogen_bm:
		to_ret.append({"position":position, "div":"BC", "e1move":rubi_bm, "e1score":rubi_score, "e1depth":rubi_depth, "e2move":halogen_bm, "e2score": halogen_score, "e2depth":halogen_depth})
	if stockfish_bm != halogen_bm: 
		to_ret.append({"position":position, "div":"AC", "e1move":stockfish_bm, "e1score":stockfish_score, "e1depth":stockfish_depth, "e2move":halogen_bm, "e2score": halogen_score, "e2depth":halogen_depth})
	return to_ret

def export(results, filename):
	with open(f"{filename}.txt", "w") as f:
		for r in results:
			f.write(str(r))
			f.write("\n")

def fuzzer(seed_position, number_required_divergences=100):
	divergences = 0
	AB_divergences = []
	BC_divergences = []
	AC_divergences = []
	position = seed_position
	valid_positions = 0
	while (
		valid_positions < 100
		# divergences < number_required_divergences
		# and len(crash) + len(hang) < number_required_mutations
	):
		mutationChoice = random.randrange(0, 5)
		if mutationChoice == 0:
			tentative_position = change_piece(position)
		elif mutationChoice == 1:
			tentative_position = change_color(position)
		elif mutationChoice == 2:
			tentative_position = add_piece(position)
		elif mutationChoice == 3:
			tentative_position = remove_piece(position)
		elif mutationChoice == 4:
			tentative_position = move_piece(position)

		print(tentative_position)
		with open("input_sh.txt", "w") as input_sh: #the inputs to stockfish and halogen
			input_sh.write(f'position fen {tentative_position} w - - 0 1\ngo depth 20\nucinewgame')
		with open("input_r.txt", "w") as input_r: #the input to rubichess
			input_r.write(f'position fen {tentative_position} w - - 0 1\ngo depth 20\nwait\n')

		result = analyze(tentative_position)
		if "invalid" in result:
		    continue
			#break
		for r in result:
			divergences += 1
			position = tentative_position
			if r["div"] == "AB":
				AB_divergences.append(r)
			elif r["div"] == "BC":
				BC_divergences.append(r)
			elif r["div"] == "AC":
				AC_divergences.append(r)

		valid_positions += 1
		print(str(valid_positions) + " valid positions found")

	print("AB Divergences: " + str(len(AB_divergences)))
	#print(AB_divergences)
	export(AB_divergences, "AB_Divergences")

	print("BC Divergences: " + str(len(BC_divergences)))
	#print(BC_divergences)
	export(BC_divergences, "BC_Divergences")

	print("AC Divergences: " + str(len(AC_divergences)))
	#print(AC_divergences)
	export(AC_divergences, "AC_Divergences")

	return position


if __name__ == "__main__":
	#seed_start, seed_opening, seed_mid, seed_end
	with open("seed_mid.txt", "r") as seed_input:
		seed_pos = seed_input.read().rstrip()
	num_to_find = 100
	fuzzer(seed_pos, num_to_find)
