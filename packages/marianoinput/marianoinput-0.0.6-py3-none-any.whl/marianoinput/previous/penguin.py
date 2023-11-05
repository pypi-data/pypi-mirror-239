#created 21 Nov, 2022
#enc 27 Nov, 2022





def enc_0001_getprompt_fornum(asfloat,callno,desc,usedefault,defaultval):
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
def enc_0002_getnumber(desc, defaultval, asfloat=False, usedefault=True, callno=1) :
       
    
    prompt=enc_0001_getprompt_fornum(asfloat,callno,desc,usedefault,defaultval)
    prompt+=" >>\n "
        
    res=input(prompt)
    res=res.strip().upper()
    result=defaultval
    
    if len(res)==0  and usedefault:
        return defaultval
    
    if len(res)==0:
        return enc_0002_getnumber(desc,defaultval,asfloat=asfloat,\
                         usedefault=usedefault,callno=callno+1)
                         
    
    try:
        if asfloat:
            return float(res)
        else:
            return int(res)        
    except:
        return enc_0002_getnumber(desc,defaultval,asfloat=asfloat,\
                        usedefault=usedefault,callno=callno+1)        
    pass

def enc_0003_isNan(val):
    t=type(val)
    if t==int or t ==float:
        return False
    return true

    

# for integers and floats   
def enc_0004_getnumberbw(desc,minval,maxval, asfloat=False, callno=1):
    if enc_0003_isNan(minval) or enc_0003_isNan(maxval) or minval>maxval:
        print("invalid min and max values")
        return 0

    prompt=enc_0001_getprompt_fornum(asfloat,callno,desc,False,0)
    prompt+=f"\nminimum {minval}, maximum {maxval} >>\n "
    
    res=input(prompt)
    res=res.strip().upper()
    
    
    if len(res)==0:
        return enc_0004_getnumberbw\
                (desc,minval,maxval, asfloat=asfloat, callno=callno+1)
    
    
    try:
        if asfloat:
            result=float(res)
        else:               
            result=int(res)
        
        if result>=minval and result<=maxval:
            return result
        else:
            return enc_0004_getnumberbw(desc,minval,maxval,asfloat=asfloat,callno=callno+1)
        
        
    except:
        return enc_0004_getnumberbw(desc,minval,maxval,asfloat=asfloat,callno=callno+1)      
    pass

def enc_0005_getyesno(desc, attempt=1):
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
        return enc_0005_getyesno(desc,attempt)
    pass

def enc_0006_getstr(desc, defaultval="",  minlen=1, callno=1):
    
    if enc_0003_isNan(minlen) and minlen>=1:
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
        return enc_0006_getstr(desc,minlen=minlen,defaultval=defaultval, callno=callno+1)
    pass

class PenguinPrompt: 
    """
    help line 1
    help line 2
    """
    def prompt_yesno(self,desc):
        return enc_0005_getyesno(desc)

    def prompt_str(self,desc,minlen=1):
        return enc_0006_getstr(desc,minlen=minlen)
    
    def prompt_str_default(self,desc,defaultval,minlen=1):
        return enc_0006_getstr(desc,defaultval=defaultval,minlen=minlen)
    



    def prompt_int_default(self,desc,defaultval):
        return enc_0002_getnumber(desc,defaultval,asfloat=False,usedefault=True)
    
    def prompt_int(self,desc):
        return enc_0002_getnumber(desc,0,asfloat=False,usedefault=False)
    
    def prompt_int_range(self,desc,minval,maxval):
        return enc_0004_getnumberbw(desc,minval,maxval,asfloat=False)

    
    

    def prompt_float_default(self,desc,defaultval):
        return enc_0002_getnumber(desc,defaultval,asfloat=True,usedefault=True)
    
    def prompt_float(self,desc):
        return enc_0002_getnumber(desc,0,asfloat=True,usedefault=False)


    def prompt_float_range(self,desc,minval,maxval):
        return enc_0004_getnumberbw(desc,minval,maxval,asfloat=True)
    
    pass



    





    
    





