# Procedimiento para procesar los datos de Ergast API en formato csv con PowerBI

1. Cambiar configuración regional
    - Archivo -> Opciones y Configuración -> Opciones -> Global -> Configuración Regional -> Idioma del modelo -> `Inglés(Estados Unidos)`
    - Archivo -> Opciones y Configuración -> Opciones -> Archivo actual -> Configuración Regional -> Configuración regional para la importación -> `Inglés(Estados Unidos)`

&nbsp; &nbsp; 

2. Cargar datos a través de script Python
    - Ir a `Obtener datos -> Script de Python` y pegar el script (Si falla comprobar ruta de archivos)
    - Seleccionar todas las tablas disponibles y hacer click en `Transformar datos`

&nbsp; &nbsp; 

3. Editar tablas (Seleccionar siempre `Sustituir la actual`):
    - **circuits**: cambiar tipo de columnas `lat` y `lng` a *Número decimal*
    - **driver_standings**: cambiar tipo de columnas `driverStandingsId`, `raceId`, `driverId`, `postion` y `wins` a *Número entero*. Cambiar `points` a *Número decimal*
    - **drivers**: cambiar tipo de columnas `driverId` y `number` a *Número entero*. Cambiar `dob` a *Fecha*. Crear columna personalizada con nombre `fullName` y consulta `[forename]&" "&[surname]`
    - **lap_times**: cambiar tipo de columna `time` a *Duración*
    - **pit_stops**: cambiar tipo de columna `duration` a *Duración*
    - **qualifying**: cambiar tipo de columnas `q1`, `q2` y `q3` a *Duración*
    - **races**: cambiar tipo de columnas `raceId`, `year`, `round` y `circuitId` a *Número entero*. Cambiar `date`, `fp1_date`, `fp2_date`, `fp3_date`, `quali_date` y `sprint_date` a *Fecha*. Cambiar `time`, `fp1_time`, `fp2_time`, `fp3_time`, `quali_time` y `sprint_time` a *Hora*
    - **results**: cambiar `fastestLapTime` a *Duración*. Cambiar `fastestLapSpeed` a *Número decimal*
    - **sprint_results**: cambiar `fastestLapTime` a *Duración*

&nbsp; &nbsp; 

4. hacer click en `Cerrar y aplicar`.

&nbsp; &nbsp; 

5. Comprobar el modelo de datos
    - Crear relación entre `seasons[year]` y `races[year]`
    - Eliminar relación entre `results` y `sprint_results`
    - Comprobar el resto de relaciones del modelo. Se deberían establecer de forma automática, por lo que solo queda corregir cualquier problema, que deberían ser pocos o nada.