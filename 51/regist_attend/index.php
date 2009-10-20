<?php
  /* settings */
set_include_path(implode(PATH_SEPARATOR, array(
                    realpath('/home/shnsk/lib/ZendFramework-1.9.4/library'),
                    realpath('/home/shnsk/lib/Smarty-2.6.22/libs/'),
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

if (!defined('BASE_URI')) {
  define('BASE_URI',
         (getenv('BASE_URI') ?
	  getenv('BASE_URI') :
	  preg_replace("/index.php$/", '',getenv('SCRIPT_NAME'))));
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

/* レイアウトの設定 */
require_once 'Zend/Layout.php';
Zend_Layout::startMvc(array('layoutPath' =>
			    APPLICATION_PATH.'/views/layouts'));

/* フロントコントローラにディスパッチ */
require_once 'Zend/Controller/Front.php';
$front_controller = Zend_Controller_Front::getInstance();
$front_controller->setControllerDirectory(APPLICATION_PATH.'/controllers');
/* http://home.shnsk.net/prosym/s2009-entry/auth/login
 ->
 http://home.shnsk.net/auth/login
*/

$front_controller->dispatch();
