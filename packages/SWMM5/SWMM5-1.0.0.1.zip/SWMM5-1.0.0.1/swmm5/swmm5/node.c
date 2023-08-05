//-----------------------------------------------------------------------------
//   node.c
//
//   Project:  EPA SWMM5
//   Version:  5.0
//   Date:     6/19/07   (Build 5.0.010)
//             2/4/08    (Build 5.0.012)
//             1/21/09   (Build 5.0.014)
//             4/10/09   (Build 5.0.015)
//             6/22/09   (Build 5.0.016)
//             11/18/09  (Build 5.0.018)
//             07/30/10  (Build 5.0.019)
//   Author:   L. Rossman
//
//   Conveyance system node functions.
//-----------------------------------------------------------------------------
#define _CRT_SECURE_NO_DEPRECATE

#include <malloc.h>
#include <string.h>
#include <math.h>
#include "headers.h"
#include "findroot.h"

//-----------------------------------------------------------------------------                  
//  Shared variables
//-----------------------------------------------------------------------------                  
static int     Kstar;                  // storage unit index
static double  Vstar;                  // storage unit volume (ft3)

//-----------------------------------------------------------------------------
//  External functions (declared in funcs.h)
//-----------------------------------------------------------------------------
//  node_readParams        (called from readNode in input.c)
//  node_validate          (called from project_validate) 
//  node_initState         (called from project_init)
//  node_setOldHydState    (called from routing_execute)
//  node_setOldQualState   (called from routing_execute)
//  node_initInflow        (called from routing_execute)
//  node_setOutletDepth    (called from routing_execute)
//  node_getLosses         (called from removeLosses in routing.c)             //(5.0.015 - LR)
//  node_getSystemOutflow  (called from removeOutflows in routing.c)
//  node_getResults        (called from output_saveNodeResults)
//  node_getSurfArea
//  node_getDepth
//  node_getVolume
//  node_getPondedDepth
//  node_getPondedArea
//  node_getOutflow
//  node_getMaxOutflow

//-----------------------------------------------------------------------------
//  Local functions
//-----------------------------------------------------------------------------
static void   node_setParams(int j, int type, int k, double x[]);
static int    junc_readParams(int j, int k, char* tok[], int ntoks);

static int    outfall_readParams(int j, int k, char* tok[], int ntoks);
static void   outfall_setOutletDepth(int j, double yNorm, double yCrit, double z);

static int    storage_readParams(int j, int k, char* tok[], int ntoks);
static int    storage_readInfilParams(int j, char* tok[], int ntoks, int n);   //(5.0.015 - LR)
static double storage_getDepth(int j, double v);
static double storage_getVolume(int j, double d);
static double storage_getSurfArea(int j, double d);
static void   storage_getVolDiff(double y, double* f, double* df);
static double storage_getOutflow(int j, int i);
static double storage_getLosses(int j, double tStep);                          //(5.0.019 - LR)

static int    divider_readParams(int j, int k, char* tok[], int ntoks);
static void   divider_validate(int j);
static double divider_getOutflow(int j, int link);


//=============================================================================

int node_readParams(int j, int type, int k, char* tok[], int ntoks)
//
//  Input:   j = node index
//           type = node type code
//           k = index of node type
//           tok[] = array of string tokens
//           ntoks = number of tokens
//  Output:  returns an error code
//  Purpose: reads node properties from a tokenized line of input.
//
{
    switch ( type )
    {
      case JUNCTION: return junc_readParams(j, k, tok, ntoks);
      case OUTFALL:  return outfall_readParams(j, k, tok, ntoks);
      case STORAGE:  return storage_readParams(j, k, tok, ntoks);
      case DIVIDER:  return divider_readParams(j, k, tok, ntoks);
      default:       return 0;
    }
}

//=============================================================================

void  node_setParams(int j, int type, int k, double x[])
//
//  Input:   j = node index
//           type = node type code
//           k = index of node type
//           x[] = array of property values
//  Output:  none
//  Purpose: assigns property values to a node.
//
{
    Node[j].type       = type;
    Node[j].subIndex   = k;
    Node[j].invertElev = x[0] / UCF(LENGTH);
    Node[j].crownElev  = Node[j].invertElev;
    Node[j].initDepth  = 0.0;
    Node[j].newVolume  = 0.0;
    Node[j].fullVolume = 0.0;
    Node[j].fullDepth  = 0.0;
    Node[j].surDepth   = 0.0;
    Node[j].pondedArea = 0.0;
    Node[j].degree     = 0;
    switch (type)
    {
      case JUNCTION:
        Node[j].fullDepth = x[1] / UCF(LENGTH);
        Node[j].initDepth = x[2] / UCF(LENGTH);
        Node[j].surDepth  = x[3] / UCF(LENGTH);
        Node[j].pondedArea = x[4] / (UCF(LENGTH)*UCF(LENGTH));
        break;

      case OUTFALL:
        Outfall[k].type        = (int)x[1];
        Outfall[k].fixedStage  = x[2] / UCF(LENGTH);
        Outfall[k].tideCurve   = (int)x[3];
        Outfall[k].stageSeries = (int)x[4];
        Outfall[k].hasFlapGate = (char)x[5];
        break;

      case STORAGE:
        Node[j].fullDepth  = x[1] / UCF(LENGTH);
        Node[j].initDepth  = x[2] / UCF(LENGTH);
        Storage[k].aCoeff  = x[3];
        Storage[k].aExpon  = x[4];
        Storage[k].aConst  = x[5];
        Storage[k].aCurve  = (int)x[6];
        Node[j].pondedArea = x[7] / (UCF(LENGTH)*UCF(LENGTH));
        Storage[k].fEvap   = x[8];
        break;

      case DIVIDER:
        Divider[k].link      = (int)x[1];
        Divider[k].type      = (int)x[2];
        Divider[k].flowCurve = (int)x[3];
        Divider[k].qMin      = x[4] / UCF(FLOW);
        Divider[k].dhMax     = x[5];
        Divider[k].cWeir     = x[6];
        Node[j].fullDepth    = x[7] / UCF(LENGTH);
        Node[j].initDepth    = x[8] / UCF(LENGTH);
        Node[j].surDepth     = x[9] / UCF(LENGTH);
        Node[j].pondedArea   = x[10] / (UCF(LENGTH)*UCF(LENGTH));
        break;
    }
}

//=============================================================================

void  node_validate(int j)
//
//  Input:   j = node index
//  Output:  none
//  Purpose: validates a node's properties.
//
{
    // --- see if full depth was increased to accommodate conduit crown        //(5.0.014 - LR)
    if ( Node[j].fullDepth > Node[j].oldDepth && Node[j].oldDepth > 0.0 )      //(5.0.014 - LR)
    {                                                                          //(5.0.014 - LR)
        report_writeWarningMsg(WARN02, Node[j].ID);                            //(5.0.015 - LR)
    }                                                                          //(5.0.014 - LR)

    // --- check that initial depth does not exceed max. depth
    if ( Node[j].initDepth > Node[j].fullDepth + Node[j].surDepth )
        report_writeErrorMsg(ERR_NODE_DEPTH, Node[j].ID);

    if ( Node[j].type == DIVIDER ) divider_validate(j);
}

//=============================================================================

void node_initState(int j)
//
//  Input:   j = node index
//  Output:  none
//  Purpose: initializes a node's state variables at start of simulation.
//
{
    int p;

    // --- initialize depth
    Node[j].oldDepth = Node[j].initDepth;
    Node[j].newDepth = Node[j].oldDepth;
    Node[j].crownElev = Node[j].invertElev;

    // --- initialize volume
//  Node[j].fullVolume = 0.0;                                                  //(5.0.014 - LR)
//  Node[j].newVolume = 0.0;                                                   //(5.0.014 - LR)
    Node[j].fullVolume = node_getVolume(j, Node[j].fullDepth);
    Node[j].oldVolume = node_getVolume(j, Node[j].oldDepth);
    Node[j].newVolume = Node[j].oldVolume;

    // --- initialize water quality state
    for (p = 0; p < Nobjects[POLLUT]; p++)
    {
        Node[j].oldQual[p]  = 0.0;
        Node[j].newQual[p]  = 0.0;
    }

    // --- initialize any inflow
    Node[j].oldLatFlow = 0.0;
    Node[j].newLatFlow = 0.0;

    // --- initialize HRT in storage nodes
    if ( Node[j].type == STORAGE )
    {
        Storage[Node[j].subIndex].hrt = 0.0;
        grnampt_initState(Storage[Node[j].subIndex].infil);                    //(5.0.015 - LR)
    }
}

//=============================================================================

void node_setOldHydState(int j)
//
//  Input:   j = node index
//  Output:  none
//  Purpose: replaces a node's old hydraulic state values with new ones.
//
{
    Node[j].oldDepth    = Node[j].newDepth;
    Node[j].oldLatFlow  = Node[j].newLatFlow;
    Node[j].oldVolume   = Node[j].newVolume;
}

//=============================================================================

void node_setOldQualState(int j)
//
//  Input:   j = node index
//  Output:  none
//  Purpose: replaces a node's old water quality state values with new ones.
//
{
    int p;
    for (p = 0; p < Nobjects[POLLUT]; p++)
    {
        Node[j].oldQual[p] = Node[j].newQual[p];
        Node[j].newQual[p] = 0.0;
    }
}

//=============================================================================

void node_initInflow(int j, double tStep)
//
//  Input:   j = node index
//           tStep = time step (sec)
//  Output:  none
//  Purpose: initializes a node's inflow at start of next time step.
//
{
    // --- initialize inflow & outflow
    Node[j].oldFlowInflow = Node[j].inflow;
    Node[j].oldNetInflow  = Node[j].inflow - Node[j].outflow;
    Node[j].inflow = Node[j].newLatFlow;
    Node[j].outflow = 0.0;

    // --- set overflow to any excess stored volume
    if ( Node[j].newVolume > Node[j].fullVolume )
        Node[j].overflow = (Node[j].newVolume - Node[j].fullVolume) / tStep;
    else Node[j].overflow = 0.0;
}

//=============================================================================

double node_getDepth(int j, double v)
//
//  Input:   j = node index
//           v = volume (ft3)
//  Output:  returns depth of water at a node (ft)
//  Purpose: computes a node's water depth from its volume.
//
{
    switch ( Node[j].type )
    {
      case STORAGE: return storage_getDepth(j, v);
      default:      return 0.0;
    }
}

//=============================================================================

double node_getVolume(int j, double d)
//
//  Input:   j = node index
//           d = water depth (ft)
//  Output:  returns volume of water at a node (ft3)
//  Purpose: computes volume stored at a node from its water depth.
//
{
    switch ( Node[j].type )
    {
      case STORAGE: return storage_getVolume(j, d);

      default:
        if ( Node[j].fullDepth > 0.0 )                                         //(5.0.014 - LR)
            return Node[j].fullVolume * (d / Node[j].fullDepth);               //(5.0.014 - LR)
        else return 0.0;
    }
}

//=============================================================================

double  node_getSurfArea(int j, double d)
//
//  Input:   j = node index
//           d = water depth (ft)
//  Output:  returns surface area of water at a node (ft2)
//  Purpose: computes surface area of water stored at a node from water depth.
//
{
    switch (Node[j].type)
    {
      case STORAGE: return storage_getSurfArea(j, d);
      default:      return 0.0;        
    }
}

//=============================================================================

double node_getOutflow(int j, int k)
//
//  Input:   j = node index
//           k = link index
//  Output:  returns flow rate (cfs)
//  Purpose: computes outflow from node available for inflow into a link.
//
{
    switch ( Node[j].type )
    {
      case DIVIDER: return divider_getOutflow(j, k);
      case STORAGE: return storage_getOutflow(j, k);
      default:      return Node[j].inflow + Node[j].overflow;
    }
}

//=============================================================================

double node_getMaxOutflow(int j, double q, double tStep)
//
//  Input:   j = node index
//           q = original outflow rate (cfs)
//           tStep = time step (sec)
//  Output:  returns modified flow rate (cfs)
//  Purpose: limits outflow rate from a node with storage volume.
//
{
    double qMax;
    if ( Node[j].fullVolume > 0.0 )
    {
        qMax = Node[j].inflow + Node[j].oldVolume / tStep;                     //(5.0.014 - LR)
        if ( q > qMax ) q = qMax;
    }
    return MAX(0.0, q);
}

//=============================================================================

double node_getSystemOutflow(int j, int *isFlooded)
//
//  Input:   j = node index
//           isFlooded = TRUE if node becomes flooded
//  Output:  returns flow rate lost from system (cfs)
//  Purpose: computes flow rate at outfalls and flooded nodes.
//
{
    double outflow = 0.0;;

    // --- assume there is no flooding
    *isFlooded = FALSE;

    // --- if node is an outfall
    if ( Node[j].type == OUTFALL )
    {
        // --- node receives inflow from outfall conduit
        if ( Node[j].outflow == 0.0 ) outflow = Node[j].inflow;

        // --- node sends flow into outfall conduit
        //     (therefore it has a negative outflow)
        else
        {                                                                      //(5.0.015 - LR)
            outflow = -Node[j].outflow;                      
            Node[j].inflow = fabs(outflow);                                    //(5.0.015 - LR)
        }                                                                      //(5.0.015 - LR)

        // --- set overflow and volume to 0
        Node[j].overflow = 0.0;
        Node[j].newVolume = 0.0;
    }

    // --- node is a terminal node under Steady or Kin. Wave routing
    else if ( RouteModel != DW &&
              Node[j].degree == 0 &&
              Node[j].type != STORAGE
            )
    {
        if ( Node[j].outflow == 0.0 ) outflow = Node[j].inflow;
        Node[j].overflow = 0.0;
        Node[j].newVolume = 0.0;
    }

    // --- otherwise node is an interior node and any
    //     overflow is considered as system outflow and flooding
    else 
    {
        if ( Node[j].newVolume <= Node[j].fullVolume)                          //(5.0.012 - LR)
            outflow = Node[j].overflow;                                        //(5.0.012 - LR)
        if ( outflow > 0.0 ) *isFlooded = TRUE;
    }
    return outflow;
}

//=============================================================================

void node_getResults(int j, double f, float x[])
//
//  Input:   j = node index
//           f = weighting factor
//           x[] = array of nodal reporting variables
//  Output:  none
//  Purpose: computes weighted average of old and new results at a node.
//
{
    int    p;
    double z;
    double f1 = 1.0 - f;

    z = (f1 * Node[j].oldDepth + f * Node[j].newDepth) * UCF(LENGTH);
    x[NODE_DEPTH] = (float)z;
    z = Node[j].invertElev * UCF(LENGTH);
    x[NODE_HEAD] = x[NODE_DEPTH] + (float)z;
    z = (f1*Node[j].oldVolume + f*Node[j].newVolume) * UCF(VOLUME);
    x[NODE_VOLUME]  = (float)z;
    z = (f1*Node[j].oldLatFlow + f*Node[j].newLatFlow) * UCF(FLOW); 
    x[NODE_LATFLOW] = (float)z;
    z = (f1*Node[j].oldFlowInflow + f*Node[j].inflow) * UCF(FLOW);
    x[NODE_INFLOW] = (float)z;
    z = Node[j].overflow * UCF(FLOW);
    x[NODE_OVERFLOW] = (float)z;
    for (p = 0; p < Nobjects[POLLUT]; p++)
    {
        z = f1*Node[j].oldQual[p] + f*Node[j].newQual[p];
        x[NODE_QUAL+p] = (float)z;
    }
}

//=============================================================================

void   node_setOutletDepth(int j, double yNorm, double yCrit, double z)
//
//  Input:   j = node index
//           yNorm = normal flow depth (ft)
//           yCrit = critical flow depth (ft)
//           z = offset of connecting outfall link from node invert (ft)
//  Output:  none
//  Purpose: sets water depth at a node that serves as an outlet point.
//
{
    switch (Node[j].type)
    {
      // --- do nothing if outlet is a storage unit
      case STORAGE:
        return;

      // --- if outlet is a designated outfall then use outfall's specs
      case OUTFALL:
        outfall_setOutletDepth(j, yNorm, yCrit, z);
        break;

      // --- for all other nodes, use min. of critical & normal depths
      default:
        if ( z > 0.0 ) Node[j].newDepth = 0.0;
        else Node[j].newDepth = MIN(yNorm, yCrit);
    }
}

//=============================================================================

double node_getPondedDepth(int j, double v)
//
//  Input:   j = node index
//           v = water volume (ft3)
//  Output:  returns depth of water at a node (ft)
//  Purpose: computes depth of water at a node based on volume.
//
{
    double y;

    // --- if volume below full volume, use normal getDepth function
    if ( v <= Node[j].fullVolume ) return node_getDepth(j, v);

    // --- find ponded volume
    v = v - Node[j].fullVolume;

    // --- depth equals full depth + ponded volume / ponded area
    y = Node[j].fullDepth;
    if ( Node[j].pondedArea > 0.0 ) y += v / Node[j].pondedArea;
    return y;
}

//=============================================================================

double node_getPondedArea(int j, double d)
//
//  Input:   j = node index
//           d = water depth (ft)
//  Output:  returns surface area of water at a node (ft2)
//  Purpose: computes surface area of water at a node based on depth.
//
{
    double a;

    // --- use regular getSurfArea function if node not flooded
    if ( d <= Node[j].fullDepth || Node[j].pondedArea == 0.0 )
    {
        return node_getSurfArea(j, d);
    }

    // --- compute ponded depth
    d = d - Node[j].fullDepth;

    // --- use ponded area for flooded node                                    //(5.0.019 - LR)
    a = Node[j].pondedArea;                                                    //(5.0.019 - LR)
    if ( a <= 0.0 ) a = node_getSurfArea(j, Node[j].fullDepth);
    return a;
}

//=============================================================================

double node_getLosses(int j, double tStep)                                     //(5.0.019 - LR)
//
//  Input:   j = node index
//           evap = system evaporation rate (ft/sec)
//  Output:  returns evaporation rate at node (ft3)
//  Purpose: computes node's volume lost to evaporation over a given time step.
//
{
    if ( Node[j].type == STORAGE ) return storage_getLosses(j, tStep);         //(5.0.019 - LR)
    else return 0.0;
}

//=============================================================================
//                   J U N C T I O N   M E T H O D S
//=============================================================================

int junc_readParams(int j, int k, char* tok[], int ntoks)
//
//  Input:   j = node index
//           k = junction index
//           tok[] = array of string tokens
//           ntoks = number of tokens
//  Output:  returns an error message
//  Purpose: reads a junction's properties from a tokenized line of input.
//
//  Format of input line is:
//     nodeID  elev  maxDepth  initDepth  surDepth  aPond 
{
    int    i;
    double x[6];
    char*  id;

    if ( ntoks < 2 ) return error_setInpError(ERR_ITEMS, "");
    id = project_findID(NODE, tok[0]);
    if ( id == NULL ) return error_setInpError(ERR_NAME, tok[0]);

    // --- parse invert elev., max. depth, init. depth, surcharged depth,
    //     & ponded area values
    for ( i = 1; i <= 5; i++ )
    {
        x[i-1] = 0.0;
        if ( i < ntoks )
        {
            if ( ! getDouble(tok[i], &x[i-1]) )
                return error_setInpError(ERR_NUMBER, tok[i]);
        }
    }

    // --- check for non-negative values (except for invert elev.)
    for ( i = 1; i <= 4; i++ )
    {
        if ( x[i] < 0.0 ) return error_setInpError(ERR_NUMBER, tok[i+1]);
    }

    // --- add parameters to junction object
    Node[j].ID = id;
    node_setParams(j, JUNCTION, k, x);
    return 0;
}


//=============================================================================
//                   S T O R A G E   M E T H O D S
//=============================================================================

int storage_readParams(int j, int k, char* tok[], int ntoks)
//
//  Input:   j = node index
//           k = storage unit index
//           tok[] = array of string tokens
//           ntoks = number of tokens
//  Output:  returns an error message
//  Purpose: reads a storage unit's properties from a tokenized line of input.
//
//  Format of input line is:
//     nodeID  elev  maxDepth  initDepth  FUNCTIONAL  a1  a2  a0  aPond  fEvap
//     nodeID  elev  maxDepth  initDepth  TABULAR     curveID  aPond  fEvap
//
{
    int    i, m, n;
    double x[9];
    char*  id;

    // --- get ID name
    if ( ntoks < 6 ) return error_setInpError(ERR_ITEMS, "");
    id = project_findID(NODE, tok[0]);
    if ( id == NULL ) return error_setInpError(ERR_NAME, tok[0]);

    // --- get invert elev, max. depth, & init. depth
    for ( i = 1; i <= 3; i++ )
    {
        if ( ! getDouble(tok[i], &x[i-1]) )
            return error_setInpError(ERR_NUMBER, tok[i]);
    }

    // --- get surf. area relation type
    m = findmatch(tok[4], RelationWords);
    if ( m < 0 ) return error_setInpError(ERR_KEYWORD, tok[4]);
    x[3] = 0.0;                        // a1 
    x[4] = 0.0;                        // a2
    x[5] = 0.0;                        // a0
    x[6] = -1.0;                       // curveID
    x[7] = 0.0;                        // aPond
    x[8] = 0.0;                        // fEvap

    // --- get surf. area function coeffs.
    if ( m == FUNCTIONAL )
    {
        for (i=5; i<=7; i++)
        {
            if ( i < ntoks )
            {
                if ( ! getDouble(tok[i], &x[i-2]) )
                    return error_setInpError(ERR_NUMBER, tok[i]);
            }
        }
        n = 8;
    }

    // --- get surf. area curve name
    else
    {
        m = project_findObject(CURVE, tok[5]);
        if ( m < 0 ) return error_setInpError(ERR_NAME, tok[5]);
        x[6] = m;
        n = 6;
    }

    // --- get ponded area if present 
    if ( ntoks > n)
    {
        if ( ! getDouble(tok[n], &x[7]) )
            return error_setInpError(ERR_NUMBER, tok[n]);
        n++;
    }

    // --- get evaporation fraction if present
    if ( ntoks > n )
    {
        if ( ! getDouble(tok[n], &x[8]) )
            return error_setInpError(ERR_NUMBER, tok[n]);
        n++;                                                                   //(5.0.015 - LR)
    }

    // --- add parameters to storage unit object
    Node[j].ID = id;
    node_setParams(j, STORAGE, k, x);

    // --- read infiltration parameters if present
    if ( ntoks > n ) return storage_readInfilParams(j, tok, ntoks, n);         //(5.0.015 - LR)
    return 0;
}

//=============================================================================

////  New function added to release 5.0.015  ////                              //(5.0.015 - LR)

int storage_readInfilParams(int j, char* tok[], int ntoks, int n)
{
    int       i, k;
    double    x[3];
    TGrnAmpt* infil;

    // --- read Grenn-Ampt infiltration parameters from input tokens
    if ( ntoks < n + 3 ) return error_setInpError(ERR_ITEMS, "");
    for (i = 0; i < 3; i++)
    {
        if ( ! getDouble(tok[n+i], &x[i]) )
            return error_setInpError(ERR_NUMBER, tok[n+i]);
    }

    // --- create a Green-Ampt infiltration object for the storage node
    k = Node[j].subIndex;
    infil = Storage[k].infil;
    if ( infil == NULL )
    {
        infil = (TGrnAmpt *) malloc(sizeof(TGrnAmpt));
        if ( infil == NULL ) return error_setInpError(ERR_MEMORY, "");
        Storage[k].infil = infil;
    }

    // --- add the infiltration parameters to the Green-Ampt object
    if ( !grnampt_setParams(infil, x) ) return error_setInpError(ERR_NUMBER, "");
    return 0;
}

//=============================================================================

double storage_getDepth(int j, double v)
//
//  Input:   j = node index
//           v = volume (ft3)
//  Output:  returns depth of water at a storage node (ft)
//  Purpose: computes a storage node's water depth from its volume.
//
{
    int    k = Node[j].subIndex;
    int    i = Storage[k].aCurve;
    double d, e;

    // --- return max depth if a max. volume has been computed
    //     and volume is > max. volume
    if ( Node[j].fullVolume > 0.0
    &&   v >= Node[j].fullVolume ) return Node[j].fullDepth;
    if ( v == 0.0 ) return 0.0;

    // --- use tabular area v. depth curve
    if ( i >= 0 )
        return table_getInverseArea(&Curve[i], v*UCF(VOLUME)) / UCF(LENGTH);

    // --- use functional area v. depth relation
    else
    {
        v *= UCF(VOLUME);
        if ( Storage[k].aExpon == 0.0 )
        {
            d = v / (Storage[k].aConst + Storage[k].aCoeff);
        }
        else if ( Storage[k].aConst == 0.0 )
        {
            e = 1.0 / (Storage[k].aExpon + 1.0);
            d = pow(v / (Storage[k].aCoeff * e), e);
        }
        else
        {
            Kstar = k;
            Vstar = v;
            d = v / (Storage[k].aConst + Storage[k].aCoeff);
            findroot_Newton(0.0, Node[j].fullDepth*UCF(LENGTH), &d,
                            0.001, storage_getVolDiff);            
        }
        d /= UCF(LENGTH);
        if ( d > Node[j].fullDepth ) d = Node[j].fullDepth;
        return d;
    }
}

//=============================================================================

void  storage_getVolDiff(double y, double* f, double* df)
//
//  Input:   y = depth of water (ft)
//  Output:  f = volume of water (ft3)
//           df = dVolume/dDepth (ft2)
//  Purpose: computes volume and its derivative with respect to depth
//           at storage node Kstar using the node's area versus depth function.
//
{
    double e = Storage[Kstar].aExpon + 1.0;
    double v = Storage[Kstar].aConst * y + Storage[Kstar].aCoeff /
               e * pow(y, e);
    *f = v - Vstar;
    *df = Storage[Kstar].aConst + Storage[Kstar].aCoeff * pow(y, e-1.0);
}

//=============================================================================

double storage_getVolume(int j, double d)
//
//  Input:   j = node index
//           d = depth (ft)
//  Output:  returns volume of stored water (ft3)
//  Purpose: computes a storage node's water volume from its depth.
//
{
    int    k = Node[j].subIndex;
    int    i = Storage[k].aCurve;
    double v;

    // --- return full volume if depth >= max. depth
    if ( d == 0.0 ) return 0.0;
    if ( d >= Node[j].fullDepth                                                //(5.0.016 - LR)
    &&   Node[j].fullVolume > 0.0 ) return Node[j].fullVolume;

    // --- use table integration if area v. depth table exists
    if ( i >= 0 )
        return table_getArea(&Curve[i], d*UCF(LENGTH)) / UCF(VOLUME);          //(5.0.010 - LR)
/*
    {
        v = table_getArea(&Curve[i], d*UCF(LENGTH)) / UCF(VOLUME);
        if ( v  < 1.e-6 ) return 0.0;
        if ( Node[j].fullVolume > 0.0 ) v = MIN(v, Node[j].fullVolume);
        return v;
    }
*/
    // --- otherwise use functional area v. depth relation
    else
    {
        d *= UCF(LENGTH);
        v = Storage[k].aConst * d;
        v += Storage[k].aCoeff / (Storage[k].aExpon+1.0) *
             pow(d, Storage[k].aExpon+1.0);
        return v / UCF(VOLUME);
    }
}

//=============================================================================

double storage_getSurfArea(int j, double d)
//
//  Input:   j = node index
//           d = depth (ft)
//  Output:  returns surface area (ft2)
//  Purpose: computes a storage node's surface area from its water depth.
//
{
    double area;
    int k = Node[j].subIndex;
    int i = Storage[k].aCurve;
    if ( i >= 0 )
        area = table_lookupEx(&Curve[i], d*UCF(LENGTH));
    else
    {
        if ( Storage[k].aExpon == 0.0 )
            area = Storage[k].aConst + Storage[k].aCoeff;
        else area = Storage[k].aConst + Storage[k].aCoeff *
                    pow(Node[j].newDepth*UCF(LENGTH), Storage[k].aExpon);
    }
    return area / UCF(LENGTH) / UCF(LENGTH);
}

//=============================================================================

double storage_getOutflow(int j, int i)
//
//  Input:   j = node index
//           i = link index
//  Output:  returns flow from storage node into conduit link (cfs)
//  Purpose: finds outflow from a storage node into its connecting conduit link
//           ( non-conduit links have their own getInflow functions).
//
{
    int    k;
    double a, y;

    // --- link must be a conduit
    if ( Link[i].type != CONDUIT ) return 0.0;

    // --- find depth of water in conduit
    y = Node[j].newDepth - Link[i].offset1;                                    //(5.0.012 - LR)

    // --- return 0 if conduit empty or full flow if full
    if ( y <= 0.0 ) return 0.0;
    if ( y >= Link[i].xsect.yFull ) return Link[i].qFull;

    // --- if partially full, return normal flow
    k = Link[i].subIndex;
    a = xsect_getAofY(&Link[i].xsect, y);
    return Conduit[k].beta * xsect_getSofA(&Link[i].xsect, a);
}

//=============================================================================

//  This function was re-written for release 5.0.019.  ////                    (5.0.019 - LR)

double storage_getLosses(int j, double tStep)
//
//  Input:   j = node index
//           tStep = time step (sec)
//  Output:  returns volume of water evaporated & infiltrated (ft3)
//  Purpose: computes volume of water evaporated & infiltrated from a storage
//           node over a given time step.
//
{
    double depth;
    double area = 0.0;
    double area0 = 0.0;
    double evapRate;
    double evapLoss = 0.0;
    double infilLoss = 0.0;
    double totalLoss = 0.0;
    double maxLoss;
    TGrnAmpt* infil;

    // --- adjust evaporation rate for storage unit's evaporation potential
    evapRate = Evap.rate * Storage[Node[j].subIndex].fEvap;
    if ( evapRate > 0.0 )
    {
        // --- find surface area available for evaporation
        depth = Node[j].oldDepth;
        if ( depth > FUDGE ) area += storage_getSurfArea(j, depth);
        depth = Node[j].newDepth;
        if ( depth > FUDGE ) area += storage_getSurfArea(j, depth);

        // --- compute evaporation loss over average area
        evapLoss = 0.5 * area * evapRate * tStep;
    }

    // --- compute infiltration loss
    infil = Storage[Node[j].subIndex].infil;
    if (infil)
    {
        // --- find average depth over time step
        depth = 0.5 * (Node[j].oldDepth + Node[j].newDepth);

        // --- get surface area at avg. depth and at bottom of unit
        area0 = storage_getSurfArea(j, 0.0);
        area = area0;
        if ( depth > FUDGE ) area = storage_getSurfArea(j, depth);
        if ( area > 0.0 )
        {
            // --- get average depth assuming sloped sides
            depth = depth / 2.0 * (1.0 + area0/area);

            // --- compute infil. loss considering ponded depth
            infilLoss = grnampt_getInfil(infil, tStep, 0.0, depth) *
                        area * tStep;
        }
    }

    // --- compute total loss
    totalLoss = evapLoss + infilLoss;
    maxLoss = 0.5 * (Node[j].oldVolume + Node[j].newVolume);
    if ( totalLoss > 0.0 )
    {
        if ( totalLoss > maxLoss )
        {
            evapLoss = (evapLoss / totalLoss) * maxLoss;
            totalLoss = maxLoss;
        }
    }
    Storage[Node[j].subIndex].evapLoss = evapLoss;
    Storage[Node[j].subIndex].losses = totalLoss;
    return totalLoss;
}

//=============================================================================
//                   D I V I D E R   M E T H O D S
//=============================================================================

int divider_readParams(int j, int k, char* tok[], int ntoks)
//
//  Input:   j = node index
//           k = divider index
//           tok[] = array of string tokens
//           ntoks = number of tokens
//  Output:  returns an error message
//  Purpose: reads a flow divider's properties from a tokenized line of input.
//
//  Format of input line is:
//    nodeID  elev  divLink  TABULAR  curveID (optional params)
//    nodeID  elev  divLink  OVERFLOW (optional params)
//    nodeID  elev  divLink  CUTOFF  qCutoff (optional params)
//    nodeID  elev  divLink  WEIR    qMin  dhMax  cWeir (optional params)
//  where optional params are:
//    maxDepth  initDepth  surDepth  aPond    
//
{
    int    i, m, m1, m2, n;
    double x[11];
    char*  id;

    // --- get ID name
    if ( ntoks < 4 ) return error_setInpError(ERR_ITEMS, "");
    id = project_findID(NODE, tok[0]);
    if ( id == NULL ) return error_setInpError(ERR_NAME, tok[0]);

    // --- get invert elev.
    if ( ! getDouble(tok[1], &x[0]) ) return error_setInpError(ERR_NUMBER, tok[1]);

    // --- initialize parameter values
    for ( i=1; i<11; i++) x[i] = 0.0;

    // --- check if no diverted link supplied
    if ( strlen(tok[2]) == 0 || strcmp(tok[2], "*") == 0 ) x[1] = -1.0;

    // --- otherwise get index of diverted link
    else
    {
        m1 = project_findObject(LINK, tok[2]);
        if ( m1 < 0 ) return error_setInpError(ERR_NAME, tok[2]);
        x[1] = m1;
    }
    
    // --- get divider type
	n = 4;
    m1 = findmatch(tok[3], DividerTypeWords);
    if ( m1 < 0 ) return error_setInpError(ERR_KEYWORD, tok[3]);
    x[2] = m1;

    // --- get index of flow diversion curve for Tabular divider
    x[3] = -1;
    if ( m1 == TABULAR_DIVIDER )
    {
        if ( ntoks < 5 ) return error_setInpError(ERR_ITEMS, "");
        m2 = project_findObject(CURVE, tok[4]);
        if ( m2 < 0 ) return error_setInpError(ERR_NAME, tok[4]);
        x[3] = m2;
        n = 5;
    }

    // --- get cutoff flow for Cutoff divider
    if ( m1 == CUTOFF_DIVIDER )
    {
        if ( ntoks < 5 ) return error_setInpError(ERR_ITEMS, "");
        if ( ! getDouble(tok[4], &x[4]) )
            return error_setInpError(ERR_NUMBER, tok[4]);
        n = 5;
    }

    // --- get qmin, dhMax, & cWeir for Weir divider
    if ( m1 == WEIR_DIVIDER )
    {
        if ( ntoks < 7 ) return error_setInpError(ERR_ITEMS, "");
        for (i=4; i<7; i++)
             if ( ! getDouble(tok[i], &x[i]) )
                 return error_setInpError(ERR_NUMBER, tok[i]);
        n = 7;
    }

    // --- no parameters needed for Overflow divider
    if ( m1 == OVERFLOW_DIVIDER ) n = 4;

    // --- retrieve optional full depth, init. depth, surcharged depth
    //      & ponded area
    m = 7;
    for (i=n; i<ntoks && m<11; i++)
    {
        if ( ! getDouble(tok[i], &x[m]) )
        {
            return error_setInpError(ERR_NUMBER, tok[i]);
        }
        m++;
    }
 
    // --- add parameters to data base
    Node[j].ID = id;
    node_setParams(j, DIVIDER, k, x);
    return 0;
}

//=============================================================================

void  divider_validate(int j)
//
//  Input:   j = node index
//  Output:  none
//  Purpose: validates a flow divider's properties.
//
{
    int i, k;

    // --- check that diverted link is attached to divider
    k = Node[j].subIndex;
    i = Divider[k].link;
    if ( i < 0 || ( Link[i].node1 != j && Link[i].node2 != j) )                //(5.0.010 - LAR)
    {
        report_writeErrorMsg(ERR_DIVIDER_LINK, Node[j].ID);
    }

    // --- validate parameters supplied for weir-type divider
    if ( Divider[k].type == WEIR_DIVIDER )
    {
        if ( Divider[k].dhMax <= 0.0 || Divider[k].cWeir <= 0.0 )
            report_writeErrorMsg(ERR_WEIR_DIVIDER, Node[j].ID);
        else
        {
            // --- find flow when weir is full
            Divider[k].qMax = Divider[k].cWeir * pow(Divider[k].dhMax, 1.5)
                              / UCF(FLOW);
            if ( Divider[k].qMin > Divider[k].qMax )
                report_writeErrorMsg(ERR_WEIR_DIVIDER, Node[j].ID);
        }
    }
}

//=============================================================================

double divider_getOutflow(int j, int k)
//
//  Input:   j = node index
//           k = index of diversion link
//  Output:  returns diverted flow rate (cfs)
//  Purpose: computes flow sent through divider node into its diversion link.
//
//  NOTE: requires that links be previously sorted so that the non-diversion
//        link always gets evaluated before the diversion link
{
    int    i;                     // index of divider node
    int    m;                     // index of diverted flow table
    double qIn;                   // inflow to divider
    double qOut;                  // diverted outflow
    double f;                     // fraction of weir divider full

    qIn = Node[j].inflow + Node[j].overflow;
    i = Node[j].subIndex;
    switch ( Divider[i].type )
    {
      case CUTOFF_DIVIDER:
        if ( qIn <= Divider[i].qMin ) qOut = 0.0;
        else qOut = qIn - Divider[i].qMin;
        break;

      case OVERFLOW_DIVIDER:
        // --- outflow sent into non-diversion link is simply node's inflow
        if ( k != Divider[i].link ) qOut = qIn;

        // --- diversion link receives any excess of node's inflow and
        //     outflow sent previously into non-diversion link
        else qOut = qIn - Node[j].outflow;
        if ( qOut < FLOW_TOL ) qOut = 0.0;
        return qOut;

      case WEIR_DIVIDER:
        // --- no flow if inflow < qMin
        if ( qIn <= Divider[i].qMin ) qOut = 0.0;

        // --- otherwise use weir eqn.
        else
        {
            // --- find fractional depth of flow over weir
            f = (qIn - Divider[i].qMin) /
                (Divider[i].qMax - Divider[i].qMin);

            // --- if weir surcharged, use orifice eqn.
            if ( f > 1.0 ) qOut = Divider[i].qMax * sqrt(f);
            
            // --- otherwise use weir eqn.
            else qOut = Divider[i].cWeir *
                        pow(f*Divider[i].dhMax, 1.5) / UCF(FLOW);
        }
        break;

      case TABULAR_DIVIDER:
        m = Divider[i].flowCurve;
        if ( m >= 0 )
            qOut = table_lookup(&Curve[m], qIn * UCF(FLOW)) / UCF(FLOW);
        else qOut = 0.0;
        break;

      default: qOut = 0.0;
    }

    // --- make sure outflow doesn't exceed inflow
    if ( qOut > qIn ) qOut = qIn;

    // --- if link k not the diversion link, then re-define qOut as 
    //     the undiverted flow
    if ( k != Divider[i].link )
    {
        qOut = qIn - qOut;
    }
    return qOut;
}


//=============================================================================
//                    O U T F A L L   M E T H O D S
//=============================================================================

int outfall_readParams(int j, int k, char* tok[], int ntoks)
//
//  Input:   j = node index
//           k = outfall index
//           tok[] = array of string tokens
//           ntoks = number of tokens
//  Output:  returns an error message
//  Purpose: reads an outfall's properties from a tokenized line of input.
//
//  Format of input line is:
//    nodeID  elev  FIXED  fixedStage (flapGate)
//    nodeID  elev  TIDAL  curveID (flapGate)
//    nodeID  elev  TIMESERIES  tseriesID (flapGate)
//    nodeID  elev  FREE (flapGate)
//    nodeID  elev  NORMAL (flapGate)
//
{
    int    i, m, n;
    double x[6];
    char*  id;

    if ( ntoks < 3 ) return error_setInpError(ERR_ITEMS, "");
    id = project_findID(NODE, tok[0]);                      // node ID
    if ( id == NULL )
        return error_setInpError(ERR_NAME, tok[0]);
    if ( ! getDouble(tok[1], &x[0]) )                       // invert elev. 
        return error_setInpError(ERR_NUMBER, tok[1]);
    i = findmatch(tok[2], OutfallTypeWords);               // outfall type
    if ( i < 0 ) return error_setInpError(ERR_KEYWORD, tok[2]);
    x[1] = i;                                              // outfall type
    x[2] = 0.0;                                            // fixed stage
    x[3] = -1.;                                            // tidal curve
    x[4] = -1.;                                            // tide series
    x[5] = 0.;                                             // flap gate
    n = 4;
    if ( i >= FIXED_OUTFALL )
    {
        if ( ntoks < 4 ) return error_setInpError(ERR_ITEMS, "");
        n = 5;
        switch ( i )
        {
        case FIXED_OUTFALL:                                // fixed stage
          if ( ! getDouble(tok[3], &x[2]) )
              return error_setInpError(ERR_NUMBER, tok[3]);
          break;
        case TIDAL_OUTFALL:                                // tidal curve
          m = project_findObject(CURVE, tok[3]);              
          if ( m < 0 ) return error_setInpError(ERR_NAME, tok[3]);
          x[3] = m;
          break;
        case TIMESERIES_OUTFALL:                           // stage time series
          m = project_findObject(TSERIES, tok[3]);            
          if ( m < 0 ) return error_setInpError(ERR_NAME, tok[3]);
          x[4] = m;
          Tseries[m].refersTo = TIMESERIES_OUTFALL;                            //(5.0.019 - LR)
        }
    }
    if ( ntoks == n )
    {
        m = findmatch(tok[n-1], NoYesWords);               // flap gate
        if ( m < 0 ) return error_setInpError(ERR_KEYWORD, tok[n-1]);
        x[5] = m;
    }
    Node[j].ID = id;
    node_setParams(j, OUTFALL, k, x);
    return 0;
}

//=============================================================================

void outfall_setOutletDepth(int j, double yNorm, double yCrit, double z)
//
//  Input:   j = node index
//           yNorm = normal flow depth in outfall conduit (ft)
//           yCrit = critical flow depth in outfall conduit (ft)
//           z = height to outfall conduit invert (ft)
//  Output:  none
//  Purpose: sets water depth at an outfall node.
//
{
    double   x, y;                     // x,y values in table
    double   yNew;                     // new depth above invert elev. (ft)
    double   stage;                    // water elevation at outfall (ft)
    int      k;                        // table index
    int      i = Node[j].subIndex;     // outfall index
    DateTime currentDate;              // current date/time in days

    switch ( Outfall[i].type )
    {
      case FREE_OUTFALL:
        if ( z > 0.0 ) Node[j].newDepth = 0.0;
        else Node[j].newDepth = MIN(yNorm, yCrit);
        return;

      case NORMAL_OUTFALL:
        if ( z > 0.0 ) Node[j].newDepth = 0.0;
        else Node[j].newDepth = yNorm;
        return;

      case FIXED_OUTFALL:
        stage = Outfall[i].fixedStage;
        break;

      case TIDAL_OUTFALL:
        k = Outfall[i].tideCurve;
        table_getFirstEntry(&Curve[k], &x, &y);
        currentDate = NewRoutingTime / MSECperDAY;
        x += ( currentDate - floor(currentDate) ) * 24.0;
        stage = table_lookup(&Curve[k], x) / UCF(LENGTH);                      //(5.0.012 - LR)
        break;

      case TIMESERIES_OUTFALL:
        k = Outfall[i].stageSeries;
        currentDate = StartDateTime + NewRoutingTime / MSECperDAY;
        stage = table_tseriesLookup(&Tseries[k], currentDate, TRUE) /          //(5.0.012 - LR)
                UCF(LENGTH);
        break;
      default: stage = Node[j].invertElev;
    }

    // --- now determine depth at node given outfall stage elev.
 
    // --- let critical flow depth be min. of critical & normal depth
    yCrit = MIN(yCrit, yNorm);

    // --- if elev. of critical depth is below outfall stage elev. then
    //     the outfall stage determines node depth
    if ( yCrit + z + Node[j].invertElev < stage )
    {
        yNew = stage - Node[j].invertElev;
    }

    // --- otherwise if the outfall conduit lies above the outfall invert
    else if ( z > 0.0 )
    {
        // --- if the outfall stage lies below the bottom of the outfall
        //     conduit then the result is distance from node invert to stage
        if ( stage < Node[j].invertElev + z )
            yNew = MAX(0.0, (stage - Node[j].invertElev));

        // --- otherwise stage lies between bottom of conduit and critical
        //     depth in conduit so result is elev. of critical depth
        else
            yNew = z + yCrit;
    }

    // --- and for case where there is no conduit offset and outfall stage
    //     lies below critical depth, then node depth = critical depth 
    else yNew = yCrit;
    Node[j].newDepth = yNew;
}

//=============================================================================
