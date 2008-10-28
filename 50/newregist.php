<?php
require_once "newregist_conf.php";
header('Content-Type: text/html; charset=EUC-JP');

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
	$Psday   = $Psdaymonth.'/'.$Psdayday;
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
	
	//セッションへ渡し
	$_SESSION['Pname'] =$Pname;
	$_SESSION['Pname1']=$Pname1;
	$_SESSION['Pname2']=$Pname2;
	$_SESSION['Pkana'] =$Pkana;
	$_SESSION['Pkana1']=$Pkana1;
	$_SESSION['Pkana2']=$Pkana2;
	$_SESSION['Psex']  =$Psex;
	$_SESSION['Page']  =$Page;
	$_SESSION['Porg']  =$Porg;
	$_SESSION['Paddr'] =$Paddr;
	$_SESSION['Phone1']=$Phone1;
	$_SESSION['Phone2']=$Phone2;
	$_SESSION['Phone3']=$Phone3;
	$_SESSION['Pemail']=$Pemail;
	$_SESSION['Paddr'] =$Paddr;
	$_SESSION['Psent'] =$Psent;
	$_SESSION['Phone'] =$Phone;
	$_SESSION['Penter']=$Penter;
	$_SESSION['Pipsj'] =$Pipsj;
	$_SESSION['Pknum'] =$Pknum;
	$_SESSION['Ppay']  =$Ppay;
	$_SESSION['Psday'] =$Psday;
	$_SESSION['Proom'] =$Proom;
	$_SESSION['Paite'] =$Paite;
	$_SESSION['Patena']=$Patena;
	$_SESSION['Popt1'] =$Popt1;
	$_SESSION['Popt2'] =$Popt2;
	$_SESSION['Popt3'] =$Popt3;
	$_SESSION['Papost'] =$Papost;
	$_SESSION['Papost1']=$Papost1;
	$_SESSION['Papost2']=$Papost2;
	$_SESSION['Petc']  =$Petc;
	$_SESSION['Prcpt']=$Prcpt;
	$_SESSION['Psmoke']=$Psmoke;
	
	//入力エラーチェック
	//エラー項目は$Keyxxxを1にすることで、$Errorcolor色の※を表示する
	if($Needname ==1 &&($Pname1==null || $Pname2==null)){$error[] = '氏名';        $Keyname=1;}
	if($Needkana ==1 &&($Pkana1==null || $Pkana2==null)){$error[] = 'カナ氏名';    $Keykana=1;}
	if($Needsex  ==1 && $Psex==null){                    $error[] = '性別';        $Keysex=1;}
	if($Needorg  ==1 && $Porg==null){                    $error[] = '所属';        $Keyorg=1;}
	if($Needemail==1 && $Pemail==null){                  $error[] = '電子メール';  $Keyemail=1;}
	if($Needaddr ==1 &&( $Paddr==null
		|| $Papost1==null || !ctype_digit($Papost1)==1
		|| $Papost2==null || !ctype_digit($Papost2)==1 )){
			$error[] = '住所';
			$Keyadd=1; }
	if($Needphone==1 &&($Phone1==null || $Phone2==null            ||$Phone3==null
		|| !ctype_digit($Phone1)==1   || !ctype_digit($Phone2)==1 || !ctype_digit($Phone3)==1)){
                                                         $error[] = '電話番号';     $Keyphone=1;}
	if($Needsent==1 && $Psent==null){                    $error[] = '送付区分';     $Keysent=1;}
//	if(!checkdate($Psdaymonth,$Psdayday,$Psdayyear)){    $error[] = '送金/振込み日';}
	if($Needenter==1 &&($Penter==null || $Pipsj==null)){ $error[] = '参加資格';     $Keyenter=1;}
	if($Pipsj    =='会員' && $Pknum==null) {             $error[] = '会員番号';     $Keyenter=1;}
	if($Ppay==null) {                                    $error[] = '支払方法';     $Keypay=1;}
	if($Needroom ==1 && $Proom==null){                   $error[] = '希望する部屋'; $Keyroom=1;}
	if($Needatena==1 &&(is_array($Popt) 
		&& in_array("seikyu",$Popt) && $Patena==null)){  $error[] = '請求書の宛名'; $Keyopt=1;}
	if($Needrcpt && $Prcpt==null) { $error[] = '領収書'; $Keyrcpt=1;}
	if($Needsmoke && $Psmoke==null) { $error[] = '喫煙調査'; $Keyrcpt=1;}
	$errCount=count($error);
}
//作成関数----------------------------------------
	function add_flg($isneed,$item){
		if($isneed==0) return "  ".$item;
		else return "※".$item;
	}
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

	function form_PulldownWithNone($name,$low,$high,$ed,$step){
		$none = "無回答";
		print "<select name=$name>\n";
		for($i=$low;$i<=$high;$i+=$step){
			print "<option value=$i";
				if($i==$ed) print " selected";
			print ">$i</option>\n";
		}
		print "<option value=$none>$none</option>\n";
		print "</select>\n";
	}

	function form_Pulldown($name,$low,$high,$ed,$step){
		print "<select name=$name>\n";
		for($i=$low;$i<=$high;$i+=$step){
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

//		form_Pulldown($nameY,$toyear-1,$toyear+1,$toyear,1);
//		print "年\n";
		form_Pulldown($nameM,1,12,$tomonth,1);
		print "月\n";
		form_Pulldown($nameD,1,31,$today,1);
		print "日";
		if ($nameM < 11) $nameY = $toyear+1;
		else $nameY = $toyear;
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
	tr_Making('住所',0);			print "〒".$_SESSION['Papost']."<br />";
									print $_SESSION['Paddr'];
	tr_Making('送付区分',0);		print $_SESSION['Psent'];
	tr_Making('電話番号',0);		print $_SESSION['Phone'];
	tr_Making('参加資格<br />(社会人学生は一般)',0);	print $_SESSION['Penter'];
		print " / ";				print $_SESSION['Pipsj']." ".$_SESSION['Pknum'];
	tr_Making('支払方法',0);		print $_SESSION['Ppay']."<br />";
		print "送金/振り込み日 : ";	print $_SESSION['Psday'];
	tr_Making('希望する部屋',0);	print $_SESSION['Proom']." ".$_SESSION['Paite'];
	tr_Making('請求書の宛名',0);		print $_SESSION['Patena'];
	tr_Making('領収書',0);		print $_SESSION['Prcpt'];
	tr_Making('喫煙調査',0);		print $_SESSION['Psmoke'];
	tr_Making('その他ご要望',0);	print $_SESSION['Petc'];
	print "</td></tr></table>";
	
	print "<br />以上の内容で送信します。<br />\n";
	print "<table border=0><tr><td>";
//	print "<form action=\"$script\" method=\"post\">";
//	print "<input type=hidden name=\"state\" value=\"return\">";
//	print "<input type=submit value=\" 戻る \">\n";
//	print "</form></td>";
	print "<td><form action=\"$script\" method=\"post\">\n";
	print "<input type=hidden name=\"state\" value=\"save\">";
	print "<input type=submit value=\" 送信 \">\n";
	print "</form></td></tr></table>";
}
elseif($_POST['state']=='save'){
/*- 送信されたとき --------------------------------------*/
	//ログファイル保存
	$data = date("Y/m/d H:i:s");
	$data.= ",".$_SESSION['Pname'];
	$data.= ",".$_SESSION['Pkana'];
	$data.= ",".$_SESSION['Psex'];
	$data.= ",".$_SESSION['Page'];
	$data.= ",".$_SESSION['Porg'];
	$data.= ",".$_SESSION['Pemail'];
	$data.= ",".$_SESSION['Papost'];
	$data.= ",".$_SESSION['Paddr'];
	$data.= ",".$_SESSION['Psent'];
	$data.= ",".$_SESSION['Phone'];
	$data.= ",".$_SESSION['Penter'];
	$data.= ",".$_SESSION['Pipsj'];
	$data.= ",".$_SESSION['Pknum'];
	$data.= ",".$_SESSION['Ppay'];
	$data.= ",".$_SESSION['Psday'];
	$data.= ",".$_SESSION['Proom'];
	$data.= ",".$_SESSION['Paite'];
	$data.= ",".$_SESSION['Popt1'];
	$data.= ",".$_SESSION['Prcpt'];
	$data.= ",".$_SESSION['Patena'];
	$data.= ",".$_SESSION['Psmoke'];
//	$data.= ",".$_SESSION['Popt2'];
//	$data.= ",".$_SESSION['Popt3'];
	$data.= ",".$_SESSION['Petc'];
	$data.= "\n";
	//	$data = mb_convert_encoding($data, "EUC-JP", "auto"); 
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
	
	//関係者にメールで送信
	$datam = $mheader;
	$datam.= "\n受付日時:".date("Y/m/d H:i:s");
	$datam.= "\n氏名:".$_SESSION['Pname'];
	$datam.= "\n氏名読み:".$_SESSION['Pkana'];
	$datam.= "\n性別:".$_SESSION['Psex'];
	$datam.= "\n歳代:".$_SESSION['Page'];
	$datam.= "\n所属:".$_SESSION['Porg'];
	$datam.= "\nメール:".$_SESSION['Pemail'];
	$datam.= "\n郵便番号:".$_SESSION['Papost'];
	$datam.= "\n住所:".$_SESSION['Paddr'];
	$datam.= "\n送付区分:".$_SESSION['Psent'];
	$datam.= "\n電話番号:".$_SESSION['Phone'];
	$datam.= "\n参加資格:".$_SESSION['Penter'];
	$datam.= "\n会員？:".$_SESSION['Pipsj'];
	$datam.= "\n会員番号:".$_SESSION['Pknum'];
	$datam.= "\n支払い方法:".$_SESSION['Ppay'];
	$datam.= "\n支払い予定日:".$_SESSION['Psday'];
	$datam.= "\n部屋希望:".$_SESSION['Proom'];
	$datam.= "\n請求書:".$_SESSION['Popt1'];
	$datam.= "\n領収書:".$_SESSION['Prcpt'];
	$datam.= "\n請求書宛名:".$_SESSION['Patena'];
	$datam.= "\n禁煙調査:".$_SESSION['Psmoke'];
	$datam.= "\n備考:".$_SESSION['Petc'];
	$datam.= "\n";
	$datam = mb_convert_encoding($datam, "ISO-2022-JP", "EUC-JP"); 


	mail($mtoaddr, $msubject, $datam, $mheaders, $mparams);
	mail($_SESSION['Pemail'], $msubject, $datam, $mheaders, $mparams);
//	mail("gian@cs.uec.ac.jp", $msubject, $datam, $mheaders, $mparams);

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
		print "の項目が未入力もしくは不正です．ブラウザのキャッシュをクリアして，最初からやり直してください．</p>";
	}
	
	print "<form action=\"$script\" method=\"post\">\n";
	print "<table border=1>";
	print "<tr><td width=130></td><td width=450>";
	tr_Making(add_flg($Needname, '氏名'),$Keyname);
		print "姓 :"; form_Text(Pname1,$_SESSION['Pname1'],20);
		print "名 :"; form_Text(Pname2,$_SESSION['Pname2'],20);
	tr_Making(add_flg($Needkana,'カナ氏名'),$Keykana);
		print "姓 :"; form_Text(Pkana1,$_SESSION['Pkana1'],20);
		print "名 :"; form_Text(Pkana2,$_SESSION['Pkana2'],20);
	tr_Making(add_flg($Needsex,'性別'),$Keysex);
		form_Radio(Psex,'男性',$_SESSION['Psex']);
		form_Radio(Psex,'女性',$_SESSION['Psex']);
	tr_Making('年齢',$Keyage);
		form_PulldownWithNone(Page,10,100,$_SESSION['Page'],10);
		print "歳代&nbsp;&nbsp;（部屋割りの参考にさせて頂きますが，必須ではありません）";
	tr_Making(add_flg($Needorg,'所属'),$Keyorg);
		form_Text(Porg,$_SESSION['Porg'],50);
	tr_Making(add_flg($Needemail,'電子メール'),$Keyemail);
		form_Text(Pemail,$_SESSION['Pemail'],50);
	tr_Making(add_flg($Needaddr,'住所'),$Keyadd);
		print "〒"; form_Text(Papost1,$_SESSION['Papost1'],3);
		print "-";  form_Text(Papost2,$_SESSION['Papost2'],5);
		print "<br />";
		form_Text(Paddr,$_SESSION['Paddr'],75);
	tr_Making(add_flg($Needsent,'送付区分'),$Keysent);
		form_Radio(Psent,'自宅',  $_SESSION['Psent']);
		form_Radio(Psent,'勤務先',$_SESSION['Psent']);
	tr_Making(add_flg($Needphone,'電話番号'),$Keyphone);
		form_Text(Phone1,$_SESSION['Phone1'],7); print " - ";
		form_Text(Phone2,$_SESSION['Phone2'],7); print " - ";
		form_Text(Phone3,$_SESSION['Phone3'],7);
	tr_Making(add_flg($Needenter,'参加資格<br />(社会人学生は一般)'),$Keyenter);
		form_Radio(Penter,'一般',$_SESSION['Penter']);
		form_Radio(Penter,'学生',$_SESSION['Penter']);
		form_Radio(Penter,'発表者（学生）',$_SESSION[Penter]);
		form_Radio(Penter,'発表者（６５歳以上）',$_SESSION[Penter]);
		print "<hr size=1 />";
		form_Radio(Pipsj,'会員',$_SESSION['Pipsj']);
		print "（会員番号 : "; form_Text(Pknum,$_SESSION['Pknum'],20); print "）";
		form_Radio(Pipsj,'非会員',$_SESSION['Pipsj']);
	tr_Making('※支払方法',$Keypay);
		form_Radio(Ppay,$Payment1,$_SESSION['Ppay']);	print "<br />";
		form_Radio(Ppay,$Payment2,$_SESSION['Ppay']);	print "<br />";
		form_Radio(Ppay,$Payment3,$_SESSION['Ppay']);	print "<br />";
		print "送金/振込み予定日"; pay_day(Psday);
	tr_Making('※希望する部屋',$Keyroom);
		form_Radio(Proom,$Stay1,$_SESSION['Proom']); print $Stay1cost."<br />";
		form_Radio(Proom,$Stay2,$_SESSION['Proom']); print $Stay2cost."<br />";
		form_Radio(Proom,$Stay3,$_SESSION['Proom']); print $Stay3cost."<br />";
		form_Radio(Proom,$Stay4,$_SESSION['Proom']); print $Stay4cost."<br />";
		print "同室希望の場合は，「その他ご要望」欄にその旨を記入し，部屋の人数分のお名前を列挙してください．<br />";
		print "※部屋の人数や相部屋に関しては，希望通りにならない場合もあります．<br />";
	tr_Making(add_flg($Needatena, '請求書などの宛名'),$Keyatena);
		form_Text(Patena,$_SESSION['Patena'],30);
	tr_Making(add_flg($Needrcpt, '領収書'),$Keyrcpt);
		form_Radio(Prcpt,'参加費と宿泊費の２枚',$_SESSION['Prcpt']);
		form_Radio(Prcpt,'参加費宿泊費一括の１枚',$_SESSION['Prcpt']);
		form_Radio(Prcpt,'不要',$_SESSION['Prcpt']);
	tr_Making(add_flg($Needsmoke, '喫煙調査'),$Keysmoke);
		form_Radio(Psmoke,'喫煙室',$_SESSION['Psmoke']);
		form_Radio(Psmoke,'禁煙室',$_SESSION['Psmoke']);
	tr_Making('その他ご要望',$etckey);
		form_Textarea(Petc,$_SESSION['Petc'],4,60);
	print "</td></tr></table>";
	
	print "<input type=hidden name=\"state\" value=\"confirm\">\n";
	if($errCount==0){//エラーがない場合---------------------
		print "<input type=submit value=\"参加申し込み\">\n";
	}
	print "</form>\n";
	
	}
	print $FOOTER;
?>
