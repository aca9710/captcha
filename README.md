<!-- title: Prueba -->

![datacimex][def]


# Emisor de tarjetas de remesas

## Servidor web

#### Interprete : 
   python 3.8

#### Framework: 
   Flask

#### Front end: 
   Bootstrap v5.0

#### Base de datos: 
   postgresql 11

___

#### Variables de entorno:
  Relacionadas con la base de datos

  | <u>Variable</u> | <u>Descripci&oacute;n</u>                           |
  | :-------------- | :-------------------------------------------------- |
  | RMS_USR         | Usuario para acceder a la base de datos             |
  | RMS_DBNAME      | Base de datos en el servidor de postgresql          |
  | RMS_HOST        | Url donde se encuentra el servidor de base de datos |
  | RMS_CLV         | Clave para acceder al servidor de base de datos     |
  | RMS_PUERTO      | Puerto asociado al servidor de base de datos        |

  Relacionadas con la configuracion de la aplicacion

  | <u>Variable</u> | <u>Descripci&oacute;n</u>                                           |
  | :-------------- | :------------------------------------------------------------------ |
  | RMS_MAIL        | Servidor de correos                                                 |
  | RMS_LDAP        | Servidor de LDAP                                                    |
  | RMS_LDAP_PT     | Puerto para el servidor de LDAP                                     |
  | RMS_TMP         | Carpeta de ficheros temporales                                      |
  | RMS_LOG         | Carpeta donde se van a escribir las trazas de la aplicacion         |
  | RMS_LOAD        | Carpeta donde se van a guardar los ficheros importados desde la web |
  | RMS_RPT         | Carpeta donde se van a guardar los reportes de la aplicacion        |
  | RMS_ERROR       | Carpeta donde se va a escribir el fichero de error                  |
  | RMS_DEBUG       | Coloca la aplicacion en modo DEBUG valores posibles (SI/NO)         |


Servidor FTP

  | <u>Variable</u> | <u>Descripci&oacute;n</u>        |
  | :-------------- | :------------------------------- |
  | RMS_FTP_HOST    | URL del servidor ftp de fincimex |
  | RMS_FTP_PUERTO  | Puerto del servidor ftp          |
  | RMS_FTP_USR     | Usuario del servidor ftp         |
  | RMS_FTP_CLV     | Clave del servidor ftp           |



___








   


[def]: static/img/datacimex.png