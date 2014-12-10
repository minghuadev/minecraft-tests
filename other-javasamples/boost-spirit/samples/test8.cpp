/* compile with g++ 4.5.1: g++ -I boost_1_47_0 test7.cpp */
/* compile with g++ 4.8.3: g++ -I boost_1_46_1 test8.cpp */

#include "test8.hpp"

using namespace boost::fusion;

int dec_indents=0;

struct Foo_s { int i; typedef char j_t[10]; Foo_s::j_t j; };
BOOST_FUSION_ADAPT_STRUCT( Foo_s,  (int, i)  (Foo_s::j_t, j) )

struct Bar_s { int v; typedef Foo_s w_t[2]; Bar_s::w_t w; };
BOOST_FUSION_ADAPT_STRUCT( Bar_s, (int, v)  (Bar_s::w_t, w) )

int main(int argc, char *argv[]) {
  Bar_s f = { 2, {{ 3, "abcd" },{ 4, "defg" }} };
  Dec_s<Bar_s>::decode(f);
  return 0;
}

