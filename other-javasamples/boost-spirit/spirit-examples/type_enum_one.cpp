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
#include <iostream>
#include <vector>
#include <string>

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

///////////////////////////////////////////////////////////////////////////////
//
//  Our comma separated list parser
//
///////////////////////////////////////////////////////////////////////////////
bool
parse_numbers(char const* str, vector<string>& v, size_t len, string & nm)
{
    const char * s0 = str;
    const char * s1 = str+len;
    cout << "str: " << (s1-s0) << endl;

    skip_grammar skip_rule;
    identif_grammar identif_rule;

    string itm;
    string val;

    parse_info<> result = 
        parse(s0, s1, 

        //  Begin grammar
        (
            str_p("enum") >> identif_rule[assign_a(nm)] >> '{' >> 
            ( identif_rule[assign_a(itm)][clear_a(val)] >> 
              *( '=' >> ( identif_rule | int_p | hex_p )[assign_a(val)] ))[push_back_a(v, itm)] 
            >> *(',' >> identif_rule[push_back_a(v)]) >> eps_p 
        )
        ,
        //  End grammar

        skip_rule );

    cout << "str: " << (s1-s0) << endl;
    cout << "result:" << endl;
    cout << "hit: " << result.hit << " full: " << result.full << " length: " << result.length << endl;
    cout << "stop: " << (result.stop -s0) << endl;
    string rest(result.stop, s1);
    cout << "rest: " << rest << " size: " << rest.size() << endl;
    return result.full;
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

    string str;
    while (getline(cin, str))
    {
        if (str.empty() || str[0] == 'q' || str[0] == 'Q')
            break;

        vector<string> v;
        string nm;
        if ( parse_numbers(str.c_str(), v, str.size(), nm ))
        {
            cout << "-------------------------\n";
            cout << "Parsing succeeded\n";
            cout << str << " Parses OK: " << nm << " " << endl;

            for (vector<string>::size_type i = 0; i < v.size(); ++i)
                cout << i << ": " << v[i] << endl;

            cout << "-------------------------\n";
        }
        else
        {
            cout << "-------------------------\n";
            cout << "Parsing failed\n";
            cout << "-------------------------\n";
        }
    }

    cout << "Bye... :-) \n\n";
    return 0;
}


