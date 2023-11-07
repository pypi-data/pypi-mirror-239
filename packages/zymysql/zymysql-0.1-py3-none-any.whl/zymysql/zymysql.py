
#用于数据库操作，包括增删改查
import pymysql.cursors
# import json
# import base64
# import datetime
# import gzip
# import zipfile
# import os
class Mysql():
    def __init__(self,tabname):
        self.tabname = tabname
        self.connection = pymysql.connect(host='localhost',  # 主机号
                                          # host='192.168.2.19',
                                          # host='192.168.3.6',         # raspberry
                                          # host='10.168.1.118',        # 蒲公英
                                          # host='169.254.218.130',     # localhost
                                          # host="192.168.1.168",
                                          port=3306,  # 端口号
                                          user='root',  # 用户名
                                          #password='ranking2018',  # 密码
                                          db='sanyi',  # 需要连接的数据库
                                          # db='mysql',  # 需要连接的数据库
                                          charset='utf8',  # 编码
                                          read_default_file=None,  # 从默认配置文件（my.ini/my.cnf）中读取参数
                                          autocommit=True,  # 自动添加选项
                                          cursorclass=pymysql.cursors.DictCursor)  # 选择Cursor类型
    def run(self):
        sql = "SELECT * FROM "+self.tabname
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)                   #执行sql语句
                       # print(cursor.fetchall())                #得到返回
                       cursor.close()                          #关闭

        except Exception as e:
             print(e)
        return s
    def creattable(self,datas):
        keys=list(datas.keys())
        keyname = '(' + "`"+keys[0]+"`"+" varchar(255) NULL"

        del keys[0]
        for key in keys:
            if(key=="CompressedData"):
                keyname = keyname + ',' + "`" + key + "`" + " varbinary(20000) NULL"
            else:
                keyname = keyname + ',' +  "`"+key+"`"+" varchar(255) NULL"
        keyname = keyname + ');'
        sql="drop table"+"`"+self.tabname
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       # print(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        #sql="CREATE TABLE `mysql`."+"`"+self.tabname+"`"+" (`username1` varchar(255) NULL,`passwrd` varchar(255) NULL);"
        sql = "CREATE TABLE `mysql`." + "`" + self.tabname + "`" + keyname
        #sql = "CREATE TABLE `mysql`." + "`" + self.tabname + "`" + " (`username1` ,`passwrd`);"
        # print(sql)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       # print(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        return s
    def calID(self,data):
        sql = "SELECT "+data+" FROM " + self.tabname
        # print(sql)
        s=[]

        try:
              with self.connection.cursor() as cursor:         #创建游标
                       flag=cursor.execute(sql)
                       s=cursor.fetchall()
                       cursor.close()
        except Exception as e:
             print(e)
             s.append({data: "ss0"})
        try:
            s[0][data][2:]
        except:
            s=[]
            s.append({data: "ss0"})
        count=int(s[0][data][2:])
        flag= int(s[0][data][2:])
        del s[0]
        re=[]
        re.append(count)
        for i in s:                #查找最大值
            if(flag<int(i[data][2:])):
                flag=int(i[data][2:])
            re.append(int(i[data][2:]))
        re.sort()
        # print(re)
        flag=flag+1
        count=re[0]
        del re[0]
        for k in re:               #查找空值
            if((k-count))>1:
                flag=count+1
            count=k


        return data[0:2]+str(flag)

    def checkdatas(self,datas):
        data=datas[0]
        s=' '
        flag=0
        del datas[0]
        for i in datas:
            data= data+' and '+i
        sql = "SELECT * FROM "+self.tabname+" where "+data
        # print(sql)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       flag=cursor.execute(sql)
                       s=(cursor.fetchall())
                       cursor.close()
        except Exception as e:
             print(e)
        return s,flag
    def getall(self):
        sql = "SELECT * FROM "+self.tabname
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       count=cursor.execute(sql)
                       liststr=(cursor.fetchall())
                       cursor.close()
        except Exception as e:
             print(e)
        return liststr,len(str(liststr).split("},"))
    def getsub(self,subname):
        sql = "SELECT "+subname+" FROM "+self.tabname
        s=0
        str1=""
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       str1=(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        return str1,len(str(str1).split(","))
    def insert(self,datas):
        sql = "SELECT * FROM "+self.tabname
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       keys=(list(cursor.fetchone().keys()))
                       cursor.close()
        except Exception as e:
             print(e)
        keyname='('+keys[0]
        keyvalues='('+"%s"
        del keys[0]
        for key in keys:
            keyname=keyname+','+key
            keyvalues =keyvalues+','+"%s"
        keyname=keyname+')'
        keyvalues=keyvalues+')'
        sql = "INSERT INTO "+self.tabname+ keyname+" VALUES "+keyvalues # 插入数据（插入）
        #print(sql)
        try:
            with self.connection.cursor() as cursor:  # 创建游标
                cursor.execute(sql, datas)
        except Exception as e:
            print(e)
        return s
    def insertbydic(self,datas):
        #sql = "SELECT * FROM "+self.tabname
        #try:
        #      with self.connection.cursor() as cursor:         #创建游标
        #               s=cursor.execute(sql)
         #              rkeys=keys=(list(cursor.fetchone().keys()))
         #              cursor.close()
        #except Exception as e:
        #     print(e)
        #print(sql)
        keys = (list(datas.keys()))              #创建列表
        listdatas=[]
        listdatas.append(datas[keys[0]])
        keyname='('+keys[0]
        keyvalues='('+"%s"
        del keys[0]
        for key in keys:
            keyname=keyname+','+key
            keyvalues =keyvalues+','+"%s"
            try:
                listdatas.append(datas[key])
            except:
                listdatas.append(0)
        keyname=keyname+')'
        keyvalues=keyvalues+')'
        sql = "INSERT INTO "+self.tabname+ keyname+" VALUES "+keyvalues # 插入数据（插入）
        #print(sql)
        #print(listdatas)
        try:
            with self.connection.cursor() as cursor:  # 创建游标
                s=cursor.execute(sql, listdatas)
        except Exception as e:
            print(e)
            s=0
        return s
    def delatebyindex(self,index):
        sql = "DELETE FROM "+self.tabname+" limit "+str(index)
        #print(sql)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       # print(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        return s
    def delatebyindex_to_all(self,index):
        sql = "DELETE FROM "+self.tabname+" limit "+str(index)\
              #+",-1"
        # print(sql)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       # print(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        return s
    def delate(self,datas):
        data=datas[0]
        s=' '
        del datas[0]
        # print(data)
        for i in datas:
            data= data+' and '+i
        sql = "DELETE FROM "+self.tabname+" where "+data
        # print(sql)
        # print(data)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql)
                       print(cursor.fetchall())
                       cursor.close()

        except Exception as e:
             print(e)
        return s
    def delatebyIDS(self,datas):
        keys=list(datas.keys())
        value=datas[keys[0]]
        values=value.split(",")
        for i in values:
            delatelist=[]
            delatelist.append(keys[0]+"="+"'"+i+"'")
            # print(delatelist)
            self.delate(delatelist)
    def modify(self,seckey,mainkey,datas):
        sql = "update "+self.tabname+"  set "+seckey+"=%s"+" where "+mainkey+"=%s"
        # print(sql)
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       s=cursor.execute(sql,datas)
                       cursor.close()
        except Exception as e:
             print(e)
        return s
    ###############
    #输入： datas
    #例子： {"deviceId":"s-01","deviceName":"设备1","deviceCode":""}
    #output datastr      列表数据
    #        count       列表数量
    def  databycheckdatas(self,datas):                #通过检索项返回列表数据，输入数据为字典
        sqldatas=[]
        keys = (list(datas.keys()))   #得到健值
        for key in keys:
            # print(key)
            if(datas[key]!=''):
                if(datas[key][0]!='!')&(datas[key][0]!='^'):
                    if(key=="start_create_time"):
                        sqldatas.append("createTime"+">"+"'"+datas[key]+"'")
                    if(key=="end_create_time"):
                        sqldatas.append("createTime"+"<"+"'"+datas[key]+"'")
                    if(key=="time"):
                        sqldatas.append("time"+">"+"'"+datas[key]+"'")
                    if (key == "editTime"):
                        sqldatas.append("editTime" + "<" + "'" + datas[key] + "'")
                    if((key != "start_create_time")&(key !="end_create_time")&(key !="time")) :
                        sqldatas.append(key+"="+"'"+datas[key]+"'")
                elif(datas[key][0]=='^'):
                    sqldatas.append(key + ">" + "'" + '100' + "'")
                    sqldatas.append(key + "<" + "'" + '136' + "'")
                else:
                    sqldatas.append(key + "!=" + "'" + datas[key][1:] + "'")
        # print(sqldatas)
        data=sqldatas[0]
        s=' '
        del sqldatas[0]
        for i in sqldatas:
            data= data+' and '+i
        sql = "SELECT * FROM "+self.tabname+" where "+data
        # print(sql)
        datastr=""
        count=1
        try:
              with self.connection.cursor() as cursor:         #创建游标
                       count=cursor.execute(sql)
                       datastr=(cursor.fetchall())
                       cursor.close()
        except Exception as e:
             print(e)
        return datastr,count
    def close(self):
        self.connection.close()
    def get_columns(self):
        sql = "show full columns from " + self.tabname
        # print(sql)
        try:
            with self.connection.cursor() as cursor:  # 创建游标
                s = cursor.execute(sql)
                str1 = (cursor.fetchall())
                cursor.close()
        except Exception as e:
            print(e)
        return str1

# Connect to the database
'''connection = pymysql.connect(host='localhost',    #主机号
                             port=3306,           #端口号
                             user='root',         #用户名
                             password='123456',   #密码
                             db='MySql',          #需要连接的数据库
                             charset='utf8',   #编码
                             read_default_file=None, #从默认配置文件（my.ini/my.cnf）中读取参数
                             autocommit=True,  #自动添加选项
                             cursorclass=pymysql.cursors.DictCursor)  #选择Cursor类型

try:
    with connection.cursor() as cursor:         #创建游标
        # Read a single record
        #sql = "SELECT `name`, `pass` FROM `logname`"
        #sql = "SELECT * FROM `logname` where name='zhang' and pass='123'" #选择密码登录符合条件的（查找）
        #sql = "INSERT INTO logname (name,pass) VALUES (%s,%s);"  # 插入数据（插入）
        #sql = "DELETE from logname where name=%s"              #删除数据（删除）
        sql = "update logname  set pass=%s where name=%s"          #修改数据（修改）
        #print(cursor.executemany(sql,[('张悦','123'),('lisi','234')]))                  #执行SQL语句
        #result = cursor.fetchall()
        #cursor.execute(sql,['张悦'])
        cursor.execute(sql, ['34','zhang'])
       # print(result)
       # connection.commit()
        cursor.close()
except Exception as e:
    print(e)
finally:
    connection.close()

'''




if __name__ == '__main__':


    # device=Mysql("device")
    # device.creattable()
    #print(device.calID("deviceId"))
    #alarm=Mysql("alarm")
    #alarm.modify("isHandle","alarmId",[1,"a-1"])
    #a={'{"sa":"1"}'}
    #print(list(a))
    #a="维保星级"
    #mapdata=Mysql("mapdata")
    #data,c=mapdata.getall()
    #for i in data:
    #    i["position"]=[float(i["x"])/1000000,float(i["y"])/1000000]
    #print(data)
    #passage=Mysql("passage")
    #passage.modify("isHandle=%s status","passageId",["pa1","1 1"])
    #passage = Mysql("passage")
   # s,c=passage.checkdatas(["deviceId='de2'","passageCode='002'"])
    #d=Mysql(s[0]["passageId"])
    #data={"data":0,"time":datetime.datetime.now(),"isWarning":0,"status":0}
    #data["data"]=4
    #data["isWarning"]=0
    #data["status"]=0
    #d.insertbydic(data)
    #f_src = open("file/模块功能.docx", "rb")  # 打开文件
    #f_tar = gzip.open("file/模块功能.rar", "wb")  # 创建压缩文件对象
    #f_tar.writelines(f_src)
    #f_tar.close()
   # f_src.close()
   # print(os.listdir("file/"))

   # azip = zipfile.ZipFile('file/bb.zip', 'w')
   # azip.write('file/模块功能.docx', '模块功能.docx', compress_type=zipfile.ZIP_DEFLATED)
    #azip.close()
    #test=Mysql("pa2")
    #test.creattable({"name":"","pass":""}) #新建数据库类
    #logname=Mysql("logname")              #新建表实体
    #print(logname.getall())               #得到表单中所有数据
    #print(logname.getsub("name,pass"))    #选择自己想要的条目

    #datas=[]
    #datas.append("name='zhang'")
    #datas.append("pass<'38'")
    #datas.append("pass>'32'")
    #print(logname.checkdatas(datas))               #从表中查找元素
    #logname.insert(["admin","admin"])      #向表中插入数据
    #datas.append("name='zhang'")
    #logname.delate(["name='zhang'"])        #删除数据
    #logname.modify('pass','name',['39','we'])           #修改数据
    #logname.close()
   # now=datetime.datetime.now()
    #device = Mysql("device")
    #print(device.getall())
    #print(request.args)
    #totaldata={"total":4,"rows":[{"deviceId":"FI-SW-01","deviceName":"Ki","deviceCode":"10.00","deviceBrand":"P","status":"2","isAuto":"0","isWarning":"0","createTime":"2019-01-01","editTime":"2019-01-02"}]}
    #totaldata["rows"]=(device.getall())
    #s=device.getall()
    #print(device.databycheckdatas({"deviceId":"s-01","deviceName":"设备1","deviceCode":""}))
    #print(totaldata)

    #device.insertbydic({"deviceId":"FI-SW-01","deviceName":"Ki","deviceCode":"10.00","deviceBrand":"P","status":"2","isAuto":"0","isWarning":"0","createTime":"2019-01-01","editTime":"2019-01-02"})

    #device.delatebyIDS({"deviceCode":["s-05","s-04"]})
   # device.close()
   #  pa=Mysql("pa23_wav_real")
   #  pa21 = Mysql("pa21_wav_real")
   #  pa19 = Mysql("pa19_wav_real")
   #  pa_list,pacount= pa.getall()
   #  ss=pa_list[0]
   #  ss["createTime"]=datetime.datetime.now()
   #  #pa.insertbydic(ss)
   #  pa.delatebyindex_to_all(2)
   #  pa21.insertbydic(ss)
   #  pa19.insertbydic(ss)
   #  # pa.insertbydic(pa_list[1])
   #  # pa.insertbydic(pa_list[2])
   #  # pa.insertbydic(pa_list[3])
   #  pastr,pacunt=pa.getall()
   #  print(pastr[-1])
   #  print(datetime.datetime.now() - now)
   #  if(pacount>10):
   #      pa.delatebyindex_to_all(7)
   # a=[1,2,3,4,5]
   # for i in a[::-1]:
   #     print(i)
   # test=Mysql("pa35_wav")
   # test.creattable( {"passageId": "pa25", "data": "", "time": "", "isWarning": "", "status": "",
   #       # 新建通道数据库类
   #       "dau_id": "",
   #       "slot_id": "",
   #       "chan_id": "",
   #       "point_id": "",
   #       "fGapVolt": "",  # 键相间隙电压；（建相）
   #       "fSpeed": "",  # 键相转速（键相）
   #       "byAlarmFlag": "",  # 报警状态标志，Bit0 – 3： 高高报、高报、低低、低(过程量/通讯过程量)
   #       "fValue": "",  # 过程量值（过程量/通信过程量）
   #       "warningFlag": "",  # 特征值高报状态
   #       "dangerFlag": "",  # 特征值高高报状态；
   #       "byComplexFlag": "",  # 综合报警状态
   #       "fRMS": "",  # 有效值
   #       "fPeak": "",  # 真峰值
   #       "fPtP": "",  # 真峰峰值
   #       "fKurtosis": "",  # 峭度
   #       "fCrestFactor": "",  # 波峰因素
   #       "fOverallValue": "",  # 通频值
   #       "f1XA": "",  # 一倍频幅值
   #       "f1XP": "",  # 一倍频相位
   #       "f2XA": "",  # 二倍频幅值
   #       "f2XP": "",  # 二倍频相位
   #       "fAve": "",  # 平均值
   #       "dwCompressedLen": "",  # 波形字节长度
   #       "CompressedData": "",  # 波形数组
   #       "createTime": ""  # 创建时间
   #       })
   # test.close()
   #  process=Mysql("process")
   #  print(process.get_columns())
   taskbatch=Mysql("taskbatch")
   taskbatch.insertbydic({"batchid":"ads"})
