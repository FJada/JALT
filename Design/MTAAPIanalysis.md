Using python pandas I was able to decipher the standards of the API 


## Station Data
> R032,R145,42 ST-TIMES SQ,1237ACENQRS,IRT
> R032,A021,42 ST-TIMES SQ,1237ACENQRS,BMT
> R032,R143,42 ST-TIMES SQ,ACENQRS1237,IRT
> R032,R146,42 ST-TIMES SQ,1237ACENQRS,IRT
> R033,R151,42 ST-TIMES SQ,1237ACENQRS,IRT
> R033,R148,42 ST-TIMES SQ,1237ACENQRS,IRT
> R033,R150,42 ST-TIMES SQ,1237ACENQRS,IRT
> R033,R153,42 ST-TIMES SQ,1237ACENQRS,IRT
> R033,R147,42 ST-TIMES SQ,1237ACENQRS,IRT

Here 42 ST-TIMES SQ stands for the station. 1237ACENDRS stands for all of the trains that are offered 
at the times square station. IRT and BMT indicate what type of train it is and what tunnel is used for that line. 
Here you can also see that there are 4 remotes and 5 booths. 

## Turnstile Data 
> A002,R051,02-00-00,
> 07-27-13,00:00:00,REGULAR,004209603,001443585,
> 07-27-13,04:00:00,REGULAR,004209643,001443593,
> 07-27-13,08:00:00,REGULAR,004209663,001443616,
> 07-27-13,12:00:00,REGULAR,004209741,001443687,
> 07-27-13,16:00:00,REGULAR,004210004,001443740,
> 07-27-13,20:00:00,REGULAR,004210276,001443777,
> 07-28-13,00:00:00,REGULAR,004210432,001443801,
> 07-28-13,04:00:00,REGULAR,004210472,001443805

The top line indicates the specific turnstile at a specific station. The next few rows show data that checks every
4 hours. The first column being the date, second being the time, third is status report, and fourth read entry and exit. 


