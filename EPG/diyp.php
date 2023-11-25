<?php
header('Content-Type: application/json;charset=UTF-8');
date_default_timezone_set('Asia/Shanghai');
set_time_limit (24 * 60 * 60);
if (file_exists('./cache/e.xml')){	
	$sctimetemp = filemtime ('./cache/e.xml');
	$sctime = date("ymd",$sctimetemp);
	$xztime = date("ymd",time());
	if ($sctime<$xztime){epgqzgx();}
}else{epgqzgx();}
isset($_GET['ch']) ? $ch=$_GET['ch']:$ch = "";
isset($_GET['date']) ? $date=$_GET['date']:$date = "";
isset($_GET['id']) ? $id=$_GET['id']:$id = "";
if($ch<>""){
	$zhongwen=$ch;
}
if($id<>""){
	$zhongwen=$id;
}
if($id=="" and $ch==""){
	$zhongwen=-1;
}
$jintiantime=date('Y-m-d');
if($date==""){
	$date=$jintiantime;
}
if(file_exists('./cache/'.$date.'.txt')){
	$diypfilesjwj='./cache/'.$date.'.txt';
	$datelisttime=$date;
}else{
	$datelisttime=-1;
}
$meiyoupindao=array("url"=>"atvmao.com",
		"date"=> $date,
		"epg_data" => array(array("start"=>"00:00","end"=> "02:00","title"=>  "精彩节目"),
				array("start"=>"02:00","end"=> "04:00","title"=>  "精彩节目"),
				array("start"=>"04:00","end"=> "06:00","title"=>  "精彩节目"),
				array("start"=>"06:00","end"=> "08:00","title"=>  "精彩节目"),
				array("start"=>"08:00","end"=> "10:00","title"=>  "精彩节目"),
				array("start"=>"10:00","end"=> "12:00","title"=>  "精彩节目"),
				array("start"=>"12:00","end"=> "14:00","title"=>  "精彩节目"),
				array("start"=>"14:00","end"=> "16:00","title"=>  "精彩节目"),
				array("start"=>"16:00","end"=> "18:00","title"=>  "精彩节目"),
				array("start"=>"18:00","end"=> "20:00","title"=>  "精彩节目"),
				array("start"=>"20:00","end"=> "22:00","title"=>  "精彩节目"),
				array("start"=>"22:00","end"=> "23:59","title"=>  "精彩节目")
				),
		"channel_name"=>  $zhongwen
		);
if($zhongwen<>-1 and $datelisttime<>-1){
	$tempzfc=readover("./cache/pdlist.txt");
	$tempzdypd=readover("./cache/zdypd.txt");
	$pipeiname=preg_quote($ch,"/");
	$pipeizfcch="/<pft>".$pipeiname."\|([^<pfb>]+)/";
	if(preg_match($pipeizfcch, $tempzdypd,$pipeixtpd)){
		$zhongwen=$pipeixtpd[1];
	}elseif(preg_match($pipeizfcch, $tempzfc,$pipeixtpd)){
           		$zhongwen=$pipeixtpd[1];
	}
	$pindaonameb=json_decode(readover('./cache/list.txt'),true);
	if($pindaonameb[$zhongwen]<>""){
		$diyparray= json_decode(readover($diypfilesjwj),true);
		if(isset($diyparray[$pindaonameb[$zhongwen]]['date'])){
			if($diyparray[$pindaonameb[$zhongwen]]['date']==$date  && is_array($diyparray[$pindaonameb[$zhongwen]]['epg_data'])){
				echo json_encode($diyparray[$pindaonameb[$zhongwen]],JSON_UNESCAPED_UNICODE);
			}else{
				echo json_encode($meiyoupindao,JSON_UNESCAPED_UNICODE);;
			}
		}else{
			echo json_encode($meiyoupindao,JSON_UNESCAPED_UNICODE);
		}
	}else{
		echo json_encode($meiyoupindao,JSON_UNESCAPED_UNICODE);
	}
}else{
	echo json_encode($meiyoupindao,JSON_UNESCAPED_UNICODE);
}
function epgqzgx(){
	$xml=simplexml_load_file(epgfile('http://epg.51zmt.top:8000/e.xml.gz'));
	$xml = json_encode($xml);
	$xml =json_decode($xml, true);
	$dangt=date('Ymd');
	$xiatian=date("Y-m-d", strtotime("+1 days"));
	$delshancrwj=date("Y-m-d", strtotime("-8 days"));
	if(file_exists('./cache/'.$delshancrwj.'.txt')){
		unlink('./cache/'.$delshancrwj.'.txt');
	}
	foreach($xml["channel"] as  $row) {
		$listar[$row['@attributes']['id']]=array( 'channel_name' =>$row['display-name'],'date'=>date('Y-m-d'),'url'=>'epg.51zmt.top:8000');
		$tianx[$row['@attributes']['id']]=array( 'channel_name' =>$row['display-name'],'date'=>date("Y-m-d", strtotime("+1 days")),'url'=>'epg.51zmt.top:8000');
		$pindaomane[$row['display-name']]=$row['@attributes']['id'];
	}
	foreach($xml["programme"] as $row) {
		$cesstart=str_replace(' +0800',"",$row['@attributes']['start']);
		$cesstop=str_replace(' +0800',"",$row['@attributes']['stop']);
		$qushijian=substr($cesstart,0,8);
		$kaisstart=substr($cesstart,8,2).":".substr($cesstart,10,2);
		$jiessstart=substr($cesstop,8,2).":".substr($cesstop,10,2);
		if($dangt==$qushijian){
			$listar[$row["@attributes"]["channel"]]["epg_data"][]=array("start" => $kaisstart,"end" => $jiessstart,'title' => $row['title']);
		}else{	
			$tianx[$row["@attributes"]["channel"]]["epg_data"][]=array("start" => $kaisstart,"end" => $jiessstart,'title' => $row['title']);
		}
	}
	writeover('./cache/'.date('Y-m-d').".txt", json_encode($listar,JSON_UNESCAPED_UNICODE));
	writeover('./cache/'.$xiatian.".txt", json_encode($tianx,JSON_UNESCAPED_UNICODE));
	writeover('./cache/list.txt', json_encode($pindaomane,JSON_UNESCAPED_UNICODE));
}
function readover($filename,$method="rb")
{
	if($handle=@fopen($filename,$method)){
		flock($handle,LOCK_SH);
		$filedata=@fread($handle,filesize($filename));
		fclose($handle);
	}
	return $filedata;
}
function writeover($filename,$data,$method="rb+")
{
	touch($filename);
	$handle=fopen($filename,$method);
	flock($handle,LOCK_EX);
	fputs($handle,$data);
	if($method=="rb+") ftruncate($handle,strlen($data));
	fclose($handle);
}
function epgfile($epgxzurldz,$destination_folder="./cache/")
{
	$url = $epgxzurldz;
	$newfname = $destination_folder . basename($url);
	$file = fopen ($url, "rb");
	if($file){
		$newf = fopen ($newfname, "wb");
		if ($newf)
			while(!feof($file)) {
				fwrite($newf, fread($file, 1024 * 8 ), 1024 * 8 );
			}
	}
	if ($file) {
		fclose($file);
	}
	if ($newf) {
		fclose($newf);
	}
	$buffer_size = 4096;
	$out_file_name = str_replace('.gz', '', $newfname);
	$file = gzopen($newfname, 'rb');
	$out_file = fopen($out_file_name, 'wb');
	$str='';
	while(!gzeof($file)) {
		fwrite($out_file, gzread($file, $buffer_size));
	}
    	fclose($out_file);
    	gzclose($file);
	unlink($newfname);
	return $out_file_name;
}
?>