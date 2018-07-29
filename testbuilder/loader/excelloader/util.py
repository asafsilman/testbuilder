import string

def colnum_string(n):
    div=n
    string=""
    while div>0:
        module=(div-1)%26
        string=chr(65+module)+string
        div=int((div-module)/26)
    return string
	
def colstring_num(col):
	num = 0
	for c in col:
		if c in string.ascii_letters:
			num = num * 26 + (ord(c.upper()) - ord('A')) + 1
	return num

def split_cell_string(cell):

    for i in range(len(cell)):
        if cell[i].isnumeric():
            return cell[:i], int(cell[i:])
    else:
        return None