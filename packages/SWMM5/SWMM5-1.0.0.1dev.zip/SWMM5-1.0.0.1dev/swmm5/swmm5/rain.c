//-----------------------------------------------------------------------------
//   rain.c
//
//   Project: EPA SWMM5
//   Version: 5.0
//   Date:    6/19/07   (Build 5.0.010)
//            7/16/07   (Build 5.0.011)
//            4/10/09   (Build 5.0.015)
//            6/22/09   (Build 5.0.016)
//            07/30/10  (Build 5.0.019)
//            04/20/11  (Build 5.0.022)
//   Author:  L. Rossman
//
//   Places rainfall data from external files into a SWMM rainfall
//   interface file.
//
//   The following types of external data files are supported:
//   NWS_TAPE:            NCDC NWS TD 3240 or 3260 data in fixed field widths
//   NWS_SPACE_DELIMITED: NCDC NWS TD (DSI) 3240 or 3260 data in space delimited
//                        format, with or without header lines, with or without //(5.0.015 - LR)
//                        station name                                          //(5.0.015 - LR)
//   NWS_COMMA_DELIMITED: NCDC NWS TD (DSI) 3240 or 3260 data in comma delimited
//                        format, with or without header lines
//   AES_HLY:             Canadian AES hourly data with 3-digit year
//   CMC_HLY:             Canadian CMC hourly data in HLY03 or HLY21 format
//   CMC_FIF:             Canadian CMC fifteen minute data in in FIF21 format
//   STD_SPACE_DELIMITED: standard SWMM space delimted format:
//                        StaID  Year  Month  Day  Hour  Minute  Rainfall
//
//   The layout of the SWMM binary rainfall interface file is:
//     File stamp ("SWMM5-RAIN") (10 bytes)
//     Number of SWMM rain gages in file (4-byte int)
//     Repeated for each rain gage:
//       recording station ID (not SWMM rain gage ID) (MAXMSG+1 (=80) bytes)
//       gage recording interval (seconds) (4-byte int)
//       starting byte of rain data in file (4-byte int)
//       ending byte+1 of rain data in file (4-byte int)
//     For each gage:
//       For each time period with non-zero rain:
//         Date/time for start of period (8-byte double)
//         Rain depth (inches) (4-byte float)
//-----------------------------------------------------------------------------
#define _CRT_SECURE_NO_DEPRECATE

#include <stdlib.h>
#include <string.h>
#include "headers.h"

//-----------------------------------------------------------------------------
//  Constants
//-----------------------------------------------------------------------------
enum RainFileFormat {UNKNOWN_FORMAT, NWS_TAPE, NWS_SPACE_DELIMITED,
                     NWS_COMMA_DELIMITED, AES_HLY, CMC_HLY, CMC_FIF,
                     STD_SPACE_DELIMITED};
enum ConditionCodes {NO_CONDITION, ACCUMULATED_PERIOD, DELETED_PERIOD,
                     MISSING_PERIOD};

//-----------------------------------------------------------------------------
//  Shared variables
//-----------------------------------------------------------------------------
TRainStats RainStats;                  // see objects.h for definition
int        Condition;                  // rainfall condition code
int        TimeOffset;                 // time offset of rainfall reading (sec)
int        RainType;                   // rain measurement type code
int        Interval;                   // rain measurement interval (sec)
double     UnitsFactor;                // units conversion factor
float      RainAccum;                  // rainfall depth accumulation
char       *StationID;                 // station ID appearing in rain file
DateTime   AccumStartDate;             // date when accumulation begins        //(5.0.010 - LR)
DateTime   PreviousDate;               // date of previous rainfall record     //(5.0.022 - LR)
int        GageIndex;                  // index of rain gage analyzed          //(5.0.022 - LR)
int        hasStationName;             // true if data contains station name   //(5.0.015 - LR)

//-----------------------------------------------------------------------------
//  External functions (declared in funcs.h)
//-----------------------------------------------------------------------------
//  rain_open   (called by swmm_start in swmm5.c)
//  rain_close  (called by swmm_end in swmm5.c)

//-----------------------------------------------------------------------------
//  Local functions
//-----------------------------------------------------------------------------
static void createRainFile(int count);
static int  rainFileConflict(int i);                                           //(5.0.019 - LR)              
static void initRainFile(void);
static int  findGageInFile(int i, int kount);
static int  addGageToRainFile(int i);
static int  findFileFormat(FILE *f, int i, int *hdrLines);
static void readFile(FILE *f, int fileFormat, int hdrLines, DateTime day1,
            DateTime day2);
static int  readNWSLine(char *line, int fileFormat, DateTime day1,
            DateTime day2);
static int  readCMCLine(char *line, int fileFormat, DateTime day1,
            DateTime day2);
static int  readStdLine(char *line, DateTime day1, DateTime day2);
static void saveAccumRainfall(DateTime date1, int hour, int minute, long v);   //(5.0.010 - LR)
static void saveRainfall(DateTime date1, int hour, int minute, float x,
            char isMissing);
static void setCondition(char flag);
static int  getNWSInterval(char *elemType);
static int  parseStdLine(char *line, int *year, int *month, int *day,
            int *hour, int *minute, float *value);

//=============================================================================

void  rain_open(void)
//
//  Input:   none
//  Output:  none
//  Purpose: opens binary rain interface file and RDII processor.
//
{
    int i;
    int count;

    // --- see how many gages get their data from a file
    count = 0;
    for (i = 0; i < Nobjects[GAGE]; i++)
    {
        if ( Gage[i].dataSource == RAIN_FILE ) count++;
    }
    Frain.file = NULL;
    if ( count == 0 )
    {
        Frain.mode = NO_FILE;
    }

    // --- see what kind of rain interface file to open
    else switch ( Frain.mode )
    {
      case SCRATCH_FILE:
        getTmpName(Frain.name);
        if ( (Frain.file = fopen(Frain.name, "w+b")) == NULL)
        {
            report_writeErrorMsg(ERR_RAIN_FILE_SCRATCH, "");
            return;
        }
        break;

      case USE_FILE:
        if ( (Frain.file = fopen(Frain.name, "r+b")) == NULL)
        {
            report_writeErrorMsg(ERR_RAIN_FILE_OPEN, Frain.name);
            return;
        }
        break;

      case SAVE_FILE:
        if ( (Frain.file = fopen(Frain.name, "w+b")) == NULL)
        {
            report_writeErrorMsg(ERR_RAIN_FILE_OPEN, Frain.name);
            return;
        }
        break;
    }

    // --- create new rain file if required
    if ( Frain.mode == SCRATCH_FILE || Frain.mode == SAVE_FILE )
    {
        createRainFile(count);
    }

    // --- initialize rain file
    if ( Frain.mode != NO_FILE ) initRainFile();

    // --- open RDII processor (creates/opens a RDII interface file)
    rdii_openRdii();
}

//=============================================================================

void rain_close(void)
//
//  Input:   none
//  Output:  none
//  Purpose: closes rain interface file and RDII processor.
//
{
    if ( Frain.file )
    {
        fclose(Frain.file);
        if ( Frain.mode == SCRATCH_FILE ) remove(Frain.name);
    }
    Frain.file = NULL;
    rdii_closeRdii();
}

//=============================================================================

void createRainFile(int count)
//
//  Input:   count = number of files to include in rain interface file
//  Output:  none
//  Purpose: adds rain data from all rain gage files to the interface file.
//
{
    int   i, k;
    int   kount = count;               // number of gages in data file
    int   filePos1;                    // starting byte of gage's header data
    int   filePos2;                    // starting byte of gage's rain data
    int   filePos3;                    // starting byte of next gage's data
    int   interval;                    // recording interval (sec)
    int   dummy = -1;
    char  staID[MAXMSG+1];             // gage's ID name
    char  fileStamp[] = "SWMM5-RAIN";

    // --- make sure interface file is open and no error condition
    if ( ErrorCode || !Frain.file ) return;

    // --- write file stamp & # gages to file
    fwrite(fileStamp, sizeof(char), strlen(fileStamp), Frain.file);
    fwrite(&kount, sizeof(int), 1, Frain.file);
    filePos1 = ftell(Frain.file); 

    // --- write default fill-in header records to file for each gage
    //     (will be replaced later with actual records)
    if ( count > 0 ) report_writeRainStats(-1, &RainStats);
    for ( i = 0;  i < count; i++ )
    {
        fwrite(staID, sizeof(char), MAXMSG+1, Frain.file);
        for ( k = 1; k <= 3; k++ )
            fwrite(&dummy, sizeof(int), 1, Frain.file);
    }
    filePos2 = ftell(Frain.file);

    // --- loop through project's  rain gages,
    //     looking for ones using rain files
    for ( i = 0; i < Nobjects[GAGE]; i++ )
    {
        if ( ErrorCode || Gage[i].dataSource != RAIN_FILE ) continue;
        if ( rainFileConflict(i) ) break;                                      //(5.0.019 - LR)

        // --- position rain file to where data for gage will begin
        fseek(Frain.file, filePos2, SEEK_SET);

        // --- add gage's data to rain file
        if ( addGageToRainFile(i) )
        {
            // --- write header records for gage to beginning of rain file
            filePos3 = ftell(Frain.file);
            fseek(Frain.file, filePos1, SEEK_SET);
            sstrncpy(staID, Gage[i].staID, MAXMSG);
            interval = Interval;
            fwrite(staID,      sizeof(char), MAXMSG+1, Frain.file);
            fwrite(&interval,  sizeof(int), 1, Frain.file);
            fwrite(&filePos2,  sizeof(int), 1, Frain.file);
            fwrite(&filePos3,  sizeof(int), 1, Frain.file);
            filePos1 = ftell(Frain.file);
            filePos2 = filePos3;
            report_writeRainStats(i, &RainStats);
        }
    }

    // --- if there was an error condition, then delete newly created file
    if ( ErrorCode )
    {
        fclose(Frain.file);
        Frain.file = NULL;
        remove(Frain.name);
    }
}

//=============================================================================

////  New function added to release 5.0.019  ////                              //(5.0.019 - LR)

int rainFileConflict(int i)
//
//  Input:   i = rain gage index
//  Output:  returns 1 if file conflict found, 0 if not
//  Purpose: checks if a rain gage's station ID matches another gage's
//           station ID but the two use different rain data files.
//
{
    int j;
    char* staID = Gage[i].staID;
    char* fname = Gage[i].fname;
    for (j = 1; j < i; j++)
    {
        if ( strcomp(Gage[j].staID, staID) && !strcomp(Gage[j].fname, fname) )
        {
            report_writeErrorMsg(ERR_RAIN_FILE_CONFLICT, Gage[i].ID);
            return 1;
        }
    }
    return 0;
}

//=============================================================================

int addGageToRainFile(int i)
//
//  Input:   i = rain gage index
//  Output:  returns 1 if successful, 0 if not
//  Purpose: adds a gage's rainfall record to rain interface file
//
{
    FILE* f;                           // pointer to rain file
    int   fileFormat;                  // file format code
    int   hdrLines;                    // number of header lines skipped

    // --- let StationID point to NULL
    StationID = NULL;

    // --- check that rain file exists
    if ( (f = fopen(Gage[i].fname, "rt")) == NULL )
        report_writeErrorMsg(ERR_RAIN_FILE_DATA, Gage[i].fname);
    else
    {
        fileFormat = findFileFormat(f, i, &hdrLines);
        if ( fileFormat == UNKNOWN_FORMAT )
        {
            report_writeErrorMsg(ERR_RAIN_FILE_FORMAT, Gage[i].fname);
        }
        else
        {
            GageIndex = i;                                                     //(5.0.022 - LR)
            readFile(f, fileFormat, hdrLines, Gage[i].startFileDate,
                     Gage[i].endFileDate);
        }
        fclose(f);
    }
    if ( ErrorCode ) return 0;
    else
    return 1;
}

//=============================================================================

void initRainFile(void)
//
//  Input:   none
//  Output:  none
//  Purpose: initializes rain interface file for reading.
//
{
    char  fileStamp[] = "SWMM5-RAIN";
    char  fStamp[] = "SWMM5-RAIN";
    int   i;
    int   kount;
    long  filePos;

    // --- make sure interface file is open and no error condition
    if ( ErrorCode || !Frain.file ) return;

    // --- check that interface file contains proper file stamp
    rewind(Frain.file);
    fread(fStamp, sizeof(char), strlen(fileStamp), Frain.file);
    if ( strcmp(fStamp, fileStamp) != 0 )
    {
        report_writeErrorMsg(ERR_RAIN_FILE_FORMAT, "");
        return;
    }
    fread(&kount, sizeof(int), 1, Frain.file);
    filePos = ftell(Frain.file);

    // --- locate information for each raingage in interface file
    for ( i = 0; i < Nobjects[GAGE]; i++ )
    {
        if ( ErrorCode || Gage[i].dataSource != RAIN_FILE ) continue;

        // --- match station ID for gage with one in file
        fseek(Frain.file, filePos, SEEK_SET);
        if ( !findGageInFile(i, (int)kount) ||                                 //(5.0.019 - LR)
             Gage[i].startFilePos == Gage[i].endFilePos )                      //(5.0.019 - LR)
        {
            report_writeErrorMsg(ERR_RAIN_FILE_GAGE, Gage[i].ID);
            //return;                                                          //(5.0.019 - LR)
        }
    }
}

//=============================================================================

int findGageInFile(int i, int kount)
//
//  Input:   i     = rain gage index
//           kount = number of rain gages stored on interface file
//  Output:  returns TRUE if successful, FALSE if not
//  Purpose: checks if rain gage's station ID appears in interface file.
//
{
    int   k;
    int  interval;
    int  filePos1, filePos2;
    char  staID[MAXMSG+1];

    for ( k = 1; k <= kount; k++ )
    {
        fread(staID,      sizeof(char), MAXMSG+1, Frain.file);
        fread(&interval,  sizeof(int), 1, Frain.file);
        fread(&filePos1,  sizeof(int), 1, Frain.file);
        fread(&filePos2,  sizeof(int), 1, Frain.file);
        if ( strcmp(staID, Gage[i].staID) == 0 )
        {
            // --- match found; save file parameters
            Gage[i].rainType     = RAINFALL_VOLUME;
            Gage[i].rainInterval = interval;
            Gage[i].startFilePos = (long)filePos1;
            Gage[i].endFilePos   = (long)filePos2;
            Gage[i].currentFilePos = Gage[i].startFilePos;
            return TRUE;
        }
    }
    return FALSE;
}

//=============================================================================

int findFileFormat(FILE *f, int i, int *hdrLines)
//
//  Input:   f = ptr. to rain gage's rainfall data file
//           i = rain gage index
//  Output:  hdrLines  = number of header lines found in data file;
//           returns type of format used in a rainfall data file
//  Purpose: finds the format of a gage's rainfall data file.
//
{
    int   fileFormat;
    int   lineCount;
    int   maxCount = 5;
    int   n;
    int   div;
    long  sn2;
    char  recdType[4];
    char  elemType[5];                                                         //(5.0.010 - RD)
    char  line[MAXLINE];
    int   year, month, day, hour, minute;
    int   elem;
    float x;
    
    // --- check first few lines for known formats
    fileFormat = UNKNOWN_FORMAT;
    hasStationName = FALSE;                                                    //(5.0.015 - LR)
    UnitsFactor = 1.0;
    Interval = 0;
    *hdrLines = 0;
    for (lineCount = 1; lineCount <= maxCount; lineCount++)
    {
        if ( fgets(line, MAXLINE, f) == NULL ) return fileFormat;

        // --- check for NWS space delimited format
        n = sscanf(line, "%6d %2d %4s", &sn2, &div, elemType);
        if ( n == 3 )
        {
            Interval = getNWSInterval(elemType);
            TimeOffset = Interval;
            if ( Interval > 0 )
            {
                fileFormat = NWS_SPACE_DELIMITED;
                break;
            }
        }

////  Added for release 5.0.015  ////                                          //(5.0.015 - LR)
        // --- check for NWS space delimited format w/ station name
        n = sscanf(&line[37], "%2d %4s %2s %4d", &div, elemType, recdType, &year);
        if ( n == 4 )
        {
            Interval = getNWSInterval(elemType);
            TimeOffset = Interval;
            if ( Interval > 0 )
            {
                fileFormat = NWS_SPACE_DELIMITED;
                hasStationName = TRUE;
                break;
            }
        }

        // --- check for NWS coma delimited format
        n = sscanf(line, "%6d,%2d,%4s", &sn2, &div, elemType);
        if ( n == 3 )
        {
            Interval = getNWSInterval(elemType);
            TimeOffset = Interval;
            if ( Interval > 0 )
            {
                fileFormat = NWS_COMMA_DELIMITED;
                break;
            }
        }

////  Added for release 5.0.016  ////                                          //(5.0.016 - LR)
        // --- check for NWS comma delimited format w/ station name
        n = sscanf(&line[37], "%2d,%4s,%2s,%4d", &div, elemType, recdType, &year);
        if ( n == 4 )
        {
            Interval = getNWSInterval(elemType);
            TimeOffset = Interval;
            if ( Interval > 0 )
            {
                fileFormat = NWS_COMMA_DELIMITED;
                hasStationName = TRUE;
                break;
            }
        }

        // --- check for NWS TAPE format
        n = sscanf(line, "%3s%6d%2d%4s", recdType, &sn2, &div, elemType);
        if ( n == 4 )
        {
            Interval = getNWSInterval(elemType);
            TimeOffset = Interval;
            if ( Interval > 0 )
            {
                fileFormat = NWS_TAPE;
                break;
            }
        }

        // --- check for AES type
        n = sscanf(line, "%7d%3d%2d%2d%3d", &sn2, &year, &month, &day, &elem);
        if ( n == 5 )
        {
            if ( elem == 123 && strlen(line) >= 185 )
            {
                fileFormat = AES_HLY;
                Interval = 3600;
                TimeOffset = Interval;
                UnitsFactor = 1.0/MMperINCH;
                break;
            }
        }

        // --- check for CMC types
        n = sscanf(line, "%7d%4d%2d%2d%3d", &sn2, &year, &month, &day, &elem);
        if ( n == 5 )
        {
            if ( elem == 159 && strlen(line) >= 691 )
            {
                fileFormat = CMC_FIF;
                Interval = 900;
            }
            else if ( elem == 123 && strlen(line) >= 186 )
            {
                fileFormat = CMC_HLY;
                Interval = 3600;
            }
            if ( fileFormat == CMC_FIF || fileFormat == CMC_HLY )
            {
                TimeOffset = Interval;
                UnitsFactor = 1.0/MMperINCH;
                break;
            }
        }

        // --- check for standard format
        if ( parseStdLine(line, &year, &month, &day, &hour, &minute, &x) )
        {
            fileFormat = STD_SPACE_DELIMITED;
            RainType = Gage[i].rainType;
            Interval = Gage[i].rainInterval;
            if ( Gage[i].rainUnits == SI ) UnitsFactor = 1.0/MMperINCH;
            TimeOffset = 0;
            StationID = Gage[i].staID;
            break;         
        }
        (*hdrLines)++;

    }
    if ( fileFormat != UNKNOWN_FORMAT ) Gage[i].rainInterval = Interval;
    return fileFormat;
}

//=============================================================================

int getNWSInterval(char *elemType)
//
//  Input:   elemType = code from NWS rainfall file
//  Output:  returns rainfall recording interval (sec)
//  Purpose: decodes NWS rain gage recording interval value
//
{
    if      ( strcmp(elemType, "HPCP") == 0 ) return 3600; // 1 hr rainfall
    else if ( strcmp(elemType, "QPCP") == 0 ) return 900;  // 15 min rainfall
    else if ( strcmp(elemType, "QGAG") == 0 ) return 900;  // 15 min rainfall
    else return 0;
} 

//=============================================================================

void readFile(FILE *f, int fileFormat, int hdrLines, DateTime day1,
              DateTime day2)
//
//  Input:   f          = ptr. to gage's rainfall data file
//           fileFormat = code of data file's format
//           hdrLines   = number of header lines in data file
//           day1       = starting day of record of interest
//           day2       = ending day of record of interest
//  Output:  none
//  Purpose: reads rainfall records from gage's data file to interface file.
//
{
    char line[MAXLINE];
    int  i, n;

    rewind(f);
    RainStats.startDate  = NO_DATE;
    RainStats.endDate    = NO_DATE;
    RainStats.periodsRain = 0;
    RainStats.periodsMissing = 0;
    RainStats.periodsMalfunc = 0;
    RainAccum = 0.0;
    AccumStartDate = NO_DATE;                                                  //(5.0.010 - LR)
    PreviousDate = NO_DATE;                                                    //(5.0.022 - LR)

    for (i = 1; i <= hdrLines; i++)
    {
        if ( fgets(line, MAXLINE, f) == NULL ) return;
    }
    while ( fgets(line, MAXLINE, f) != NULL )
    {
       switch (fileFormat)
       {
         case STD_SPACE_DELIMITED:
          n = readStdLine(line, day1, day2);
          break;

         case NWS_TAPE:
         case NWS_SPACE_DELIMITED:
         case NWS_COMMA_DELIMITED:
           n = readNWSLine(line, fileFormat, day1, day2);
           break;

         case AES_HLY:
         case CMC_FIF:
         case CMC_HLY:
           n = readCMCLine(line, fileFormat, day1, day2);
           break;

         default:
           n = -1;
           break;
       }
       if ( n < 0 ) break;
    }
}

//=============================================================================

int readNWSLine(char *line, int fileFormat, DateTime day1, DateTime day2)
//
//  Input:   line       = line of data from rainfall data file
//           fileFormat = code of data file's format
//           day1       = starting day of record of interest
//           day2       = ending day of record of interest
//  Output:  returns -1 if past end of desired record, 0 if data line could
//           not be read successfully or 1 if line read successfully
//  Purpose: reads a line of data from a rainfall data file and writes its
//           data to the rain interface file.
//
{
    char     flag1, flag2, isMissing;
    DateTime date1;
    long     result = 1;
    int      k, y, m, d, n;
    int      hour, minute;
    long     v;
    float    x;
    int      lineLength = strlen(line)-1;
    int      nameLength = 0;                                                   //(5.0.015 - LR)

    // --- get year, month, & day from line
    switch ( fileFormat )
    {
      case NWS_TAPE:
        if ( lineLength <= 30 ) return 0;
        if (sscanf(&line[17], "%4d%2d%4d%3d", &y, &m, &d, &n) < 4) return 0;
        k = 30;
        break;

      case NWS_SPACE_DELIMITED:
        if ( hasStationName ) nameLength = 31;                                 //(5.0.015 - LR)
        if ( lineLength <= 28 + nameLength ) return 0;                         //(5.0.015 - LR)
        k = 18 + nameLength;                                                   //(5.0.015 - LR)
        if (sscanf(&line[k], "%4d %2d %2d", &y, &m, &d) < 3) return 0;         //(5.0.015 - LR)
        k = k + 10;                                                            //(5.0.015 - LR)
        break;

      case NWS_COMMA_DELIMITED:
        if ( lineLength <= 28 ) return 0;
        if ( sscanf(&line[18], "%4d,%2d,%2d", &y, &m, &d) < 3 ) return 0;
        k = 28;
        break;

      default: return 0;
    }

    // --- see if date is within period of record requested
    date1 = datetime_encodeDate(y, m, d);
    if ( day1 != NO_DATE && date1 < day1 ) return 0;
    if ( day2 != NO_DATE && date1 > day2 ) return -1;

    // --- read each recorded rainfall time, value, & codes from line
    while ( k < lineLength )
    {
		flag1 = 0;
        flag2 = 0;                                                             //(5.0.016 - LR)
		v = 99999;
		hour = 25;
		minute = 0;
        switch ( fileFormat )
        {
          case NWS_TAPE:
            n = sscanf(&line[k], "%2d%2d%6d%c%c",
                       &hour, &minute, &v, &flag1, &flag2);
            k += 12;
            break;

          case NWS_SPACE_DELIMITED:
            n = sscanf(&line[k], " %2d%2d %6d %c %c",
                       &hour, &minute, &v, &flag1, &flag2);
            k += 16;
            break;

          case NWS_COMMA_DELIMITED:
            n = sscanf(&line[k], ",%2d%2d,%6d,%c,%c",
                       &hour, &minute, &v, &flag1, &flag2);
            k += 16;
            break;

		  default: n = 0;
        }

        // --- check that we at least have an hour, minute & value             //(5.0.016 - LR)
        //     (codes might be left off of the line)                           //(5.0.016 - LR)
        if ( n < 3 || hour >= 25 ) break;                                      //(5.0.016 - LR)

        // --- set special condition code & update daily & hourly counts

        setCondition(flag1);
        if ( Condition == DELETED_PERIOD ||                                    //(5.0.011 - LR)
             Condition == MISSING_PERIOD ||                                    //(5.0.011 - LR)
             flag1 == 'M' ) isMissing = TRUE;                                  //(5.0.011 - LR)
        else if ( v == 99999 ) isMissing = TRUE;
        else isMissing = FALSE;

        // --- handle accumulation codes                                       //(5.0.010 - LR)
        if ( flag1 == 'a' )                                                    //(5.0.010 - LR)
        {                                                                      //(5.0.010 - LR)
            AccumStartDate = date1 + datetime_encodeTime(hour, minute, 0);     //(5.0.010 - LR)
        }                                                                      //(5.0.010 - LR)
        else if ( flag1 == 'A' )                                               //(5.0.010 - LR)
        {                                                                      //(5.0.010 - LR)
            saveAccumRainfall(date1, hour, minute, v);                         //(5.0.010 - LR)
        }                                                                      //(5.0.010 - LR)

        // --- handle all other conditions                                     //(5.0.010 - LR)
        else                                                                   //(5.0.010 - LR)
        {                                                                      //(5.0.010 - LR)
            // --- convert rain measurement to inches & save it                //(5.0.010 - LR)
            x = (float)v / 100.0f; 
            if ( x > 0 || isMissing )                                          //(5.0.011 - LR)
                saveRainfall(date1, hour, minute, x, isMissing);               //(5.0.011 - LR)
        }                                                                      //(5.0.010 - LR)

        // --- reset condition code if special condition period ended
        if ( flag1 == 'A' || flag1 == '}' || flag1 == ']') Condition = 0;
    }
    return result;
}

//=============================================================================

void  setCondition(char flag)
{
    switch ( flag )
    {
      case 'a': 
      case 'A':
        Condition = ACCUMULATED_PERIOD;
        break;
      case '{':
      case '}':
        Condition = DELETED_PERIOD;
        break;
      case '[':
      case ']':
        Condition = MISSING_PERIOD;
        break;
      default:
        Condition = NO_CONDITION;
    }
}

//=============================================================================

int readCMCLine(char *line, int fileFormat, DateTime day1, DateTime day2)
//
//  Input:   line = line of data from rainfall data file
//           fileFormat = code of data file's format
//           day1 = starting day of record of interest
//           day2 = ending day of record of interest
//  Output:  returns -1 if past end of desired record, 0 if data line could
//           not be read successfully or 1 if line read successfully
//  Purpose: reads a line of data from an AES or CMC rainfall data file and
//           writes its data to the rain interface file.
//
{
    char     flag, isMissing;
    DateTime date1;
    long     sn, v;
    int      col, j, jMax, elem, y, m, d, hour, minute;
    float    x;

    // --- get year, month, day & element code from line
    if ( fileFormat == AES_HLY )
    {
        if ( sscanf(line, "%7d%3d%2d%2d%3d", &sn, &y, &m, &d, &elem) < 5 )
            return 0;
        if ( y < 100 ) y = y + 2000;
        else           y = y + 1000;
        col = 17;
    }
    else
    {
        if ( sscanf(line, "%7d%4d%2d%2d%3d", &sn, &y, &m, &d, &elem) < 5 )
            return 0;
        col = 18;
    }

    // --- see if date is within period of record requested
    date1 = datetime_encodeDate(y, m, d);
    if ( day1 != NO_DATE && date1 < day1 ) return 0;
    if ( day2 != NO_DATE && date1 > day2 ) return -1;

    // --- make sure element code is for rainfall
    if ( fileFormat == AES_HLY && elem != 123 ) return 0;
    else if ( fileFormat == CMC_FIF && elem != 159 ) return 0;
    else if ( fileFormat == CMC_HLY && elem != 123 ) return 0;

    // --- read rainfall from each recording interval
    hour = 0;                          // starting hour
    minute = 0;                        // starting minute
    jMax = 24;                         // # recording intervals
    if ( fileFormat == CMC_FIF ) jMax = 96;
    for (j=1; j<=jMax; j++)
    {
        if ( sscanf(&line[col], "%6d%c", &v, &flag) < 2 ) return 0;
        col += 7;
        if ( v == -99999 ) isMissing = TRUE;
        else               isMissing = FALSE;

        // --- convert rain measurement from 0.1 mm to inches and save it
        x = (float)( (double)v / 10.0 / MMperINCH);
        if ( x > 0 || isMissing)
        {
            saveRainfall(date1, hour, minute, x, isMissing);
        }

        // --- update hour & minute for next interval
        if ( fileFormat == CMC_FIF )
        {
            minute += 15;
            if ( minute == 60 )
            {
                minute = 0;
                hour++;
            }
        }
        else hour++;
    }
    return 1;
}

//=============================================================================

int readStdLine(char *line, DateTime day1, DateTime day2)
//
//  Input:   line = line of data from a standard rainfall data file
//           day1 = starting day of record of interest
//           day2 = ending day of record of interest
//  Output:  returns -1 if past end of desired record, 0 if data line could
//           not be read successfully or 1 if line read successfully
//  Purpose: reads a line of data from a standard rainfall data file and
//           writes its data to the rain interface file.
//
{
    DateTime date1;
    DateTime date2;                                                            //(5.0.022 - LR)
    int      year, month, day, hour, minute;
    float    x;

    // --- parse data from input line
    if (!parseStdLine(line, &year, &month, &day, &hour, &minute, &x)) return 0;

    // --- see if date is within period of record requested
    date1 = datetime_encodeDate(year, month, day);
    if ( day1 != NO_DATE && date1 < day1 ) return 0;
    if ( day2 != NO_DATE && date1 > day2 ) return -1;

// Added for release 5.0.022  //////////////                                   //(5.0.022 - LR)
    // --- see if record is out of sequence
    date2 = date1 + datetime_encodeTime(hour, minute, 0);
    if ( date2 <= PreviousDate )
    {
        report_writeLine(
            "ERROR 318: the following line is out of sequence in rainfall file ");
        report_writeLine(Gage[GageIndex].fname);
        report_writeLine(line);
        ErrorCode = ERR_RAIN_FILE_SEQUENCE;
        return -1;
    }
    PreviousDate = date2;
////////////////////////////////////////////

    switch (RainType)
    {
      case RAINFALL_INTENSITY:
        x = x * Interval / 3600.0f;
        break;

      case CUMULATIVE_RAINFALL:
        if ( x >= RainAccum )
        {
            x = x - RainAccum;
            RainAccum += x;
        }
        else RainAccum = x;
        break;
    }
    x *= (float)UnitsFactor;

    // --- save rainfall to binary interface file
    saveRainfall(date1, hour, minute, x, FALSE);
    return 1;
}

//=============================================================================

////  This function was re-written for release 5.0.022  ////                   //(5.0.022 - LR)

int parseStdLine(char *line, int *year, int *month, int *day, int *hour,
                 int *minute, float *value)
//
//  Input:   line = line of data from a standard rainfall data file
//  Output:  *year = year when rainfall occurs
//           *month = month of year when rainfall occurs
//           *day = day of month when rainfall occurs
//           *hour = hour of day when rainfall occurs
//           *minute = minute of hour when rainfall occurs
//           *value = rainfall value (user units);
//           returns 0 if data line could not be parsed successfully or
//           1 if line parsed successfully
//  Purpose: parses a line of data from a standard rainfall data file.
//
{
    int n;
    char token[256];

    n = sscanf(line, "%s%d%d%d%d%d%f", token, year, month, day, hour, minute, value);
    if ( n < 7 ) return 0;
    if ( StationID != NULL && !strcomp(token, StationID) ) return 0;
    return 1;
}

//=============================================================================

void saveAccumRainfall(DateTime date1, int hour, int minute, long v)
//
//  Input:   date1 = date of latest rainfall reading (in DateTime format)
//           hour = hour of day of latest rain reading
//           minute = minute of hour of latest rain reading
//           v = accumulated rainfall reading in hundreths of inches
//  Output:  none
//  Purpose: divides accumulated rainfall evenly into individual recording
//           periods over the accumulation period and writes each period's
//           rainfall to the binary rainfall file.
//
//  This function was added to Release 5.0.010.                                //(5.0.010 - LR)
//
{
    DateTime date2;
    int      n, j;
    float    x;

    // --- return if accumulated start date is missing                         //(5.0.022 - LR)
    if ( AccumStartDate == NO_DATE ) return;
    //if ( v == -99999 ) return;                                               //(5.0.022 - LR)

    // --- find number of recording intervals over accumulation period
    date2 = date1 + datetime_encodeTime(hour, minute, 0);
    n = (datetime_timeDiff(date2, AccumStartDate) / Interval) + 1;

    // --- update count of rain or missing periods                             //(5.0.022 - LR)
    if ( v == 99999 )                                                          //(5.0.022 - LR)
    {                                                                          //(5.0.022 - LR)
        RainStats.periodsMissing += n;                                         //(5.0.022 - LR)
        return;                                                                //(5.0.022 - LR)
    }                                                                          //(5.0.022 - LR)
    RainStats.periodsRain += n;                                                //(5.0.022 - LR)

    // --- divide accumulated amount evenly into each period
    x = (float)v / (float)n / 100.0f;

    // --- save this amount to file for each period
    if ( x > 0.0f )
    {
        date2 = datetime_addSeconds(AccumStartDate, -TimeOffset);
        if ( RainStats.startDate == NO_DATE ) RainStats.startDate = date2;
        for (j = 0; j < n; j++)
        {
            fwrite(&date2, sizeof(DateTime), 1, Frain.file);
            fwrite(&x, sizeof(float), 1, Frain.file);
            date2 = datetime_addSeconds(date2, Interval);
            RainStats.endDate = date2;
        }
    }

    // --- reset start of accumulation period
    AccumStartDate = NO_DATE;
}


//=============================================================================

void saveRainfall(DateTime date1, int hour, int minute, float x, char isMissing)
//
//  Input:   date1 = date of rainfall reading (in DateTime format)
//           hour = hour of day of current rain reading
//           minute = minute of hour of current rain reading
//           x = rainfall reading in inches
//           isMissing = TRUE if rainfall value is missing
//  Output:  none
//  Purpose: writes current rainfall reading from an external rainfall file
//           to project's binary rainfall file.
//
{
    DateTime date2;
    double   seconds;

    if ( isMissing ) RainStats.periodsMissing++;
    else             RainStats.periodsRain++;

    // --- if rainfall not missing then save it to rainfall interface file
    if ( !isMissing )
    {
        seconds = 3600*hour + 60*minute - TimeOffset;
        date2 = datetime_addSeconds(date1, seconds);

        // --- write date & value (in inches) to interface file
        fwrite(&date2, sizeof(DateTime), 1, Frain.file);
        fwrite(&x, sizeof(float), 1, Frain.file);

        // --- update actual start & end of record dates
        if ( RainStats.startDate == NO_DATE ) RainStats.startDate = date2;
        RainStats.endDate = date2;
    }
}
//=============================================================================
