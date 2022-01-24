require 'mp'


local function run_cmd(cmd, param_string)
    command_str = string.format("%s '%s'", cmd, param_string or "")
    local result = os.execute(command_str)

    return result
end


function print_subs()
	local subs = mp.get_property('sub-text')
	run_cmd('dire_send_text video', subs)
end


function start_watch()
	mp.observe_property("sub-text", "string", print_subs)
end

mp.add_key_binding('d', start_watch)
