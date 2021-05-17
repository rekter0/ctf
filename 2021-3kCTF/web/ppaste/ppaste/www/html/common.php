<?php
session_start();
$db = new SQLite3('../db/ppaste.db');
function ci($i){
	return SQLite3::escapeString($i);
}
function sqlArray($q){
	global $db;
	$res = $db->query($q);
	$a=array();
	while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
		$a[]=$row;
	}
	return $a;
}
function uExists($u){
	return (@count(@sqlArray("SELECT * FROM users WHERE user='".ci($u)."'")[0])>0)?True:False;
}
function puts($status,$data=NULL){
	header("Content-Type: application/json");
	echo json_encode(array(
							"STATUS"=>($status===1?"success":"error"),
							"DATA"=>($data!==NULL?$data:NULL)
						  )
					);
	exit;
}
function qInternal($endpoint,$payload=null){
	$url = 'http://localhost:8082/'.$endpoint;
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
	if($payload!==null){
		curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
	}
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$result = curl_exec($ch);
	curl_close($ch);
	return(@$result?$result:'false');
}

function whoami(){
	return @sqlArray("SELECT * FROM users WHERE user='".ci($_SESSION['usr']['user'])."' limit 0,1")[0];
}

function myPastes(){
	return @sqlArray("SELECT id,title,content FROM pastes WHERE user='".ci($_SESSION['usr']['user'])."'");
}


