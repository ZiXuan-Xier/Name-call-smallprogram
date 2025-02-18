import tkinter as tk
import json
import re
from operator import index
from time import sleep

# 统一把表格的设置放这里
GRID_CONFIG = {
    'X_offset': 0.05,
    'Y_offset': 0.05,
    'X_space': 0.15,
    'Y_space': 0.1,
    'Columns': 6
}

# 简单包装一下数据容器，对数据的各种修改均通过这个容器操作
class DataManager:
    def __init__(self) -> None:
        self.data: list[str] = []

    def save(self, file_path: str = './save/cache.json') -> None:
        with open(file_path, 'w+', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)

    def load(self, file_path: str = './save/cache.json') -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            load_data = json.load(f)
        # 略过校验load_data是否符合要求
        self.data = load_data

    # 返回插入数据的index
    def add(self, value: str) -> int:
        self.data.append(value)     #append 方法用于在列表的末尾添加一个新的元素
        return len(self.data) - 1

    def remove(self, index: int) -> None:
        del self.data[index]

    def all_remove(self)->None:
        self.data: list[str] = []




# 包装一下对按扭组合的管理器，对按钮组合的各项功能由这个容器操作
class CellManager:
    def __init__(self, root: tk.Tk, data_manager: DataManager, config: dict[str, float] = GRID_CONFIG) -> None:
                        #root，主窗口，data_manager，按钮状态管理，config，按钮位置，GRID_CONFIG是已经拟定好的字典
        self.root = root
        self.data_manager = data_manager
        self.config = config
        # 把按钮存在list中
        self.cells: list[CellButton] = []


    def add_cell(self, text: str, index: int) -> None:
        self.cells.append(CellButton(index, text, self))

    def init_cells(self) -> None:
        for cell in self.cells:
            cell.button.destroy()
        # 重置按钮list，python自动销毁这些CellButton对象实例
        self.cells = []
        for index, text in enumerate(self.data_manager.data):
            self.cells.append(CellButton(index, text, self))
    def cell_all_remove(self)-> None:
        for cell in self.cells:
            cell.button.destroy()


    def on_cell_remove(self, removed_index: int) -> None:
        self.data_manager.remove(removed_index)
        del self.cells[removed_index]
        for new_index in range(removed_index, len(self.cells)):
            self.cells[new_index].update(new_index)
    #更新每个按钮的位置

# 包装一下按钮
class CellButton:
    def __init__(self, index: int, text: str, cell_manager: CellManager):
        self.index = index
        self.text = text
        self.cell_manager = cell_manager
        self.button: tk.Button = None
        self.all_remove_Cell()
        self.create()

    def remove(self) -> None:
        self.button.destroy()
        self.cell_manager.on_cell_remove(self.index)

    def all_remove(self)-> None:
        self.cell_manager.cell_all_remove()
        for i in range(len(data_manager.data)-1,-1,-1):
            self.cell_manager.on_cell_remove(i)


    def all_remove_Cell(self)-> None:
        self.button_all_delete = tk.Button(root, text='一键删除', width=8, height=1, command=self.all_remove, font=6)
        self.button_all_delete.place(relx=0.84, rely=0.001)


    def create(self) -> None:
        self.button =tk.Button(self.cell_manager.root, text=self.text,
                               width=15,height=2, font=('微软雅黑',14,'bold'),
                               command=self.remove)
        x, y = self.get_position()
        self.button.place(relx = x, rely = y)

    def update(self, new_index: int) -> None:
        self.button.destroy()
        self.index = new_index
        self.create()

    def get_position(self) -> tuple[float, float]:
        row_n = int(self.index / self.cell_manager.config['Columns'])
        column_n = self.index % self.cell_manager.config['Columns']
        x = self.cell_manager.config['X_offset'] + column_n * self.cell_manager.config['X_space']
        y = self.cell_manager.config['Y_offset'] + row_n * self.cell_manager.config['Y_space']
        return (x, y)

def load_cache() -> None:
    data_manager.load()
    cell_manager.init_cells()

def save_cache() -> None:
    data_manager.save()

def all_input()-> None:
    all_text=str(p.get())
    textlist=re.split("[,|，. 。-]",all_text)
    if len(textlist)>1:
        for i in range(len(textlist)):
            index=data_manager.add(textlist[i])
            cell_manager.add_cell(textlist[i],index)
    else:
        text = str(p.get())
        index = data_manager.add(text)
        cell_manager.add_cell(text, index)







#更新日志
class Update_log:
    def __init__(self,index):
        self.index=index
        pass
    def date(self):
         window=tk.Toplevel()
         window.title('更新日志')
         window.geometry('1024x860')
         self.index=1
         self.text={}
         self.text[1]='【V-1.0|2024,11,24】代码初步框架完成，但是底层逻辑错误，仅能运行简单功能，不可存读取'
         self.text[2]='【V-1.1|2024,11,25】由张先生帮助重构优化代码，成功实现存读取功能'
         self.text[3]='【V-1.2|2024,11,27】新增功能：多数据一键输入创建按钮'
         self.text[4]='【V-1.2.1|2025,2,18】极大的优化代码释放内存空间，新增功能：一键删除'
         for self.index in range(1,len(self.text)+1):
             self.upl=tk.Label(window,text=f'{self.text[self.index]}',font=('微软雅黑',16))
             self.upl.place(relx=0,rely=(self.index-1)*0.04)

root=tk.Tk()
root.title('统计小程序')
root.geometry('1280x800')
rl=tk.Label(root,text='这是一款主要用于统计签到人数、提交人数等功能的小程序,更多功能正在开发中~',font=('微软雅黑',12,'bold'))
root.resizable(False,False)
root.iconbitmap("title.ico")
rl.place(relx=0.257,rely=0.76)
rl1=tk.Label(root,text='V-1.2.1\n子轩大魔王',font=('微软雅黑',18,'bold'))
rl1.place(relx=0.88,rely=0.9)


update=Update_log(index)
data_manager = DataManager()        
cell_manager = CellManager(root, data_manager)



p=tk.Entry(root,width=25,font=('微软雅黑',22))
p.place(relx=0.31,rely=0.8)
ball=tk.Button(root,text='创建',width=20,height=2,command=all_input,font=('微软雅黑',16,'bold'))
ball.place(relx=0.36,rely=0.87)
#button_all_delete=tk.Button(root,text='一键删除',width=8,height=1,command=all_remove,font=6)
#button_all_delete.place(relx=0.90,rely=0.001)
b_save=tk.Button(root,text='保存',width=13,height=2,command=save_cache)
b_save.place(relx=0.61,rely=0.89)
b_load=tk.Button(root,text='读取',width=13,height=2,command=load_cache)
b_load.place(relx=0.71,rely=0.89)
b_update=tk.Button(root,text='更新日志',width=11,height=1,command=update.date)
b_update.place(relx=0.892,rely=0.86)

root.mainloop()
