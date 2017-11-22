set ws=createobject("wscript.shell")
do
if Hour(Now)>=9 and Hour(Now)<16 then
	ws.run "D:\gw_trade\run.bat"
end if
wscript.sleep 3600000
loop