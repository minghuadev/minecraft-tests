
#ifndef TEST8_DEC_HPP_H
#define TEST8_DEC_HPP_H

#include <typeinfo>
#include <string>

#include <boost/fusion/include/sequence.hpp>
#include <boost/fusion/include/algorithm.hpp>
#include <boost/fusion/include/adapt_struct.hpp>
#include <boost/fusion/include/is_sequence.hpp>
#include <boost/mpl/eval_if.hpp>
#include <boost/type_traits.hpp> // is_array, is_class, remove_bounds
#include <boost/lexical_cast.hpp>
#include <cxxabi.h>
#include <stdio.h>

extern int dec_indents; /* 0, 4, 8, ... */
struct NL {
    static void print() { printf("\n");
        for (int i=0; i<dec_indents; i++) printf(" ");
    }
};

template <typename T2> struct Dec_s;

template <typename S, typename N> struct Comma {
  static inline void comma() { printf(" , "); }
};
template <typename S> struct Comma<S, typename
 boost::mpl::prior<typename boost::fusion::result_of::size<S>::type >::type> {
   static inline void comma() {}
};

template <typename S, typename N> struct DecImplSeqItr_s {
  typedef typename boost::fusion::result_of::value_at<S, N>::type current_t;
  typedef typename boost::mpl::next<N>::type next_t;
  typedef boost::fusion::extension::struct_member_name<S, N::value> name_t;
  static inline void decode(S& s) {
    printf(" \"%s\" = ", name_t::call() );
    Dec_s<current_t>::decode(boost::fusion::at<N>(s));
    Comma<S, N>::comma();  // Insert comma or not
    DecImplSeqItr_s<S, next_t>::decode(s);
  }
};
template <typename S>
struct DecImplSeqItr_s<S, typename boost::fusion::result_of::size<S>::type > {
    static inline void decode(S& s) { }
};
template <typename S>
struct DecImplSeqStart_s:DecImplSeqItr_s<S, boost::mpl::int_<0> > {};

template <typename S> struct DecImplSeq_s {
  typedef DecImplSeq_s<S> type;
  static void decode(S & s) {
    printf("  struct  start --- { --- ");
    dec_indents += 4;
    NL::print();
    DecImplSeqStart_s<S>::decode(s);
    dec_indents -= 4;
    NL::print();
    printf("  struct  done  --- } --- ");
    NL::print();
  };
};

template <typename T2> struct DecImplArray_s {
  typedef DecImplArray_s<T2> type;
  typedef typename boost::remove_bounds<T2>::type slice_t;
  static const size_t size = sizeof(T2) / sizeof(slice_t);
  static inline void decode(T2 & t) {
    printf("  array start --- [ --- ");
    dec_indents += 4;
    NL::print();
    for(size_t idx=0; idx<size; idx++) {
        Dec_s<slice_t>::decode(t[idx]);
        if (idx < size-1) {
            NL::print(); printf(" , ");
        }
    }
    dec_indents -= 4;
    NL::print();
    printf("  array done  --- ] --- \n");
    NL::print();
  }
};

template <typename T2> struct DecImplVoid_s {
  typedef DecImplVoid_s<T2> type;
  static void decode(T2   & t) {
    int status = 0;
    const char *realname = abi::__cxa_demangle(typeid(t).name(),0,0,&status);
#if 0
    printf("  typename: %s  value: %s  realname: %s\n", typeid(t).name(),
           boost::lexical_cast<std::string>(t).c_str(), realname);
    NL::print();
#else
    printf(" type %s", realname);
    NL::print();
#endif
  };
};

template <typename T2> struct DecCalc_s {
  typedef
    typename boost::mpl::eval_if< boost::fusion::traits::is_sequence<T2>, 
                                  DecImplSeq_s<T2>,
    typename boost::mpl::eval_if< boost::is_array<T2>,
                                  boost::mpl::identity< DecImplArray_s<T2> >,
    DecImplVoid_s<T2>   > >
  ::type type;
};

template <typename T2> struct Dec_s : public DecCalc_s<T2>::type { };

#endif /* #ifndef TEST8_DEC_HPP_H */

