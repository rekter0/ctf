<?php

	$url = 'http://localhost:8082/';
	$payload=False;
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
	if($payload!==null){
		curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
	}
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$result = curl_exec($ch);
	curl_close($ch);
	var_dump($result);

