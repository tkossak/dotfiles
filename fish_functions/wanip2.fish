# Defined in - @ line 1
function wanip2 --wraps='wget -qO - http://ipecho.net/plain' --description 'alias wanip2 wget -qO - http://ipecho.net/plain'
  wget -qO - http://ipecho.net/plain $argv;
end
