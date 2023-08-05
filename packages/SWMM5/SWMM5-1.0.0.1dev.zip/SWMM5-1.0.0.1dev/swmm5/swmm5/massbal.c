//-----------------------------------------------------------------------------
//   massbal.c
//
//   Project:  EPA SWMM5
//   Version:  5.0
//   Date:     6/19/07   (Build 5.0.010)
//             2/4/08    (Build 5.0.012)
//             4/10/09   (Build 5.0.015)
//             10/7/09   (Build 5.0.017)
//             11/18/09  (Build 5.0.018)
//             07/30/10  (Build 5.0.019)
//   Author:   L. Rossman
//
//   Mass balance functions
//-----------------------------------------------------------------------------
#define _CRT_SECURE_NO_DEPRECATE

#include <stdlib.h>
#include <math.h>
#include "headers.h"

//-----------------------------------------------------------------------------
//  Constants   
//-----------------------------------------------------------------------------
static const double MAX_RUNOFF_BALANCE_ERR = 10.0;
static const double MAX_FLOW_BALANCE_ERR   = 10.0;

//-----------------------------------------------------------------------------
//  Shared variables   
//-----------------------------------------------------------------------------
TRunoffTotals    RunoffTotals;    // overall surface runoff continuity totals
TLoadingTotals*  LoadingTotals;   // overall WQ washoff continuity totals
TGwaterTotals    GwaterTotals;    // overall groundwater continuity totals 
TRoutingTotals   FlowTotals;      // overall routed flow continuity totals 
TRoutingTotals*  QualTotals;      // overall routed WQ continuity totals 
TRoutingTotals   StepFlowTotals;  // routed flow totals over time step
TRoutingTotals   OldStepFlowTotals;
TRoutingTotals*  StepQualTotals;  // routed WQ totals over time step

//-----------------------------------------------------------------------------
//  Exportable variables
//-----------------------------------------------------------------------------
double*  NodeInflow;              // total inflow volume to each node (ft3)
double*  NodeOutflow;             // total outflow volume from each node (ft3)
double   TotalArea;               // total drainage area (ft2)

//-----------------------------------------------------------------------------
//  External functions (declared in funcs.h)
//-----------------------------------------------------------------------------
//  massbal_open                (called from swmm_start in swmm5.c)
//  massbal_close               (called from swmm_end in swmm5.c)
//  massbal_report              (called from swmm_end in swmm5.c)
//  massbal_updateRunoffTotals  (called from subcatch_getRunoff)
//  massbal_updateLoadingTotals (called from subcatch_getBuildup)              //(5.0.019 - LR)
//  massbal_updateGwaterTotals  (called from updateMassBal in gwater.c)
//  massbal_updateRoutingTotals (called from routing_execute)
//  massbal_initTimeStepTotals  (called from routing_execute)
//  massbal_addInflowFlow       (called from routing.c)
//  massbal_addInflowQual       (called from routing.c)
//  massbal_addOutflowFlow      (called from removeOutflows in routing.c)
//  massbal_addOutflowQual      (called from removeOutflows in routing.c)
//  massbal_addNodeLosses       (called from findEvap in routing.c)            //(5.0.015 - LR)
//  massbal_addReactedMass      (called from qualrout.c & treatmnt.c)
//  massbal_getStepFlowError    (called from routing.c)                        //(5.0.012 - LR)

//-----------------------------------------------------------------------------
//  Local Functions   
//-----------------------------------------------------------------------------
double massbal_getBuildup(int pollut);
double massbal_getStorage(char isFinalStorage);
double massbal_getStoredMass(int pollut);                                      //(5.0.019 - LR)
double massbal_getRunoffError(void);
double massbal_getLoadingError(void);
double massbal_getGwaterError(void);
double massbal_getFlowError(void);
double massbal_getQualError(void);


//=============================================================================

int massbal_open()
//
//  Input:   none
//  Output:  returns error code
//  Purpose: opens and initializes mass balance continuity checking.
//
{
    int j, n;

    // --- initialize global continuity errors
    RunoffError = 0.0;
    GwaterError = 0.0;
    FlowError   = 0.0;
    QualError   = 0.0;

    // --- initialize runoff totals
    RunoffTotals.rainfall    = 0.0;
    RunoffTotals.evap        = 0.0;
    RunoffTotals.infil       = 0.0;
    RunoffTotals.runoff      = 0.0;
    RunoffTotals.snowRemoved = 0.0;
    RunoffTotals.initStorage = 0.0;
    RunoffTotals.initSnowCover = 0.0;
    TotalArea = 0.0;
    for (j = 0; j < Nobjects[SUBCATCH]; j++)
    {
        RunoffTotals.initStorage += subcatch_getStorage(j);                    //(5.0.019 - LR)
        RunoffTotals.initSnowCover += snow_getSnowCover(j);
        TotalArea += Subcatch[j].area;
    }

    // --- initialize groundwater totals
    GwaterTotals.infil        = 0.0;
    GwaterTotals.upperEvap    = 0.0;
    GwaterTotals.lowerEvap    = 0.0;
    GwaterTotals.lowerPerc    = 0.0;
    GwaterTotals.gwater       = 0.0;
    GwaterTotals.initStorage  = 0.0;
    GwaterTotals.finalStorage = 0.0;
    for ( j = 0; j < Nobjects[SUBCATCH]; j++ )
    {
        GwaterTotals.initStorage += gwater_getVolume(j) * Subcatch[j].area;
    }

    // --- initialize node flow & storage totals
    FlowTotals.dwInflow = 0.0;
    FlowTotals.wwInflow = 0.0;
    FlowTotals.gwInflow = 0.0;
    FlowTotals.iiInflow = 0.0;
    FlowTotals.exInflow = 0.0;
    FlowTotals.flooding = 0.0;
    FlowTotals.outflow  = 0.0;
    FlowTotals.reacted  = 0.0;
    FlowTotals.initStorage = 0.0;
    for (j = 0; j < Nobjects[NODE]; j++)
        FlowTotals.initStorage += Node[j].newVolume;
    for (j = 0; j < Nobjects[LINK]; j++)
        FlowTotals.initStorage += Link[j].newVolume;
    StepFlowTotals = FlowTotals;

    // --- initialize arrays to null
    LoadingTotals = NULL;
    QualTotals = NULL;
    StepQualTotals = NULL;
    NodeInflow = NULL;
    NodeOutflow = NULL;

    // --- allocate memory for WQ washoff continuity totals
    n = Nobjects[POLLUT];
    if ( n > 0 )
    {
        LoadingTotals = (TLoadingTotals *) calloc(n, sizeof(TLoadingTotals));
        if ( LoadingTotals == NULL )
        {
             report_writeErrorMsg(ERR_MEMORY, "");
             return ErrorCode;
        }
        for (j = 0; j < n; j++)
        {
            LoadingTotals[j].initLoad      = massbal_getBuildup(j);
            LoadingTotals[j].buildup       = 0.0;
            LoadingTotals[j].deposition    = 0.0;
            LoadingTotals[j].sweeping      = 0.0;
            LoadingTotals[j].infil         = 0.0;
            LoadingTotals[j].bmpRemoval    = 0.0;
            LoadingTotals[j].runoff        = 0.0;
            LoadingTotals[j].finalLoad     = 0.0;
        }
    }

    // --- allocate memory for nodal WQ continuity totals
    if ( n > 0 )
    {
         QualTotals = (TRoutingTotals *) calloc(n, sizeof(TRoutingTotals));
         StepQualTotals = (TRoutingTotals *) calloc(n, sizeof(TRoutingTotals));
         if ( QualTotals == NULL || StepQualTotals == NULL )
         {
             report_writeErrorMsg(ERR_MEMORY, "");
             return ErrorCode;
         }
     }

    // --- initialize WQ totals
    for (j = 0; j < n; j++)
    {
        QualTotals[j].dwInflow = 0.0;
        QualTotals[j].wwInflow = 0.0;
        QualTotals[j].gwInflow = 0.0;
        QualTotals[j].exInflow = 0.0;
        QualTotals[j].flooding = 0.0;
        QualTotals[j].outflow  = 0.0;
        QualTotals[j].reacted  = 0.0;
        QualTotals[j].initStorage = massbal_getStoredMass(j);                  //(5.0.019 - LR)
    }

    // --- initialize totals used over a single time step
    massbal_initTimeStepTotals();
 
    // --- allocate memory for nodal flow continuity
    if ( Nobjects[NODE] > 0 )
    {
        NodeInflow = (double *) calloc(Nobjects[NODE], sizeof(double));
        if ( NodeInflow == NULL )
        {
             report_writeErrorMsg(ERR_MEMORY, "");
             return ErrorCode;
        }
        NodeOutflow = (double *) calloc(Nobjects[NODE], sizeof(double));
        if ( NodeOutflow == NULL )
        {
             report_writeErrorMsg(ERR_MEMORY, "");
             return ErrorCode;
        }
        for (j = 0; j < Nobjects[NODE]; j++) NodeInflow[j] = Node[j].newVolume;
    }
    return ErrorCode;
}

//=============================================================================

void massbal_close()
//
//  Input:   none
//  Output:  none
//  Purpose: frees memory used by mass balance system.
//
{
    FREE(LoadingTotals);
    FREE(QualTotals);
    FREE(StepQualTotals);
    FREE(NodeInflow);
    FREE(NodeOutflow);
}

//=============================================================================

void massbal_report()
//
//  Input:   none
//  Output:  none
//  Purpose: reports mass balance results.
//
{
    int    j;
    double gwArea = 0.0;

    if ( Nobjects[SUBCATCH] > 0 )
    {
        if ( massbal_getRunoffError() > MAX_RUNOFF_BALANCE_ERR ||
             RptFlags.continuity == TRUE
           ) report_writeRunoffError(&RunoffTotals, TotalArea);

        if ( Nobjects[POLLUT] > 0 && !IgnoreQuality )                          //(5.0.018 - LR)
        {
            if ( massbal_getLoadingError() > MAX_RUNOFF_BALANCE_ERR ||
                 RptFlags.continuity == TRUE
               ) report_writeLoadingError(LoadingTotals);
        }
    }

    if ( Nobjects[AQUIFER] > 0  && !IgnoreGwater )                             //(5.0.018 - LR)
    {
        if ( massbal_getGwaterError() > MAX_RUNOFF_BALANCE_ERR ||
             RptFlags.continuity == TRUE )
        {
            for ( j = 0; j < Nobjects[SUBCATCH]; j++ )
            {
                if ( Subcatch[j].groundwater ) gwArea += Subcatch[j].area;
            }
            if ( gwArea > 0.0 ) report_writeGwaterError(&GwaterTotals, gwArea);
       }
    }

    if ( Nobjects[NODE] > 0 && !IgnoreRouting )                                //(5.0.018 - LR)
    {
        if ( massbal_getFlowError() > MAX_FLOW_BALANCE_ERR ||
             RptFlags.continuity == TRUE
           ) report_writeFlowError(&FlowTotals);
    
        if ( Nobjects[POLLUT] > 0 && !IgnoreQuality )                          //(5.0.018 - LR)
        {
            if ( massbal_getQualError() > MAX_FLOW_BALANCE_ERR ||
                 RptFlags.continuity == TRUE
               ) report_writeQualError(QualTotals);
        }
    }
}

//=============================================================================

double massbal_getBuildup(int p)
//
//  Input:   p = pollutant index
//  Output:  returns total pollutant buildup (lbs or kg)
//  Purpose: computes current total buildup of a pollutant over study area.
//
{
    int    i, j;
    double load = 0.0;
    for (j=0; j<Nobjects[SUBCATCH]; j++)
    {
        for (i = 0; i < Nobjects[LANDUSE]; i++)
        {
            load += Subcatch[j].landFactor[i].buildup[p];
        }
        load += Subcatch[j].pondedQual[p] * subcatch_getDepth(j) *
                    Subcatch[j].area * Pollut[p].mcf;
    }
    return load;
}

//=============================================================================

void massbal_updateRunoffTotals(double vRainfall, double vEvap, double vInfil,
                                double vRunoff)
//
//  Input:   vRain   = rainfall volume (ft3)
//           vEvap   = evaporation volume (ft3)
//           vInfil  = infiltration volume (ft3)
//           vRunoff = runoff volume (ft3)
//  Output:  none
//  Purpose: updates runoff totals after current time step.
//
{
    RunoffTotals.rainfall += vRainfall;
    RunoffTotals.evap     += vEvap;
    RunoffTotals.infil    += vInfil;
    RunoffTotals.runoff   += vRunoff;
}

//=============================================================================

void massbal_updateGwaterTotals(double vInfil, double vUpperEvap, double vLowerEvap,
                                double vLowerPerc, double vGwater)
//
//  Input:   vInfil = volume depth of infiltrated water (ft)
//           vUpperEvap = volume depth of upper evaporation (ft)
//           vLowerEvap = volume depth of lower evaporation (ft)
//           vLowerPerc = volume depth of percolation to deep GW (ft)
//           vGwater = volume depth of groundwater outflow (ft)
//  Output:  none
//  Purpose: updates groundwater totals after current time step.
//
{
    GwaterTotals.infil     += vInfil;
    GwaterTotals.upperEvap += vUpperEvap;
    GwaterTotals.lowerEvap += vLowerEvap;
    GwaterTotals.lowerPerc += vLowerPerc;
    GwaterTotals.gwater    += vGwater;
}

//=============================================================================

void massbal_initTimeStepTotals()
//
//  Input:   none
//  Output:  none
//  Purpose: initializes routing totals for current time step.
//
{
    int j;
    OldStepFlowTotals = StepFlowTotals;
    StepFlowTotals.dwInflow  = 0.0;
    StepFlowTotals.wwInflow  = 0.0;
    StepFlowTotals.gwInflow  = 0.0;
    StepFlowTotals.iiInflow  = 0.0;
    StepFlowTotals.exInflow  = 0.0;
    StepFlowTotals.flooding  = 0.0;
    StepFlowTotals.outflow   = 0.0;
    StepFlowTotals.reacted   = 0.0;
    for (j=0; j<Nobjects[POLLUT]; j++)
    {
        StepQualTotals[j].dwInflow  = 0.0;
        StepQualTotals[j].wwInflow  = 0.0;
        StepQualTotals[j].gwInflow  = 0.0;
        StepQualTotals[j].iiInflow  = 0.0;
        StepQualTotals[j].exInflow  = 0.0;
        StepQualTotals[j].flooding  = 0.0;
        StepQualTotals[j].outflow   = 0.0;
        StepQualTotals[j].reacted   = 0.0;
    }
}

//=============================================================================

void massbal_addInflowFlow(int type, double q)
//
//  Input:   type = type of inflow
//           q    = inflow rate (cfs)
//  Output:  none
//  Purpose: adds flow inflow to routing totals for current time step.
//
{
    switch (type)
    {
      case DRY_WEATHER_INFLOW: StepFlowTotals.dwInflow += q; break;
      case WET_WEATHER_INFLOW: StepFlowTotals.wwInflow += q; break;
      case GROUNDWATER_INFLOW: StepFlowTotals.gwInflow += q; break;
      case RDII_INFLOW:        StepFlowTotals.iiInflow += q; break;
      case EXTERNAL_INFLOW:    StepFlowTotals.exInflow += q; break;
    }
}

//=============================================================================

void massbal_updateLoadingTotals(int type, int p, double w)
//
//  Input:   type = type of inflow
//           p    = pollutant index
//           w    = mass loading
//  Output:  none
//  Purpose: adds inflow mass loading to loading totals for current time step.
//
{
    switch (type)
    {
      case BUILDUP_LOAD:     LoadingTotals[p].buildup    += w; break;
      case DEPOSITION_LOAD:  LoadingTotals[p].deposition += w; break;
      case SWEEPING_LOAD:    LoadingTotals[p].sweeping   += w; break;
      case INFIL_LOAD:       LoadingTotals[p].infil      += w; break;
      case BMP_REMOVAL_LOAD: LoadingTotals[p].bmpRemoval += w; break;
      case RUNOFF_LOAD:      LoadingTotals[p].runoff     += w; break;
    }
}

//=============================================================================

void massbal_addInflowQual(int type, int p, double w)
//
//  Input:   type = type of inflow
//           p    = pollutant index
//           w    = mass flow rate (mass/sec)
//  Output:  none
//  Purpose: adds quality inflow to routing totals for current time step.
//
{
    if ( p < 0 || p >= Nobjects[POLLUT] ) return;
    switch (type)
    {
      case DRY_WEATHER_INFLOW: StepQualTotals[p].dwInflow += w; break;
      case WET_WEATHER_INFLOW: StepQualTotals[p].wwInflow += w; break;
      case GROUNDWATER_INFLOW: StepQualTotals[p].gwInflow += w; break;
      case EXTERNAL_INFLOW:    StepQualTotals[p].exInflow += w; break;
      case RDII_INFLOW:        StepQualTotals[p].iiInflow += w; break;
   }
}

//=============================================================================

void massbal_addOutflowFlow(double q, int isFlooded)
//
//  Input:   q = outflow flow rate (cfs)
//           isFlooded = TRUE if outflow represents internal flooding
//  Output:  none
//  Purpose: adds flow outflow over current time step to routing totals.
//
{
    if ( q >= 0.0 )
    {
        if ( isFlooded ) StepFlowTotals.flooding += q;
        else             StepFlowTotals.outflow += q;
    }
    else StepFlowTotals.exInflow -= q;
}

//=============================================================================

void massbal_addOutflowQual(int p, double w, int isFlooded)
//
//  Input:   p = pollutant index
//           w = mass outflow rate (mass/sec)
//           isFlooded = TRUE if outflow represents internal flooding
//  Output:  none
//  Purpose: adds pollutant outflow over current time step to routing totals.
//
{
    if ( p < 0 || p >= Nobjects[POLLUT] ) return;
    if ( w >= 0.0 )
    {
        if ( isFlooded ) StepQualTotals[p].flooding += w;
        else             StepQualTotals[p].outflow += w;
    }
    else StepQualTotals[p].exInflow -= w;
}

//=============================================================================

void massbal_addReactedMass(int p, double w)
//
//  Input:   p = pollutant index
//           w = rate of mass reacted (mass/sec)
//  Output:  none
//  Purpose: adds mass reacted during current time step to routing totals.
//
{
    if ( p < 0 || p >= Nobjects[POLLUT] ) return;
    StepQualTotals[p].reacted += w;
}

//=============================================================================

void massbal_addNodeLosses(double losses)                                      //(5.0.015 - LR)
//
//  Input:   losses = evaporation + infiltration loss from all nodes (ft3)     //(5.0.015 - LR)
//  Output:  none
//  Purpose: adds node losses over current time step to routing totals.
//
{
    StepFlowTotals.reacted += losses;                                          //(5.0.015 - LR)
    FlowTotals.reacted += losses;                                              //(5.0.015 - LR)
}

//=============================================================================

void massbal_updateRoutingTotals(double tStep)
//
//  Input:   tStep = time step (sec)
//  Output:  none
//  Purpose: updates overall routing totals with totals from current time step.
//
{
    int j;
    FlowTotals.dwInflow += StepFlowTotals.dwInflow * tStep;
    FlowTotals.wwInflow += StepFlowTotals.wwInflow * tStep;
    FlowTotals.gwInflow += StepFlowTotals.gwInflow * tStep;
    FlowTotals.iiInflow += StepFlowTotals.iiInflow * tStep;
    FlowTotals.exInflow += StepFlowTotals.exInflow * tStep;
    FlowTotals.flooding += StepFlowTotals.flooding * tStep;
    FlowTotals.outflow  += StepFlowTotals.outflow * tStep;
    for (j = 0; j < Nobjects[POLLUT]; j++)
    {
        QualTotals[j].dwInflow += StepQualTotals[j].dwInflow * tStep;
        QualTotals[j].wwInflow += StepQualTotals[j].wwInflow * tStep;
        QualTotals[j].gwInflow += StepQualTotals[j].gwInflow * tStep;
        QualTotals[j].iiInflow += StepQualTotals[j].iiInflow * tStep;
        QualTotals[j].exInflow += StepQualTotals[j].exInflow * tStep;
        QualTotals[j].flooding += StepQualTotals[j].flooding * tStep;
        QualTotals[j].outflow  += StepQualTotals[j].outflow * tStep;
        QualTotals[j].reacted  += StepQualTotals[j].reacted * tStep;
    }

    for ( j=0; j<Nobjects[NODE]; j++)
    {
        NodeInflow[j] += Node[j].inflow * tStep;
        if ( Node[j].type == OUTFALL || Node[j].degree == 0 )
        {
            NodeOutflow[j] += Node[j].inflow * tStep;
        }
        else
        {
            NodeOutflow[j] += Node[j].outflow * tStep;                         //(5.0.012 - LR)
            if ( Node[j].newVolume <= Node[j].fullVolume )                     //(5.0.012 - LR)
                NodeOutflow[j] += Node[j].overflow * tStep;                    //(5.0.012 - LR)
        }
    }
}

//=============================================================================

double massbal_getStorage(char isFinalStorage)
//
//  Input:   isFinalStorage = TRUE if at final time period
//  Output:  returns storage volume used (ft3)
//  Purpose: computes total system storage (nodes + links) filled
//
{
    int    j;
    double totalStorage = 0.0;
    double nodeStorage;

    // --- get volume in nodes                                                 //(5.0.017 - LR)
    for (j = 0; j < Nobjects[NODE]; j++)
    {
        nodeStorage = Node[j].newVolume;
        if ( isFinalStorage ) NodeOutflow[j] += nodeStorage;
        totalStorage += nodeStorage;
    }

    // --- skip final link storage for Steady Flow routing                     //(5.0.017 - LR)
    if ( isFinalStorage && RouteModel == SF ) return totalStorage;             //(5.0.017 - LR)

    // --- add on volume stored in links                                       //(5.0.017 - LR)
    for (j = 0; j < Nobjects[LINK]; j++)
    {
        totalStorage += Link[j].newVolume;
    }
    return totalStorage;
}

//=============================================================================

void massbal_getSysFlows(double f, double sysFlows[])
//
//  Input:   f = time weighting factor
//  Output:  sysFlows = array of total system flows
//  Purpose: retrieves time-weighted average of old and new system flows.
//
{
    double f1 = 1.0 - f;
    sysFlows[SYS_DWFLOW] = (f1 * OldStepFlowTotals.dwInflow +
                             f * StepFlowTotals.dwInflow) * UCF(FLOW);
    sysFlows[SYS_GWFLOW] = (f1 * OldStepFlowTotals.gwInflow +
                             f * StepFlowTotals.gwInflow) * UCF(FLOW);
    sysFlows[SYS_IIFLOW] = (f1 * OldStepFlowTotals.iiInflow +
                             f * StepFlowTotals.iiInflow) * UCF(FLOW);
    sysFlows[SYS_EXFLOW] = (f1 * OldStepFlowTotals.exInflow +
                             f * StepFlowTotals.exInflow) * UCF(FLOW);
    sysFlows[SYS_FLOODING] = (f1 * OldStepFlowTotals.flooding +
                               f * StepFlowTotals.flooding) * UCF(FLOW);
    sysFlows[SYS_OUTFLOW] = (f1 * OldStepFlowTotals.outflow +
                              f * StepFlowTotals.outflow) * UCF(FLOW);
    sysFlows[SYS_STORAGE] = (f1 * OldStepFlowTotals.finalStorage +
                              f * StepFlowTotals.finalStorage) * UCF(VOLUME);
}

//=============================================================================

double massbal_getRunoffError()
//
//  Input:   none
//  Output:  none
//  Purpose: computes runoff mass balance error.
//
{
    int    j;                                                                  //(5.0.019 - LR)
    double totalInflow;
    double totalOutflow;

    // --- find final storage on all subcatchments
    RunoffTotals.finalStorage = 0.0;
    RunoffTotals.finalSnowCover = 0.0;
    for (j = 0; j < Nobjects[SUBCATCH]; j++)
    {
        RunoffTotals.finalStorage += subcatch_getStorage(j);                   //(5.0.019 - LR)
        RunoffTotals.finalSnowCover += snow_getSnowCover(j);
    }

    // --- get snow removed from system
    RunoffTotals.snowRemoved = Snow.removed;

    // --- compute % difference between total inflow and outflow
    totalInflow  = RunoffTotals.rainfall +
                   RunoffTotals.initStorage +
                   RunoffTotals.initSnowCover;
    totalOutflow = RunoffTotals.evap +
                   RunoffTotals.infil +
                   RunoffTotals.runoff +
                   RunoffTotals.snowRemoved +
                   RunoffTotals.finalStorage +
                   RunoffTotals.finalSnowCover;
    RunoffTotals.pctError = 0.0;
    if ( fabs(totalInflow - totalOutflow) < 1.0 )
    {
        RunoffTotals.pctError = TINY;
    }
    else if ( totalInflow > 0.0 )
    {
        RunoffTotals.pctError = 100.0 * (1.0 - totalOutflow / totalInflow);
    }
    else if ( totalOutflow > 0.0 )
    {
        RunoffTotals.pctError = 100.0 * (totalInflow / totalOutflow - 1.0);
    }
    RunoffError = RunoffTotals.pctError;
    return RunoffTotals.pctError;
}

//=============================================================================

double massbal_getLoadingError()
//
//  Input:   none
//  Output:  none
//  Purpose: computes runoff load mass balance error.
//
{
    int    j;
    double loadIn;
    double loadOut;
    double maxError = 0.0;

    for (j = 0; j < Nobjects[POLLUT]; j++)
    {
        // --- get final pollutant loading remaining on land surface
        LoadingTotals[j].finalLoad = massbal_getBuildup(j);

        // --- compute total load added to study area
        loadIn = LoadingTotals[j].initLoad +
                 LoadingTotals[j].buildup +
                 LoadingTotals[j].deposition;
    
        // --- compute total load removed from study area
        loadOut = LoadingTotals[j].sweeping +
                  LoadingTotals[j].infil +
                  LoadingTotals[j].bmpRemoval +
                  LoadingTotals[j].runoff +
                  LoadingTotals[j].finalLoad;

        // --- compute mass balance error
        LoadingTotals[j].pctError = 0.0;
        if ( fabs(loadIn - loadOut) < 0.001 )
        {
            LoadingTotals[j].pctError = TINY;
        }
        else if ( loadIn > 0.0 )
        {
            LoadingTotals[j].pctError = 100.0 * (1.0 - loadOut / loadIn);
        }
        else if ( loadOut > 0.0 )
        {
            LoadingTotals[j].pctError = 100.0 * (loadIn / loadOut - 1.0);
        }
        maxError = MAX(maxError, LoadingTotals[j].pctError);

        // --- report total counts as log10
        if ( Pollut[j].units == COUNT )
        {
            LoadingTotals[j].finalLoad  = LOG10(LoadingTotals[j].finalLoad);
            LoadingTotals[j].initLoad   = LOG10(LoadingTotals[j].initLoad);
            LoadingTotals[j].buildup    = LOG10(LoadingTotals[j].buildup);
            LoadingTotals[j].deposition = LOG10(LoadingTotals[j].deposition);
            LoadingTotals[j].sweeping   = LOG10(LoadingTotals[j].sweeping);
            LoadingTotals[j].infil      = LOG10(LoadingTotals[j].infil);
            LoadingTotals[j].bmpRemoval = LOG10(LoadingTotals[j].bmpRemoval);
            LoadingTotals[j].runoff     = LOG10(LoadingTotals[j].runoff);
            LoadingTotals[j].finalLoad  = LOG10(LoadingTotals[j].finalLoad);
        }
    }
    return maxError;
}

//=============================================================================

double massbal_getGwaterError()
//
//  Input:   none
//  Output:  none
//  Purpose: computes groundwater mass balance error.
//
{
    int    j;
    double totalInflow;
    double totalOutflow;

    // --- find final storage in groundwater
    GwaterTotals.finalStorage = 0.0;
    for ( j = 0; j < Nobjects[SUBCATCH]; j++ )
    {
        GwaterTotals.finalStorage += gwater_getVolume(j) * Subcatch[j].area;
    }

    // --- compute % difference between total inflow and outflow
    totalInflow  = GwaterTotals.infil +
                   GwaterTotals.initStorage;
    totalOutflow = GwaterTotals.upperEvap +
                   GwaterTotals.lowerEvap +
                   GwaterTotals.lowerPerc +
                   GwaterTotals.gwater +
                   GwaterTotals.finalStorage;
    GwaterTotals.pctError = 0.0;
    if ( fabs(totalInflow - totalOutflow) < 1.0 )
    {
        GwaterTotals.pctError = TINY;
    }
    else if ( totalInflow > 0.0 )
    {
        GwaterTotals.pctError = 100.0 * (1.0 - totalOutflow / totalInflow);
    }
    else if ( totalOutflow > 0.0 )
    {
        GwaterTotals.pctError = 100.0 * (totalInflow / totalOutflow - 1.0);
    }
    GwaterError = GwaterTotals.pctError;
    return GwaterTotals.pctError;
}

//=============================================================================

double massbal_getFlowError()
//
//  Input:   none
//  Output:  none
//  Purpose: computes flow routing mass balance error.
//
{
    double totalInflow;
    double totalOutflow;

    // --- get final volume of nodes and links
    FlowTotals.finalStorage = massbal_getStorage(TRUE);

    // --- compute % difference between total inflow and outflow
    totalInflow  = FlowTotals.dwInflow +
                   FlowTotals.wwInflow +
                   FlowTotals.gwInflow +
                   FlowTotals.iiInflow +
                   FlowTotals.exInflow +
                   FlowTotals.initStorage;
    totalOutflow = FlowTotals.flooding +
                   FlowTotals.outflow +
                   FlowTotals.reacted + 
                   FlowTotals.finalStorage;
    FlowTotals.pctError = 0.0;
    if ( fabs(totalInflow - totalOutflow) < 1.0 )
    {
        FlowTotals.pctError = TINY;
    }
    else if ( totalInflow > 0.0 )
    {
        FlowTotals.pctError = 100.0 * (1.0 - totalOutflow / totalInflow);
    }
    else if ( totalOutflow > 0.0 )
    {
        FlowTotals.pctError = 100.0 * (totalInflow / totalOutflow - 1.0);
    }
    FlowError = FlowTotals.pctError;
    return FlowTotals.pctError;
}

//=============================================================================

double massbal_getQualError()
//
//  Input:   none
//  Output:  none
//  Purpose: computes water quality routing mass balance error.
//
{
    int    p;                                                                  //(5.0.019 - LR)
    double maxQualError = 0.0;
    //double finalStorage;                                                     //(5.0.019 - LR)
    double totalInflow;
    double totalOutflow;
    double cf;

    // --- analyze each pollutant
    for (p = 0; p < Nobjects[POLLUT]; p++)
    {
        // --- get final mass stored in nodes and links
        QualTotals[p].finalStorage = massbal_getStoredMass(p);                 //(5.0.019 - LR)

        // --- compute % difference between total inflow and outflow
        totalInflow  = QualTotals[p].dwInflow +
                       QualTotals[p].wwInflow +
                       QualTotals[p].gwInflow +
                       QualTotals[p].iiInflow +
                       QualTotals[p].exInflow +
                       QualTotals[p].initStorage;
        totalOutflow = QualTotals[p].flooding +
                       QualTotals[p].outflow +
                       QualTotals[p].reacted +
                       QualTotals[p].finalStorage;                             //(5.0.019 - LR)
        QualTotals[p].pctError = 0.0;
        if ( fabs(totalInflow - totalOutflow) < 0.001 )
        {
            QualTotals[p].pctError = TINY;
        }
        else if ( totalInflow > 0.0 )
        {
            QualTotals[p].pctError = 100.0 * (1.0 - totalOutflow / totalInflow);
        }
        else if ( totalOutflow > 0.0 )
        {
            QualTotals[p].pctError = 100.0 * (totalInflow / totalOutflow - 1.0);
        }

        // --- update max. error among all pollutants
        if ( fabs(QualTotals[p].pctError) > fabs(maxQualError) )
        {
            maxQualError = QualTotals[p].pctError;
        }

        // --- convert totals to reporting units (lbs, kg, or Log(Count))
        cf = LperFT3;
        if ( Pollut[p].units == COUNT )
        {
            QualTotals[p].dwInflow     = LOG10(cf * QualTotals[p].dwInflow);
            QualTotals[p].wwInflow     = LOG10(cf * QualTotals[p].wwInflow);
            QualTotals[p].gwInflow     = LOG10(cf * QualTotals[p].gwInflow);
            QualTotals[p].iiInflow     = LOG10(cf * QualTotals[p].iiInflow);
            QualTotals[p].exInflow     = LOG10(cf * QualTotals[p].exInflow);
            QualTotals[p].flooding     = LOG10(cf * QualTotals[p].flooding);
            QualTotals[p].outflow      = LOG10(cf * QualTotals[p].outflow);
            QualTotals[p].reacted      = LOG10(cf * QualTotals[p].reacted);
            QualTotals[p].initStorage  = LOG10(cf * QualTotals[p].initStorage);
            QualTotals[p].finalStorage = LOG10(cf * QualTotals[p].finalStorage);
        }
        else
        {
            cf = cf * UCF(MASS);
            if ( Pollut[p].units == UG ) cf /= 1000.0;
            QualTotals[p].dwInflow     *= cf;
            QualTotals[p].wwInflow     *= cf; 
            QualTotals[p].gwInflow     *= cf; 
            QualTotals[p].iiInflow     *= cf; 
            QualTotals[p].exInflow     *= cf; 
            QualTotals[p].flooding     *= cf; 
            QualTotals[p].outflow      *= cf; 
            QualTotals[p].reacted      *= cf; 
            QualTotals[p].initStorage  *= cf; 
            QualTotals[p].finalStorage *= cf; 
        }
    }
    QualError = maxQualError;
    return maxQualError;
}
//=============================================================================

////  New function added.  ////                                                //(5.0.012 - LR)
double massbal_getStepFlowError()
//
//  Input:   none
//  Output:  returns fractional difference between total inflow and outflow.
//  Purpose: computes flow routing mass balance error at current time step.
//
{
    double totalInflow;
    double totalOutflow;

    // --- compute % difference between total inflow and outflow
    totalInflow  = StepFlowTotals.dwInflow +
                   StepFlowTotals.wwInflow +
                   StepFlowTotals.gwInflow +
                   StepFlowTotals.iiInflow +
                   StepFlowTotals.exInflow;
    totalOutflow = StepFlowTotals.flooding +
                   StepFlowTotals.outflow +
                   StepFlowTotals.reacted;
    if ( totalInflow > 0.0 )       return 1.0 - totalOutflow / totalInflow;
    else if ( totalOutflow > 0.0 ) return totalInflow / totalOutflow - 1.0;
    else return 0.0;
}

//=============================================================================

////  New function added (as suggested by RED)  ////                           //(5.0.019 - LR)
double massbal_getStoredMass(int p)
//
//  Input:   p = pollutant index
//  Output:  returns mass of pollutant.
//  Purpose: computes mass of pollutant stored in conveyance network.
//
{
    int j;
    double storedMass = 0.0;

    // --- get mass stored in nodes
    for (j = 0; j < Nobjects[NODE]; j++)
        storedMass += Node[j].newVolume * Node[j].newQual[p];

    // --- get mass stored in links (except for Steady Flow routing)
    if ( RouteModel != SF )
    {
        for (j = 0; j < Nobjects[LINK]; j++)
            storedMass += Link[j].newVolume * Link[j].newQual[p];
    }
    return storedMass;
}

//=============================================================================
