SET DEFAULT TO c:\Liquida\

ultimo_dia = DAY(DATE())
mes = MONTH(DATE())
anio = YEAR(DATE())

DELETE FILE c:\Liquida\enlace_microsip_precios_mes.DBF
DELETE FILE c:\Liquida\enlace_microsip_saldos.dbf
SELECT DISTINCT precio FROM lprodrec WHERE codprod  == 'L001' AND fecha >= DATE(anio,mes,01) ANd fecha <= DATE(anio,mes,15) into cursor quincena1
SELECT DISTINCT precio FROM lprodrec WHERE codprod  == 'L001' AND fecha >= DATE(anio,mes,16) ANd fecha <= DATE(anio,mes,ultimo_dia) into cursor quincena2
SELECT quincena1.precio as precio1, quincena2.precio as precio2 from quincena1, quincena2 INTO TABLE enlace_microsip_precios_mes.DBF
COUNT TO R

if R > 1 THEN 
	=mesSagebox(":( No se enviara nada a microsip, no se aceptan precios diferentes por quincena")
ENDIF

IF R == 0 THEN
	=mesSagebox(":( No se enviara nada a microsip, captura primero las liquidaciones de la [segunda] quincena")
ENDIF

IF R == 1 THEN
	SELECT clave, kilos1, importe1, intereses, retencione, fecha FROM LSALDOSP WHERE situacion="A" AND kilos1>0  AND facturacio="F" AND fecha >= DATE(anio,mes,01) ANd fecha <= DATE(anio,mes,ultimo_dia) ORDER BY CLAVE, FECHA INTO TABLE enlace_microsip_saldos.dbf
ENDIF

CLEAR EVENTS
CLOSE DATA ALL