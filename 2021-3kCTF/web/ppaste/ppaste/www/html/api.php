<?php
include 'common.php';
include '../flag.php';

if (@$_SERVER["REQUEST_METHOD"]!=="POST" OR @$_SERVER["CONTENT_TYPE"]!=="application/json") puts(0);

$uInput=@file_get_contents("php://input");
if(strlen($uInput)>512) puts(0);

$data = json_decode($uInput,true);
if(!is_array($data)) puts(0);

if(is_array(@$data['d'])){
	foreach ($data['d'] as $key => $value) {
		if(strlen($value)<4) puts(0);
	}	
}

switch (@$data['action']) {
	case 'register':
		if(@$data['d']['user'] AND @$data['d']['pass']){
			if(!@$data['d']['invite']) puts(0);
			$checkInvite = @json_decode(@qInternal("invites",json_encode(array("invite"=>$data['d']['invite']))),true);
			if($checkInvite===FALSE) puts(0);
			if(uExists($data['d']['user'])) puts(0);
			$db->exec("INSERT INTO users(user,pass,priv) VALUES ('".ci($data['d']['user'])."' ,'".ci($data['d']['pass'])."' , '0')");
			if($db->lastInsertRowID()){
				puts(1);
			}else{
				puts(0);
			}
		}
		puts(0);
		break;
	case 'login':
		if(@$data['d']['user'] AND @$data['d']['pass']){
			$tU=@sqlArray("SELECT * FROM users WHERE user='".ci($data['d']['user'])."' limit 0,1")[0];
			if(@count($tU)<1) puts(0);
			if(@$data['d']['pass']!==$tU['pass']) puts(0);
			$_SESSION['usr']=$tU;
			puts(1);
		}
		puts(0);
		break;
	case 'pastes':
		$tU=whoami();
		if(!$tU) puts(0);
		puts(1,myPastes());
		break;
	case 'new':
		$tU=whoami();
		if(!$tU) puts(0);
		if(@$data['d']['title'] AND @$data['d']['content']){
			$data['d']['title'] = preg_replace("/\s+/", "", $data['d']['title']);
			$db->exec("INSERT INTO pastes(id,title,content,user) VALUES ('".sha1(microtime().$_SESSION['usr']['user'])."', '".ci($data['d']['title'])."' ,'".ci(($data['d']['content']))."' , '".ci($_SESSION['usr']['user'])."')");
			if($db->lastInsertRowID()){
				puts(1);
			}else{
				puts(0);
			}
		}
		puts(0);
		break;
	case 'view':
		if(@$data['d']['paste_id']){
			$tP=@sqlArray("SELECT * FROM pastes WHERE id='".ci($data['d']['paste_id'])."' limit 0,1")[0];
			if(@count($tP)<1) puts(0);
			puts(1,$tP);
		}
		puts(0);
		break;
	case 'download':
		if(@$data['d']['paste_id'] AND @$data['d']['type'] ){
			$tP=@sqlArray("SELECT * FROM pastes WHERE id='".ci($data['d']['paste_id'])."' limit 0,1")[0];
			if(@count($tP)<1) puts(0);
			if($data['d']['type']==='text'){
				header('Content-Type: text/plain');
				header('Content-Disposition: attachment; filename="'.sha1(time()).'.txt"');
				echo str_repeat("-", 80)."\n--------- ".$tP['title']."\n".str_repeat("-", 80)."\n".$tP['content'];
				exit;
			}
			if($data['d']['type']==='_pdf'){
				require_once('../TCPDF/config/tcpdf_config.php');
				require_once('../TCPDF/tcpdf.php');
				$pdf = new TCPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);
				$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);
				$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
				$pdf->SetFont('helvetica', '', 9);
				$pdf->AddPage();
				$html = '<h2>'.$tP['title'].'</h2><br><h2>'.str_repeat("-", 40).'</h2><pre>'.htmlentities($tP['content'],ENT_QUOTES).'</pre>';
				$pdf->writeHTML($html, true, 0, true, 0);
				$pdf->lastPage();
				$pdf->Output(sha1(time()).'.pdf', 'D');
				exit;
			}
		}
		puts(0);
		break;
	case 'admin':
		$tU=whoami();
		if(!@$tU OR @$tU['priv']!==1) puts(0);
		$ret["invites"]=json_decode(qInternal("invites"),true);
		$ret["users"]  =json_decode(qInternal("users"),true);
		$ret["flag"]   =$flag;
		puts(1,$ret);
		break;
	default:
		puts(0);
		break;
}

puts(0);
exit;
?>
