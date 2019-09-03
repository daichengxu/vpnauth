# 项目vpnauth
# 用途
# 0、openvpn用户管理
# 1、通过Web管理,不用ssh到服务器签key
# 2、密码原来是明文,现在是加密的
# 3、日志入库,通过Web看登录日志

# 一、运行环境
centos7.5
python3.6.2
Django1.11.20
sqlite3
openvpn2.4.6
easy-rsa3

# 二、安装包
mkdir -p /home/vpn/install
cd /home/vpn/install
上传项目vpnauth-3.0.zip包
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
wget https://media.djangoproject.com/releases/1.11/Django-1.11.20.tar.gz

# 三、安装sqllite,如果找不到sqlite3的开发库，就不会编译安装sqlite3的相关模块
yum -y install sqlite sqlite-devel dos2unix lrzsz

#安装python3.6.2
cd /home/vpn/install
tar xf Python-3.6.2.tar.xz
cd Python-3.6.2
./configure --prefix=/home/vpn/python
make && make install
ln -s /home/vpn/python/bin/python3.6 /usr/bin/python3
ln -s /home/vpn/python/bin/python3.6 /usr/bin/python3.6

#安装Django-1.11.20
cd /home/vpn/install
tar xf Django-1.11.20.tar.gz
cd Django-1.11.20
/home/vpn/python/bin/python3.6 setup.py install

#部署项目
cd /home/vpn/install
unzip vpnauth-3.0.zip
cd vpnauth-3.0
mv vpnauth /home/vpn/
#移动脚本到openvpn目录下
cp scripts/checkpsw* /etc/openvpn/
chmod 755 /etc/openvpn/checkpsw*

#初始化数据,添加超级管理员
cd /home/vpn/vpnauth
/home/vpn/python/bin/python3.6 manage.py makemigrations
/home/vpn/python/bin/python3.6 manage.py migrate
/home/vpn/python/bin/python3.6 manage.py createsuperuser #(需要输入 用户名、邮箱、密码 要求8位及中英文)

#由于openvpn权限为nobody需要修改项目权限
chown -R nobody.nobody /home/vpn/vpnauth

#django启动命令
cd /home/vpn/vpnauth
/home/vpn/python/bin/python3.6 manage.py runserver 0.0.0.0:80  #可自定义监听ip及端口

# 四、配置openvpn
#修改openvpn server端配置,增加以下参数
#server端配置
vim /etc/openvpn/server.conf
auth-user-pass-verify /etc/openvpn/checkpsw.sh via-env
script-security 3
verify-client-cert require  #此选项为强制客户端认证证书，可选项

#客户端修改配置,增加以下参数
auth-nocache
auth-user-pass

#重启openvpn服务
service openvpn restart

# 浏览地址
#1、改密码地址
http://x.x.x.x
#2、管理后台地址
http://x.x.x.x/admin

###########################################################################################
###django的配置
项目下的setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'vpnauth.db'), #指定数据文件
    }
}

#脚本指定的项目路径
/etc/openvpn/checkpsw.py
sys.path.append('/home/vpn/')