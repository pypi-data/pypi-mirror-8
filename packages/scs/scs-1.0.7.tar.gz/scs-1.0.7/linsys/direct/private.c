#include "private.h"

static timer linsysTimer;
static scs_float totalSolveTime;

char * getLinSysMethod(Data * d, Priv * p) {
	char * tmp = scs_malloc(sizeof(char) * 128);
	sprintf(tmp, "sparse-direct, nnz in A = %li", (long) d->A->p[d->n]);
	return tmp;
}

char * getLinSysSummary(Priv * p, Info * info) {
	char * str = scs_malloc(sizeof(char) * 128);
	scs_int n = p->L->n;
	sprintf(str, "\tLin-sys: nnz in L factor: %li, avg solve time: %1.2es\n", (long ) (p->L->p[n] + n),
			totalSolveTime / (info->iter + 1) / 1e3);
	totalSolveTime = 0;
	return str;
}

void freePriv(Priv * p) {
	if (p) {
		if (p->L)
			cs_spfree(p->L);
		if (p->P)
			scs_free(p->P);
		if (p->D)
			scs_free(p->D);
		if (p->bp)
			scs_free(p->bp);
		scs_free(p);
	}
}

cs * formKKT(Data * d) {
	/* ONLY UPPER TRIANGULAR PART IS STUFFED
	 * forms column compressed KKT matrix
	 * assumes column compressed form A matrix
	 *
	 * forms upper triangular part of [I A'; A -I]
	 */
	scs_int j, k, kk;
	cs * K_cs;
	AMatrix * A = d->A;
	/* I at top left */
	const scs_int Anz = A->p[d->n];
	const scs_int Knzmax = d->n + d->m + Anz;
	cs * K = cs_spalloc(d->m + d->n, d->m + d->n, Knzmax, 1, 1);

#ifdef EXTRAVERBOSE
	scs_printf("forming KKT\n");
#endif

	if (!K) {
		return NULL;
	}
	kk = 0;
	for (k = 0; k < d->n; k++) {
		K->i[kk] = k;
		K->p[kk] = k;
		K->x[kk] = d->rho_x;
		kk++;
	}
	/* A^T at top right : CCS: */
	for (j = 0; j < d->n; j++) {
		for (k = A->p[j]; k < A->p[j + 1]; k++) {
			K->p[kk] = A->i[k] + d->n;
			K->i[kk] = j;
			K->x[kk] = A->x[k];
			kk++;
		}
	}
	/* -I at bottom right */
	for (k = 0; k < d->m; k++) {
		K->i[kk] = k + d->n;
		K->p[kk] = k + d->n;
		K->x[kk] = -1;
		kk++;
	}
	/* assert kk == Knzmax */
	K->nz = Knzmax;
	K_cs = cs_compress(K);
	cs_spfree(K);
	return (K_cs);
}

scs_int LDLInit(cs * A, scs_int P[], scs_float **info) {
	*info = (scs_float *) scs_malloc(AMD_INFO * sizeof(scs_float));
#ifdef DLONG
	return(amd_l_order(A->n, A->p, A->i, P, (scs_float *) NULL, *info));
#else
	return (amd_order(A->n, A->p, A->i, P, (scs_float *) NULL, *info));
#endif
}

scs_int LDLFactor(cs * A, scs_int P[], scs_int Pinv[], cs **L, scs_float **D) {
	scs_int kk, n = A->n;
	scs_int * Parent = scs_malloc(n * sizeof(scs_int));
	scs_int * Lnz = scs_malloc(n * sizeof(scs_int));
	scs_int * Flag = scs_malloc(n * sizeof(scs_int));
	scs_int * Pattern = scs_malloc(n * sizeof(scs_int));
	scs_float * Y = scs_malloc(n * sizeof(scs_float));
	(*L)->p = (scs_int *) scs_malloc((1 + n) * sizeof(scs_int));

	/*scs_int Parent[n], Lnz[n], Flag[n], Pattern[n]; */
	/*scs_float Y[n]; */

	LDL_symbolic(n, A->p, A->i, (*L)->p, Parent, Lnz, Flag, P, Pinv);

	(*L)->nzmax = *((*L)->p + n);
	(*L)->x = (scs_float *) scs_malloc((*L)->nzmax * sizeof(scs_float));
	(*L)->i = (scs_int *) scs_malloc((*L)->nzmax * sizeof(scs_int));
	*D = (scs_float *) scs_malloc(n * sizeof(scs_float));

	if (!(*D) || !(*L)->i || !(*L)->x || !Y || !Pattern || !Flag || !Lnz || !Parent)
		return -1;

#ifdef EXTRAVERBOSE
	scs_printf("numeric factorization\n");
#endif
	kk = LDL_numeric(n, A->p, A->i, A->x, (*L)->p, Parent, Lnz, (*L)->i, (*L)->x, *D, Y, Pattern, Flag, P, Pinv);
#ifdef EXTRAVERBOSE
	scs_printf("finished numeric factorization\n");
#endif

	scs_free(Parent);
	scs_free(Lnz);
	scs_free(Flag);
	scs_free(Pattern);
	scs_free(Y);
	return (n - kk);
}

void LDLSolve(scs_float *x, scs_float b[], cs * L, scs_float D[], scs_int P[], scs_float * bp) {
	/* solves PLDL'P' x = b for x */
	scs_int n = L->n;
	if (P == NULL) {
		if (x != b) /* if they're different addresses */
			memcpy(x, b, n * sizeof(scs_float));
		LDL_lsolve(n, x, L->p, L->i, L->x);
		LDL_dsolve(n, x, D);
		LDL_ltsolve(n, x, L->p, L->i, L->x);
	} else {
		LDL_perm(n, bp, b, P);
		LDL_lsolve(n, bp, L->p, L->i, L->x);
		LDL_dsolve(n, bp, D);
		LDL_ltsolve(n, bp, L->p, L->i, L->x);
		LDL_permt(n, x, bp, P);
	}
}

void _accumByAtrans(scs_int n, scs_float * Ax, scs_int * Ai, scs_int * Ap, const scs_float *x, scs_float *y) {
	/* y  = A'*x
	 A in column compressed format
	 parallelizes over columns (rows of A')
	 */
	scs_int p, j;
	scs_int c1, c2;
	scs_float yj;
#ifdef OPENMP
#pragma omp parallel for private(p,c1,c2,yj)
#endif
	for (j = 0; j < n; j++) {
		yj = y[j];
		c1 = Ap[j];
		c2 = Ap[j + 1];
		for (p = c1; p < c2; p++) {
			yj += Ax[p] * x[Ai[p]];
		}
		y[j] = yj;
	}
}

void _accumByA(scs_int n, scs_float * Ax, scs_int * Ai, scs_int * Ap, const scs_float *x, scs_float *y) {
	/*y  = A*x
	 A in column compressed format
	 this parallelizes over columns and uses
	 pragma atomic to prevent concurrent writes to y
	 */
	scs_int p, j;
	scs_int c1, c2;
	scs_float xj;
	/*#pragma omp parallel for private(p,c1,c2,xj)  */
	for (j = 0; j < n; j++) {
		xj = x[j];
		c1 = Ap[j];
		c2 = Ap[j + 1];
		for (p = c1; p < c2; p++) {
			/*#pragma omp atomic */
			y[Ai[p]] += Ax[p] * xj;
		}
	}
}

void accumByAtrans(Data * d, Priv * p, const scs_float *x, scs_float *y) {
	AMatrix * A = d->A;
	_accumByAtrans(d->n, A->x, A->i, A->p, x, y);
}

void accumByA(Data * d, Priv * p, const scs_float *x, scs_float *y) {
	AMatrix * A = d->A;
	_accumByA(d->n, A->x, A->i, A->p, x, y);
}

scs_int factorize(Data * d, Priv * p) {
	scs_float *info;
	scs_int *Pinv, amd_status, ldl_status;
	cs *C, *K = formKKT(d);
	if (!K) {
		return -1;
	}
	amd_status = LDLInit(K, p->P, &info);
	if (amd_status < 0)
		return (amd_status);
#ifdef EXTRAVERBOSE
	if(d->verbose) {
		scs_printf("Matrix factorization info:\n");
#ifdef DLONG
		amd_l_info(info);
#else
		amd_info(info);
#endif
	}
#endif
	Pinv = cs_pinv(p->P, d->n + d->m);
	C = cs_symperm(K, Pinv, 1);
	ldl_status = LDLFactor(C, NULL, NULL, &p->L, &p->D);
	cs_spfree(C);
	cs_spfree(K);
	scs_free(Pinv);
	scs_free(info);
	return (ldl_status);
}

Priv * initPriv(Data * d) {
	Priv * p = scs_calloc(1, sizeof(Priv));
	scs_int n_plus_m = d->n + d->m;
	p->P = scs_malloc(sizeof(scs_int) * n_plus_m);
	p->L = scs_malloc(sizeof(cs));
	p->bp = scs_malloc(n_plus_m * sizeof(scs_float));
	p->L->m = n_plus_m;
	p->L->n = n_plus_m;
	p->L->nz = -1;

	if (factorize(d, p) < 0) {
		freePriv(p);
		return NULL;
	}
	totalSolveTime = 0.0;
	return p;
}

scs_int solveLinSys(Data * d, Priv * p, scs_float * b, const scs_float * s, scs_int iter) {
	/* returns solution to linear system */
	/* Ax = b with solution stored in b */
	tic(&linsysTimer);
	LDLSolve(b, b, p->L, p->D, p->P, p->bp);
	totalSolveTime += tocq(&linsysTimer);
#ifdef EXTRAVERBOSE
	scs_printf("linsys solve time: %1.2es\n", tocq(&linsysTimer) / 1e3);
#endif
	return 0;
}

