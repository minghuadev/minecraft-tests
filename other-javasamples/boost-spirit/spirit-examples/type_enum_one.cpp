/*
 * type_enum_one.cpp
 *      derived from number_list.cpp
 */

/*=============================================================================
    Copyright (c) 2002-2003 Joel de Guzman
    http://spirit.sourceforge.net/

    Use, modification and distribution is subject to the Boost Software
    License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
    http://www.boost.org/LICENSE_1_0.txt)
=============================================================================*/
///////////////////////////////////////////////////////////////////////////////
//
//  This sample demontrates a parser for a comma separated list of numbers
//  This is discussed in the "Quick Start" chapter in the Spirit User's Guide.
//
//  [ JDG 5/10/2002 ]
//
///////////////////////////////////////////////////////////////////////////////
#include <boost/spirit/core.hpp>
#include <boost/spirit/utility.hpp>
#include <boost/spirit/symbols.hpp>

#include <boost/spirit/actor/push_back_actor.hpp>
#include <boost/spirit/actor/assign_actor.hpp>
#include <boost/spirit/actor/clear_actor.hpp>
#include <boost/spirit/actor/insert_at_actor.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <map>

//#include <stdlib.h> /* for strtol */
#include <boost/lexical_cast.hpp>

///////////////////////////////////////////////////////////////////////////////
using namespace std;
using namespace boost::spirit;

///////////////////////////////////////////////////////////////////////////////
struct skip_grammar : public grammar<skip_grammar>
{   template <typename ScannerT> struct definition {
        rule<ScannerT> r; rule<ScannerT> const& start() const { return r; }
        definition(skip_grammar const& /*self*/) {
            r = comment_p("//") | comment_p("/*", "*/") ;
        }
    };
};

struct identif_grammar : public grammar<identif_grammar>
{   template <typename ScannerT> struct definition {
        rule<ScannerT> r; rule<ScannerT> const& start() const { return r; }
        definition(identif_grammar const& /*self*/) {
            r = lexeme_d[ ((alpha_p | '_' | '$') >> *(alnum_p | '_' | '$')) ] ;
        }
    };
};

struct result_s {
    int    hit;
    size_t hitlen;
    size_t reslen;
    int    full;
};

///////////////////////////////////////////////////////////////////////////////
//
//  Our comma separated list parser
//
///////////////////////////////////////////////////////////////////////////////
bool
parse_numbers(char const* strarg, size_t lenarg, string & enm, vector<string>& v, 
              map<string,string> &mm, struct result_s & resu)
{
    const char * s0 = strarg;
    const char * s1 = strarg+lenarg;
    cout << "strarg: " << (s1-s0) << endl;

    skip_grammar    skip_rule;
    identif_grammar identif_rule;

    //map<string,string>::value_type k;
    //[insert_at_a(mm,k.first)] 
    string itm, val;

    parse_info<> result = 
        parse(s0, s1, 

        //  Begin grammar
        (
            str_p("enum") >> identif_rule[assign_a(enm)] >> '{' 
            >> 
                ( identif_rule[assign_a(itm)][clear_a(val)] >> 
                  *( '=' >> ( identif_rule | int_p | hex_p )[assign_a(val)] )
                )[push_back_a(v, itm)] [insert_at_a(mm,itm,val)] 
            >> 
            *(',' >> 
                ( identif_rule[assign_a(itm)][clear_a(val)] >> 
                  *( '=' >> ( identif_rule | int_p | hex_p )[assign_a(val)] )
                )[push_back_a(v, itm)] [insert_at_a(mm,itm,val)] 
             ) 
            >>  *ch_p(',') >> '}' >> eps_p 
        )
        ,
        //  End grammar

        space_p );

    cout << "str: " << (s1-s0) << endl;
    cout << "result:" << endl;
    cout << "hit: " << result.hit << " full: " << result.full << " length: " << result.length << endl;
    cout << "stop: " << (result.stop -s0) << endl;
    string rest(result.stop, s1);
    cout << "rest: " << rest << " size: " << rest.size() << endl;

    if ( result.hit ) {
        resu.hit = 1;
        resu.hitlen = (result.stop -s0);
        resu.reslen = (rest.size());
    } else {
        resu.hit = 0;
        resu.hitlen = 0;
        resu.reslen = lenarg;
    }
    if ( result.full ) {
        resu.full = 1;
    } else {
        resu.full = 0;
    }

    return result.full || result.hit;
}

////////////////////////////////////////////////////////////////////////////
//
//  Main program
//
////////////////////////////////////////////////////////////////////////////
int
main()
{
    cout << "/////////////////////////////////////////////////////////\n\n";
    cout << "\t\tA comma separated list parser for Spirit...\n\n";
    cout << "/////////////////////////////////////////////////////////\n\n";

    cout << "Give me a comma separated list of numbers.\n";
    cout << "The numbers will be inserted in a vector of numbers\n";
    cout << "Type [q or Q] to quit\n\n";

    int rc = 0; /* default ok */
    string str;
    while (getline(cin, str))
    {
        if (str.empty() || str[0] == 'q' || str[0] == 'Q')
            break;

        vector<string> v;
        string nm;
        map<string,string> m;
        struct result_s resu;
        if ( parse_numbers(str.c_str(), str.size(), nm, v, m, resu) )
        {
            cout << "-------------------------\n";
            cout << "Parsing succeeded\n";
            cout << str << " Parses OK: " << nm << " " << endl;
            
            int enumvalue = 0;
            for (vector<string>::size_type i = 0; i < v.size(); ++i) {
                string k = v[i];
                map<string,string>::iterator itr = m.find(k);
                if ( itr == m.end() ) {
                    cout << i << ": " << k << " <empty>" << endl;
                    cout << "Error: no map second value" << endl;
                    rc = 1;
                    break;
                } else {
                    string r = itr->second;
                    int t = enumvalue;
                    if ( r.size() > 0 ) {
                        //char * endp; t = strtol(r.c_str(), &endp, 10);
                        try {
                            int x = boost::lexical_cast<int>( r.c_str() );
                            t = x;
                        } catch( boost::bad_lexical_cast const& ) {
                            std::cout << "Error: input string was not valid: " 
                                             << r.c_str() << " " << std::endl;
                        }
                    }
                    cout << i << ": " << k << "==" << t << "==" << endl;
                    m.erase (itr);
                    enumvalue = t + 1;
                }
            }
            if ( rc ) {
            cout << "-------------------------\n";
                    break;
            }
            map<string,string>::iterator iter;
            for (iter = m.begin(); iter != m.end(); iter++) {
                cout << "more: " << iter->first << " " << iter->second << endl;
                    rc = 1;
            }
            if ( rc ) {
                    cout << "Error: map values not all used by the vector" << endl;
            cout << "-------------------------\n";
                    break;
            }
            cout << "-------------------------\n";
        }
        else
        {
            cout << "-------------------------\n";
            cout << "Parsing failed\n";
            cout << "-------------------------\n";
            rc = 1;
            break;
        }
    }

    cout << "Bye... :-) \n\n";
    return rc;
}


