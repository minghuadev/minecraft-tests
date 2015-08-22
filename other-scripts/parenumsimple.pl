#!/usr/bin/perl -w
# parenumsimple.pl  -- parse simplified c enum definitions  

use strict;

my $incomment = 0;
my @lines = <>;
my $nlines = $#lines + 1;

# evaluate comments: allow one comment per line at the line end 
my @newlines = ();
for (my $j=0; $j < $nlines; $j++) {
    my $k = $lines[$j];
    my $len = length($k);
    my $newk = "";
    for ( my $i = 0 ; $i < $len; $i++) {
        my ($c, $c2) = (substr($k, $i, 1), substr($k, $i+1, 1));
        if ( ! $incomment ) {
            if ( $c eq '/' && $c2 eq '*' ) {
                    $incomment = 1;
                    $i ++; # next char 
            } elsif ( $c eq '/' && $c2 eq '/' ) {
                    last; # next line
            } else {
                    $newk .= $c;
            }
        } elsif ( $c eq '*' && $c2 eq '/' ) {
            $incomment = 0;
            $i++; # next char
            my $rest = ($i+1 < $len-1)?substr($k, $i+1):""; 
            if ( $rest =~ m/\S+/ ) {
                    print "Error: line ", $j+1, " char ", $i, 
                          " comment must be at end of line\n";
                    print "Param: len ", $len, " at ", $i+1, 
                          " rest ", $rest, "\n";
                    print "Line: ", $k, "\n";
                    exit 1;
            }
        }
    }
    push @newlines, $newk;
}

# print comments: 
my @enumaccu = ();
my $enumvalue = 0;
my $enumstate = 0; # 1: enum <tag> , 2: enum <tag> { 
for (my $j=0; $j < $nlines; $j++) {
    my $k = $newlines[$j];
    if ( $enumstate == 0 && $k =~ m/^\s*enum\s+(.*)$/ ) {
         #  enum <tag> {
         #  enum <tag> 
         my $rest = $1;
         my $tag = "";
         if ( $rest =~ m/^(\w+[\w\d_]*)\s+\{\s*$/ ) {
             $tag = $1;
             $enumstate = 2;
         } elsif ( $rest =~ m/^(\w+[\w\d_]*)\s*$/ ) {
             $tag = $1;
             $enumstate = 1;
         } else {
             print "Error: line ", $j+1, 
                   " enum start line must be \"enum <tag> {\" ", 
                   "or \"enum <tag>\"\n";
             print "Line: ", $k, "\n";
             exit 1;
         }
         push @enumaccu, $tag;
    } elsif ( $enumstate == 1 ) {
         #  {
         if ( $k =~ m/^\s*\{\s*$/ ) {
             $enumstate = 2;
         } else {
             print "Error: line ", $j+1, 
                   " enum start without \"{\"\n";
             print "Line: ", $k, "\n";
             exit 1;
         }
    } elsif ( $enumstate == 2 ) {
         if ( $k =~ m/^\s*(\w+[\w\d_]*)\s*=\s*(\S+)\s*,\s*$/ ) {
             my ($n, $v) = ($1, $2);
             my $vpre = substr($v, 0, 2); 
             $v = hex(substr($v, 2)) if $vpre eq '0x';
             push @enumaccu, $n."=".$v;
             $enumvalue = $v + 1;
         } elsif ( $k =~ m/^\s*(\w+[\w\d_]*)\s*=\s*(\S+)\s*$/ ) {
             my ($n, $v) = ($1, $2);
             my $vpre = substr($v, 0, 2); 
             $v = hex(substr($v, 2)) if $vpre eq '0x';
             push @enumaccu, $n."=".$v;
             $enumvalue = $v + 1;
             $enumstate = 3; # last enum line
         } elsif ( $k =~ m/^\s*(\w+[\w\d_]*)\s*,\s*$/ ) {
             my ($n, $v) = ($1, $enumvalue);
             push @enumaccu, $n."=".$v;
             $enumvalue = $v + 1;
         } elsif ( $k =~ m/^\s*(\w+[\w\d_]*)\s*$/ ) {
             my ($n, $v) = ($1, $enumvalue);
             push @enumaccu, $n."=".$v;
             $enumvalue = $v + 1;
             $enumstate = 3; # last enum line
         } elsif ( $k =~ m/^\s*}.*$/ ) {
             $enumstate = 4;
         } elsif ( $k =~ m/\S+/ ) {
             print "Error: line ", $j+1, 
                   " enum value line hitting unknown char 1\n";
             print "Line: ", $k, "\n";
             exit 1;
         }
    } elsif ( $enumstate == 3 ) {
         if ( $k =~ m/^\s*}.*$/ ) {
             $enumstate = 4;
         } elsif ( $k =~ m/\S+/ ) {
             print "Error: line ", $j+1, 
                   " enum value line hitting unknown char 2\n";
             print "Line: ", $k, "\n";
             exit 1;
         }
    }
    if ( $enumstate == 4 ) {
             my $etag = shift @enumaccu;
             print "Etag: ", $etag, "\n";
             while (@enumaccu) {
                 my $eval = shift @enumaccu;
                 print "    : ", $eval, "\n";
             }
             $enumvalue = 0;
             $enumstate = 0;
             @enumaccu = ();
    }
}


