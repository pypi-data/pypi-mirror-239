#python-in\penguin001.py
#created 21 Nov, 2022
#enc 27 Nov, 2022





def _kixtvsqtx_jsvryq(asfloat,callno,desc,usedefault,defaultval):
    stype=""
    if asfloat==False:
        stype=" (integer) "
        if callno>1:
            stype=" (integer- no decimals) "
    
    result=""
            
    if usedefault:
        result =desc+stype+" default is "+ str(defaultval)
    else:
        result =desc+stype
        
    if callno>1:
        result=f"attempt {callno}\n"+result
        
    return result

 
    

# for floats and ints
def _ljyszrgjw(desc, defaultval, asfloat=False, usedefault=True, callno=1) :
       
    
    prompt=_kixtvsqtx_jsvryq(asfloat,callno,desc,usedefault,defaultval)
    prompt+=" >>\n "
        
    res=input(prompt)
    res=res.strip().upper()
    result=defaultval
    
    if len(res)==0  and usedefault:
        return defaultval
    
    if len(res)==0:
        return _ljyszrgjw(desc,defaultval,asfloat=asfloat,\
                         usedefault=usedefault,callno=callno+1)
                         
    
    try:
        if asfloat:
            return float(res)
        else:
            return int(res)        
    except:
        return _ljyszrgjw(desc,defaultval,asfloat=asfloat,\
                        usedefault=usedefault,callno=callno+1)        
    pass

def _oyNgt(val):
    t=type(val)
    if t==int or t ==float:
        return False
    return True

    

# for integers and floats   
def _kixryqfivfa(desc,minval,maxval, asfloat=False, callno=1):
    if _oyNgt(minval) or _oyNgt(maxval) or minval>maxval:
        print("invalid min and max values")
        return 0

    prompt=_kixtvsqtx_jsvryq(asfloat,callno,desc,False,0)
    prompt+=f"\nminimum {minval}, maximum {maxval} >>\n "
    
    res=input(prompt)
    res=res.strip().upper()
    
    
    if len(res)==0:
        return _kixryqfivfa\
                (desc,minval,maxval, asfloat=asfloat, callno=callno+1)
    
    
    try:
        if asfloat:
            result=float(res)
        else:               
            result=int(res)
        
        if result>=minval and result<=maxval:
            return result
        else:
            return _kixryqfivfa(desc,minval,maxval,asfloat=asfloat,callno=callno+1)
        
        
    except:
        return _kixryqfivfa(desc,minval,maxval,asfloat=asfloat,callno=callno+1)      
    pass

def _ljydjxst(desc, attempt=1):
    prompt=desc+"?\n Yes(Y) or No(N)  >>  \n"
    if attempt>=2:
        prompt=desc+" ?  attempt "+str(attempt)+"\n Yes(Y) or No(N) >>  \n"
        
    
    res=input(prompt)
    res=res.strip().upper()
    if res=='Y' or res=='YES' or res=='TRUE':
        return True
    elif res=="N" or res=="NO" or res=="FALSE":
        return False
    else:    
        attempt+=1
        return _ljydjxst(desc,attempt)
    pass

def _mkzyzx(desc, defaultval="",  minlen=1, callno=1):
    
    if _oyNgt(minlen) and minlen>=1:
        print("invalid mimimum length")
        return ""
    
    prompt=""
    if callno>1:
        prompt+=f"attempt {callno}\n"
    
    if defaultval=="":
        prompt+=f"Enter {desc}"
    else:
        prompt+=f"Enter {desc} default is {defaultval}"
    
    if minlen>=2:
        prompt+=" min length="+str(minlen)+"  >>  \n"
    else:
        prompt+=" >>  \n"
        
    
    res=input(prompt).strip()
    
    
    if len(res)==0 and defaultval!="":
        #print("001deug","res=",res,"defaultval=",defaultval)
        return defaultval
    
    elif len(res)>=minlen:
        return res
    else:
        return _mkzyzx(desc,minlen=minlen,defaultval=defaultval, callno=callno+1)
    pass

class PenguinPrompt: 
    """
    help line 1
    help line 2
    """
    def prompt_yesno(self,desc):
        return _ljydjxst(desc)

    def prompt_str(self,desc,minlen=1):
        return _mkzyzx(desc,minlen=minlen)
    
    def prompt_str_default(self,desc,defaultval,minlen=1):
        return _mkzyzx(desc,defaultval=defaultval,minlen=minlen)
    



    def prompt_int_default(self,desc,defaultval):
        return _ljyszrgjw(desc,defaultval,asfloat=False,usedefault=True)
    
    def prompt_int(self,desc):
        return _ljyszrgjw(desc,0,asfloat=False,usedefault=False)
    
    def prompt_int_range(self,desc,minval,maxval):
        return _kixryqfivfa(desc,minval,maxval,asfloat=False)

    
    

    def prompt_float_default(self,desc,defaultval):
        return _ljyszrgjw(desc,defaultval,asfloat=True,usedefault=True)
    
    def prompt_float(self,desc):
        return _ljyszrgjw(desc,0,asfloat=True,usedefault=False)


    def prompt_float_range(self,desc,minval,maxval):
        return _kixryqfivfa(desc,minval,maxval,asfloat=True)
    
    pass



msg="""Hello Welcom to mariano input
marianoinput has PenguinPrompt,
with which you can use to easily get valid user input.
If user inputs invalid input, then it will re-prompt the user

To start :

from marianoinput import PenguinPrompt
pen= PenguinPrompt()
       
       
       
# Examples:
print("Example 1")
age=pen.prompt_int("whats you age ?")
print("your age is:",age)

print("Example 2")
age=pen.prompt_int_range("whats you age ?", 18,100)
print("your age is:",age)       
    
print("Example 3")
height=pen.prompt_float("whats you height in meters ?")
print("your height is:",height)       
    
print("Example 4")
height=pen.prompt_float_range("whats you height in meters ?",1,3)
print("your height is:",height)        
    

print("Example 5")
yesno= pen.prompt_yesno("Do you wish to continue ?")
print("you selected ",yesno)


       
       """

print(msg)


    





    
    





