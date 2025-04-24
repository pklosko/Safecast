# Safecast
[Safecast](https://safecast.org/) data publication &amp; stats scripts &amp; tools

## publicateLogs.py
Clean logs and create archive to send to SURO (for more info see [Detektor záření SAFECAST a jeho využití pro veřejnost](https://www.suro.cz/aplikace/czechrad-wiki/index.php/Detektor_z%C3%A1%C5%99en%C3%AD_SAFECAST_a_jeho_vyu%C5%BEit%C3%AD_pro_ve%C5%99ejnost))

- DateTime validity check
- Ommit LOGS inside the "Geofencing" zones
- Print some stats


### CONFIG - publicateLogs.cfg
```none
[DEFAULT]
# TAR archive will be created here
pub_dir=pub/
# Original LOG files will be saved here
save_dir=LOG_archiv/2025/
# !!! DIRECTORIES MUST EXISTS !!!

# SAFECAST ID
sfID=1234

[GEOFENCING]
#Ommit lines/logs in area defined by circle.
#Circle center [Lat, Lon] ; radius[m]
1=50.0797500,14.4304000,1500 #Prague
2=49.1800739,14.3761972,1000 # Temelin NPP
#...
#n=
```

### USAGE
- Create "pub_dir" and "save_dir" folders into the root of SD card
- Copy files to Saafecast SD card root
- Run script

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.