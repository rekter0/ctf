#!/usr/bin/perl
print "+ Auth?> ";
my $Auth = <STDIN>;
chomp $Auth;
if ($Auth ne '35ec04cd3b79ab89896836c69257ce86487cf55f'){
	exit();
}


print "+ Who r u?: ";
my $name = <STDIN>;
chomp $name;
$name=~s/\.//g;
$name=~s/\///g;
$name=~s/ //g;
my $points = 0;
my $gold   = 0;
my $goldrequired = 250;

while(show_help() and $uInput = <STDIN>){
	chomp $uInput;
	if($uInput eq "1"){
		my $rand1 = int(rand(100));
		my $rand2 = int(rand(100));
		my $res = $rand1 + $rand2;

		print "Lets do math, i can only do addition\n";
		print "$rand1 + $rand2 ?\n> ";
		my $subm = <STDIN>;
		chomp $subm;

		if( int($subm) == $res ){
			if($points<=1000){
				$points++;
			}
		}else{
			$points--;
		}


	}elsif($uInput eq "2"){
		print "? how much points u wanna spend\n";
		print "! 1 GOLD = 1000 POINTS\n> ";
		my $subm = <STDIN>;
		chomp $subm;
		if( ($subm) <= $points and int($subm)>=0 ){
			$points -= ($subm);
			$gold   += ($subm)/1000;
		}

	}elsif($uInput eq "3"){
		print "? how much gold u wanna spend\n";
		print "! 1 GOLD = 1000 POINTS\n> ";
		my $subm = <STDIN>;
		chomp $subm;
		if( ($subm) <= $gold  and int($subm)>=0){
			$gold   -= ($subm);
			$points += ($subm)*1000;
		}
	}elsif($uInput eq "4"){
		if($gold<=$goldrequired){
			print "! you no gold\n";
			print "! no scoreboard for u\n";
		}else{
			#$score = qx/for i in \$(ls -t \/app\/files | head -5); do printf "\$i:"; cat "\/app\/files\/\$i"; echo ""; done;/;
			$score = "Temporarily disabled\n";
			print $score;
		}
	}elsif($uInput eq "5"){
		if($gold<=$goldrequired){
			print "! no";
		}else{
			print "LOAD GAME SAVE...\n";
			open (SAVEGAME, "/app/files/".$name) or break;
			while ($line = <SAVEGAME>) {
				chomp $line;
			    $gold = $line ;
			    close(SAVEGAME);
			    print "SAVE LOADED\n";
			    break;
			}
		}
		
		
	}elsif($uInput eq "6"){
		if($gold<=$goldrequired){
			print "! no";
		}else{
			print "SAVING GAME...\n";
			open(SAVEGAME, '>', "/app/files/".$name) or break;
			print SAVEGAME $gold;
			close(SAVEGAME);
			print "GAME SAVED \n";
		}
	}elsif($uInput eq "7"){
		exit();
	}
}


sub show_help{
	print "\n\n? What you wanna do <$name>\n";
	print "* u hav $points points\n";
	print "* u hav $gold gold\n";
	print "[1] DO MATH\n";
	print "[2] BUY GOLD\n";
	print "[3] SELL GOLD\n";
	print "[4] SCOREBOARD\n";
	print "[5] LOAD GAME\n";
	print "[6] SAVE GAME\n";
	print "[7] EXIT\n";
	print "> ";
}

