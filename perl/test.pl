#use strict;
use Socket qw(EFAULT :crlf);
use Fcntl;

sub main
{
        my ($argc,@argv)=@_;
        my $ip=$argv[0];
        my $comm=$argv[1];
        #print "$host\n$comm\n";

        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time-24*3600); 
        $year+=1900;
        ++$mon;
        my $time= $year.$mon.$mday;
        my $time1;

        my $cmd="snmpwalk -v 2c -c $comm $ip 1.3.6.1.4.1.2019.4.9.111.4.1.1.26.1.49.1.49";
        my $result_string=`$cmd`;
        #SNMPv2-SMI::enterprises.2019.4.9.111.4.1.1.26.1.49.1.49.8084.1 = Gauge32: 20
        #print "$result_string\n";
        
        my $result;
        if ($result_string=~/Gauge32\:\s+(\d+)/) {
                $result=$1;
                print "$result\n";
        }

        
}

main($#ARGV,@ARGV);