# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國103年 意傳文化科技
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
import unicodedata

class 阿拉伯數字():
	一二三 = '一二三四五六七八九'
	兩 = '兩'
	細位 = ['', '十', '百', '千', ]
	大位 = ['', '萬', '億', '兆', ]
	def 是數字無(self, 數字):
		return 數字.isdigit()
	def 是號碼無(self, 數字):
		return self.是數字無(數字)
	def 是數量無(self, 數字):
		if not self.是數字無(數字):
			return False
		if len(數字) > 16:  # 到「兆」
			return False
		if self.變半形(數字).startswith('0'):
			return False
		return True
	
	def 變半形(self, 數字):
		return unicodedata.normalize('NFKC', 數字)
	
	def 轉號碼(self, 空, 數字):
		if not self.是號碼無(數字):
			return 數字
		空一二三 = 空 + self.一二三
		漢字 = []
		for 數 in 數字:
			漢字.append(空一二三[int(數)])
		return ''.join(漢字)
	
	def 轉數量(self, 空, 數字):
		if not self.是數量無(數字):
			return 數字
		空一二三 = 空 + self.一二三
		漢字 = []
		頭前有空號無 = False
		大位有數字無 = False
		for 所在 in range(len(數字)):
			數值 = int(數字[所在])
			數細位 = (len(數字) - 所在 - 1) % 4
			數大位 = (len(數字) - 所在 - 1) // 4
			if 數值 == 0:
				頭前有空號無 = True
			else:
				大位有數字無 = True
				if 頭前有空號無:
					漢字.append(空一二三[0])
					頭前有空號無 = False
				if 數值 == 2:
					if 數細位 == 1 or (所在 != 0 and 數細位 == 0):  # 二十佮兩億零二萬
						漢字.append(空一二三[2])
# 					elif 數細位==0 and 數大位==0:#二
# 						漢字.append(空一二三[2])
					else:
						漢字.append(self.兩)
				else:
					漢字.append(空一二三[數值])
				漢字.append(self.細位[數細位])
			if 數細位 == 0 and 大位有數字無:
				漢字.append(self.大位[數大位])
				頭前有空號無 = False
				大位有數字無 = False
		結果 = ''.join(漢字)
		if 結果.startswith('一十'):
			return 結果[1:]
		return 結果
	
	def 轉閩南語數量無(self, 數量):
		return self.轉閩南語數量(數量) != 數量
	
	def 轉閩南語數量(self, 數量):
		if len(數量) == 4 and \
			數量.startswith(self.一二三[0]) and 數量[-1] in self.細位:
			if 數量[-2] == self.兩:
				return 數量[1] + self.一二三[1]
			return 數量[1:-1]
		if len(數量) == 5 and 數量.startswith(self.一二三[0]) \
			and 數量[-2] in self.細位\
			and 數量[-1] in self.大位:
			if 數量[-3] == self.兩:
				return 數量[1:-3] + self.一二三[1] + 數量[-1]
			return 數量[1:-2] + 數量[-1]
		if len(數量) >= 4 and \
			 (數量[-3] in self.細位 or 數量[-3] in self.大位) and \
			 數量[-1] in self.細位:
			if 數量[:-1].endswith(self.兩):
				結果 = 數量[:-2] + self.一二三[1]
			else:
				結果 = 數量[:-1]
		else:
			結果 = 數量
		return 結果.replace('一十', '十')
	
	def 轉客家話數量無(self, 數量):
		return self.轉客家話數量(數量) != 數量
	
	def 轉客家話數量(self, 數量):
		if len(數量) == 4 and \
			數量.startswith(self.一二三[0]) and 數量[-1] in self.細位:
			if 數量[-2] == self.兩:
				return 數量[1] + self.一二三[1]
			return 數量[1:-1]
		if len(數量) >= 4 and \
			 (數量[-3] in self.細位 or 數量[-3] in self.大位) and \
			 數量[-1] in self.細位:
			return 數量[:-1]
		return 數量
	
	def 轉官話數量無(self, 數量):
		return self.轉官話數量(數量) != 數量
	
	def 轉官話數量(self, 數量):
		if len(數量) >= 4 and \
			 (數量[-3] in self.細位 or 數量[-3] in self.大位) and \
			 數量[-1] in self.細位:
			if 數量[-2] == self.兩:
				return 數量[:-2] + self.一二三[1]
			return 數量[:-1]
		return 數量
			
