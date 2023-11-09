import copy
import nl4py,time,copy

global list_zone
global list_pyturtle
list_pyturtle=[]
list_street=[]

def resize_world(n,x0,xf,y0,yf):
        c = "resize_world "+list2nllist([x0,xf,y0,yf])
        c = n.report(c)
        return c
def list2nllist(lis):
        s="["
        for i in lis:
            if type(i) == str:
                s+=' "'+i+'" '
            else :
                s+=' '+str(i)+' '
        s+="]"
        return s
def set_background(n,image):
        c = "set_background "+list2nllist([image])
        c = n.report(c)
        return c
def de_copy(a):
    return copy.deepcopy(a)
def run_netlogo(netlogo_home="C:/Program Files/NetLogo 6.2.2"):
    
    nl4py.initialize(netlogo_home)
    nl4py.startServer(netlogo_home)
    model = "./nelogopy.nlogo"
    n=nl4py.NetLogoApp()
    n.openModel(model)
    n.command("setup")
    return n
def distancebetween(n,fromm=0,target=1):
        id_fromm=fromm.id
        id_target=target.id
        c = "distanceto "+list2nllist([id_fromm,id_target])
        c = n.report(c)
        return c

def getxyturtle(n,turtle):
        id_turtle=turtle.id
        c = "getxyturtle "+list2nllist([id_turtle])
        c = n.report(c)
        c=eval(c)
        return c

class n_model:
    def __init__(self,netlogo_home="C:/Program Files/NetLogo 6.2.2"):
        pass
    def gui(self,netlogo_home="C:/Program Files/NetLogo 6.2.2"):
            nl4py.initialize(netlogo_home)
            nl4py.startServer(netlogo_home)
            model = "./nelogopy.nlogo"
            self=nl4py.NetLogoApp()
            self.openModel(model)
            self.command("setup")
           
            return self
            
class turtle:
    def __init__(self,n):
        self.id= id
        self.n= n
    def distanceto(self,target=1):
        id_fromm=self.id
        id_target=target.id
        c = "distanceto "+list2nllist([id_fromm,id_target])
        c = self.n.report(c)
        # idd = int(c[:-2])
        return c
    
    def face_to(self,target=1):
        id_fromm=self.id
        id_target=target.id
        c="faceto "+list2nllist([id_fromm,id_target])
        c=self.n.report(c)
        idd= int(c[:-2])
        return idd
    def move_to(self,id_target):
        fr=self.id
        c="moveto "+list2nllist([fr,id_target.id])
        c=self.n.report(c)

    def hideturtle(self):
        turtleid=self.id
        c="hideturtle "+list2nllist([turtleid])
        self.n.report(c)
    def set_shape(self,shape):
        turtleid=self.id
        c="set_shape "+list2nllist([turtleid,shape])
        self.n.report(c)
    def setxy(self,x,y):
        turtleid=self.id
        c="turtle_setxy "+list2nllist([turtleid,x,y])
        self.n.report(c)


    def fd(self,repeat=1):
        fr=self.id
        c="fdfd "+list2nllist([fr,repeat])
        self.n.report(c)

class street :
    def __init__(self, n,fromm=0,too=1,label="street",id_s=0,labelcolor=0,color=0,shape="aa",thickness=0.5):
        fromm=fromm.id
        too=too.id
        self.id = id
        self.create_street_ft(n,fromm,too,label,id_s,labelcolor,color,shape,thickness)
    def create_street_ft(self,n,fromm=20,too=10,label="street",id_s=0,labelcolor=0,color=0,shape="aa",thickness=0.5):
        c="create-street-ft "+list2nllist([fromm,too,label,id_s,labelcolor,color,shape,thickness])
        c=n.report(c)
        self.id= int(c[:-2])
        list_street.append(self)
        return self

class pyturtle(turtle) :
    def __init__(self, n,x=0,y=0,id=0,shape="car",size_shape=4,color=0,name="zn",labelcolor=0):

        super().__init__(n)
        self.id = id
        self.create_pyturtle_xyid(n,x,y,id,shape,size_shape,color,name,labelcolor)
  
    def create_pyturtle_xyid(self,n,x,y,id,shape,size_shape,color,name,labelcolor,):
        c="create-pyturtle-xyid "+list2nllist([x,y,id,shape,size_shape,color,name,labelcolor])
        c=n.report(c)
        self.id= int(c[:-2])
        return self