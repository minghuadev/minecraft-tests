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
#include <boost/spirit/actor/push_back_actor.hpp>
#include <iostream>
#include <vector>
#include <string>

///////////////////////////////////////////////////////////////////////////////
using namespace std;
using namespace boost::spirit;

///////////////////////////////////////////////////////////////////////////////
//
//  Our comma separated list parser
//
///////////////////////////////////////////////////////////////////////////////
bool
parse_numbers(char const* str, vector<double>& v, size_t len)
{
    const char * s0 = str;
    const char * s1 = str+len;
    cout << "str: " << (s1-s0) << endl;

    parse_info<> result = 
        parse(s0, s1, 

        //  Begin grammar
        (
            real_p[push_back_a(v)] >> *(',' >> real_p[push_back_a(v)]) >> eps_p
        )
        ,
        //  End grammar

        space_p);
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

        vector<double> v;
        if (parse_numbers(str.c_str(), v, str.size() ))
        {
            cout << "-------------------------\n";
            cout << "Parsing succeeded\n";
            cout << str << " Parses OK: " << endl;

            for (vector<double>::size_type i = 0; i < v.size(); ++i)
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


