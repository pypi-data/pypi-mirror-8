/*
  C code for calculating a potential and its forces on a grid
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#define CHUNKSIZE 1
//Potentials
#include <galpy_potentials.h>
#include <actionAngle.h>
#include <integrateFullOrbit.h>
#include <interp_2d.h>
#include <cubic_bspline_2d_coeffs.h>
/*
  MAIN FUNCTIONS
*/
void calc_potential(int nR,
		    double *R,
		    int nz,
		    double *z,
		    int npot,
		    int * pot_type,
		    double * pot_args,
		    double *out,
		    int * err){
  int ii, jj, tid, nthreads;
#ifdef _OPENMP
  nthreads = omp_get_max_threads();
#else
  nthreads = 1;
#endif
  double * row= (double *) malloc ( nthreads * nz * ( sizeof ( double ) ) );
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_actionAngleArgs(npot,potentialArgs,pot_type,pot_args);
  //Run through the grid and calculate
  UNUSED int chunk= CHUNKSIZE;
#pragma omp parallel for schedule(static,chunk) private(ii,tid,jj)	\
  shared(row,npot,potentialArgs,R,z,nR,nz)
  for (ii=0; ii < nR; ii++){
#ifdef _OPENMP
    tid= omp_get_thread_num();
#else
    tid = 0;
#endif
    for (jj=0; jj < nz; jj++){
      *(row+jj+tid*nz)= evaluatePotentials(*(R+ii),*(z+jj),npot,potentialArgs);
    }
    put_row(out,ii,row+tid*nz,nz); 
  }
  for (ii=0; ii < npot; ii++) {
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
  free(row);
}
void calc_rforce(int nR,
		 double *R,
		 int nz,
		 double *z,
		 int npot,
		 int * pot_type,
		 double * pot_args,
		 double *out,
		 int * err){
  int ii, jj, tid, nthreads;
#ifdef _OPENMP
  nthreads = omp_get_max_threads();
#else
  nthreads = 1;
#endif
  double * row= (double *) malloc ( nthreads * nz * ( sizeof ( double ) ) );
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_leapFuncArgs_Full(npot,potentialArgs,pot_type,pot_args);
  //Run through the grid and calculate
  UNUSED int chunk= CHUNKSIZE;
#pragma omp parallel for schedule(static,chunk) private(ii,tid,jj)	\
  shared(row,npot,potentialArgs,R,z,nR,nz)
  for (ii=0; ii < nR; ii++){
#ifdef _OPENMP
    tid= omp_get_thread_num();
#else
    tid = 0;
#endif
    for (jj=0; jj < nz; jj++){
      *(row+jj+tid*nz)= calcRforce(*(R+ii),*(z+jj),0.,0.,npot,potentialArgs);
    }
    put_row(out,ii,row+tid*nz,nz); 
  }
  for (ii=0; ii < npot; ii++) {
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
  free(row);
}
void calc_zforce(int nR,
		 double *R,
		 int nz,
		 double *z,
		 int npot,
		 int * pot_type,
		 double * pot_args,
		 double *out,
		 int * err){
  int ii, jj, tid, nthreads;
#ifdef _OPENMP
  nthreads = omp_get_max_threads();
#else
  nthreads = 1;
#endif
  double * row= (double *) malloc ( nthreads * nz * ( sizeof ( double ) ) );
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_leapFuncArgs_Full(npot,potentialArgs,pot_type,pot_args);
  //Run through the grid and calculate
  UNUSED int chunk= CHUNKSIZE;
#pragma omp parallel for schedule(static,chunk) private(ii,tid,jj)	\
  shared(row,npot,potentialArgs,R,z,nR,nz)
  for (ii=0; ii < nR; ii++){
#ifdef _OPENMP
    tid= omp_get_thread_num();
#else
    tid = 0;
#endif
    for (jj=0; jj < nz; jj++){
      *(row+jj+tid*nz)= calczforce(*(R+ii),*(z+jj),0.,0.,npot,potentialArgs);
    }
    put_row(out,ii,row+tid*nz,nz); 
  }
  for (ii=0; ii < npot; ii++) {
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
  free(row);
}
void eval_potential(int nR,
		    double *R,
		    double *z,
		    int npot,
		    int * pot_type,
		    double * pot_args,
		    double *out,
		    int * err){
  int ii;
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_actionAngleArgs(npot,potentialArgs,pot_type,pot_args);
  //Run through and evaluate
  for (ii=0; ii < nR; ii++){
    *(out+ii)= evaluatePotentials(*(R+ii),*(z+ii),npot,potentialArgs);
  }
  for (ii=0; ii < npot; ii++) {
    if ( (potentialArgs+ii)->i2d )
      interp_2d_free((potentialArgs+ii)->i2d) ;
    if ((potentialArgs+ii)->accx )
      gsl_interp_accel_free ((potentialArgs+ii)->accx);
    if ((potentialArgs+ii)->accy )
      gsl_interp_accel_free ((potentialArgs+ii)->accy);
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
}
void eval_rforce(int nR,
		 double *R,
		 double *z,
		 int npot,
		 int * pot_type,
		 double * pot_args,
		 double *out,
		 int * err){
  int ii;
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_leapFuncArgs_Full(npot,potentialArgs,pot_type,pot_args);
  //Run through and evaluate
  for (ii=0; ii < nR; ii++){
    *(out+ii)= calcRforce(*(R+ii),*(z+ii),0.,0.,npot,potentialArgs);
  }
  for (ii=0; ii < npot; ii++) {
    if ( (potentialArgs+ii)->i2drforce )
      interp_2d_free((potentialArgs+ii)->i2drforce) ;
    if ((potentialArgs+ii)->accxrforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accxrforce );
    if ((potentialArgs+ii)->accyrforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accyrforce );
    if ( (potentialArgs+ii)->i2dzforce )
      interp_2d_free((potentialArgs+ii)->i2dzforce) ;
    if ((potentialArgs+ii)->accxzforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accxzforce );
    if ((potentialArgs+ii)->accyzforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accyzforce );
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
}
void eval_zforce(int nR,
		 double *R,
		 double *z,
		 int npot,
		 int * pot_type,
		 double * pot_args,
		 double *out,
		 int * err){
  int ii;
  //Set up the potentials
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_leapFuncArgs_Full(npot,potentialArgs,pot_type,pot_args);
  //Run through and evaluate
  for (ii=0; ii < nR; ii++){
    *(out+ii)= calczforce(*(R+ii),*(z+ii),0.,0.,npot,potentialArgs);
  }
  for (ii=0; ii < npot; ii++) {
    if ( (potentialArgs+ii)->i2drforce )
      interp_2d_free((potentialArgs+ii)->i2drforce) ;
    if ((potentialArgs+ii)->accxrforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accxrforce );
    if ((potentialArgs+ii)->accyrforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accyrforce );
    if ( (potentialArgs+ii)->i2dzforce )
      interp_2d_free((potentialArgs+ii)->i2dzforce) ;
    if ((potentialArgs+ii)->accxzforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accxzforce );
    if ((potentialArgs+ii)->accyzforce )
      gsl_interp_accel_free ((potentialArgs+ii)->accyzforce );
    free((potentialArgs+ii)->args);
  }
  free(potentialArgs);
}
