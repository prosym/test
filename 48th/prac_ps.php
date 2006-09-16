<?php
require_once "prac_conf.php";
session_start();

//処理部分-------------------------------------------------
if($_POST['state']=='confirm'){
/*-- 「参加申し込み」が押された時 ------------------------*/
	//POST値受け取り
	import_request_variables('p','');
	$Pname   = $Pname1." ".$Pname2;
	$Pkana   = $Pkana1." ".$Pkana2;
	$Phone   = $Phone1."-".$Phone2."-".$Phone3;
	$Papost  = $Papost1."-".$Papost2;
	$Paddr   = $Paddr1.$Paddr2.$Paddr3;
	$Psday   = $Psdayyear.'/'.$Psdaymonth.'/'.$Psdayday;
	//タグの無効化と","をピリオドへ置換
	$Pname   = htmlspecialchars($Pname);	$Pname   = str_replace(',','.',$Pname);
	$Pkana   = htmlspecialchars($Pkana);	$Pkana   = str_replace(',','.',$Pkana);
	$Porg    = htmlspecialchars($Porg); 	$Porg    = str_replace(',','.',$Porg);
	$Pemail  = htmlspecialchars($Pemail);	$Pemail  = str_replace(',','.',$Pemail);
	$Paddr   = htmlspecialchars($Paddr);	$Paddr   = str_replace(',','.',$Paddr);
	$Pknum   = htmlspecialchars($Pknum);	$Pknum   = str_replace(',','.',$Pknum);
	$Paite   = htmlspecialchars($Paite);	$Paite   = str_replace(',','.',$Paite);
	$Patena  = htmlspecialchars($Patena);	$Patena  = str_replace(',','.',$Patena);
	$Petc    = htmlspecialchars($Petc); 	$Petc    = str_replace(',','.',$Petc);
	$Papost  = str_replace(',','.',$Papost);
	$Phone   = str_replace(',','.',$Phone);
	$Petc    = str_replace("\r\n", "<br>", $Petc);
	$Petc    = str_replace("\r", "<br>", $Petc);
	$Petc    = str_replace("\n", "<br>", $Petc);
	if(is_array($Popt)){
		if(in_array("seikyu",$Popt)) $Popt1 = '請求書要';
		if(in_array("bunri",$Popt))  $Popt2 = '領収書分離';
		if(in_array("smoke",$Popt))  $Popt3 = '喫煙';
	}
	
	//セッションへ渡し
	$_SESSION['Pname'] =$Pname;  $_SESSION['Pname1']=$Pname1; $_SESSION['Pname2']=$Pname2;
	$_SESSION['Pkana'] =$Pkana;  $_SESSION['Pkana1']=$Pkana1; $_SESSION['Pkana2']=$Pkana2;
	$_SESSION['Psex']  =$Psex;   $_SESSION['Page']  =$Page;   $_SESSION['Porg']  =$Porg;
	$_SESSION['Paddr1']=$Paddr1; $_SESSION['Paddr2']=$Paddr2; $_SESSION['Paddr3']=$Paddr3;
	$_SESSION['Phone1']=$Phone1; $_SESSION['Phone2']=$Phone2; $_SESSION['Phone3']=$Phone3;
	$_SESSION['Pemail']=$Pemail; $_SESSION['Paddr'] =$Paddr;  $_SESSION['Psent'] =$Psent;
	$_SESSION['Phone'] =$Phone;  $_SESSION['Penter']=$Penter; $_SESSION['Pipsj'] =$Pipsj;
	$_SESSION['Pknum'] =$Pknum;  $_SESSION['Ppay']  =$Ppay;   $_SESSION['Psday'] =$Psday;
	$_SESSION['Proom'] =$Proom;  $_SESSION['Paite'] =$Paite;  $_SESSION['Patena']=$Patena;
	$_SESSION['Popt1'] =$Popt1;  $_SESSION['Popt2'] =$Popt2;  $_SESSION['Popt3'] =$Popt3;
	$_SESSION['Ppost'] =$Ppost;  $_SESSION['Ppost1']=$Ppost1; $_SESSION['Ppost2']=$Ppost2;
	$_SESSION['Petc']  =$Petc;
	
	//入力エラーチェック
	//エラー項目は$Keyxxxを1にすることで、$Errorcolor色の※を表示する
	if($Needname ==1 &&($Pname1==null || $Pname2==null)){$error[] = '氏名';        $Keyname=1;}
	if($Needkana ==1 &&($Pkana1==null || $Pkana2==null)){$error[] = 'カナ氏名';    $Keykana=1;}
	if($Needsex  ==1 && $Psex==null){                    $error[] = '性別';        $Keysex=1;}
	if($Needorg  ==1 && $Porg==null){                    $error[] = '所属';        $Keyorg=1;}
	if($Needemail==1 && $Pemail==null){                  $error[] = '電子メール';  $Keyemail=1;}
	if($Needaddr ==1 &&(    $Ppost1==null  || $Ppost2==null
		|| $Paddr1==null || $Paddr2 ==null || $Paddr3 ==null
		|| !ctype_digit($Ppost1)==1		   || !ctype_digit($Ppost2)==1)){
                                                         $error[] = '住所';         $Keyadd=1;}
	if($Needphone==1 &&($Phone1==null || $Phone2==null            ||$Phone3==null
		|| !ctype_digit($Phone1)==1   || !ctype_digit($Phone2)==1 || !ctype_digit($Phone3)==1)){
                                                         $error[] = '電話番号';     $Keyphone=1;}
	if($Needsent==1 && $Psent==null){                    $error[] = '送付区分';     $Keysent=1;}
	if(!checkdate($Psdaymonth,$Psdayday,$Psdayyear)){    $error[] = '送金/振込み日';}
	if($Needenter==1 &&($Penter==null || $Pipsj==null)){ $error[] = '参加資格';     $Keyenter=1;}
	if($Pipsj    =='会員' && $Pknum==null) {             $error[] = '会員番号';     $Keyenter=1;}
	if($Ppay==null) {                                    $error[] = '支払方法';     $Keypay=1;}
	if($Needroom ==1 && $Proom==null){                   $error[] = '希望する部屋'; $Keyroom=1;}
	if($Needatena==1 &&(is_array($Popt) 
		&& in_array("seikyu",$Popt) && $Patena==null)){  $error[] = '請求書の宛名'; $Keyopt=1;}
	$errCount=count($error);
}
//作成関数----------------------------------------
	function form_Text($name,$value,$size){
		print "<input type=text name=$name value=\"$value\" size=$size>";
	}

	function form_Radio($name,$value,$ed){
		print "<input type=radio name=$name value=\"$value\"";
		if($value==$ed) print " checked";
		print ">$value&nbsp;&nbsp;\n";
	}

	function form_Checkbox($name,$value,$ed){
		print "<input type=checkbox name=$name value=$value";
		if($ed==1) print " checked";
		print ">";
	}

	function form_Textarea($name,$value,$rows,$cols){
		print "<textarea name=$name rows=$rows cols=$cols>$value</textarea>";
	}

	function form_Pulldown($name,$low,$high,$ed){
		print "<select name=$name>\n";
		for($i=$low;$i<=$high;$i++){
			print "<option value=$i";
				if($i==$ed) print " selected";
			print ">$i</option>\n";
		}
		print "</select>\n";
	}

	//日付取得--------------------------------------------------
	function pay_day($name){
		$toyear = date("Y");
		$tomonth= date("n");
		$today  = date("j");
		$nameY=$name."year";
		$nameM=$name."month";
		$nameD=$name."day";

		form_Pulldown($nameY,$toyear-1,$toyear+1,$toyear);
		print "年\n";
		form_Pulldown($nameM,1,12,$tomonth);
		print "月\n";
		form_Pulldown($nameD,1,31,$today);
		print "日";
	}

	//テーブルと見出し作成--------------------------------------
	function tr_Making($value,$key){
		print "</td></tr>\n";
		print "<tr><td>$value";
		if($key==1) print "&nbsp;<a class=\"key\">※</a>";
		print "</td>\n<td>";
	}

//実表示部分-----------------------------------------------------
print $HEADER;
print $TITLE."\n<hr />\n";
	
if($_POST['state']=='confirm' && $errCount==0){
/*- 参加申し込みが押されてかつエラーがなかったとき -------*/
	//送信確認画面
	print "<table border=1>";
	print "<tr><td width=130></td><td width=450>";
	tr_Making('氏名',0);			print $_SESSION['Pname'];
	tr_Making('カナ氏名',0);		print $_SESSION['Pkana'];
	tr_Making('性別',0);			print $_SESSION['Psex'];
	tr_Making('年齢',0);			print $_SESSION['Page'];
	tr_Making('所属',0);			print $_SESSION['Porg'];
	tr_Making('電子メール',0);		print $_SESSION['Pemail'];
	tr_Making('住所',0);			print "〒".$_SESSION['Ppost']."<br />";
									print $_SESSION['Paddr'];
	tr_Making('送付区分',0);		print $_SESSION['Psent'];
	tr_Making('電話番号',0);		print $_SESSION['Phone'];
	tr_Making('参加資格<br />(社会人学生は一般)',0);	print $_SESSION['Penter'];
		print " / ";				print $_SESSION['Pipsj']." ".$_SESSION['Pknum'];
	tr_Making('支払方法',0);		print $_SESSION['Ppay']."<br />";
		print "送金/振り込み日 : ";	print $_SESSION['Psday'];
	tr_Making('希望する部屋 <br /> (学生は4名1室)',0);	print $_SESSION['Proom']." ".$_SESSION['Paite'];
	tr_Making('オプション',0);
		if(!is_array($Popt)) print "---";
		else{
			if(in_array("seikyu",$Popt)) print "見積書と納品書が必要(宛名：".$_SESSION['Patena'].")<br />";
			if(in_array("bunri",$Popt))  print "金額を参加費と宿泊食事費に分離する（領収書）<br />";
			if(in_array("smoke",$Popt))  print "喫煙部屋希望<br />";
		}
	tr_Making('その他ご要望',0);	print $_SESSION['Petc'];
	print "</td></tr></table>";
	
	print "<br />以上の内容で送信します。<br />\n";
	print "<table border=0><tr><td>";
	print "<form action=\"$script\" method=\"post\">";
	print "<input type=hidden name=\"state\" value=\"return\">";
	print "<input type=submit value=\" 戻る \">\n";
	print "</form></td>";
	print "<td><form action=\"$script\" method=\"post\">\n";
	print "<input type=hidden name=\"state\" value=\"save\">";
	print "<input type=submit value=\" 送信 \">\n";
	print "</form></td></tr></table>";
}
elseif($_POST['state']=='save'){
/*- 送信されたとき --------------------------------------*/
	//ログファイル保存
	$data = date("Y/m/d H:i:s");
	$data.= ",".$_SESSION['Pname'].",".$_SESSION['Pkana'].",".$_SESSION['Psex'];
	$data.= ",".$_SESSION['Page'].",".$_SESSION['Porg'].",".$_SESSION['Pemail'];
	$data.= ",".$_SESSION['Ppost'].",".$_SESSION['Paddr'].",".$_SESSION['Psent'];
	$data.= ",".$_SESSION['Phone'].",".$_SESSION['Penter'].",".$_SESSION['Pipsj'];
	$data.= ",".$_SESSION['Pknum'].",".$_SESSION['Ppay'].",".$_SESSION['Psday'];
	$data.= ",".$_SESSION['Proom'].$_SESSION['Paite'].",".$_SESSION['Popt1'];
	$data.= ",".$_SESSION['Patena'].",".$_SESSION['Popt2'].",".$_SESSION['Popt3'];
	$data.= ",".$_SESSION['Petc'];
	//ログファイルがなかった場合は作成し、あった場合は上書きする
	if(!file_exists($LogFile)){
		$fp = fopen($LogFile,'w');
	}else{
		$fp = fopen($LogFile,'a+');
	}
	flock($fp,LOCK_EX);
	fputs($fp,$data."\n");
	flock($fp,LOCK_UN);
	fclose($fp);
	
	print "<br />参加申し込みを受け付けました。<br />";
	print "<p align=\"center\"><a href=\"".$ReturnURL."\">";
	print "戻る</a></p>";
session_destroy();
}
else{
/*- 初期フォーム表示 -------------------------------------*/
	print $NOTICE."\n<hr />\n";
	
	if($errCount>=1){//エラーがある場合---------------------
		print "<p class=error>ERROR!! <br />";
		for($i=0;$i<$errCount;$i++) {
			print $error[$i];
			if($i<$errCount-1) print ", ";
		}
		print "の項目が未入力もしくは不正です。</p>";
	}
	
	print "<form action=\"$script\" method=\"post\">\n";
	print "<table border=1>";
	print "<tr><td width=130></td><td width=450>";
	tr_Making('氏名',$Keyname);
		print "名字 :";				form_Text(Pname1,$_SESSION['Pname1'],20);
		print "名前 :";				form_Text(Pname2,$_SESSION['Pname2'],20);
	tr_Making('カナ氏名',$Keykana);
		print "名字 :";				form_Text(Pkana1,$_SESSION['Pkana1'],20);
		print "名前 :";				form_Text(Pkana2,$_SESSION['Pkana2'],20);
	tr_Making('性別',$Keysex);
									form_Radio(Psex,'男性',$_SESSION['Psex']);
									form_Radio(Psex,'女性',$_SESSION['Psex']);
	tr_Making('年齢',$Keyage);		form_Pulldown(Page,18,99,$_SESSION['Page']);
		print "歳&nbsp;&nbsp;（部屋割りの参考にさせて頂きますが，必須ではありません";
	tr_Making('所属',$Keyorg);
									form_Text(Porg,$_SESSION['Porg'],50);
	tr_Making('電子メール',$Keyemail);
									form_Text(Pemail,$_SESSION['Pemail'],50);
	tr_Making('住所',$Keyadd);
		print "〒";					form_Text(Ppost1,$_SESSION['Ppost1'],3);
		print "-";					form_Text(Ppost2,$_SESSION['Ppost2'],5);
		print "<br />都道府県 :";	form_Text(Paddr1,$_SESSION['Paddr1'],10);
		print "市町村 :";			form_Text(Paddr2,$_SESSION['Paddr2'],20);
		print "<br />番地 :";		form_Text(Paddr3,$_SESSION['Paddr3'],75);
	tr_Making('送付区分',$Keysent);
		form_Radio(Psent,'自宅',  $_SESSION['Psent']);
		form_Radio(Psent,'勤務先',$_SESSION['Psent']);
	tr_Making('電話番号',$Keyphone);
									form_Text(Phone1,$_SESSION['Phone1'],7);
		print " - ";				form_Text(Phone2,$_SESSION['Phone2'],7);
		print " - ";				form_Text(Phone3,$_SESSION['Phone3'],7);
	tr_Making('参加資格<br />(社会人学生は一般)',$Keyenter);
		form_Radio(Penter,'一般',$_SESSION['Penter']);
		form_Radio(Penter,'学生',$_SESSION['Penter']);
		form_Radio(Penter,'発表学生',$Penter);			print "<hr size=1 />";
		form_Radio(Pipsj,'会員',$_SESSION['Pipsj']);		print "(会員番号 : ";
		form_Text(Pknum,$_SESSION['Pknum'],20);			print ")";
		form_Radio(Pipsj,'非会員',$_SESSION['Pipsj']);
	tr_Making('支払方法',$Keypay);
		form_Radio(Ppay,$Payment1,$_SESSION['Ppay']);	print "<br />";
		form_Radio(Ppay,$Payment2,$_SESSION['Ppay']);	print "<br />";
		form_Radio(Ppay,$Payment3,$_SESSION['Ppay']);	print "<br />";
		print "送金/振り込み日";						pay_day(Psday);
	tr_Making('希望する部屋 <br /> (学生は4名1室)',$Keyroom);
		form_Radio(Proom,$Stay1,$_SESSION['Proom']);			print $Stay1cost."<br />";
		form_Radio(Proom,$Stay2,$_SESSION['Proom']);			print $Stay2cost." 同室相手";
				form_Text(Paite,$_SESSION['Paite'],25);			print "<br />";
		form_Radio(Proom,$Stay3,$_SESSION['Proom']);			print $Stay3cost." 同室相手";
				form_Text(Paite,$_SESSION['Paite'],25);			print "<br />";
		form_Radio(Proom,$Stay4,$_SESSION['Proom']);			print $Stay4cost." 同室相手";
				form_Text(Paite,$_SESSION['Paite'],25);			print "<br />";
		print "※希望通りにならない場合もあります<br />";
	tr_Making('オプション',$Keyopt);
			if(is_array($Popt) && in_array(seikyu,$Popt)) $ed=1;
			else $ed=0;
		form_Checkbox('Popt[]',"seikyu",$ed);	print "見積書と納品書が必要\n";
		print "--請求書の宛名";					form_Text(Patena,$_SESSION['Patena'],30);
		print "<br />\n";
			if(is_array($Popt) && in_array(bunri,$Popt)) $ed=1;
			else $ed=0;
		form_Checkbox('Popt[]',"bunri",$ed);	print "金額を参加費と宿泊食事費に分離する（領収書）<br />\n";
			if(is_array($Popt) && in_array(smoke,$Popt)) $ed=1;
			else $ed=0;
		form_Checkbox('Popt[]',"smoke",$ed);	print "喫煙部屋希望<br />\n";
	tr_Making('その他ご要望',$etckey);				form_Textarea(Petc,$_SESSION['Petc'],4,60);
	print "</td></tr></table>";
	
	print "<input type=hidden name=\"state\" value=\"confirm\">\n";
	print "<input type=submit value=\"参加申し込み\">\n";
	print "</form>\n";
	
	}
	print $FOOTER;
?>
