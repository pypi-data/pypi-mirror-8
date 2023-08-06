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
import os
import gzip

class 腳本程式:
	def _執行檔路徑加尾(self, 執行檔路徑):
		if 執行檔路徑 != '' and not 執行檔路徑.endswith('/'):
			return 執行檔路徑 + '/'
		return 執行檔路徑
	def _走指令(self, 指令):
		回傳值 = os.system(指令)
		if 回傳值 != 0:
			raise RuntimeError('指令走到一半發生問題！！指令：{0}'
				.format(指令))
	def _細項目錄(self, 資料目錄, 細項名):
		細項目錄 = os.path.join(資料目錄, 細項名)
		os.makedirs(細項目錄, exist_ok=True)
		return 細項目錄
	def _陣列寫入檔案(self, 檔名, 陣列):
		self._字串寫入檔案(檔名, '\n'.join(陣列))
	def _字串寫入檔案(self, 檔名, 字串):
		檔案 = open(檔名, 'w')
		print(字串, file=檔案)
		檔案.close()
	def _讀檔案(self, 檔名):
		檔案 = open(檔名, 'r')
		資料 = []
		for 一逝 in 檔案:
			一逝 = 一逝.rstrip()
			if 一逝 != '':
				資料.append(一逝)
		檔案.close()
		return 資料
	def _檔案合做一个(self, 平行檔名, 語言平行語料, 編碼器):
		with open(平行檔名, 'w') as 寫檔:
			for 語言檔案 in 語言平行語料:
				if 語言檔案.endswith('.gz'):
					開檔 = gzip.open
				else:
					開檔 = open
				with 開檔(語言檔案, mode='rt') as 檔案:
					for 一逝 in 檔案.readlines():
						print(編碼器.編碼(一逝.strip()), file=寫檔)
