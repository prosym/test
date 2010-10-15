<?php
set_include_path(implode(PATH_SEPARATOR, array(
                    realpath('/home/shnsk/lib/ZendFramework-1.9.4/library'),
		    get_include_path(),
)));

/* some codes inspired from Zend_Application in Zend Framework 1.8.x */
require_once 'Zend/Config/Ini.php';

if (!defined('APPLICATION_ENV')) {
  define('APPLICATION_ENV',
	 (getenv('APPLICATION_ENV') ?
	  getenv('APPLICATION_ENV') :
	  'production'));
 }
if (!defined('APPLICATION_PATH')) {
  define('APPLICATION_PATH',
	 (getenv('APPLICATION_PATH') ?
	  getenv('APPLICATION_PATH') :
	  realpath(dirname(__FILE__) . '/../application')));
 }

/* 設定ファイルの読み込み */
class Options {
  static $_instance = null;
  static function getInstance()
  {
    if (self::$_instance == null) {
      self::$_instance = new self();
    }
    return self::$_instance;
  }

  static function getOptions()
  {
    if (self::$_instance == null) {
      self::$_instance = new self();
    }
    return self::$_instance->options;
  }

  static function getConfig()
  {
    if (self::$_instance == null) {
      self::$_instance = new self();
    }
    return self::$_instance->config;
  }


  private function setPhpSettings(array $settings, $prefix = '')
  {
    foreach ($settings as $key => $value) {
      $key = empty($prefix) ? $key : $prefix . $key;
      if (is_scalar($value)) {
	ini_set($key, $value);
      } elseif (is_array($value)) {
	$this->setPhpSettings($value, $key . '.');
      }
    }
  }
  private function __construct()
  {
    $config_file = APPLICATION_PATH . '/configs/application.ini';
    $this->config = new Zend_Config_Ini($config_file, APPLICATION_ENV);
    $this->options = $this->config->toArray();

    if (!empty($this->options['phpsettings'])) {
      $this->setPhpSettings($this->options['phpsettings']);
    }
  }
}

$options = Options::getOptions();
$eventname = $options['event']['name'];
$main_site = $options['event']['main_site'];
?>
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head>  
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
  <title><?php echo $eventname ?></title>
</head>
<body>
<h1>
<?php echo $eventname ?>参加申し込みは締切ました</h1>
</body>
</html>
