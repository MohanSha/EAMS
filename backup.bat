@echo off
set /p name="Enter Year RunMonth_RunIndex(17_0102_r1): 

::local backup
::mysqldump -u root hr > hr_backup_%name%.sql
::mysqladmin -u root create hr_backup_%name%
::mysql -u root hr_backup_%name% < hr_backup_%name%.sql

::Remote backup
mysqldump -uattend -pattend01 -h 172.16.3.24 hr > hr_backup_%name%.sql
mysqladmin -uattend -pattend01 -h 172.16.3.24 create hr_backup_%name%
mysql -uattend -pattend01 -h 172.16.3.24 hr_backup_%name% < hr_backup_%name%.sql