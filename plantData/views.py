# Create your views here.
# -*- encoding:utf-8 -*-
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template.loader import get_template
from django.template import context,RequestContext
from django.shortcuts import render_to_response,render
from plantData.models import *
import datetime
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def expert_login(request):
    errors=[]
    if 'txtExpertName' in request.GET:
        exName=request.GET['txtExpertName']
        exPw=request.GET['expertPassword']
        if not exName.strip():
            errors.append("用户名不能为空!")
        else:
            exAccount=Expert.objects.filter(exp_acount__icontains=exName)
            if not exAccount:
                errors.append("用户名或密码错误!")
            else:
                if exAccount[0].exp_password!=exPw:
                    errors.append("用户名或密码错误！")
                else:
                    exId=exAccount[0].expertId
                    return render_to_response('expert/expert_search.html',{'exId':exId},context_instance=RequestContext(request))#这句是跳转的决定语句
    return render_to_response('expert/expert_login.html',{'errors':errors})
def expert_userQue(request,exId,nowNum):
    error=[]
    inform=''
    credit=''
    choose=''
    id1,id2,id3=0,0,0
    name1,name2,name3=0,0,0
    expert=list(Expert.objects.filter(expertId__icontains=int(exId)))[0]
    answer1=''
    if 'plantName' in request.GET: 
        plantName = request.GET['plantName']
        if not plantName:
            error.append("请输入植物名称！")
        else:
            answer1=Plant.objects.filter(plant_name__icontains=plantName)
            if not answer1:
                error.append("您要找的植物数据不存在！")
            else:
                if len(answer1)==1:
                    id1=answer1[0].plantId
                    name1=answer1[0].plant_name
                elif len(answer1)==2:
                    id1=answer1[0].plantId
                    id2=answer1[1].plantId
                    name1=answer1[0].plant_name
                    name2=answer1[1].plant_name
                elif len(answer1)>=3:
                    id1=answer1[0].plantId
                    id2=answer1[1].plantId
                    id3=answer1[2].plantId
                    name1=answer1[0].plant_name
                    name2=answer1[1].plant_name
                    name3=answer1[2].plant_name
    if 'group1' in request.POST:
        credit=request.POST['group1']
    if 'ans' in request.POST:
        choose=request.POST['ans']        
    queSet=Question.objects.all()#数据库过滤出来的类似数组的其实是QuerySet
    queList=list(queSet)
    target=queList[int(nowNum)]
    lastNum=int(nowNum)
    nextNum=int(nowNum)
    lastQue=target
    nextQue=target
    try:
        nextQue=queList[int(nowNum)+1]
        nextNum=int(nowNum)+1
    except IndexError:
        pass
    try:
        if int(nowNum)>0:
            lastQue=queList[int(nowNum)-1]
            lastNum=int(nowNum)-1
    except IndexError:
        pass         
    if int(nowNum)==nextNum:
        target=nextQue
    if int(nowNum)==lastNum:
        target=lastQue
    targetAdd=target.imge_other1.split('plantData')[1]
    if answer1!='' and choose!='' and credit!='':
        newAns=Answer(que_id=target,pla_id=list(answer1)[int(choose)],exp_id=expert,ans_credit=credit,ans_time=str(datetime.datetime.now()).split()[0])
        newAns.save()
        inform="答案推送成功！"
    return render_to_response('expert/expert_search.html',{'exId':exId,'nowNum':nowNum,'target':target,\
                                                           'targetAdd':targetAdd,'nextNum':nextNum,\
                                                           'lastNum':lastNum,'credit':credit,'choose':choose,\
                                                           'error': error,'inform':inform,\
                                                           'id1':id1,'id2':id2,'id3':id3,\
                                                           'name1':name1,'name2':name2,'name3':name3},context_instance=RequestContext(request))

def look_pic(request,offset):
    target=Plant.objects.filter(plantId=int(offset))
    image1=target[0].plant_image1
    image2=target[0].plant_image2
    image3=target[0].plant_image3
    describe=target[0].other_details
    return render_to_response('expert/lookpic.html',{'image1':image1,'image2':image2,'image3':image3,'describe':describe})
def expertLookInfo(request,exId):
    expSet=Expert.objects.filter(expertId__icontains=exId)#数据库过滤出来的类似数组的其实是QuertSet
    expData=list(expSet)[0]    
    return render_to_response("expert/expert_info.html",{'exId':exId,'expData':expData})
def expertLookHist(request,exId):
    try:    
        expSet=Expert.objects.filter(expertId__icontains=exId)#数据库过滤出来的类似数组的其实是QuertSet
        expData=list(expSet)[0]
        resSum=[]
        ansSum=list(expData.answer_set.all())
        for x in ansSum:
            quesImge=x.que_id.imge_other1.split('plantData')[1]
            resSum.append([x,quesImge])
        return render_to_response("expert/expert_hist.html",{'exId':exId,'resSum':resSum}) 
    except:
        return render_to_response("expert/expert_hist.html",{'exId':exId})    


def user_login(request):
    errors=[]
    if 'txtUserName' in request.GET:
        userName=request.GET['txtUserName']
        userPw=request.GET['txtPassword']
        if not userName.strip():
            errors.append("用户名不能为空!")
        else:
            user=User.objects.filter(user_name__icontains=userName)
            if not user:
                errors.append("用户名或密码错误!")
            else:
                if user[0].user_passWd!=userPw:
                    errors.append("用户名或密码错误！")
                else:
                    userId=user[0].userId
                    return render_to_response('user/userQues.html',{'errors':errors,'userId':userId},context_instance=RequestContext(request))#这句是跳转的决定语句
    return render_to_response('user/user_login.html',{'errors':errors})

def add_photo(request,userId):
        return render_to_response("user/userQues.html",{'userId':userId},context_instance=RequestContext(request))
def add_photo_submit(request,userId):
    def change_time(nowTime):
        newName=nowTime.split('.')[1]+nowTime.split(':')[1]
        return newName
    message=[]
    try:
        userSet=User.objects.filter(userId__icontains=userId)#数据库过滤出来的类似数组的其实是QuerySet
        userData=list(userSet)
        assert userData!=[]        
        quesText=request.POST['message']
        reqfile = request.FILES['picfile']#picfile要和html里面一致
        img = Image.open(reqfile)
        img.thumbnail((500,500),Image.ANTIALIAS)#对图片进行等比缩放
        img_name="userPic/"+change_time(str(datetime.datetime.now()))+".png"
        img_add="/home/shichangtai/plantQS/plantData/static/"+img_name
        img.save(img_add,"png")#保存图片
        message.append("上传成功！")
        #add_into_database
        newQues=Question(user_id=userData[0],que_time=str(datetime.datetime.now()).split()[0],imge_other1=img_add,describe=quesText)
        newQues.save()
        return render_to_response("user/userQues.html",{'message':message[0],'userId':userId,'img_name':img_name},context_instance=RequestContext(request))
        #return HttpResponse("上传成功！") 
    except Exception:
        message.append("上传失败，请检查图片格式是否正确！")
        return render_to_response("user/userQues.html",{'message':message[0],'userId':userId},context_instance=RequestContext(request))
    
def userLookInfo(request,userId):
    userSet=User.objects.filter(userId__icontains=userId)#数据库过滤出来的类似数组的其实是QuertSet
    userData=list(userSet)[0]    
    return render_to_response("user/userInfo.html",{'userId':userId,'userData':userData})
def userLookHist(request,userId):
    try:    
        userSet=User.objects.filter(userId__icontains=userId)#数据库过滤出来的类似数组的其实是QuertSet
        userData=list(userSet)[0]    
        quesSum=list(userData.question_set.all())
        userQuestion=[]
        for x in quesSum:
            quesImge=x.imge_other1.split('plantData')[1]
            ansList=list(x.answer_set.all())
            if ansList:
                ans=ansList[-1]#显示最新的答案回复
            else:
                ans=''
            userQuestion.append([x,quesImge,ans])    
        return render_to_response("user/userHist.html",{'userId':userId,'userQuestion':userQuestion})  
    except:
        return render_to_response("user/userHist.html",{'userId':userId})
        
def user_regiInfo(request):       
    try:    
        inform="注册成功"        
        regiUser=request.POST['regiUserName']
        regiPass=request.POST['regiPassword']
        regiGender=request.POST['regiGender']
        regiBirth=request.POST['regiBirth']
        regiName=request.POST['regiRealName']
        assert regiUser!='' 
        assert regiPass!='' 
        assert regiGender!='' 
        newData=User(user_name=regiUser,user_passWd=regiPass,gender=regiGender,name=regiName,birth=regiBirth)
        newData.save()            
    except Exception:
        inform="注册失败，请检查所输入的信息！"   
    finally:    
        return render_to_response("user/user_register.html",{'inform':inform},context_instance=RequestContext(request))
    
