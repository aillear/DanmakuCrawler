import tkinter
import tkinter.ttk
from Support.GetFileName import GetFileName
from GUI.PanelMgr import *
from Settings import *
from Support.DataKeeper import DataKeeper
from Support.EventCenter import EventCenter
from MainWork import Visualizor
import jieba
import _thread


def WCPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != WC_PANEL_ID:
        return None
    wc_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    # 第一行
    tk.Label(wc_panel, text='生成图片名').grid(row=1, column=1)

    temp = DataKeeper.instance.GetData('imageName')
    if temp is None:
        temp = 'default'
    image_name = tk.StringVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_name).grid(row=1, column=2)

    # 第二行
    tk.Label(wc_panel, text='最大词数').grid(row=2, column=1)

    temp = DataKeeper.instance.GetData('maxWordNum')
    if temp is None:
        temp = 100
    max_word_num = tk.IntVar(value=temp)
    tk.Spinbox(wc_panel, from_=50, to=500, increment=1, textvariable=max_word_num).grid(row=2, column=2)

    # 第三行
    tk.Label(wc_panel, text='图片尺寸').grid(row=3, column=1)

    temp = DataKeeper.instance.GetData('imageWidth')
    if temp is None:
        temp = 1000
    image_width = tk.IntVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_width).grid(row=3, column=2)

    tk.Label(wc_panel, text='x').grid(row=3, column=3)

    temp = DataKeeper.instance.GetData('imageHeight')
    if temp is None:
        temp = 1000
    image_height = tk.IntVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_height).grid(row=3, column=4)

    # 第四行
    tk.Label(wc_panel, text='字体').grid(row=4, column=1)

    fonts_name = tkinter.ttk.Combobox(wc_panel)
    fonts_name['value'] = GetFileName('./Fonts')
    fonts_name.current(0)
    fonts_name.grid(row=4, column=2)

    # 第五行
    # 按钮绑定函数
    # 1.保存数据 2.新线程生成图片 3.跳转界面
    def Transmit():
        #  保存数据
        DataKeeper.instance.SendData('imageName', image_name.get())
        DataKeeper.instance.SendData('maxWordNum', max_word_num.get())
        DataKeeper.instance.SendData('imageWidth', image_width.get())
        DataKeeper.instance.SendData('imageHeight', image_height.get())
        DataKeeper.instance.SendData('font', fonts_name.get())
        # 开新线程来生成词云
        # 订阅下生成玩事件,不过一般都不久
        EventCenter.instance.AddEventListener('WCOver', AfterWC)
        _thread.start_new_thread(WCHere, ())    # 新线程生成图片
        # 跳转界面
        PanelMgr.instance.SwitchPanel(_root, WCING_PANEL_ID)

    # 生成图片之后要做的事
    # 1.取消监听 2.跳转界面
    def AfterWC():
        EventCenter.instance.RemoveEventListener('WCOver', AfterWC)
        PanelMgr.instance.SwitchPanel(_root, WCOVER_PANEL_ID)    # 跳转界面

    tk.Button(wc_panel, text='启动!', command=Transmit).grid(row=5, column=1)
    wc_panel.pack()
    return wc_panel


# 生成词云的逻辑
def WCHere():
    danmaku_list = DataKeeper.instance.GetData('danmakuList')
    image_name = f"{DataKeeper.instance.GetData('imageName')}.png"
    image_width = DataKeeper.instance.GetData('imageWidth')
    image_height = DataKeeper.instance.GetData('imageHeight')
    max_word_num = DataKeeper.instance.GetData('maxWordNum')
    font = DataKeeper.instance.GetData('font')

    text = ' '.join((jieba.lcut('\n'.join(danmaku_list))))
    Visualizor.CreateWordCloudImage(text, _file_name=image_name, _width=image_width,
                                    _height=image_height, _font_name=font, _max_words=max_word_num)

    EventCenter.instance.EventTrigger('WCOver')
