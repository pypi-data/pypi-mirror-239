
#ifdef DEC
/* MAXNUMF = 2^127 * (1 - 2^-24) */
__device__ float MAXNUMF = 1.7014117331926442990585209174225846272e38;
__device__ float MAXLOGF = 88.02969187150841;
__device__ float MINLOGF = -88.7228391116729996; /* log(2^-128) */
#else
/* MAXNUMF = 2^128 * (1 - 2^-24) */
__device__ float MAXNUMF = 3.4028234663852885981170418348451692544e38;
__device__ float MAXLOGF = 88.72283905206835;
__device__ float MINLOGF = -103.278929903431851103; /* log(2^-149) */
#endif

__device__ float LOG2EF = 1.44269504088896341;
__device__ float LOGE2F = 0.693147180559945309;
__device__ float SQRTHF = 0.707106781186547524;
__device__ float PIF = 3.141592653589793238;
__device__ float PIO2F = 1.5707963267948966192;
__device__ float PIO4F = 0.7853981633974483096;
__device__ float MACHEPF = 5.9604644775390625E-8;
