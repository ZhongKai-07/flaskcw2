var LANGUAGE_Index = "zh_CN"; //��ʶ����  
  
jQuery(document).ready(function () {  
    // alert("ҳ�����ʱ���õķ���");  
  
  LANGUAGE_Index = jQuery.i18n.normaliseLanguageCode({}); //��ȡ�����������  
  loadProperties(LANGUAGE_Index);  
});  
  
  
$(".lan_select").change(function () {  
  
  
    if (($(".lan_select").val() === "Ӣ��") || ($(".lan_select").val() === "English")) {  
        LANGUAGE_Index = "en_US";  
  } else {  
        LANGUAGE_Index = "zh_CN";  
  }  
  
    loadProperties(LANGUAGE_Index);  
  
});  
  
  
function loadProperties(type) {  
    jQuery.i18n.properties({  
        name: 'strings', // ��Դ�ļ�����  
        path: 'Languages/', // ��Դ�ļ�����Ŀ¼·��  
        mode: 'map', // ģʽ�������� Map  
        language: type, // ��Ӧ������  
        cache: false,  
        encoding: 'UTF-8',  
        callback: function () { // �ص�����  
            $('.lan_zh').html($.i18n.prop('lan_zh'));  
            $('.lan_en').html($.i18n.prop('lan_en'));  
            $('.username').html($.i18n.prop('username'));  
            $('.password').html($.i18n.prop('password'));  
        }  
    });  
}