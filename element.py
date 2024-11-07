import math

class DPoint:  
    def __init__(self, x=0, y=0):  
        self.x = x
        self.y =y 
    def __eq__(self, other):  
        # 如果 other 也是 Point 实例，并且 x 和 y 坐标相等，则返回 True  
        if isinstance(other, DPoint):  
            return (round(self.x/12)*1.0, round(self.y/12)*1.0) == (round(other.x/12)*1.0, round(other.y/12)*1.0)  
        return False  
  
    def __hash__(self):  
        # 返回 (x, y) 元组的哈希值  
        return hash((round(self.x/12)*1.0, round(self.y/12)*1.0))  
    def __getitem__(self, index):  
        # 支持通过索引访问坐标  
        if index == 0:  
            return self.x  
        elif index == 1:  
            return self.y  
        else:  
            raise IndexError("Point index out of range (0 or 1 expected)")  
  
    def __setitem__(self, index, value):  
        # 支持通过索引修改坐标  
        if index == 0:  
            self.x = value
        elif index == 1:  
            self.y = value
        else:  
            raise IndexError("Point index out of range (0 or 1 expected)") 
    def __repr__(self):  
        return f"Point({self.x}, {self.y})"  
    def as_tuple(self):
        return (self.x,self.y)


class DSegment:  
    # Segment is essentially a Line with an implied direction and length  
    def __init__(self, start_point: DPoint=DPoint(0,0), end_point: DPoint=DPoint(1,0),ref=None):  
        self.start_point = start_point  
        self.end_point = end_point  
        self.ref=ref
        self.isConstraint=False
        self.isCornerhole=False
        self.StarCornerhole = None
    def __len__(self):
        return 2

    def __eq__(self, other):  
        if isinstance(other, DSegment):  
            return (self.start_point, self.end_point,self.ref) == (other.start_point, other.end_point,self.ref)  
        return False  
  
    def __hash__(self):  
        return hash((self.start_point, self.end_point))
    def __getitem__(self, index):  
        # 支持通过索引访问坐标  
        if index == 0:  
            return self.start_point 
        elif index == 1:  
            return self.end_point  
        else:  
            raise IndexError("Point index out of range (0 or 1 expected)")  

    def __setitem__(self, index, value):  
        # 支持通过索引修改坐标  
        if index == 0:  
            self.start_point = value  
        elif index == 1:  
            self.end_point = value  
        else:  
            raise IndexError("Point index out of range (0 or 1 expected)") 
    def length(self):  
        return ((self.end_point.x - self.start_point.x) ** 2 +   
                (self.end_point.y - self.start_point.y) ** 2) ** 0.5  
    def mid_point(self):
        return DPoint((self.start_point.x+self.end_point.x)/2,(self.start_point.y+self.end_point.y)/2)
  
    def __repr__(self):  
        return f"Segment({self.start_point}, {self.end_point}, length={self.length()}, ref={self.ref})"  
    # def setConstraint(self,isConstraint=0):
    #     if isConstraint:
    #         self.isConstraint=2

#color=7 white color=3 green
class DLine:  
    def __init__(self, start_point: DPoint=DPoint(0,0), end_point: DPoint=DPoint(1,0),color=7):  
        self.start_point = start_point  
        self.end_point = end_point  
        self.color=color
        # self.computeCenterCoordinateAndWeight()

    def __repr__(self):  
        return f"Line({self.start_point}, {self.end_point})"  
    

    # def computeCenterCoordinateAndWeight(self):
    #     s=DSegment(self.start_point,self.end_point,None)
    #     self.weight=s.length()
    #     self.bc=DPoint((s.start_point.x+s.end_point.x)/2,(s.start_point.y+s.end_point.y)/2)

class DLwpolyline:  
    def __init__(self, points: list[DPoint],color=7,isClosed=False):  
        self.points = points
        self.color=color  
        self.isClosed=isClosed
        # self.computeCenterCoordinateAndWeight()
  
    def __repr__(self):  
        return f"Lwpolyline({self.points})"  
  
    # def computeCenterCoordinateAndWeight(self):
    #     w=0
    #     x=0
    #     y=0
    #     n=len(self.points)
    #     for i in range(n-1):

    #         s=DSegment(self.points[i],self.points[i+1],None)
    #         l=s.length()
    #         w+=l
    #         x+=l*(s.start_point.x+s.end_point.x)/2
    #         y+=l*(s.start_point.y+s.end_point.y)/2
    #     if self.isClosed:
    #         s=DSegment(self.points[-1],self.points[0],None)
    #         l=s.length()
    #         w+=l
    #         x+=l*(s.start_point.x+s.end_point.x)/2
    #         y+=l*(s.start_point.y+s.end_point.y)/2
    #     self.weight=w
    #     self.bc=DPoint(x/w,y/w)


class DArc:  
    def __init__(self, center: DPoint, radius: float, start_angle: float, end_angle: float,color=7):  
        self.center = center  
        self.radius = radius  
        self.start_angle = start_angle  # in degrees  
        self.end_angle = end_angle      # in degrees  
        self.color=color
        sa=start_angle/180*math.pi
        ea=end_angle/180*math.pi
        c1=math.cos(sa)
        s1=math.sin(sa)
        c2=math.cos(ea)
        s2=math.sin(ea)
        self.start_point=DPoint(center[0]+radius*c1,center[1]+radius*s1)
        self.end_point=DPoint(center[0]+radius*c2,center[1]+radius*s2)
  
    def __repr__(self):  
        return (f"Arc(center={self.center}, radius={self.radius}, "  
                f"start_angle={self.start_angle}, end_angle={self.end_angle})")  
    
    # def __eq__(self, other):
    #     if isinstance(other, DArc):
    #         return (self.center, self.radius, self.start_angle, self.end_angle) == (other.center, other.radius, other.start_angle, other.end_angle)
    #     return False
        
  

class DText:  
    def __init__(self,bound,insert: DPoint=DPoint(0,0),color=7,content="",height=100):  
        self.bound=bound
        self.insert=insert
        self.color=color
        self.content=content
        self.height=height

  
    def __repr__(self):  
        return f"Text({self.insert}, color:{self.color},content:{self.content},height:{self.height})"  
  


class DCornorHole:
    cornor_hole_id=0
    def __init__(self,segments=[]):
        self.segments=segments
        self.ID=DCornorHole.cornor_hole_id
        DCornorHole.cornor_hole_id+=1

