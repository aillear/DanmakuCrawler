# 一个小爬虫

基于`python`的小爬虫, 用于提取`bilibiili`的视频弹幕并加以简单的处理以及可视化。

运行 `main.py` 为无GUI版本

运行 `mainWithGUI.py` 为带GUI版本



具体应该实现的功能：

- 数据获取
- 数据分析
- 可视化

## 数据获取部分:

数据获取模块有以下几个功能：

- 根据用户输入的关键字以及需要的视频个数爬取相关视频的`BV`号
- 根据*BV*号获取相关视频的*cid*
- 根据*cid*获取相关视频的当前弹幕池
- 最后汇总各个视频的弹幕池，形成一个字符串列表

---

#### *BV*号获取：`BVFinder(_keyword: str, _video_count: int)`

- [x] 是否完成

- 功能实现：通过关键词获取前n页的相关视频*BV*号, 返回*BV*号的字符串列表
- 参数：
  - _keyword: 关键词
  - _video_count: 读取的视频数量
- 返回值： 获取的*BV*号字符串列表



#### *cid*获取： `CidReader(_bv: str)`

- [x] 是否完成

- 功能实现：读取BV号对应视频的cid
- 参数：_bv ： 视频*BV*号
- 返回值： 对应的*cid*



#### 弹幕池读取： `DanmakuReader(_cid: str)`

- [x] 是否完成

- 功能实现：根据cid读取当前视频弹幕池内弹幕
- 参数：cid ： cid
- 返回值： 弹幕字符串列表



#### 进一步封装：`DataCollect(_keyword: str, _video_count: int)`

- [x] 是否完成

- 功能实现： 封装本模块的功能
- 参数：
  - _keyword: 关键词
  - _video_count: 读取的视频数量
- 返回值：收集的弹幕列表





## 数据分析部分：

数据分析模块应该有以下几个功能：

- 进行简单的统计同类型弹幕个数，最后生成一个列表，列表的元素为一个元组,元组第一个元素为弹幕,第二个元素为出现次数。元组的排序按照次数从大到小
- 将上述列表保存为`.csv`文件，分为两列。每一行对应一条弹幕，第一列为弹幕数量，第二列为弹幕文本。按顺序从高到低排列。
- 将字符串列表组合成字符串并且分词，为接下来可视化做词云做准备

需要两个模块，一个负责写文件，另一个就是负责分析数据

---

#### 弹幕统计： `StrStatistics(_str_list: list[str])`

- [x] 是否完成

- 功能实现：统计传入的字符串列表中各个字符串出现的次数。返回列表元素为(string, int)样式的元组。
- 参数：_str_list： 字符串列表
- 返回值： 结果保存为特殊格式的列表



#### 文件保存： `List2CSV(_list: list[tuple[str, int]], _file_name: str)`

- [x] 是否完成

  - 功能实现：将列表按照某种规则存为`.CSV`文件。文件将保存在`DanmakuData`文件夹下

- 参数：
  - _list: 目标字典

  - _file_name： 保存的文件名

    



#### 分词：事实上，直接第三方库的接口就已经够方便了。不需要在进行封装了



## 数据可视化部分

- 通过数据分析部分得到的分词结果进行词云生成

---

#### 生成词云图：`CreateWordCloudImage(_content: str, _file_name: str, _max_words=100, _width=1000, _height=1000, _mask_name='default.png', _font_name='default.ttc')`

- [x] 是否完成

- 功能实现：创建词云图。遮罩图默认为空。此时长宽设置生效。自定义遮罩请放置在`ImageMasks`文件夹里；字体默认为微软雅黑。自定义字体请放在`Fonts`内。
- 参数：
  - _content: 分过词的内容
  - _file_name： 保存的词云图名
  - _max_words: 可以显示的最大词数
  - _width:  宽
  - _height: 高
  - _mask_name: 遮罩图片的名字
  - _font_name: 字体名



# 一个小UI系统

整活：为上面的小爬虫写一个UI。计划采用~~`pygame`~~库来实现

计划采用`tkinter`库来实现

设计了6个界面:

1. 爬虫选项界面
2. 爬取中提示界面 
3. 爬取结束界面
4. 词云生成界面
5. 生成中界面
6. 生成成功界面

界面由元素构成。为`Frame`对象

设计了一个`PanelMgr`模块用来管理界面

设计 `Delegate` 来实现多播委托

设计 `DataKeeper` 模块来全局暂存数据,用于界面之间信息交换

设计 `EventCenter` 模块,用来解决主,副线程之间通信的问题

### 界面

每一个界面都写一个文件，每一个文件都写一个函数，函数返回的就是frame类型的变量

每个函数设置一个变量，为该面板的唯一标识符。方便直接将所有面板都放进一个多播委托之内。

当函数传入的参数跟自己的标识符不一致的时候直接返回None， 一致的时候返回生成的frame面板 



#### 爬虫选项界面

- [x] done

- 关键词 -- 输入框
- 搜索数 -- 高级输入框
- 保存文件名 -- 输入框
- 启动！ -- 按钮

#### 爬取中提示界面

- [x] done

- 爬取中 -- 文本框
- 用时 -- 文本框

#### 爬取结束界面

- [x] done

- 第i条 - 文本框
- 弹幕 - 文本框
- 上一页， 下一页 -- 按钮
- 已保存为 xx.csv -- 文本框
- 去生成词云 -- 按钮

#### 词云生成界面

- [x] done
- 生成图片名 -- 输入框
- 最大次数 -- 高级输入框， 默认100
- 图片尺寸 -- 输入框
- 字体 -- 复合框
- 遮罩 -- 复合框
- 图片 -- 图片
- 启动 -- 按钮

#### 生成中界面

- [x] done

- 生成中 -- 文本框

#### 生成成功

- [x] done

- 生成成功，保存为xxx， 以下为预览 -- 文本框
- 图片 -- 图片
- 再来一次 -- 按钮

### `PanelMgr`

用来管理UI面板的单例类

主要方法: `SwitchPanel(self, _root: tk.Tk, _id: int)`

- 用于切换到目标ID的界面

### `Delegate`

实现了多播委托,重载了部分运算符。初步确保了安全性，降低代码耦合程度



### `DataKeeper`

用来解决面板之间、面板与其他模块之间信息传递的问题

降低代码耦合程度

##### 主要方法：

1. `SendData(self, name: str,  data)`
   - 向 `DataKeeper` 模块存储信息
2. `GetData(self, name: str)`
   - 向 `DataKeeper` 模块读取信息



### `EventCenter`

事件中心，用来降低代码耦合，解决不同线程之间通信问题

有加必有减！

##### 主要方法：

1. `AddEventListener(self, name: str, action)`
   - 添加事件监听， 事件名为 name， 事件为 action
2. `RemoveEventListener(self, name: str, action)`
   - 移除事件监听， 事件名为 name， 事件为 action
3. `EventTrigger(self, name: str, *args, **kwargs)`
   - 触发事件， 事件名为 name
4. `DeleteEvent(self, name: str)`
   - 删除事件， 事件名为 name
5. `Clear(self)`
   - 清除所有的事件



# 
