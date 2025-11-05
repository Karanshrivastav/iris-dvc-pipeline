-- scripts/wrk_post.lua
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
local payload = '{"instances":[[5.1,3.5,1.4,0.2]]}'
wrk.body = payload
