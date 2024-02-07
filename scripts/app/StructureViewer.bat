@ECHO OFF
REM  QBFC Project Options Begin
REM  HasVersionInfo: No
REM Companyname: 
REM Productname: 
REM Filedescription: 
REM Copyrights: 
REM Trademarks: 
REM Originalname: 
REM Comments: 
REM Productversion:  0. 0. 0. 0
REM Fileversion:  0. 0. 0. 0
REM Internalname: 
REM ExeType: console
REM Architecture: x64
REM Appicon: 
REM AdministratorManifest: No
REM  QBFC Project Options End
@ECHO ON
@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
python StructureViewer.pyw
