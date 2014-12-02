/*
 * key_value.cpp
 */

/* key = " value " */
bool parse_digits_u16(string &theline, string keystr, 
                                       uint16_t & result_u16)
{
  bool rc = false;
  string str_tmp;
  uint16_t u16_tmp;
    
    rc = parse( theline.c_str(),
                
                ( str_p(keystr.c_str()) >> '=' >> '"' >>
                  (+digit_p)[assign_a(str_tmp)] >> '"' ),

                space_p).full;
                
    if (rc) {
        u16_tmp = atoi(str_tmp.c_str());
        result_u16 = u16_tmp;
    }
    return rc;
}

/* [Interface {A|B|C|D} Amplitude {Input|Output} List] */
bool parse_interface_section(string &theline, char &outc, string & inout)
{
  bool rc = false;
  char c = 0;
  string dir;
    
    rc = parse( theline.c_str(),
                
                (  *blank_p >> ch_p('[') >> *blank_p >>
                   str_p("Interface") >> *blank_p >>
                   anychar_p[assign_a(c)] >> *blank_p >>
                   str_p("Amplitude") >> *blank_p >>
                   ( str_p("Input")[assign_a(dir)] ||
                     str_p("Output")[assign_a(dir)]   ) >> *blank_p >>
                   str_p("List") >> *blank_p >>
                   ch_p(']') >> *space_p
                ),
                
                nothing_p).full;
                
    if (rc) {
        outc = c;
        inout.assign(dir);
    }
    
    return rc;
}

/* key = " value "
 *    ( +(~blank_p) ) 
 *    ... >> ch_p('<') >> ( +anychar_p ) >> ch_p('>') >> ...
 */
bool parse_amp_v(string &theline, string keystr, vector<double> & resultv)
{
  bool rc = false;
  vector<double> tmpv;
    
    rc = parse( theline.c_str(),
                
                (  *blank_p >> str_p(keystr.c_str()) >> *blank_p >>
                   '=' >> *blank_p >> '"' >> *blank_p >>
                   ( +(~blank_p) ) >> *blank_p >>
                   ( real_p[push_back_a(tmpv)] >>
                     *( +blank_p >> real_p[push_back_a(tmpv)]) ) >> *blank_p >>
                   '"' >> *space_p
                ),
                
                nothing_p).full;
                
    if (rc) {
        resultv = tmpv;
    }
    
    return rc;
}



