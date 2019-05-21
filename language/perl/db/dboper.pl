#! /usr/bin/perl -w

use strict;
use DBI;

my $host = "47.103.14.52";
my $driver = "mysql";
my $database = "RUNOOB";

my $dsn = "DBI:$driver:database=$database:$host";
my $userid = "root";
my $password = "root";

# 连接数据库
my $dbh = DBI->connect($dsn, $userid, $password) or die $DBI::errstr;
my $sth = $dbh->prepare('show variables like "%dir%" ');
$sth->execute();

while ( my @row = $sth->fetchrow_array() )
{
    print join('\t', @row)."\n";
}
$sth->finish();
$dbh->disconnect();