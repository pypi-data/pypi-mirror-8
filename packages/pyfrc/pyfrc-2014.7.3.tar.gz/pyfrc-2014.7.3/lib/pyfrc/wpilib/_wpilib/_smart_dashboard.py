'''
    Simple + dumb implementations of SmartDashboard related objects. If you
    want a full implementation, install pynetworktables
'''


class SmartDashboard(object):

    _table = None
    
    @staticmethod
    def _reset():
        SmartDashboard._table = None
    
    @staticmethod
    def init():
        if SmartDashboard._table is None:
            SmartDashboard._table = NetworkTable.GetTable("SmartDashboard")
      
    @staticmethod
    def PutData(key, data):
        SmartDashboard._table.PutData(key, data)
    
    # not implemented in RobotPy
    #@staticmethod
    #def GetData(self, key):
    #    return SmartDashboard.data[key]
    
    @staticmethod
    def PutBoolean(key, value):
        SmartDashboard._table.PutBoolean(key, value)
        
    @staticmethod
    def GetBoolean(key):
        return SmartDashboard._table.GetBoolean(key)
    
    @staticmethod
    def PutNumber(key, value):
        SmartDashboard._table.PutNumber(key, value)
    
    @staticmethod    
    def GetNumber(key):
        return SmartDashboard._table.GetNumber(key)
        
    @staticmethod
    def PutString(key, value):
        SmartDashboard._table.PutString(key, value)
    
    @staticmethod
    def GetString(key):
        return SmartDashboard._table.GetString(key)

    @staticmethod
    def PutValue(key, value):
        SmartDashboard._table.PutValue(key, value)
    
    # not implemented in RobotPy
    #def GetValue(self, key):
    #    return SmartDashboard._table.GetValue(key)
    
class SendableChooser(object):

    def __init__(self):
        self.choices = {}
        self.selected = None

    def AddObject(self, name, obj):
        self.choices[name] = obj
        
    def AddDefault(self, name, obj):
        self.selected = name
        self.choices[name] = obj
        
    def GetSelected(self):
        if self.selected is None:
            return None
        return self.choices[self.selected]
    

class NetworkTable(object):

    _tables = {}
    
    @staticmethod
    def _reset():
        NetworkTable._tables = {}
    
    @staticmethod
    def GetTable(table_name):
        table = NetworkTable._tables.get(table_name)
        if table is None:
            table = NetworkTable._NetworkTable()
            NetworkTable._tables[table_name] = table
        return table 
        
    class _NetworkTable(object):
        
        def __init__(self):
            self.data = {}
            self._subtables = {}
        
        def IsConnected(self):
            return True
        
        def IsServer(self):
            return True
        
        def AddConnectionListener(self, listener, immediateNotify):
            pass
        
        def RemoveConnectionListener(self, listener):
            pass
        
        def AddTableListener(self, name, listener, isNew):
            pass
        
        def AddSubTableListener(self, listener):
            pass
        
        def RemoveTableListener(self, listener):
            pass
        
        def GetSubTable(self, key):
            table = self._subtables.get(key)
            if table is None:
                table = NetworkTable._NetworkTable()
                self._subtables[key] = table
            return table
        
        def ContainsKey(self, key):
            return key in self.data
        
        def ContainsSubTable(self, key):
            return key in self._subtables
        
        
        def PutData(self, key, data):
            self.data[key] = data
        
        # not implemented in RobotPy
        #def GetData(self, key):
        #    return self.data[key]
        
        def PutBoolean(self, key, value):
            if not isinstance(value, bool):
                raise RuntimeError("%s is not a boolean (is %s instead)" % (key, type(value)))
            self.data[key] = value
            
        def GetBoolean(self, key):
            return self.data[key]
        
        def PutNumber(self, key, value):
            if not isinstance(value, (int, float)):
                raise RuntimeError("%s is not a number (is %s instead)" % (key, type(value)))
            self.data[key] = value
          
        def GetNumber(self, key):
            return self.data[key]
            
        def PutString(self, key, value):
            self.data[key] = str(value)
        
        def GetString(self, key):
            return self.data[key]
    
        def PutValue(self, key, value):
            self.data[key] = value
    
        # not implemented in RobotPy
        #@staticmethod
        #def GetValue(self,key):
        #    return self.data[key]
    
class ITableListener(object):
    pass

class LiveWindow(object):
    
    @staticmethod
    def GetInstance():
        try:
            return LiveWindow._instance
        except:
            LiveWindow._instance = LiveWindow()
            
        return LiveWindow._instance
    
    def SetEnabled(self, enabled):
        pass

#
# complex types.. 
#

class ComplexData(object):
    
    def __init__(self, type):
        self.type = type
        
    def GetType(self):
        return self.type

class ArrayData(ComplexData):
    
    def __init__(self, type):
        super().__init__(type)
        self._array = []
        
        
    def remove(self, index):
        del self._array[index]
        
    def setSize(self, size):
        raise NotImplementedError("I'm lazy")
    
    def size(self):
        return len(self._array)

class NumberArray(ArrayData):
    
    def __init__(self):
        super().__init__(None)
    
    def get(self, index):
        return self._array[index]
    
    def set(self, index, value):
        self._array[index] = value
    
    def add(self, value):
        self._array.append(value)

class StringArray(ArrayData):
    
    def __init__(self):
        super().__init__(None)
    
    def get(self, index):
        return self._array[index]
    
    def set(self, index, value):
        self._array[index] = value
    
    def add(self, value):
        self._array.append(value)
