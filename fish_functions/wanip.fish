# Defined in - @ line 1
function wanip --wraps='dig +short myip.opendns.com @resolver1.opendns.com' --description 'alias wanip dig +short myip.opendns.com @resolver1.opendns.com'
  dig +short myip.opendns.com @resolver1.opendns.com $argv;
end
