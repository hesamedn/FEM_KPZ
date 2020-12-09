/************************************************************************************
/***  Finite Element Simulation of the KPZ model using the Moveing Mesh method,v0.01;
/***  Date:03.09.1399                                                    
/***  Copyleft 2020 by Hesam E. Derakhshan, All lefts reserved! ;                                    
/***                                                                                                                                                                            
/************************************************************************************/
#include <iostream>
using namespace std;

//-------- Constants and Parameters -----------
const int   N     = 30;                   // Size of the lattice
const int   L     = 50;                   // The length of the simulation box [l*]
const float g     = 1./8;                 // Coupling constant g
const float dx    = 1./4;                 // Primary  Δx 
const float dt    = 1./1024;              // Δt
//------------------------------------------

class KPZClass {
    double time;          //time
    double x [L] = { };  // Array of discrete points
   //-------- initialize x----------- 
    for (int i = 0; i < L; i++)
    {
     x[i] = i * dx
     cout << x[i] << endl;  
    }
    
    double u[L] = {0};
    double u_temp[L] = {};
    double h[L] = {0};
    double xi[L] = {};
    double eta[L] = {};

public:


};

// FEM_KPZ_C++::FEM_KPZ_C++(/* args */)
// {
// }

// FEM_KPZ_C++::~FEM_KPZ_C++()
// {
// }


int main(int argc, char *argv[]) {
    cout << "Finite Element Simulation of the KPZ model using the Moveing Mesh method,v0.01" << endl;
    cout << "by Hesam Derakhshan \n" << endl;
    cout << "laste modified date: 15.09.1399" <<endl;
    vec a = linspace(0, 5, 6);
    cout << "laste modified date: 15.09.1399" <<endl;
}
