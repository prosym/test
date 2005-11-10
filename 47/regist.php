<html><body><?php
// バージョンが旧くてダメ? iconv_set_encoding("internal_encoding", "UTF-8");
// バージョンが旧くてダメ? iconv_set_encoding("output_encoding", "UTF-8");
    import_request_variables('p', 'p_');
    if ($p_seikyu == "on") {$seikyu = "必要";}
    if ($p_bunri == "on") {$bunri = "分離";}
    if ($p_smoke == "on") {$smoke = "喫煙";}
    $data = q(date("YmdHi")) . ","
	. q($p_name) . ","
	. q($p_kana) . ","
	. q($p_sex) . ","
	. q($p_age) . ","
	. q($p_org) . ","
	. q($p_email) . ","
	. q($p_address) . ","
	. q($p_soufu) . ","
	. q($p_phone) . ","
	. q($p_kubun) . ","
	. q($p_ipsj) . ","
	. q($p_knum) . ","
	. q($p_pay) . ","
	. q($p_furikomibi) . ","
	. q($seikyu) . ","
	. q($p_atena) . ","
	. q($bunri) . ","
	. q($p_room) . ","
	. q($p_aite) . ","
	. q($smoke) . ","
	. q($p_sonota) . "\n";

    $file = fopen("regist.csv", "a");
//SJISは良くないですよ    fwrite($file, e2s($data));
    fwrite($file, $data);
    fclose($file);

    $subject = "47th programming symposium registration";
    $message = e2j(
	"第47回プログラミング・シンポジウムの参加申し込みを，\n" .
	"以下の登録内容で受け付けました．\n\n" .
	"受付日時      " . date(Y年m月d日H時i分) . "\n" .
	"氏名          " . $p_name . "\n" .
	"カナ氏名      " . $p_kana . "\n" .
	"性別          " . $p_sex . "\n" .
	"年齢          " . $p_age . "\n" .
	"所属          " . $p_org . "\n" .
	"電子メール    " . $p_email . "\n" .
	"住所          " . str_replace("\n", "\n              ",
			$p_address) . "\n" .
	"送付区分      " . $p_soufu . "\n" .
	"電話番号      " . $p_phone . "\n" .
	"参加資格      " . $p_kubun . "\n" .
	"情報処理学会  " . $p_ipsj . "\n" .
	"会員番号      " . $p_knum . "\n" .
	"支払方法      " . $p_pay . "\n" .
	"振込日        " . $p_furikomibi . "\n" .
	"請求書等      " . $seikyu . "\n" .
	"請求書等宛名  " . $p_atena . "\n" .
	"金額分離      " . $bunri . "\n" .
	"部屋          " . $p_room . "名1室\n" .
	"同室相手      " . $p_aite . "\n" .
	"たばこ        " . $smoke . "\n" .
	"その他        " . $p_sonota . "\n\n" .
	"請求書，郵便振替用紙などを郵送します．\n" .
	"登録内容変更，キャンセル連絡，その他お問い合わせは，\n" .
	"prosym47@ipsj.or.jp までお願いします．\n" .
	"キャンセルの期限は，12月16日(金)です．" 
	);
    $headers = "From: prosym47@ipsj.or.jp";
    $parameters = "-f webmaster@kitty.watalab.cs.uec.ac.jp";
    $ok = (
	"受け付けました．<br>" . 
	"登録内容をメールで送信しました．<br>" .
        "メールが届かない場合は" .
	"prosym47@ipsj.or.jpにお問い合わせください．"
	);
    $ng = (
	"何らかのエラーが発生しました．<br>" .
	"prosym47@ipsj.or.jpにお問い合わせください．"
	);
    if (mail($p_email, $subject, $message, $headers, $parameters)) {
        mail("prosym47@ipsj.or.jp", $subject, $message, $headers, $parameters);
//        mail("gian@cs.uec.ac.jp", $subject, $message, $headers, $parameters);
        print($ok);
    } else {
        print($ng);
    }

    function e2s($string)
    { return(mb_convert_encoding($string, "SJIS", "EUC-JP")); }
    function s2e($string)
    { return(mb_convert_encoding($string, "EUC-JP", "SJIS")); }
    function e2j($string)
    { return(mb_convert_encoding($string, "ISO-2022-JP", "EUC-JP")); }
    function j2e($string)
    { return(mb_convert_encoding($string, "EUC-JP", "ISO-2022-JP")); }
    function j2s($string)
    { return(mb_convert_encoding($string, "SJIS", "ISO-2022-JP")); }
    function s2j($string)
    { return(mb_convert_encoding($string, "ISO-2022-JP", "SJIS")); }
    function q($string)
    { return("\"" . str_replace(",", "，", addcslashes($string, "\n\r")) . "\""); }

?></body></html>
