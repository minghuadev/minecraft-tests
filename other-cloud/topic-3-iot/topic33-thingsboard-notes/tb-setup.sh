
#mkdir -p ~/mytb/mytb-data && sudo chown -R 799:799 ~/mytb/mytb-data
#mkdir -p ~/mytb/mytb-logs && sudo chown -R 799:799 ~/mytb/mytb-logs
docker run -it \
	-p 8080:9090 -p 7070:7070 -p 1883:1883 -p 5683-5688:5683-5688/udp \
	-v ~/mytb/mytb-data:/data \
	-v ~/mytb/mytb-logs:/var/log/thingsboard \
	--name mytb --restart always thingsboard/tb-postgres


