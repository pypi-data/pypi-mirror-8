# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國102年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from 臺灣言語工具.基本元素.公用變數 import 無音
from 臺灣言語工具.基本元素.字 import 字
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.解析整理.型態錯誤 import 型態錯誤
from 臺灣言語工具.綜合標音.字綜合標音 import 字綜合標音
from 臺灣言語工具.基本元素.公用變數 import 標點符號
from 臺灣言語工具.音標系統.官話.官話注音符號 import 官話注音符號

class 官話字綜合標音(字綜合標音):
	型體 = None
	注音符號 = None
	def __init__(self, 字物件, 音標一定愛著=False):
		if not isinstance(字物件, 字):
			raise 型態錯誤('傳入來的毋是字物件！{0}，{1}'.format(type(字物件), str(字物件)))
		self.型體 = 字物件.型
		if 字物件.音 == 無音:
			self.注音符號 = 無音
		elif 字物件.音 in 標點符號:
			self.注音符號 = 無音
		else:
			注音 = 官話注音符號(字物件.音)
			if 注音.音標 == None:
				self.注音符號 = None
			elif len(注音.音標) == 1:
				self.注音符號 = '⿳' + 注音.音標 + ' '
			else:
				self.注音符號 = '⿳' * (len(注音.音標) - 1)
				if 注音.音標[-1] == '˙':
					self.注音符號 += 注音.音標[-1] + 注音.音標[:-1]
				else:
					self.注音符號 += 注音.音標
			if 音標一定愛著 and not self.標音完整無():
				raise 解析錯誤('音標無合法：{0}，{1}，{2}'.
					format(字物件, self.型體, self.注音符號))
	def 轉json格式(self):
		return {"型體":self.型體, "注音符號":self.注音符號}
	def 標音完整無(self):
		return (self.型體 != None and self.注音符號 != None)
	def __repr__(self):
		return self.轉json格式()
	def __str__(self):
		return self.轉json格式()
	def __eq__(self, 別个):
		return isinstance(別个, 官話字綜合標音) and self.型體 == 別个.型體 and \
			self.注音符號 == 別个.注音符號
