from GUI.PanelMgr import *
from Settings import *
from Support.DataKeeper import DataKeeper
from PIL import Image, ImageTk


img_tk = None

def WCOverPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != WCOVER_PANEL_ID:
        return None
    wc_over_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    image_name = DataKeeper.instance.GetData('imageName')
    if image_name is None:
        raise TypeError('image_name should not be None!')

    tk.Label(wc_over_panel, text=f'生成成功!保存为./WordCloudImage/{image_name}.png').grid(row=1, column=1)

    img = Image.open(f"./WordCloudImage/{image_name}.png")
    global img_tk
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(wc_over_panel, image=img_tk)
    label.grid(row=2)

    wc_over_panel.pack()
    return wc_over_panel
