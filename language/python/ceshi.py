import time
import datetime

date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
backup_dir = "/data/backup-tomcat/"
dir = backup_dir + date
print(dir)