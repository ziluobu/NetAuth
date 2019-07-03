#简单的网络准入Python脚本
##背景
    现在很多打印机面临有后门、漏洞、非法访问等，但是打印机却没有acl或防火墙等安全功能，并且打印机固件更新很慢，很多打印机就算知道有漏洞也没固件可更新，针对网络是固定IP的单位可以在打印机前面布放一个小型防火墙并进行策略配置即可有效降低安全风险，但是对于动态获取IP的客户端，无法动态修改防火墙配置。
##原理
    此项目是小型简单的网络准入Python脚本，可以动态获取允许访问打印客户端IP并动态调整防火墙策略。
    本程序原理是在打印机前端装一个小型防火墙（本人在打印机前面放至了一台公司闲置的netscreen ssg5防火墙），使用打印机的人安装准入脚本向准入服务器注册，注册服务器收到准入消息向防火墙发送允许策略。
！[]（https://github.com/ziluobu/NetAuth/blob/master/1.png）
    如上原理图，1、所有需要访问资源的终端执行准入到服务器注册。2、服务器定时向防火墙更新授权策略。3、终端可以访问授权网络。
##其他
    本程序只是临时编写，由于自己使用很多功能都不健全，如准入注册没有身份认证，传输没有加密等，但是作为临时解决方案可以使用。