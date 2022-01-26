function DireLookup()
	let line = split(getline('.')[col('.')-1:])[0]
	let cmd = "dire_cli " . line
	let def = system(cmd)
	vsplit defn
	call append(0, split(def, '\v\n'))
	normal! gg
endfunction

function DireSearchLine()
	let line =  getline(".")
	let cmd = "dire_cli " . line
	let def = system(cmd)
	call append(0, split(def, '\v\n'))
	normal! gg
endfunction

function DireSearch()
	call inputsave()
	let word = input('search word: ')
	call inputrestore()
	let cmd = "dire_cli " . word
	let def = system(cmd)
	tabnew
	call append(0, split(def, '\v\n'))
	normal! gg
endfunction


function DireGlob()
	call inputsave()
	let word = input('search glob: ')
	call inputrestore()
	let cmd = "dire_cli -g " . "'" . word . "'"
	let def = system(cmd)
	tabnew
	call append(0, split(def, '\v\n'))
	normal! gg
endfunction

