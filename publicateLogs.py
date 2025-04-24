import csv
import sys
import os
import geopy.distance
from datetime import datetime
import configparser
import shutil
import tarfile
import os.path

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
        
        
BASE_DIR     = os.path.abspath(os.path.dirname(__file__))
os.chdir(BASE_DIR)
cfg = configparser.ConfigParser()
cfg.read(BASE_DIR+'/publicateLogs.cfg')

# SAFECAST ID/No
sfID = cfg['DEFAULT']['sfID']
# directories to 
# - publicate
# - store archve data
pub_dir   = cfg['DEFAULT']['pub_dir']
save_dir  = cfg['DEFAULT']['save_dir']

# load GEOFENCING areas to ommit in the logs
geofencing=cfg._sections['GEOFENCING']
gf = {}
for i in geofencing:
  gf[i] = (cfg['GEOFENCING'][i]).split(",")

now = datetime.now()

aderCOEF = 0.0365296803652968
totalCPM = 0
avgCPM = 0
minCPM = 10000
maxCPM = 0
count = 0
latPrew = 0
lonPrew = 0
tsPrew = 0
dist = 0
totalDist = 0

v = 0
dtStr = ''
dtStrPrew = ''
days = 0

if len(sys.argv) > 1:
  dir_path=(sys.argv[1])
else:
  dir_path = r'./'

for file in os.listdir(dir_path):
  if (file.endswith('.log') or file.endswith('.LOG')) :
    print(dir_path+file)
    days = days + 1
    line = 0
    wrongDateCnt = 0
    insideBASECnt = 0
    
# Create file inside "to publicate" folder    
    f = open(dir_path+pub_dir+file, 'w', newline='')
    
    with open(dir_path+file, newline='') as csvfile:
      logreader = csv.reader(csvfile, delimiter=',')
      logwriter = csv.writer(f)
      
      for row in logreader:
        insideBase = 0
        try:
          pp15s = int(row[4])
          dtStr = row[2]
          try:
            # DateTime validity check
            ts = int(datetime.datetime.fromisoformat(dtStr.rstrip('Z')).timestamp())
          except:
            wrongDateCnt = wrongDateCnt + 1
            dtStr = dtStr.replace(dtStr[:10], dtStrPrew[:10])
            try:
              ts = int(datetime.datetime.fromisoformat(dtStr.rstrip('Z')).timestamp())
            except:
              ts = tsPrew+5
              
          rawLat = float(row[7])
          rawLon = float(row[9])
          latD = int(rawLat/100)
          lonD = int(rawLon/100)
          lat = latD + ((rawLat - (latD*100))/60)
          lon = lonD + ((rawLon - (lonD*100))/60)
          if (line > 0):
            dist = geopy.distance.geodesic((latPrew, lonPrew), (lat,lon)).m
            for gfi in gf:
              if ((geopy.distance.geodesic((float(gf[gfi][0]), float(gf[gfi][1])), (lat,lon)).m) < float(gf[gfi][2])):
                insideBase = 1
#                print("Inside GeoFencing area => ommit log line")
                insideBASECnt = insideBASECnt + 1
            v = (dist / (ts-tsPrew))
          latPrew = lat
          lonPrew = lon
          tsPrew = ts
          dtStrPrew = dtStr
          currCPM = int(row[3])
          totalCPM = totalCPM + currCPM
          if(currCPM < minCPM):
            minCPM = currCPM
          if(currCPM > maxCPM):
            maxCPM = currCPM
          totalDist = totalDist + dist
          count = count + 1
          line = line + 1
          
          if(pp15s > 20):
            print(row)
#          print(dtStr, ts, lat, lon, dist, v)
        except IndexError:
          None
        if (insideBase == 0):  
          logwriter.writerow(row)  
#     DEBUG
#        if (count > 10):
#          quit()
    if wrongDateCnt > 0 :
      print('Wrong Date Time Count' , wrongDateCnt)
    if insideBASECnt > 0 :
      print('!!! ' , insideBASECnt , ' measured points inside the GEOFENCING zone !!! Ommit logs ')

#Write file s
# - to publicate
# - move processed file to archive - clean ROOT path of SD card                    
    f.close()
    shutil.move(dir_path+file, dir_path+save_dir+file)
# - create tar archive
make_tarfile(dir_path+sfID+'_'+now.strftime("%Y%m%d-%H%M%S")+'_pub.tar.gz', dir_path+pub_dir)

avgCPM = totalCPM / count

print('')
print('#########################################')
print('')
print('Number of measurement days: ', days)
print('Total CPM:', totalCPM)
print('CPM min/max/avg:', "%.2f/" % (minCPM), "%.2f/" % (maxCPM), "%.2f" % (avgCPM))
print('ADER min/max/avg:', "%.2f/" % (minCPM * aderCOEF), "%.2f/" % (maxCPM * aderCOEF), "%.2f" % (avgCPM * aderCOEF), ' [microSv/h]')
print('Total measure count: ', count)
print('Total distance: ', "%.2f" % (totalDist/1000), 'km')
print('AVG measures/day: ', "%.2f" % (count/days))
print('AVG distance/day: ', "%.2f" % ((totalDist/1000)/days), 'km')
        
input("Press enter to exit ;)")
