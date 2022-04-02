-- Warning: This was pretty much just hacked together with a bunch of
-- os.executes and the code quality is pretty bad (even compared to the rest of the code).
-- Read at your own risk

require 'mp'

-- The location of your anki media
media =  '~/.local/share/Anki2/User\\ 1/collection.media/'


local function run_cmd(cmd, param_string)
    command_str = string.format("%s '%s'", cmd, param_string or "")
    local file = io.popen(command_str)
		local str = file:read "*a"

    return str

end


function print_subs()
	local subs = mp.get_property('sub-text')
	run_cmd('dire_send_text -a video', subs)
end

function make_card()
	local subs = mp.get_property('sub-text')
	local sub_delay = mp.get_property_native("sub-delay")
	local subs_start = mp.get_property('sub-start') + sub_delay
	local subs_end = mp.get_property('sub-end') + sub_delay
	local filename = mp.get_property('filename')

	local time = tostring(os.time())
	local name = time .. '.mp3'
	local name_img = time .. '.jpg'
	local out_file = media .. name
	local out_file_img = media .. name_img
	local command_result = run_cmd('python ~/.config/mpv/mpv_select_text.py', subs)
	if(command_result == "None\n" ) then
		return
	end
	os.execute(string.format('ffmpeg -ss %s -to %s -i \'%s\' %s', tostring(subs_start), tostring(subs_end), filename, out_file))
	os.execute(string.format('ffmpeg -ss %s -i \'%s\' -frames:v 1 %s', subs_start, filename, out_file_img))
	os.execute(string.format('convert %s -resize 250x %s', out_file_img, out_file_img))
	os.execute(string.format('dire_cli -c \'%s\' \'%s\' \'<audio src="%s" controls></audio><img src="%s"/>\'', command_result, subs, name, name_img))

end


function start_watch()
	mp.observe_property("sub-text", "string", print_subs)
end

mp.add_key_binding('d', start_watch)
mp.add_key_binding('c', make_card)

