

cdef extern from "include/SparseVectorExt.h":  
   cdef cppclass SparseVectorExt[T]:  
      int nonZeros()
      int rows()
      int size() 
      SparseVectorExt() 
      SparseVectorExt(int)
      SparseVectorExt(SparseVectorExt[T]) 
      SparseVectorExt[T] abs()
      SparseVectorExt[T] add(SparseVectorExt[T]&)
      SparseVectorExt[T] hadamard(SparseVectorExt[T]&)
      SparseVectorExt[T] negate()
      SparseVectorExt[T] subtract(SparseVectorExt[T]&)
      T coeff(int)
      T dot(SparseVectorExt[T]&)
      T sumValues()
      void fill(T)
      void insertVal(int, T) 
      void nonZeroInds(long*)
      void nonZeroVals(T*)
      void reserve(int)
      void scalarMultiply(double)
      void slice(int*, int, SparseVectorExt[T]*) 
      
cdef class csarray1d_signed_char:
    cdef SparseVectorExt[signed char] *thisPtr   
cdef class csarray1d_short:
    cdef SparseVectorExt[short] *thisPtr   
cdef class csarray1d_int:
    cdef SparseVectorExt[int] *thisPtr   
cdef class csarray1d_long:
    cdef SparseVectorExt[long] *thisPtr   
cdef class csarray1d_float:
    cdef SparseVectorExt[float] *thisPtr   
cdef class csarray1d_double:
    cdef SparseVectorExt[double] *thisPtr   
