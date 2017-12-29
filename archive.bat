@echo off
mysql -u root -p hr -e "INSERT INTO hra.ac_data (SELECT * FROM hr.ac_data);" -e "INSERT INTO hra.att_report (SELECT * FROM hr.att_report);" -e "INSERT INTO hra.att_stage01 (SELECT * FROM hr.att_stage01);" -e "INSERT INTO hra.erp_report (SELECT * FROM hr.erp_report);" -e "INSERT INTO hra.mob_data (SELECT * FROM hr.mob_data);"
::mysql -u root -p hr -e "INSERT INTO hra.att_report (SELECT * FROM hr.att_report);"
::mysql -u root -p hr -e "INSERT INTO hra.att_stage01 (SELECT * FROM hr.att_stage01);"
::mysql -u root -p hr -e "INSERT INTO hra.calendar (SELECT * FROM hr.calendar);"
::mysql -u root -p hr -e "INSERT INTO hra.email (SELECT * FROM hr.email);"
::mysql -u root -p hr -e "INSERT INTO hra.erp_report (SELECT * FROM hr.erp_report);"
::mysql -u root -p hr -e "INSERT INTO hra.holiday (SELECT * FROM hr.holiday);"
::mysql -u root -p hr -e "INSERT INTO hra.mob_data (SELECT * FROM hr.mob_data);"

echo ALL DONE
echo Attendance has been archived !!